# Deployment

## Backend — Render (Docker web service)
- **Root Directory:** `BackApp`
- **Dockerfile Path:** `Dockerfile` (the Dockerfile now lives inside `BackApp/`, alongside `requirements.txt`)
- **Environment variables:** copy from `.env.example` and set real values for:
  - `DATABASE_URL` — Supabase Postgres connection string (use the direct/`postgres` connection string, not the pooled anon one, so the backend isn't blocked by Row Level Security)
  - `API_CORS_ORIGINS` — your Vercel frontend URL(s), comma-separated
  - `OPENAI_API_KEY`
  - `UPLOAD_DIR`, `MAX_UPLOAD_MB`, `YOLO_MODEL` as needed
- Requires a Postgres driver in `requirements.txt` (`psycopg2-binary`) — already added, otherwise the app crashes on startup when it tries to connect.

## Frontend — Vercel
- **Root Directory:** `FrontApp`
- Set `NEXT_PUBLIC_API_URL` to your Render API URL (e.g. `https://your-service.onrender.com/api/v1`)

## Database — Supabase
Apply `database.sql` in the Supabase SQL editor for Row Level Security and the
production schema. Note: `BackApp`'s `init_db()` also calls
`Base.metadata.create_all()` on startup, which will create the `matches`
table automatically if it doesn't exist yet — but you should still run
`database.sql` first so RLS policies are in place before the app starts
writing to it.