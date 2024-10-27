import asyncio
from middleware.rag_app import RagApp
from middleware.rag_pipeline import RagPipeline
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from lib.models.api import MWRequest, MWResponse
from fastapi.responses import StreamingResponse

#  Import A module from my own project that has the routes defined
# from redorg.routers import saved_items

origins = [
    "http://localhost:8080",
]


app = FastAPI()
# webapp.include_router(saved_items.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_pipe = RagPipeline()


@app.post("/search")
async def root(request: MWRequest):
    response = rag_pipe.search(request)
    mw_response = MWResponse(pipeline_output=response, status=0)
    return StreamingResponse(mw_response, media_type="text/event-stream")
    # return mw_response
