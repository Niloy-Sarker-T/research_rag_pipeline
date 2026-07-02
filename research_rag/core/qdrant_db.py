from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    VectorParams,
    PointStruct
)

from sentence_transformers import SentenceTransformer


COLLECTION_NAME = "research_papers"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

client = QdrantClient(
    host="localhost",
    port=6333
)

model = SentenceTransformer(EMBEDDING_MODEL)



def create_collection():
    """
    Creates the collection only if it doesn't already exist.
    """

    collections = client.get_collections().collections
    collection_names = [c.name for c in collections]

    if COLLECTION_NAME not in collection_names:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,               # MiniLM embedding dimension
                distance=Distance.COSINE
            )
        )

        print(f"Collection '{COLLECTION_NAME}' created.")

    else:

        print(f"Collection '{COLLECTION_NAME}' already exists.")



def insert_chunks(embedded_chunks):
    """
    Stores embedded chunks into Qdrant.
    """

    points = []

    for chunk in embedded_chunks:

        point = PointStruct(

            id=chunk["chunk_id"],

            vector=chunk["embedding"].tolist(),

            payload={

                "text": chunk["text"],

                "page_number": chunk["page_number"],

                "section": chunk["section"]

            }

        )

        points.append(point)

    client.upsert(

        collection_name=COLLECTION_NAME,

        points=points

    )

    print(f"{len(points)} chunks inserted into Qdrant.")



def retrieve(question, top_k=5):
    """
    Searches Qdrant using semantic similarity.
    Returns the top matching chunks.
    """

    query_vector = model.encode(question).tolist()

    results = client.search(

        collection_name=COLLECTION_NAME,

        query_vector=query_vector,

        limit=top_k

    )

    return results


def build_context(results):
    """
    Converts retrieved chunks into
    a prompt-ready context.
    """

    context = ""

    for result in results:

        payload = result.payload

        context += f"""
Page: {payload['page_number']}
Section: {payload['section']}

{payload['text']}

----------------------------------

"""

    return context


def search_context(question, top_k=5):
    """
    Complete retrieval pipeline.

    Question
        ↓
    Embedding
        ↓
    Qdrant Search
        ↓
    Prompt Context
    """

    results = retrieve(question, top_k)

    context = build_context(results)

    return context
