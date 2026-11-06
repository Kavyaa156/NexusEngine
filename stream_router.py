from fastapi import APIRouter
from starlette.responses import StreamingResponse
from models import QueryRequest
import asyncio

router = APIRouter()

@router.post("/stream")
async def stream_query(body: QueryRequest):
    async def event_generator():
        words = body.prompt.split()
        for word in words:
            await asyncio.sleep(0.2)
            yield f"data: {word}\n\n"

        yield f"data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")