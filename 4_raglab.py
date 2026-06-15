"""RAG-based faculty lab for an engineering-college policy scenario.

This file is a separate, runnable lab that builds on the existing faculty example.
It shows a simple Retrieval-Augmented Generation (RAG) workflow for an engineering
college faculty member in India.

What this lab demonstrates:
- How PDF documents in the pdfs folder become the knowledge base for the lab.
- How retrieval finds the most relevant material for a policy decision question.
- How the LLM uses retrieved PDF context to produce a grounded recommendation.

This lab uses PDF content as the knowledge source, so faculty can see how a real
RAG workflow relies on document retrieval rather than an in-memory prompt.
"""

import os
import warnings
from pathlib import Path

warnings.filterwarnings(
    "ignore",
    message=r"Core Pydantic V1 functionality isn't compatible with Python 3\.14 or greater\.",
    category=UserWarning,
)

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

try:
    from azure.ai.evaluation import CoherenceEvaluator, GroundednessEvaluator, RelevanceEvaluator
except ImportError:
    CoherenceEvaluator = None
    GroundednessEvaluator = None
    RelevanceEvaluator = None

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents import SearchClient
    from azure.search.documents.indexes import SearchIndexClient
    from azure.search.documents.indexes.models import (
        HnswAlgorithmConfiguration,
        SearchField,
        SearchFieldDataType,
        SearchIndex,
        SearchableField,
        SemanticConfiguration,
        SemanticField,
        SemanticPrioritizedFields,
        SemanticSearch,
        SimpleField,
        VectorSearch,
        VectorSearchProfile,
    )
except ImportError:
    AzureKeyCredential = None
    SearchClient = None
    SearchIndexClient = None
    HnswAlgorithmConfiguration = None
    SearchField = None
    SearchFieldDataType = None
    SearchIndex = None
    SearchableField = None
    SemanticConfiguration = None
    SemanticField = None
    SemanticPrioritizedFields = None
    SemanticSearch = None
    SimpleField = None
    VectorSearch = None
    VectorSearchProfile = None

try:
    from langchain_openai import AzureOpenAIEmbeddings
except ImportError:
    AzureOpenAIEmbeddings = None

load_dotenv()


def resolve_azure_openai_settings():
    """Use Azure-specific values when they exist, otherwise fall back to the existing OPENAPI_* settings."""
    base_url = os.getenv("OPENAPI_BASE_URL", "")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

    if not azure_endpoint:
        if base_url.endswith("/openai/v1"):
            azure_endpoint = base_url.rsplit("/openai/v1", 1)[0]
        elif "/openai/" in base_url:
            azure_endpoint = base_url.split("/openai/", 1)[0]
        else:
            azure_endpoint = base_url

    return {
        "azure_endpoint": azure_endpoint,
        "api_key": os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("OPENAPI_API_KEY", "test-key"),
        "deployment": os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT") or "text-embedding-3-small",
        "api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
    }


def build_llm():
    """Create the LLM client using the same OPENAPI_* values as the other lab."""
    return ChatOpenAI(
        base_url=os.getenv("OPENAPI_BASE_URL", "http://127.0.0.1:8765/v1"),
        api_key=os.getenv("OPENAPI_API_KEY", "test-key"),
        model=os.getenv("OPENAPI_MODEL", "mock-model"),
        temperature=0.2,
    )


def build_azure_eval_model_config():
    """Build model config used by azure-ai-evaluation evaluators."""
    settings = resolve_azure_openai_settings()
    return {
        "azure_endpoint": settings["azure_endpoint"],
        "api_key": settings["api_key"],
        "azure_deployment": os.getenv("AZURE_OPENAI_EVAL_DEPLOYMENT")
        or os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")
        or os.getenv("OPENAPI_MODEL", "mock-model"),
        "api_version": settings["api_version"],
    }


def azure_search_enabled():
    """Return True when Azure AI Search and embedding settings are available."""
    settings = resolve_azure_openai_settings()
    return all(
        [
            os.getenv("AZURE_SEARCH_ENDPOINT"),
            os.getenv("AZURE_SEARCH_API_KEY"),
            os.getenv("AZURE_SEARCH_INDEX_NAME"),
            settings["azure_endpoint"],
            settings["api_key"],
            settings["deployment"],
        ]
    ) and AzureKeyCredential is not None and SearchClient is not None and SearchIndexClient is not None and AzureOpenAIEmbeddings is not None


def extract_pdf_text(pdf_path: str):
    """Read text from a PDF using pypdf, if available."""
    if PdfReader is None:
        return ""

    reader = PdfReader(pdf_path)
    text_chunks = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            text_chunks.append(text)
    return "\n".join(text_chunks)


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100):
    """Split text into smaller chunks for PDF-based knowledge retrieval."""
    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]
        chunks.append(chunk.strip())
        if end >= text_length:
            break
        start += chunk_size - overlap

    return [chunk for chunk in chunks if chunk]


