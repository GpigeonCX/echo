from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.price_snapshot import PriceSnapshot
from app.schemas.quote import QuoteSyncItem, QuoteSyncResult


def _safe_import_akshare():
    try:
        import akshare as ak  # type: ignore

        return ak
    except Exception:
        return None


def _sync_cash_asset(asset: Asset) -> tuple[Decimal, Decimal, str]:
    return Decimal("1"), Decimal("1"), "cash-fixed"


def _sync_hk_fx(ak) -> Decimal:
    if ak is None:
        return Decimal("0.92")
    try:
        df = ak.fx_spot_quote()
        if "symbol" in df.columns:
            row = df[df["symbol"].astype(str).str.contains("HKDCNY", case=False, na=False)]
            if not row.empty:
                return Decimal(str(row.iloc[0]["trade"]))
        if "代码" in df.columns:
            row = df[df["代码"].astype(str).str.contains("HKDCNY", case=False, na=False)]
            if not row.empty:
                return Decimal(str(row.iloc[0]["最新价"]))
    except Exception:
        pass
    return Decimal("0.92")


def _sync_fund_price(ak, code: str) -> tuple[Decimal, str]:
    if ak is None:
        raise RuntimeError("AKShare is not available")
    try:
        df = ak.fund_open_fund_info_em(symbol=code, indicator="单位净值走势")
        value = df.iloc[-1]["单位净值"]
        return Decimal(str(value)), "akshare:fud_info"
    except Exception:
        df = ak.fund_open_fund_daily_em()
        code_col = "基金代码" if "基金代码" in df.columns else "代码"
        price_col = "单位净值" if "单位净值" in df.columns else "最新单位净值"
        row = df[df[code_col].astype(str) == code]
        if row.empty:
            raise RuntimeError(f"Fund quote not found for {code}")
        return Decimal(str(row.iloc[0][price_col])), "akshare:fund_daily"


def _sync_hk_stock_price(ak, code: str) -> tuple[Decimal, str]:
    if ak is None:
        raise RuntimeError("AKShare is not available")
    df = ak.stock_hk_spot_em()
    code_col = "代码" if "代码" in df.columns else "symbol"
    price_col = "最新价" if "最新价" in df.columns else "price"
    row = df[df[code_col].astype(str).str.zfill(5) == code.zfill(5)]
    if row.empty:
        raise RuntimeError(f"HK stock quote not found for {code}")
    return Decimal(str(row.iloc[0][price_col])), "akshare:hk_spot"


def sync_quotes_once(db: Session) -> QuoteSyncResult:
    ak = _safe_import_akshare()
    assets = db.scalars(select(Asset).where(Asset.auto_quote_enabled.is_(True)).order_by(Asset.code)).all()
    synced_items: list[QuoteSyncItem] = []
    synced_at = datetime.utcnow()
    hkd_rate = _sync_hk_fx(ak)

    for asset in assets:
        try:
            if asset.asset_type in {"cash", "money_fund"}:
                price, fx_rate, source = _sync_cash_asset(asset)
            elif asset.asset_type == "fund":
                price, source = _sync_fund_price(ak, asset.code)
                fx_rate = Decimal("1")
            elif asset.asset_type == "hk_stock":
                price, source = _sync_hk_stock_price(ak, asset.code)
                fx_rate = hkd_rate
            else:
                continue

            db.add(
                PriceSnapshot(
                    asset_id=asset.id,
                    price=price,
                    fx_rate_to_cny=fx_rate,
                    captured_at=synced_at,
                )
            )
            synced_items.append(
                QuoteSyncItem(
                    code=asset.code,
                    price=float(price),
                    fx_rate_to_cny=float(fx_rate),
                    source=source,
                )
            )
        except Exception:
            continue

    db.commit()
    message = "Quotes synced" if synced_items else "No quotes synced"
    return QuoteSyncResult(
        success=bool(synced_items),
        synced_count=len(synced_items),
        synced_at=synced_at,
        message=message,
        items=synced_items,
    )
