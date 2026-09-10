class AnswerService:
    """Context-grounded answer generator.

    This credential-free version returns the most relevant retrieved context.
    The interface can later wrap a production LLM without changing the API.
    """

    def answer(self, question: str, ranked_documents: list) -> str:
        if not ranked_documents:
            return "I could not find relevant information in the indexed documents."

        best = ranked_documents[0].document
        excerpt = " ".join(best.content.strip().split())
        if len(excerpt) > 500:
            excerpt = excerpt[:497] + "..."

        return (
            f"Based on the most relevant document, here is the supporting context: "
            f"{excerpt}"
        )
