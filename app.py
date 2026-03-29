import streamlit as st
import validators

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(page_title="InsightAI", page_icon="🧠", layout="centered")

st.markdown("""
    <h1 style='text-align: center;'>🧠 InsightAI</h1>
    <p style='text-align: center;'>Summarize YouTube Videos & Websites using GenAI</p>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #

with st.sidebar:
    st.header("🔑 Settings")
    groq_api_key = st.text_input("Enter Groq API Key", type="password")
    
    summary_type = st.selectbox(
        "Summary Type",
        ["Brief (5 points)", "Detailed", "Explain like I'm 10"]
    )

# ---------------- INPUT ---------------- #

generic_url = st.text_input("🔗 Paste YouTube or Website URL")

# ---------------- LLM ---------------- #

if groq_api_key:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=groq_api_key
    )
else:
    st.warning("Please enter Groq API Key")
    st.stop()

# ---------------- BUTTON ---------------- #

if st.button("🚀 Generate Summary"):

    if not generic_url.strip():
        st.error("Please enter a URL")

    elif not validators.url(generic_url):
        st.error("Invalid URL")

    else:
        try:
            with st.spinner("🔄 Fetching and summarizing content..."):

                # -------- LOAD DATA -------- #

                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    try:
                        loader = YoutubeLoader.from_youtube_url(
                            generic_url,
                            add_video_info=False
                        )
                        docs = loader.load()
                        if not docs:
                            st.error("No transcript available ❌")
                            st.stop()
                    except:
                        st.error("Invalid or restricted YouTube video ❌")
                        st.stop()
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={"User-Agent": "Mozilla/5.0"}
                    )
                    docs = loader.load()

                # -------- PREPARE TEXT -------- #

                text = " ".join([doc.page_content for doc in docs])

                # -------- SYSTEM PROMPT -------- #

                if summary_type == "Brief (5 points)":
                    instruction = "Summarize in 5 clear bullet points."
                elif summary_type == "Detailed":
                    instruction = "Provide a detailed structured summary with headings and bullet points."
                else:
                    instruction = "Explain the content in very simple terms like to a 10-year-old."

                prompt_template = f"""
                You are an intelligent AI assistant.

                {instruction}

                Also:
                - Keep it clear and structured
                - Avoid unnecessary words
                - Highlight key insights

                Content:
                {{text}}
                """

                prompt = PromptTemplate.from_template(prompt_template)

                final_prompt = prompt.format(text=text[:12000])  # limit input

                # -------- LLM CALL -------- #

                response = llm.invoke(final_prompt)

                # -------- OUTPUT -------- #

                st.success("✅ Summary Generated")

                st.markdown("### 📌 Summary")
                st.write(response.content)

        except Exception as e:
            st.error(f"❌ Error: {e}")