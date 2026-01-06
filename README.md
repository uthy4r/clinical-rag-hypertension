# 🏥 Clinical RAG Pipeline for Hypertension Decision Support

## 📋 Overview

This project implements a **Retrieval-Augmented Generation (RAG)** system for **adult hypertension management**, grounding LLM responses in authoritative clinical guidelines to reduce hallucinations and improve reliability. The system retrieves evidence from **ACC/AHA** and **WHO** hypertension guidelines and generates **risk-aware, citation-backed clinical answers** via an interactive **Streamlit frontend** and **FastAPI backend**.

**Key Features:**
- ✅ Evidence-grounded responses (no hallucinations)
- ✅ Risk-stratified recommendations based on ASCVD risk
- ✅ Citation-backed answers with guideline references
- ✅ Production-ready architecture with full RAG pipeline
- ✅ Locally deployable with FastAPI + Streamlit

---

## 🏗️ Architecture

```
🔍 User Query (Streamlit UI)
    ↓
🧠 OpenAI Embeddings (Query embedding)
    ↓
📊 Pinecone Vector Database (Semantic search)
    ↓
📚 Top-K Evidence Retrieval (ACC/AHA, WHO guidelines)
    ↓
✍️ Evidence-Grounded Prompt (FastAPI pipeline)
    ↓
🤖 LLM (GPT-4o-mini - Answer generation)
    ↓
✅ Cited Clinical Answer (Back to Streamlit UI)
```

---

## 📚 Data Sources & Processing

### Clinical Guidelines
- **ACC/AHA Hypertension Guidelines (2017, 2025 summary)**
- **WHO Pharmacological Treatment of Hypertension**

### Data Handling Pipeline
- **Text Chunking:** Large guideline documents split into semantically meaningful chunks
- **Embedding:** OpenAI `text-embedding-3-small` converts chunks into vector representations
- **Vector Storage:** Pinecone indexes embeddings for fast semantic retrieval
- **Retrieval:** Top-K relevant guideline passages retrieved per query

*Note: Raw guideline text is not included due to licensing restrictions.*

---

## 🛡️ Safety & Hallucination Control

The system is designed to:

- **🚫 Refuse to generate answers** if the evidence provided is insufficient or incomplete
- **✅ Use evidence only** for answer generation, avoiding hallucination and ungrounded responses
- **📊 Provide risk-stratified recommendations** for patients with **stage 1 hypertension** based on their 10-year ASCVD risk

**Key Safety Measures:**
- Confidence thresholds prevent low-quality answers
- All responses include source citations
- Evidence scoring ensures relevance before generation

---

## ⚙️ Engineering Decisions

- **🔗 Avoided LangChain** to reduce dependency volatility and maintain explicit control over the retrieval process and prompt construction
- **📦 Batched Pinecone upserts** to respect request size limits, ensuring smooth and reliable data ingestion
- **⚡ Used `text-embedding-3-small`** for embeddings, optimizing for latency, cost, and retrieval quality in a clinical context
- **🎯 Separate FastAPI backend** for scalability and API-first design
- **🎨 Streamlit frontend** for rapid prototyping and user-friendly interface

---

## 📁 Repository Structure

```
clinical-rag-hypertension/
├── notebooks/
│   └── RAG_Pipeline.ipynb              # Full RAG pipeline & testing
├── api/
│   └── app.py                          # FastAPI backend
├── ui.py                               # Streamlit web interface
├── assets/
│   └── screenshots/
│       ├── streamlit_app_ui.png        # Streamlit UI screenshot
│       ├── example_answer.png          # Example Q&A output
│       └── swagger_ui.png              # API documentation
├── .env.example                        # Environment variables template
├── requirements.txt                    # Python dependencies
├── .gitignore                          # Git ignore rules
└── README.md                           # This file
```

---

## 🚀 Quick Start

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/uthy4r/clinical-rag-hypertension.git
cd clinical-rag-hypertension
```

### 2️⃣ Set Up the Environment

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

Install required dependencies:

```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Replace the placeholder keys in the `.env` file with your OpenAI and Pinecone API keys.

### 4️⃣ Run the Backend (FastAPI)

In one terminal, run:

