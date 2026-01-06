# 🏥 Clinical RAG Pipeline for Hypertension Decision Support

## 📋 Overview

This project implements a **Retrieval-Augmented Generation (RAG)** system for **adult hypertension management**, grounding LLM responses in authoritative clinical guidelines to reduce hallucinations and improve reliability. The system retrieves evidence from **ACC/AHA** and **WHO** hypertension guidelines and generates **risk-aware, citation-backed clinical answers** via an interactive **Streamlit frontend** and **FastAPI backend**.

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

## 🚀 How to Run Locally

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

## ☁️ Deploying on Streamlit Cloud

1. 📤 Push your repo to GitHub (if you haven't already)
2. 🔐 Sign in to [Streamlit Cloud](https://streamlit.io/cloud)
3. ➕ Create a new app from the GitHub repository
4. 📝 Select the `ui.py` file for deployment
5. ✨ Once deployed, you will get a live URL for your app

---

## ⚠️ Disclaimer

This system is for **educational and research purposes only** and does not provide medical advice. Always consult a healthcare professional for medical decisions. 🩺

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🎯 Next Steps

1. **Push the changes to GitHub:**

```bash
git add README.md
git commit -m "Add comprehensive README"
git push
```

2. Test your deployment (Streamlit Cloud or locally) with the final URL 🧪

---

## 💬 Questions or Contributions?

Feel free to open an issue or submit a pull request. For medical-specific inquiries, please consult the documentation or reach out to the maintainers. 👋
