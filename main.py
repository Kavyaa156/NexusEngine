from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import asyncio
import time
from models import QueryRequest
from stream_router import router as stream_router

app = FastAPI()

app.include_router(stream_router)

class NexusEngineError(Exception):
    def __init__(self, message: str, error_code: str):
        self.message = message
        self.error_code = error_code

@app.exception_handler(NexusEngineError)
async def nexus_engine_exception_handler(request: Request, exc: NexusEngineError):
    return JSONResponse(
        status_code = status.HTTP_400_BAD_REQUEST,
        content = {
            "status": "error",
            "error_code": exc.error_code,
            "message": exc.message,
        },
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        content = {
            "status": "error",
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occured inside NexusEngine",
        },
    )

# --- Performance-Tracking Middleware ---
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.monotonic()
    response = await call_next(request)
    process_time = time.monotonic() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f} seconds"
    return response

# --- Route Handler ---
@app.post("/query")
async def run_query(body: QueryRequest):
    user_prompt = body.prompt
    
    temp = body.temperature
    tokens = body.max_tokens

    await asyncio.sleep(1.0)

    return {
        "status": "success",
        "received_prompt": user_prompt,
        "parameters_used": {
            "temperature": temp,
            "max_tokens": tokens
        },
        "engine_response": f"NexusEngine successfully processed your query: '{user_prompt}'"    
    }