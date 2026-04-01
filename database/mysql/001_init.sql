CREATE TABLE account (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  account_type ENUM('broker', 'fund_platform', 'bank', 'virtual') NOT NULL,
  currency VARCHAR(10) NOT NULL DEFAULT 'CNY'
);

CREATE TABLE asset (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  code VARCHAR(32) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  asset_type ENUM('fund', 'hk_stock', 'cash', 'money_fund') NOT NULL,
  market VARCHAR(32) NOT NULL,
  currency VARCHAR(10) NOT NULL DEFAULT 'CNY',
  target_weight DECIMAL(10, 4) NOT NULL DEFAULT 0,
  auto_quote_enabled BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE holding (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  asset_id BIGINT NOT NULL,
  account_id BIGINT NOT NULL,
  quantity DECIMAL(18, 6) NOT NULL DEFAULT 0,
  average_cost DECIMAL(18, 6) NOT NULL DEFAULT 0,
  market_value_cny DECIMAL(18, 2) NOT NULL DEFAULT 0,
  CONSTRAINT fk_holding_asset FOREIGN KEY (asset_id) REFERENCES asset(id),
  CONSTRAINT fk_holding_account FOREIGN KEY (account_id) REFERENCES account(id)
);

CREATE TABLE investment_plan (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  total_budget DECIMAL(18, 2) NOT NULL,
  months INT NOT NULL,
  first_month_ratio DECIMAL(10, 4) NOT NULL,
  status ENUM('draft', 'in_progress', 'completed', 'paused') NOT NULL DEFAULT 'draft'
);

CREATE TABLE target_rule (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  version_name VARCHAR(100) NOT NULL,
  rebalance_threshold DECIMAL(10, 4) NOT NULL
);

CREATE TABLE transaction_record (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  asset_id BIGINT NOT NULL,
  account_id BIGINT NOT NULL,
  action ENUM('buy', 'sell', 'deposit', 'withdraw', 'dividend', 'manual_adjustment') NOT NULL,
  quantity DECIMAL(18, 6) NOT NULL DEFAULT 0,
  price DECIMAL(18, 6) NOT NULL DEFAULT 0,
  amount DECIMAL(18, 2) NOT NULL DEFAULT 0,
  fee DECIMAL(18, 2) NOT NULL DEFAULT 0,
  applied_date DATE NOT NULL,
  confirmed_date DATE NULL,
  nav_date DATE NULL,
  status ENUM('pending', 'confirmed') NOT NULL DEFAULT 'confirmed',
  note VARCHAR(255) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_transaction_asset FOREIGN KEY (asset_id) REFERENCES asset(id),
  CONSTRAINT fk_transaction_account FOREIGN KEY (account_id) REFERENCES account(id)
);

CREATE TABLE price_snapshot (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  asset_id BIGINT NOT NULL,
  price DECIMAL(18, 6) NOT NULL,
  fx_rate_to_cny DECIMAL(18, 6) NOT NULL DEFAULT 1,
  captured_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_price_snapshot_asset FOREIGN KEY (asset_id) REFERENCES asset(id)
);

CREATE TABLE portfolio_snapshot (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  total_assets DECIMAL(18, 2) NOT NULL,
  peak_assets DECIMAL(18, 2) NOT NULL,
  drawdown_rate DECIMAL(10, 4) NOT NULL,
  recorded_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
