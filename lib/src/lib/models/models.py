import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry
from pydantic import BaseModel, Field

# model = (
#     get_registry()
#     .get("sentence-transformers")
#     .create(name="BAAI/bge-large-en-v1.5")  # BAAI/bge-small-en-v1.5")
# )
model = get_registry().get("ollama").create(name="nomic-embed-text")


class Document(LanceModel):
    text: str = model.SourceField()
    vector: Vector(model.ndims()) = model.VectorField()
    # relevance_score: float


class RetreivedDocument(Document):
    relevance_score: float = Field(alias="_relevance_score")
    score: float | None = Field(alias="_score")


class Prompt(BaseModel):
    id: str
    template: str
