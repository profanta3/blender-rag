from pydantic import BaseModel
from openai import Stream
from lib.models.chat import Message


class MWRequest(BaseModel):
    query: str


class PipelineOutput(BaseModel):
    message: Message


class MWResponse(BaseModel):
    response_stream: Stream
    pipeline_output: PipelineOutput
    status: int | None = None
