import asyncio
import logging
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from engine import engine
from utils import setup_logging

# Setup logging at the start of the module
LOG_DIR = "logs"
log_file_path = setup_logging(log_dir=LOG_DIR)
logger = logging.getLogger("Server")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Lifespan: Launching ADS-B Engine...")
    task = asyncio.create_task(engine.run_loop())
    yield
    logger.info("Starting Lifespan: Stopping ADS-B Engine...")
    engine.stop()
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        logger.info("Engine task cancelled successfully.")

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

# --- Middleware/Error Handling ---

@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    """Global exception handler to log all errors and return a clean 500."""
    logger.exception(f"Unhandled exception during request: {exc}")
    return HTMLResponse(
        content=f"""
        <html>
            <body style="background-color: #111827; color: #f3f4f6; font-family: sans-serif; padding: 2rem;">
                <h1 style="color: #ef4444;">Internal Server Error</h1>
                <p>An unexpected error occurred. The details have been logged to <code style="color: #60a5fa;">{log_file_path}</code>.</p>
                <div style="background: #1f2937; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; font-family: monospace; overflow-x: auto;">
                    <pre style="white-space: pre-wrap;">{str(exc)}</pre>
                </div>
                <br>
                <a href="/" style="color: #60a5fa; text-decoration: none;">Return to Dashboard</a>
            </body>
        </html>
        """,
        status_code=500
    )

# --- Routes ---

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Corrected signature for Starlette/FastAPI: TemplateResponse(request, template_name, context)
    return templates.TemplateResponse(request, "index.html")

@app.get("/map", response_class=HTMLResponse)
async def map_view(request: Request):
    # Corrected signature for Starlette/FastAPI: TemplateResponse(request, template_name, context)
    return templates.TemplateResponse(request, "map.html")

@app.get("/api/aircraft")
async def get_aircraft():
    return engine.get_all_aircraft()

@app.get("/api/health")
async def health():
    return {"status": "healthy", "engine_running": engine.is_running}

@app.get("/api/logs")
async def get_logs():
    """Returns the content of the current log file."""
    try:
        if not os.path.exists(log_file_path):
            raise HTTPException(status_code=404, detail="Log file not found.")
            
        with open(log_file_path, "r") as f:
            # Read the last 500 lines for performance
            lines = f.readlines()
            content = "".join(lines[-500:])
            
        return PlainTextResponse(content)
    except Exception as e:
        logger.error(f"Failed to read logs: {e}")
        raise HTTPException(status_code=500, detail="Could not retrieve logs.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