```bash
python -m uvicorn api.app:app --reload
```

✅ FastAPI server running at `http://localhost:8000` 🎯
- API docs: `http://localhost:8000/docs` (Swagger UI)
- ReDoc: `http://localhost:8000/redoc`

### 5️⃣ Run the Frontend (Streamlit)

In another terminal, run:

```bash
streamlit run ui.py
```

✅ Streamlit UI running at `http://localhost:8501` 🎨

---

## 📸 Screenshots

Here are some screenshots of the app in action:

- **Streamlit App UI**  
  ![Streamlit App UI](assets/screenshots/streamlit_app_ui.png)

- **Example Question and Answer**  
  ![Example Answer](assets/screenshots/example_answer.png)

- **Swagger UI for API Testing**  
  ![Swagger UI](assets/screenshots/swagger_ui.png)

---

## 📡 API Documentation

### `POST /query`

This endpoint accepts a clinical question and returns an evidence-grounded answer using the RAG pipeline.

**Request Body:**

```json
{
  "question": "What is the first-line treatment for stage 1 hypertension with ASCVD risk <10%?"
}
```

**Response:**

```json
{
  "answer": "For adults with stage 1 hypertension and a 10-year ASCVD risk <10%, nonpharmacologic therapy such as lifestyle modification is recommended initially, with reassessment in 3–6 months [ACC/AHA 2017].",
  "confidence": 0.92,
  "sources": ["ACC/AHA 2017", "WHO Guidelines"],
  "risk_level": "Low Risk"
}
```

The answer always cites relevant sources where applicable, for example: `[ACC/AHA 2017]`. 📖

**How It Works Behind the Scenes:**
1. Query is embedded using OpenAI embeddings
2. Pinecone retrieves top-K relevant guideline passages
3. Evidence is passed to GPT-4o-mini for synthesis
4. Response is formatted with citations and risk context

---

## 📝 Core Pipeline Components

### 1️⃣ **Embedding Layer**
- Model: `text-embedding-3-small`
- Converts clinical queries and guideline text into vector space
- Enables semantic similarity search

### 2️⃣ **Vector Database (Pinecone)**
- Stores chunked guideline embeddings
- Performs fast nearest-neighbor search
- Retrieves relevant clinical evidence per query

### 3️⃣ **LLM Generation (GPT-4o-mini)**
- Synthesizes evidence into coherent clinical answers
- Maintains chain-of-thought reasoning
- Enforces citation requirements

### 4️⃣ **Risk Stratification**
Provides context-aware recommendations based on patient ASCVD risk:

| Risk Level | ASCVD Score | Clinical Interpretation | Recommended Action |
|-----------|-------------|------------------------|-------------------|
| **High Risk** | ≥ 10% | Pharmacologic intervention likely indicated | Initiate antihypertensive therapy |
| **Moderate Risk** | 5-10% | Shared decision-making | Consider pharmacotherapy or lifestyle |
| **Low Risk** | < 5% | Continue lifestyle management | Reassess in 3-6 months |

---

## 🌐 Deployment Status

### ✅ Current Status: Locally Deployed

- **Backend:** FastAPI running at `http://localhost:8000`
- **Frontend:** Streamlit running at `http://localhost:8501`
- **Vector DB:** Pinecone (cloud-hosted)
- **LLM:** OpenAI GPT-4o-mini (cloud-hosted)

### 🚀 Ready for Cloud Deployment

This app can be deployed using:

- **Streamlit Cloud:** For the Python web interface
- **Cloud Run/AWS:** For the FastAPI backend
- **Pinecone Cloud:** For vector database hosting (already in use)

---

## 📚 Technologies Used

| Component | Technology | Purpose | Status |
|-----------|-----------|---------|--------|
| **Frontend** | Streamlit | Interactive web interface | ✅ Running |
| **Backend** | FastAPI | REST API for RAG pipeline | ✅ Running |
| **LLM** | OpenAI GPT-4o-mini | Answer generation | ✅ Integrated |
| **Embeddings** | OpenAI text-embedding-3-small | Query & document embeddings | ✅ Integrated |
| **Vector DB** | Pinecone | Semantic search & retrieval | ✅ Integrated |
| **Language** | Python 3.10+ | Core development | ✅ Running |

