import chromadb
from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    name="devops"
)


question = "How can I automate AWS infrastructure?"

embedding = model.encode(
    question
).tolist()


results = collection.query(
    query_embeddings=[embedding],
    n_results=3
)


print("\nRetrieved documents:\n")

for document in results["documents"][0]:

    print("-" * 50)
    print(document)
