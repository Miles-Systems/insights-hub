from app.models.document import Document
from sqlalchemy.orm import Session

class DocumentRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, document: Document) -> Document:
        self.session.add(document)
        return document
    
    def get_by_id(self, document_id: int) -> Document:
        return self.session.get(Document, document_id)
    
    def get_all(self) -> list[Document]:
        return self.session.query(Document).all()
    
    def delete(self, document: Document) -> None:
        self.session.delete(document)