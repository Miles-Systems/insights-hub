from app.database.database import SessionLocal
from app.models.document import Document

def step(title):
    print(f"\n=== {title} ===")

def main():
    try:
        session = SessionLocal()
        step("Create object")
        doc = Document(filename="demo.pdf", page_count=3)
        print("Print id")
        print("id:", doc.id)

        step("Add to session")
        session.add(doc)
        print("Print id")
        print("id:", doc.id)

        step("Commit")
        session.commit()
        print("Print id")
        print("id:", doc.id)

        step("Refresh")
        session.refresh(doc)
        print("Print id")
        print("id:", doc.id)
    except Exception as e:
        if session is not None:
            session.rollback()
        print(f"Error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
