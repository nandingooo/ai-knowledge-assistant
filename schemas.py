from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)


class DocumentOut(BaseModel):
    id: int
    title: str
    content: str

    model_config = {"from_attributes": True}


class SearchResult(BaseModel):
    id: int
    title: str
    score: float
    excerpt: str


class AskRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)


class AskResponse(BaseModel):
    answer: str
    sources: list[SearchResult]
