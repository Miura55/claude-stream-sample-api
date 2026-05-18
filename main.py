import os
import dotenv
import anthropic
from fastapi import FastAPI
from fastapi.sse import EventSourceResponse
from pydantic import BaseModel

dotenv.load_dotenv()

app = FastAPI(title="Streaming Response Demo", version="1.0.0")
claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


class MessageRequest(BaseModel):
    message: str
    model: str = "claude-opus-4-5"
    max_tokens: int = 1024


@app.post("/messages")
def create_message(request: MessageRequest):
    message = claude.messages.create(
        model=request.model,
        max_tokens=request.max_tokens,
        messages=[{"role": "user", "content": request.message}],
    )
    text_block = next(b for b in message.content if isinstance(b, anthropic.types.TextBlock))
    return {"response": text_block.text}


@app.post("/messages/stream", response_class=EventSourceResponse)
def create_message_stream(request: MessageRequest):
    with claude.messages.stream(
        model=request.model,
        max_tokens=request.max_tokens,
        messages=[{"role": "user", "content": request.message}],
    ) as stream:
        for text in stream.text_stream:
            yield {'response': text, 'type': 'delta'}