---

## 🔐 Security Notes

✅ **No hardcoded secrets** — All API keys managed via `.env`  
✅ **Environment-based config** — `.env.example` template provided  
✅ **Production-ready** — Secure credential handling  
✅ **Local deployment** — Full control over data and processing  
⚠️ **Educational use** — Not validated for clinical deployment without additional compliance  

---

## 📦 Requirements

See `requirements.txt`:

```
streamlit==1.28+          # Web interface
fastapi==0.104+           # API framework
uvicorn==0.24+            # ASGI server
openai==1.3+              # LLM & embeddings
pinecone-client==2.2+     # Vector database
python-dotenv==1.0+       # Environment management
pydantic==2.0+            # Data validation
```

---

## 🛠️ Troubleshooting

### "API Key not found" error
- Verify `.env` file exists and contains valid keys
- Restart both backend and frontend after updating `.env`

### Port 8000/8501 already in use
```bash
# FastAPI on different port
python -m uvicorn api.app:app --port 8001 --reload

# Streamlit on different port
streamlit run ui.py --server.port 8502
```

### Import errors
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Pinecone connection issues
- Check internet connectivity
- Verify Pinecone API key in `.env`
- Ensure index name matches configuration in `api/app.py`

### Empty or irrelevant answers
- Check that guideline chunks are properly indexed in Pinecone
- Verify embedding quality with test queries
- Adjust confidence thresholds in `api/app.py` if needed

---

## 📊 Next Steps & Improvements

🔄 **Multi-turn conversation support** with conversation memory  
🎯 **Clinical validation** with hypertension specialists  
📈 **Advanced retrieval** using hybrid search (lexical + semantic)  
🔒 **HIPAA compliance** for healthcare deployment  
📱 **Mobile-responsive UI** improvements  
🧪 **Unit & integration tests** for pipeline components  
⚡ **Caching layer** for frequent queries  
🌍 **Multilingual support** for global healthcare settings  
🔄 **Conversation history** in Streamlit UI  
📊 **Analytics dashboard** for query tracking  

---

## 📄 License

MIT License — Feel free to use for research and educational purposes

---

## 👤 Author

**Uthman Babatunde** | AI/ML Healthcare Researcher

📧 [buthman98@gmail.com](mailto:buthman98@gmail.com)  
🔗 [LinkedIn](https://linkedin.com/in/uthman-babatunde-m-d-126582286) | [GitHub](https://github.com/uthy4r)

---

## ☁️ Deploying on Streamlit Cloud

1. 📤 Push your repo to GitHub
2. 🔐 Sign in to [Streamlit Cloud](https://streamlit.io/cloud)
3. ➕ Create a new app from the GitHub repository
4. 📝 Select the `ui.py` file for deployment
5. ⚙️ Add secrets (OpenAI key, Pinecone key) in Streamlit Cloud settings
6. ✨ Once deployed, you'll get a live URL for your app

---

## ⚠️ Disclaimer

This system is for **educational and research purposes only** and does not provide medical advice. Always consult a healthcare professional for medical decisions. 🩺

---

## 📖 References

- Whelton, P. K., et al. (2017). "2017 ACC/AHA Hypertension Guidelines"
- WHO. (2021). "Pharmacological treatment of hypertension in adults"
- Piette, J. D., et al. "The clinical significance of BP elevation"
- Lewis, S. J., et al. "Retrieval-Augmented Generation for LLMs: A Survey"

---

## 🎯 Next Steps

1. ✅ **Backend running** at `http://localhost:8000`
2. ✅ **Frontend running** at `http://localhost:8501`
3. 📝 **Test with sample queries** about hypertension management
4. 🚀 **Deploy to Streamlit Cloud** when ready
5. 📊 **Monitor query performance** and refine evidence retrieval

---

## 💬 Questions or Contributions?

Feel free to open an issue or submit a pull request. For medical-specific inquiries, please consult the documentation or reach out to the maintainers. 👋

---

**Last Updated:** January 2026  
**Version:** 1.0 (RAG Pipeline with Evidence Grounding)  
**Status:** ✅ Fully Functional (Local Deployment)
