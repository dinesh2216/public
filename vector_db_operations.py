from text_processing import process_files, settings
from langchain_community.vectorstores import Qdrant
from langchain_qdrant import QdrantVectorStore, FastEmbedSparse, RetrievalMode
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient


def get_qdrant_client():
    client = QdrantClient(api_key=settings.QDRANT_API_KEY, url=settings.QDRANT_URL)
    return client


def get_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDINGS_MODEL)
    return embeddings

def get_hybrid_embeddings():
    sparse_embedding = FastEmbedSparse(model_name=settings.SPARSE_MODEL, batch_size = settings.BATCH_SIZE)
    return sparse_embedding


def get_vector_store():
    qdrant = QdrantVectorStore(
        embedding=get_embeddings(),
        sparse_embedding=get_hybrid_embeddings(),
        retrieval_mode = RetrievalMode.HYBRID,
        collection_name=settings.COLLECTION_NAME,
        client=get_qdrant_client()
    )
    return qdrant


def save_vector_store():
    chunks = process_files()
    if chunks:
        client = get_qdrant_client()
        collections = client.get_collection_aliases()
        print(collections)
        if not client.collection_exists(settings.COLLECTION_NAME):
            Qdrant.from_documents(
                    documents=chunks,
                    embedding=get_embeddings(),
                    sparse_embedding=get_hybrid_embeddings(),
                    retrieval_mode=RetrievalMode.HYBRID,
                    url=settings.QDRANT_URL,
                    api_key=settings.QDRANT_API_KEY,
                    collection_name=settings.COLLECTION_NAME
                )
        else:
            qdrant = get_vector_store()
            qdrant.add_documents(chunks)

    print(f'{settings.COLLECTION_NAME} is created successfully')


