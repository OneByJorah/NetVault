# NetVault NOC

Local-run verified documentation.

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run
```

## Verified APIs
- `GET /api/v1/health` -> JSON health status
- `GET /api/v1/` -> JSON service info
- `GET /api/v1/config` -> service toggles and config names

## Reference map
- App factory: `app/__init__.py`
- Config: `app/config.py`
- REST API: `app/routes/api.py`
- Routes: `app/routes/{devices,backup,restore,compare,alerts,sync}.py`
- Templates: `templates/{index,devices,backup,restore,compare,alerts,cloud}.html`

## Status
✅ README references verified against actual code paths.
