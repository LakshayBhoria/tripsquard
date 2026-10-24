# 🧭 TripSquad: From Intent to Action
Fetch-A-Thon 3.0 · ASI:One Agent Challenge

**Say a trip in plain English → get a weather-aware, budgeted day-by-day plan, plus one-tap Google Calendar events and Google Maps routes. All inside an ASI:One chat.**

> "Plan a 3-day trip to Jaipur from Delhi next weekend under ₹15,000"

## Problem · Users · Outcome
- **Problem:** Planning a trip means juggling weather apps, maps, blogs, and budget sheets; chatbots only *describe* trips.
- **Users:** students, young professionals and families planning weekend/short trips.
- **Outcome:** a confirmed itinerary with calendar events + per-day route links, a budget verdict (within/over, with fixes) and a packing list.

## Architecture (multi-agent)
```
ASI:One ──ACP──► Orchestrator (intent parsing, planning, cards)
                    ├─► Weather agent  (Open-Meteo forecast + geocoding)
                    ├─► Places agent   (Wikipedia GeoSearch attractions, indoor/outdoor tagging)
                    └─► Budget agent   (distance-based transport + cost tiers + Frankfurter FX)
```
- The three workers run **in parallel** (`asyncio.gather` + `ctx.send_and_receive`).
- **Reliability:** every HTTP call retries with backoff; if a worker agent times out or fails, the orchestrator transparently **runs that tool locally** and reports it ("Budget (local fallback)"). Forecast failure ⇒ plan without weather; unknown city ⇒ friendly message.
- **Weather-aware planning:** rainy day ⇒ indoor stops; hot day ⇒ outdoor in morning/evening, indoor at midday.
- **ASI:One Interactive Cards:** `form` (trip details), `review` (confirm / change). Handles both JSON and planner-prose selections.
- **Intent parsing:** ASI1 LLM (`ASI1_API_KEY`) with a rule-based fallback that works with no key.
- Follow-ups work: "make it 4 days", "under ₹10,000".

## Run it
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # set the 4 *_SEED values to unique secrets
python run_all.py           # starts all 4 agents (ports 8000-8003)
```
1. Each agent logs an **Agent Inspector** link → open it → **Connect → Mailbox**. Do this for all four.
2. Copy the Weather / Places / Budget **addresses** from the logs into `.env` (`*_AGENT_ADDRESS`), then restart. (Skip this and the orchestrator just uses its local fallbacks.)
3. In Agentverse, open the **orchestrator** agent profile → paste `AGENTVERSE_README.md` as its overview (important for ASI:One discovery) → verify the Chat Protocol shows.
4. Open https://asi1.ai/ai/agent1qg2atark6shw2xdvmhfd8vjqj3a2stmsflyfntlk8tde6v0ltxg6jsuvlmp → enable **Agents** → ask: *"Plan a 3-day trip to Jaipur from Delhi next weekend under ₹15,000"*. Click **Confirm**.
5. Test cards without ASI:One: Agentverse → agent → **Testing** tab, or https://asi1.ai/developer/card-playground.

Offline tests (no network): `pytest -q`

## Files
`agents/` four agents · `tripsquad/tools.py` live data tools · `planner.py` itinerary + calendar/maps links · `intent.py` parser · `cards.py` interactive cards · `tests/`

## Roadmap
Payment Protocol for premium bookings, hotel/transport price APIs, group trips, saved preferences.