def ensure_azure_index(pdf_dir: str = "pdfs"):
    """Create or update an Azure AI Search index and upload PDF chunks to it."""
    if not azure_search_enabled():
        return None, "Azure AI Search configuration is not available. Add the AZURE_* variables to use the PDF-based RAG path."

    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    key = os.getenv("AZURE_SEARCH_API_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
    settings = resolve_azure_openai_settings()

    print(f"\n[Azure Search] Creating/updating index '{index_name}' at {endpoint}...")

    index_client = SearchIndexClient(endpoint, AzureKeyCredential(key))
    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint=settings["azure_endpoint"],
        api_key=settings["api_key"],
        deployment=settings["deployment"],
        model=settings["deployment"],
        openai_api_version=settings["api_version"],
    )

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String, searchable=True),
        SearchableField(name="source", type=SearchFieldDataType.String, filterable=True),
        SearchField(
            name="contentVector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=1536,
            vector_search_profile_name="default-profile",
        ),
    ]

    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="hnsw")],
        profiles=[VectorSearchProfile(name="default-profile", algorithm_configuration_name="hnsw")],
    )
    semantic_search = SemanticSearch(
        configurations=[
            SemanticConfiguration(
                name="default",
                prioritized_fields=SemanticPrioritizedFields(
                    title_field=SemanticField(field_name="source"),
                    content_fields=[SemanticField(field_name="content")],
                ),
            )
        ]
    )

    index = SearchIndex(
        name=index_name,
        fields=fields,
        vector_search=vector_search,
        semantic_search=semantic_search,
    )
    index_client.create_or_update_index(index)
    print(f"[Azure Search] Index '{index_name}' created/updated successfully.")

    search_client = SearchClient(endpoint, index_name, AzureKeyCredential(key))

    pdf_path = Path(pdf_dir)
    docs = []
    if pdf_path.exists():
        pdf_files = sorted(pdf_path.glob("*.pdf"))
        print(f"[PDF Processing] Found {len(pdf_files)} PDF file(s) in '{pdf_dir}' folder.")
        for pdf_file in pdf_files:
            print(f"  [PDF] Processing: {pdf_file.name}")
            text = extract_pdf_text(str(pdf_file))
            if not text:
                print(f"    [PDF] No text extracted from {pdf_file.name}. Skipping.")
                continue
            chunks = chunk_text(text)
            print(f"    [Chunking] Split into {len(chunks)} chunks (size=800, overlap=100).")
            for i, chunk in enumerate(chunks):
                print(f"      [Embedding] Chunk {i+1}/{len(chunks)}...", end="\r")
                docs.append(
                    {
                        "id": f"{pdf_file.stem}-{i}",
                        "content": chunk,
                        "source": pdf_file.name,
                        "contentVector": embeddings.embed_query(chunk),
                    }
                )
            print(f"      [Embedding] All {len(chunks)} chunks embedded for {pdf_file.name}")

    if docs:
        print(f"\n[Upload] Uploading {len(docs)} documents to Azure Search index...")
        search_client.upload_documents(documents=docs)
        print(f"[Upload] Successfully uploaded {len(docs)} PDF chunks to '{index_name}'.")
        return search_client, f"Indexed {len(docs)} PDF chunks in Azure AI Search."

    print("[Warning] No PDF files were found in the pdfs folder. Azure Search index is ready but empty.")
    return search_client, "No PDF files were found in the pdfs folder. Azure Search is ready but no documents were uploaded."


def azure_retrieve(question: str, top_k: int = 5):
    """Retrieve context from Azure AI Search using vector similarity."""
    if not azure_search_enabled():
        return [], "Azure AI Search is not configured."

    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    key = os.getenv("AZURE_SEARCH_API_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
    settings = resolve_azure_openai_settings()

    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint=settings["azure_endpoint"],
        api_key=settings["api_key"],
        deployment=settings["deployment"],
        model=settings["deployment"],
        openai_api_version=settings["api_version"],
    )
    vector = embeddings.embed_query(question)
    client = SearchClient(endpoint, index_name, AzureKeyCredential(key))

    results = client.search(
        search_text=None,
        vector_queries=[{"kind": "vector", "vector": vector, "fields": "contentVector"}],
        select=["content", "source"],
        top=top_k,
    )

    documents = []
    for item in results:
        documents.append(f"Source: {item.get('source', 'unknown')}\n{item.get('content', '')}")

    return documents, "Retrieved from Azure AI Search vector store."


def retrieve_context(question: str, use_azure: bool = False):
    """Retrieve context from Azure AI Search when the Azure-backed RAG path is enabled."""
    if use_azure:
        azure_context, mode = azure_retrieve(question)
        if azure_context:
            return azure_context, mode

    return [], "Azure AI Search is not configured. Add the AZURE_* variables and PDF files to use the RAG knowledge base."


