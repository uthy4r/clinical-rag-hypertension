# 🏥 Clinical RAG Pipeline for Hypertension Decision Support

## 📋 Overview

This project implements a **Retrieval-Augmented Generation (RAG)** system for **adult hypertension management**, grounding LLM responses in authoritative clinical guidelines to reduce hallucinations and improve reliability. The system retrieves evidence from **ACC/AHA** and **WHO** hypertension guidelines and generates **risk-aware, citation-backed clinical answers** via an interactive **Streamlit frontend** and **FastAPI backend**.

**Key Features:**
- ✅ Evidence-grounded responses (no hallucinations)
- ✅ Risk-stratified recommendations
- ✅ Citation-backed answers
- ✅ Production-ready architecture

---

## 🏗️ Architecture

```
🔍 User Query
    ↓
🧠 OpenAI Embeddings
    ↓
📊 Pinecone Vector Database
    ↓
📚 Top-K Evidence Retrieval
    ↓
✍️ Evidence-Grounded Prompt
    ↓
🤖 LLM (GPT-4o-mini)
    ↓
✅ Cited Clinical Answer
```

---

## 📚 Data Sources

- **ACC/AHA Hypertension Guidelines (2017, 2025 summary)**
- **WHO Pharmacological Treatment of Hypertension**

*Note: Raw guideline text is not included due to licensing restrictions.*

---

## 🛡️ Safety & Hallucination Control

The system is designed to:

- **🚫 Refuse to generate answers** if the evidence provided is insufficient or incomplete
- **✅ Use evidence only** for answer generation, avoiding hallucination and ungrounded responses
- **📊 Provide risk-stratified recommendations** for patients with **stage 1 hypertension** based on their ASCVD risk

---

## ⚙️ Engineering Decisions

- **🔗 Avoided LangChain** to reduce dependency volatility and maintain explicit control over the retrieval process and prompt construction
- **📦 Batched Pinecone upserts** to respect request size limits, ensuring smooth and reliable data ingestion
- **⚡ Used `text-embedding-3-small`** for embeddings, optimizing for latency, cost, and retrieval quality in a clinical context

---

## 📁 Repository Structure

```
clinical-rag-hypertension/
├── notebooks/
│   └── RAG_Pipeline.ipynb              # Full RAG pipeline & testing
├── api/
│   └── app.py                          # FastAPI backend
├── ui.py                               # Streamlit web interface
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

This will start the FastAPI server at `http://127.0.0.1:8000`. 🎯

### 5️⃣ Run the Frontend (Streamlit)

In another terminal, run:

```bash
streamlit run ui.py
```

This will start the Streamlit UI at `http://localhost:8501`. 🎨

---

## 📡 API Documentation

### `POST /query`

This endpoint accepts a clinical question and returns an evidence-grounded answer.

**Request Body:**

```json
{
  "question": "What is the first-line treatment for stage 1 hypertension?"
}
```

**Response:**

```json
{
  "answer": "For adults with stage 1 hypertension and a 10-year ASCVD risk <10%, nonpharmacologic therapy such as lifestyle modification is recommended initially, with reassessment in 3–6 months [ACC/AHA 2017]."
}
```

The answer will always cite relevant sources where applicable, for example: `[ACC/AHA 2017]`. 📖

---

## 📝 Model Details

### Risk Stratification Strategy

| Risk Level | ASCVD Score | Clinical Interpretation | Recommended Action |
|-----------|-------------|------------------------|-------------------|
| **High Risk** | ≥ 10% | Pharmacologic intervention likely indicated | Initiate antihypertensive therapy |
| **Moderate Risk** | 5-10% | Shared decision-making | Consider pharmacotherapy or lifestyle |
| **Low Risk** | < 5% | Continue lifestyle management | Reassess in 3-6 months |

---

## 🌐 Deployment

### Live Demo

📱 **Streamlit Cloud:** Coming soon

### Deployment Architecture

This app can be deployed using:

- **Streamlit Cloud:** For the Python web interface
- **Cloud Run/AWS:** For the FastAPI backend
- **Pinecone Cloud:** For vector database hosting

---

## 📚 Technologies Used

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit | Interactive web interface |
| **Backend** | FastAPI | REST API for RAG pipeline |
| **LLM** | OpenAI GPT-4o-mini | Answer generation |
| **Embeddings** | OpenAI text-embedding-3-small | Query & document embeddings |
| **Vector DB** | Pinecone | Semantic search & retrieval |
| **Language** | Python 3.10+ | Core development |

---

## 🔐 Security Notes

✅ **No hardcoded secrets** — All API keys managed via `.env`  
✅ **Environment-based config** — `.env.example` template provided  
✅ **Production-ready** — Secure credential handling  
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
- Restart the application after updating `.env`

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
- Ensure index name matches configuration

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

---

## 🎯 Next Steps

1. **Configure environment variables** in `.env`
2. **Run the FastAPI backend** in one terminal
3. **Launch the Streamlit app** in another terminal
4. **Test with sample queries** about hypertension management
5. **Deploy to Streamlit Cloud** when ready

---

## 💬 Questions or Contributions?

Feel free to open an issue or submit a pull request. For medical-specific inquiries, please consult the documentation or reach out to the maintainers. 👋

---

**Last Updated:** January 2026  
**Version:** 1.0 (RAG Pipeline with Evidence Grounding)
