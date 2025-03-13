from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document


def load_bellavista_documents():
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(
        collection_name="bellavista",
        embedding_function=embeddings,
        persist_directory="data",
    )

    docs = [
        Document(
            page_content=(
                "Bella Vista is a cozy Italian restaurant offering panoramic city views "
                "and an inviting atmosphere."
            )
        ),
        Document(
            page_content=(
                "Bella Vista serves only ONE specific, well known food. a classic wood-fired pizza "
                "prepared with fresh tomatoes, mozzarella, and basil. Bella vista does not serve any other food"
            )
        ),
        Document(
            page_content=(
                "Patrons often enjoy the sunset while dining; reservations are "
                "recommended for a window table."
            )
        ),
    ]

    vectorstore.add_documents(docs)
    print("Bella Vista documents added to Chroma!")
    return vectorstore


if __name__ == "__main__":
    load_bellavista_documents()
