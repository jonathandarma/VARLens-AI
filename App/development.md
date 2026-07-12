# Development

Backend (run from the **repository root** — `BackApp/main.py` uses relative
imports, so it must be launched as the `BackApp` package, not from inside
that folder):

```
python -m venv .venv
.venv/Scripts/pip install -r BackApp/requirements.txt
.venv/Scripts/uvicorn BackApp.main:app --reload
```

Frontend: `cd FrontApp; npm install; npm run dev`

Set `NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1`. The OpenAPI contract is served at `/docs`.
