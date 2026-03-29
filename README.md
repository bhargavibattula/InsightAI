# 🧠 InsightAI

**GenAI-Powered YouTube & Website Summarization Platform**

InsightAI is a high-performance GenAI application that transforms long-form video and web content into structured, readable summaries in seconds. Built using modern LLM infrastructure and optimized for speed, it delivers customizable summaries tailored to different levels of understanding.

---

## ✨ Overview

InsightAI enables users to extract meaningful insights from:
- **YouTube videos** (via transcript extraction)
- **Web pages and articles** (via content parsing)

The application leverages large language models to generate:
- Concise bullet summaries
- Detailed structured explanations
- Simplified “Explain Like I’m 10” outputs

All within a responsive and minimal interface.

---

## 🚀 Key Features

- **Multi-source summarization:** Supports both YouTube videos and web URLs.
- **Custom summary modes:** 
  - *Brief* (key points)
  - *Detailed* (structured explanation)
  - *Simplified* (beginner-friendly)
- **Fast inference:** Powered by Groq’s ultra-low latency LLM APIs.
- **Robust input handling:** Graceful handling of invalid URLs, missing transcripts, restricted content, and gracefully bypassing broken metadata-scraping libraries.
- **Clean and intuitive UI:** Built with Streamlit for rapid interaction.

---

## 🧠 System Architecture

Here is an architectural overview of how InsightAI processes your requests:

```mermaid
flowchart TD
    A[User Inputs URL & Groq API Key] --> B{URL Type}
    B -->|YouTube| C[YoutubeLoader<br/>(youtube_transcript_api)]
    B -->|Website| D[UnstructuredURLLoader<br/>(Web Scraper)]
    C --> E[Document Joiner & Text Truncator]
    D --> E
    E --> F[LangChain Prompt Template]
    F --> G[ChatGroq LLM Context<br/>(llama-3.3-70b-versatile)]
    G --> H[Streamlit UI Output]
```

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **AI / NLP:** LangChain (latest modular API), Groq LLM (llama-3.3-70b-versatile)
- **Data Extraction:** youtube_transcript_api, UnstructuredURLLoader, BeautifulSoup / Requests

---

## ⚙️ Installation & Setup

**1. Clone Repository**
```bash
git clone https://github.com/bhargavibattula/InsightAI.git
cd InsightAI
```

**2. Create Virtual Environment**
Using the standard Python method:
```bash
python -m venv .venv
```
Activate:
- **Windows:** `.venv\Scripts\activate`
- **Mac/Linux:** `source .venv/bin/activate`

*(Alternatively, you can initialize the project using the `uv` package manager: `uv venv`)*

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```
*(If using `uv` run: `uv pip install -r requirements.txt`)*

**4. Run Application**
```bash
streamlit run app.py
```
*(If using `uv` run: `uv run streamlit run app.py`)*

**5. Configure API Key**
- Generate your API key from the [Groq Console](https://console.groq.com)
- Enter it in the sidebar
- Provide a valid URL
- Click Generate Summary!

---

## 📌 Example Use Cases

- Quickly understand long technical videos
- Summarize research/blog articles
- Create notes from educational content
- Simplify complex topics

---

## 📈 Future Improvements

- 👉 Chat with video/web content
- 👉 Multi-language summarization
- 👉 Export summaries (PDF / Markdown)
- 👉 Semantic search over content

---

## 👨‍💻 Author

**Bhargavi Tejaswi**

*❤️ by bhargavibattula*

---

## ⭐ Final Note

InsightAI is designed with a focus on:
- **Performance**
- **Simplicity**
- **Real-world usability**

It demonstrates the practical application of GenAI systems for content understanding at scale.
