from fastapi import APIRouter

from app.schemas.dashboard import DashboardSummary


router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary() -> DashboardSummary:
    return DashboardSummary(
        total_assets=308452.54,
        cash_assets=60000,
        unrealized_pnl=12452.54,
        drawdown_rate=-0.082,
        peak_assets=336000,
        allocation=[
            {"name": "基金", "value": 218452.54},
            {"name": "港股", "value": 30000},
            {"name": "现金", "value": 60000},
        ],
        alerts=[
            "组合回撤 8.2%，暂未触发弹药阈值",
            "恒生科技偏离目标权重，建议关注再平衡",
        ],
    )
