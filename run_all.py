"""Start all four agents locally (one subprocess each). Ctrl+C stops everything."""
import subprocess
import sys

MODULES = ["agents.weather_agent", "agents.places_agent", "agents.budget_agent", "agents.orchestrator_agent"]

if __name__ == "__main__":
    procs = [subprocess.Popen([sys.executable, "-m", m]) for m in MODULES]
    try:
        for p in procs:
            p.wait()
    except KeyboardInterrupt:
        for p in procs:
            p.terminate()
