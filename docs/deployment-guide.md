# 部署、启动与调试指南

## 1. 项目概览

本项目当前采用单仓结构：

- 前端：Nuxt 3
- 后端：FastAPI
- ORM：SQLAlchemy
- 数据库：
  - 本地开发默认 SQLite
  - 生产部署建议 MySQL 8

## 2. 环境要求

建议环境：

- Node.js 22+
- npm 10+
- Python 3.11+
- MySQL 8.x

当前本地验证环境：

- Node.js 22.19.0
- npm 10.9.3
- Python 3.14.0

## 3. 首次拉起项目

### 3.1 启动 API

在项目根目录执行：

```powershell
cd apps/api
py -3 -m venv .venv
.venv\Scripts\python -m pip install -e .
.venv\Scripts\uvicorn app.main:app --reload
```

默认监听地址：

- `http://127.0.0.1:8000`

接口前缀：

- `http://127.0.0.1:8000/api`

说明：

- 第一次启动会自动建表
- 如果数据库为空，会自动写入演示数据
- 默认数据库文件为 `apps/api/echo.db`

### 3.2 启动 Web

在新的终端中执行：

```powershell
cd apps/web
npm install
npm run dev
```

默认访问地址：

- `http://127.0.0.1:3000`

## 4. 本地开发默认配置

当前后端默认使用：

- `DATABASE_URL=sqlite:///./echo.db`

这意味着：

- 不需要先装 MySQL 就能本地跑起来
- 适合快速验证页面、接口、流程

## 5. 切换到 MySQL

### 5.1 创建数据库

先在 MySQL 中创建数据库，例如：

```sql
CREATE DATABASE echo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5.2 配置环境变量

在 `apps/api` 目录下新建 `.env` 文件：

```env
DATABASE_URL=mysql+pymysql://root:root@127.0.0.1:3306/echo
```

也可以继续补充：

```env
APP_NAME=Echo Investment Assistant
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=echo
```

注意：

- 当前代码优先读取 `DATABASE_URL`
- 如果你不设置 `DATABASE_URL`，会继续走 SQLite

### 5.3 初始化表结构

当前 FastAPI 启动时会自动根据 SQLAlchemy 模型建表。

如果你要单独维护 MySQL 脚本，可参考：

- [database/mysql/001_init.sql](/C:/Users/duanh01/AppData/Local/Temp/vibe-kanban/worktrees/8329-0-1/echo/database/mysql/001_init.sql)

## 6. 生产部署建议

当前更稳妥的方式是前后端分开部署。

### 6.1 前端部署

可选方式：

- Vercel
- Netlify
- Linux + Nginx

构建命令：

```powershell
cd apps/web
npm install
npm run build
```

Nuxt 构建输出基于 Node Server，可用：

```powershell
node .output/server/index.mjs
```

如果前端访问的 API 不是本机，需要配置：

```env
NUXT_PUBLIC_API_BASE=http://your-api-host:8000/api
```

### 6.2 后端部署

推荐部署方式：

- Linux 云服务器
- Docker 容器
- Python 虚拟环境 + systemd

启动命令示例：

```powershell
cd apps/api
.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000
```

生产更建议：

```powershell
.venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
```

### 6.3 Nginx 反向代理建议

- `/` 转发到 Nuxt
- `/api/` 转发到 FastAPI

## 7. 常用调试方法

### 7.1 验证 API 是否正常

浏览器或命令行访问：

- `GET /`
- `GET /api/health`
- `GET /api/assets`
- `GET /api/assets/holdings`
- `GET /api/dashboard/summary`
- `GET /api/transactions`

### 7.2 手工新增一笔交易

示例请求：

```json
{
  "asset_id": 2,
  "account_id": 1,
  "action": "buy",
  "quantity": 1000,
  "price": 1.23,
  "amount": 1230,
  "fee": 0,
  "applied_date": "2026-04-01",
  "confirmed_date": "2026-04-01",
  "nav_date": "2026-04-01",
  "status": "confirmed",
  "note": "manual test"
}
```

接口：

- `POST /api/transactions`

### 7.3 重新初始化本地 SQLite

如果你只是本地调试，想重置演示数据：

1. 停掉 API
2. 删除 `apps/api/echo.db`
3. 重新启动 API

系统会自动重建表并重新灌入演示数据。

## 8. 已验证命令

以下命令已经跑通过：

### API

```powershell
cd apps/api
py -3 -m compileall apps/api
.venv\Scripts\python -m pip install -e .
```

### Web

```powershell
cd apps/web
npm install
npm run build
```

## 9. 当前功能覆盖度说明

对比原 Excel，目前已经具备：

- 资产列表
- 持仓汇总
- 交易录入
- 组合总览
- 计划列表展示

还缺的关键能力：

- 自动行情更新
- 历史峰值自动记录
- 自动回撤分档计算
- 再平衡建议金额
- 计划执行偏差跟踪
- 邮件提醒

因此，当前版本是：

- 一个可运行的 MVP 骨架
- 不是最终可替代 Excel 的完整版本

## 10. 下一步开发建议

建议按这个顺序继续：

1. 行情同步与价格快照
2. 峰值、回撤、再平衡规则
3. 计划执行对比
4. 邮件提醒
5. Excel 导入