def build_rag_chain(llm):
    """Create a simple RAG chain for faculty support.

    LangChain helps by combining:
    - a prompt template,
    - retrieved context,
    - the LLM model,
    - and a text output parser.
    """
    prompt = ChatPromptTemplate.from_template(
        "You are an academic policy assistant for an engineering college in India. "
        "Use the retrieved context below to answer the question. "
        "If context is empty, clearly state that policy cannot be determined without retrieval data.\n\n"
        "Context:\n{context}\n\n"
        "Question:\n{question}\n\n"
        "Return in this format:\n"
        "1) Decision\n"
        "2) Policy clauses used\n"
        "3) Action checklist for faculty in the next 7 days\n"
        "4) Missing documents or risks"
    )

    return prompt | llm | StrOutputParser()


def run_rag_evaluators(question: str, context_chunks, answer: str):
    """Run built-in evaluators from azure-ai-evaluation."""
    if CoherenceEvaluator is None or GroundednessEvaluator is None or RelevanceEvaluator is None:
        return [
            {
                "name": "azure_ai_evaluation_unavailable",
                "passed": False,
                "score": 0.0,
                "details": "Install azure-ai-evaluation to enable built-in evaluators.",
            }
        ]

    model_config = build_azure_eval_model_config()
    context_text = "\n\n".join(context_chunks)

    # Relevance: checks whether the response actually addresses the user's question.
    # Why it matters: even grounded answers are not useful if they miss the asked task.
    #
    # Groundedness: checks whether claims in the response are supported by retrieved context.
    # Why it matters: this is the core anti-hallucination signal for RAG quality.
    #
    # Coherence: checks clarity, structure, and logical flow of the response.
    # Why it matters: policy guidance must be understandable and actionable for faculty.
    evaluators = [
        ("relevance", RelevanceEvaluator(model_config)),
        ("groundedness", GroundednessEvaluator(model_config)),
        ("coherence", CoherenceEvaluator(model_config)),
    ]

    output = []
    for name, evaluator in evaluators:
        try:
            result = evaluator(query=question, response=answer, context=context_text)
            score = float(result.get(name, result.get("score", 0.0)))
            details = result.get("reason", result.get("justification", ""))
            output.append(
                {
                    "name": name,
                    "passed": score >= 3.0,
                    "score": round(score, 3),
                    "details": details or "azure-ai-evaluation result",
                }
            )
        except Exception as exc:
            output.append(
                {
                    "name": name,
                    "passed": False,
                    "score": 0.0,
                    "details": f"Evaluation error: {exc}",
                }
            )

    return output


def run_rag_lab(topic: str = "Data Structures", question: str = None):
    """Run the RAG lab end to end.

    The workflow:
    1. Build the query.
    2. Retrieve relevant context from the in-memory academic knowledge base.
    3. Ask the LLM to answer using that context.
    """
    if question is None:
        question = (
            "A third-year ECE student has 68 percent attendance due to emergency surgery and "
            "submitted medical records after returning. Based on attendance and exam circular PDFs, "
            "is the student eligible for end-semester exam condonation, and what approvals must faculty complete?"
        )

    print("\n[RAG Lab] Starting Retrieval-Augmented Generation workflow...")
    print(f"[Question] {question}\n")

    llm = build_llm()
    rag_chain = build_rag_chain(llm)

    use_azure = azure_search_enabled()
    print(f"[Azure Search] Enabled: {'YES' if use_azure else 'NO'}")

    if use_azure:
        # If PDF files exist, upload them into Azure AI Search before retrieval.
        ensure_azure_index("pdfs")

    print("\n[Retrieval] Fetching relevant context from Azure Search...")
    context, mode = retrieve_context(question, use_azure=use_azure)
    print(f"[Retrieval] {mode}")
    print(f"[Retrieval] Retrieved {len(context)} relevant document chunk(s).")

    print("\n[LLM] Generating grounded answer using retrieved context...")
    answer = rag_chain.invoke({"context": "\n".join(context), "question": question})
    print("[LLM] Answer generation complete.\n")

    print("[Eval] Running 3 built-in Azure AI evaluators...")
    evaluations = run_rag_evaluators(question, context, answer)
    passed_count = sum(1 for item in evaluations if item["passed"])
    print(f"[Eval] Completed. Passed {passed_count}/{len(evaluations)} evaluators.\n")

    return {
        "question": question,
        "retrieved_context": context,
        "answer": answer,
        "evaluations": evaluations,
        "retrieval_mode": mode,
        "azure_search_used": use_azure and mode == "Retrieved from Azure AI Search vector store.",
    }


if __name__ == "__main__":
    result = run_rag_lab()

    print("=== RAG Faculty Policy Lab Output ===")
    print("\nQuestion:\n")
    print(result["question"])

    print("\nRetrieval mode:\n")
    print(result["retrieval_mode"])

    print("\n**Azure AI Search Used:**")
    print("**YES**" if result["azure_search_used"] else "**NO**")

    print("\nRetrieved Context:\n")
    for item in result["retrieved_context"]:
        print("-", item)

    print("\nGenerated Answer:\n")
    print(result["answer"])

    print("\nEvaluator Results:\n")
    for item in result["evaluations"]:
        status = "PASS" if item["passed"] else "FAIL"
        print(f"- {item['name']}: {status} | score={item['score']} | {item['details']}")
