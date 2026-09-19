import os
import sys

# Ensure backend directory is in Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.routes import router as api_router
from config import settings

def get_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Smart City Lahore: Urban Intelligence and Public Preparedness API"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.API_PREFIX)
    return app

app = get_application()

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

if os.path.exists(FRONTEND_DIR):
    # Mount entire frontend directory under /static
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/", include_in_schema=False)
async def serve_frontend():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Backend is running successfully!", "docs": "Visit /docs"}

# Fallback route handlers so browser requests to /css/... or /js/... resolve safely
@app.get("/css/{file_path:path}", include_in_schema=False)
async def serve_css(file_path: str):
    css_file = os.path.join(FRONTEND_DIR, "css", file_path)
    if os.path.exists(css_file):
        return FileResponse(css_file)
    raise HTTPException(status_code=404, detail="CSS file not found")

@app.get("/js/{file_path:path}", include_in_schema=False)
async def serve_js(file_path: str):
    js_file = os.path.join(FRONTEND_DIR, "js", file_path)
    if os.path.exists(js_file):
        return FileResponse(js_file)
    raise HTTPException(status_code=404, detail="JS file not found")

@app.get("/health", tags=["System Monitoring"])
async def health_check():
    return {
        "status": "active",
        "service": settings.PROJECT_NAME,
        "openai_key_loaded": bool(settings.OPENAI_API_KEY),
        "hf_key_loaded": bool(settings.HUGGINGFACE_API_KEY)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)