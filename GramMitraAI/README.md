# GramMitra AI — Theme 12: Agents for Social Good

## Problem and solution
Telugu-speaking rural residents and farmers have difficulty finding understandable, location-relevant guidance and official resources. GramMitra accepts a goal, category, nearest town and optional crop, plans a bounded tool workflow, retrieves evidence, and provides next steps in English or Telugu. The target is a prototype, not an expert service.

## Windows / VS Code setup
Install Python 3.11+ and Node.js 20+. Open this folder in VS Code. In terminal 1:
```powershell
cd backend
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```
Set OPENAI_API_KEY to your actual API key (API billing separate from ChatGPT). Keep the key private. Save, then:
```powershell
.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```
In a new terminal at project root:
```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```
Open http://localhost:5173. API docs: http://localhost:8000/docs. No API key is needed for deterministic fallback; live weather needs Internet. Do not present fallback as AI generation.

## Architecture
React -> FastAPI -> bounded planner (OpenAI JSON or deterministic fallback) -> allowlisted tools: Indian town geocoding, SQLite resource lookup, conditional three-day weather forecast -> observations -> guarded synthesis -> UI trace + resource links. Health/civic synthesis is template-only. SQLite stores anonymous run counters and feedback, not raw prompts. The AI may choose order within the validated plan; no arbitrary URLs or commands. No external write actions are available, so approval for irreversible actions is not applicable. Feedback writes occur only on explicit user clicks. Trace is returned after completion, not streamed. API calls have timeouts and one retry. Ambiguous/unresolved locations prevent weather calls. Forecasts are not emergency warnings.

## Demo (3–5 minutes)
Choose Agriculture, Vijayawada, paddy; ask about field work over the next three days. Show the returned plan, location, weather observations, resource database output and guidance. Switch to Telugu and repeat. Use an invalid location to demonstrate safe fallback. Show impact counters and vote. Explain source limitations and no external actions.

## Deployment
Push the folder to a public GitHub repository (never commit .env or database). Render: root backend, build `pip install -r requirements.txt`, start `uvicorn main:app --host 0.0.0.0 --port $PORT`. Configure OPENAI_API_KEY, OPENAI_MODEL, CORS_ORIGINS (your exact frontend URL) and DB_PATH (persistent disk path if available). Vercel: root frontend, Vite preset, build `npm run build`, output `dist`, environment VITE_API_URL = backend HTTPS URL. Redeploy after changing env. Default SQLite on ephemeral hosting may reset; use persistent disk for durable metrics. Prototype has no accounts or rate limiting; add these before public use at scale. API key is server-only. Public usage can incur costs; set provider budget limits.

## Impact and evaluation
Track requests, completed tool workflows, Telugu usage and helpful votes. For actual impact, recruit consenting rural users and compare time to find correct official resources, task completion, comprehension and accuracy against manual search. Audit AI advice with domain experts. Do not claim observed social impact before evaluation. Official portal links are a small manually curated directory, not live eligibility data. Review links before demo. Language support includes Telugu UI and guidance; raw tool observations and resource descriptions remain English. Weather uses Open-Meteo and should be verified with IMD for warnings. No diagnosis, legal decisions or financial recommendations. The app is not an emergency service. Do not submit personal data.
