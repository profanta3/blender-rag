from lib.models.api import MWRequest, PipelineOutput
from lib.models.chat import Message
from middleware.rag_app import RagApp
from fastapi.responses import StreamingResponse


class RagPipeline:
    def __init__(self) -> None:
        self.messages: list[Message] = []
        self.rag_app = RagApp()

    def search(self, mw_request: MWRequest) -> PipelineOutput:
        new_user_msg = Message(role="user", content=mw_request.query)
        self.add_message(new_user_msg)

        bot_response_stream = self.rag_app.prompt_llm(new_user_msg.content)
        bot_msg = Message(role="bot", content=bot_response_stream)

        output = PipelineOutput(message=bot_msg)
        return output

    def add_message(self, message: Message):
        self.messages.append(message)
