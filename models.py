import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry
from pydantic import BaseModel

model = (
    get_registry().get("sentence-transformers").create(name="BAAI/bge-small-en-v1.5")
)


class Document(LanceModel):
    text: str = model.SourceField()
    vector: Vector(384) = model.VectorField()


class Prompt(BaseModel):
    id: str
    template: str
