from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Document
from .retrieval import Retriever
from .schemas import AskRequest, AskResponse, DocumentCreate, DocumentOut, SearchResult
from .services import AnswerService


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Knowledge Assistant",
    version="1.0.0",
    description="A backend-first retrieval-augmented knowledge assistant.",
)

retriever = Retriever()
answer_service = AnswerService()


def to_search_result(item) -> SearchResult:
    text = " ".join(item.document.content.strip().split())
    excerpt = text if len(text) <= 220 else text[:217] + "..."
    return SearchResult(
        id=item.document.id,
        title=item.document.title,
        score=round(item.score, 4),
        excerpt=excerpt,
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/documents", response_model=DocumentOut, status_code=201)
def create_document(payload: DocumentCreate, db: Session = Depends(get_db)):
    document = Document(title=payload.title, content=payload.content)
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


@app.get("/documents", response_model=list[DocumentOut])
def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).order_by(Document.id.desc()).all()


@app.get("/search", response_model=list[SearchResult])
def search(
    q: str = Query(min_length=1),
    top_k: int = Query(default=3, ge=1, le=10),
    db: Session = Depends(get_db),
):
    documents = db.query(Document).all()
    ranked = retriever.rank(q, documents, top_k=top_k)
    return [to_search_result(item) for item in ranked]


@app.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest, db: Session = Depends(get_db)):
    documents = db.query(Document).all()
    if not documents:
        raise HTTPException(status_code=400, detail="No documents have been indexed yet.")

    ranked = retriever.rank(payload.question, documents, top_k=payload.top_k)
    return AskResponse(
        answer=answer_service.answer(payload.question, ranked),
        sources=[to_search_result(item) for item in ranked],
    )
