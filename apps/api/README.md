# echo-api

FastAPI backend for the personal investment assistant.

Default local development uses `sqlite:///./echo.db`.
To switch to MySQL, set `DATABASE_URL` or adjust `.env`.

Quote sync:

- automatic background sync is enabled by default
- manual sync endpoint: `POST /api/quotes/sync`
- sync interval can be configured with `QUOTE_SYNC_INTERVAL_SECONDS`
