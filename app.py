import streamlit as st
import validators

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

# ---------------- STREAMLIT UI ---------------- #

st.set_page_config(page_title="YT & Website Summarizer", page_icon="🧠")
st.title("🧠 GenAI Summarizer (YouTube + Website)")
st.subheader("Paste a URL to summarize")

# Sidebar API Key
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", type="password")

# URL Input
generic_url = st.text_input("Enter URL")

# ---------------- LLM ---------------- #

if groq_api_key:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=groq_api_key
    )
else:
    st.warning("Please enter Groq API Key")
    st.stop()

# ---------------- BUTTON ACTION ---------------- #

if st.button("Summarize"):

    if not generic_url.strip():
        st.error("Please enter a URL")

    elif not validators.url(generic_url):
        st.error("Invalid URL")

    else:
        try:
            with st.spinner("Processing... ⏳"):

                # ---------------- LOAD DATA ---------------- #

                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(
                        generic_url,
                        add_video_info=False
                    )
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={"User-Agent": "Mozilla/5.0"}
                    )

                docs = loader.load()

                # ---------------- PREPARE TEXT ---------------- #

                text = " ".join([doc.page_content for doc in docs])

                # ---------------- PROMPT ---------------- #

                prompt_template = """
                Summarize the following content in 5-7 bullet points:

                {text}
                """

                prompt = PromptTemplate.from_template(prompt_template)

                final_prompt = prompt.format(text=text)

                # ---------------- LLM CALL ---------------- #

                response = llm.invoke(final_prompt)

                # ---------------- OUTPUT ---------------- #

                st.success("Summary Generated ✅")
                st.write(response.content)

        except Exception as e:
            st.error(f"Error: {e}")