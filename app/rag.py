from langchain_community.document_loaders import JSONLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def setup_rag():
    loader = JSONLoader(
        file_path="data/autostream_knowledge.json",
        jq_schema=".[] | .content",
        text_content=False
    )

    documents = loader.load()

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore