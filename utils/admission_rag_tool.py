# admission_rag_tool.py

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class AdmissionRAGTool:
    def __init__(self, brochure_path: str = None):
        if brochure_path is None:
            # Get the root of the repo regardless of where the script runs from
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            self.brochure_path = os.path.join(project_root, "knowledge")
        else:
            self.brochure_path = brochure_path
        self._init_model()
        self._load_documents()

    def _init_model(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            api_key=GROQ_API_KEY,
        )

        self.prompt = PromptTemplate(
            input_variables=["context", "input"],
            template=(
                "You are an expert admission assistant. Use ONLY the following context from the admission brochure "
                "to answer the question. Do not use external knowledge. If the answer is not in the brochure, say: "
                "'This information is not available in the brochure.'\n\n"
                "Context:\n{context}\n\n"
                "Question:\n{input}\n\n"
                "Answer:"
            ),
        )


        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    def _load_documents(self):
        loader = PyPDFDirectoryLoader(self.brochure_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        texts = text_splitter.split_documents(documents)

        self.vector_store = FAISS.from_documents(texts, self.embeddings)
        self.retriever = self.vector_store.as_retriever()

        documents_chain = create_stuff_documents_chain(llm=self.llm, prompt=self.prompt)
        self.retrieval_chain = create_retrieval_chain(self.retriever, documents_chain)

    def ask_question(self, query: str) -> str:
        response = self.retrieval_chain.invoke({"input": query})
        return response["answer"]

    def reload_brochure(self, new_path: str):
        """Call this to change the brochure content during runtime (e.g., dept-wise)"""
        self.brochure_path = new_path
        self._load_documents()
