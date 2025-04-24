import streamlit as st
import os
from research_system import run_research_system
import os 
from dotenv import load_dotenv

load_dotenv() 

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "NotPerplexity"

st.title("NotPerplexity - Agentic Web Search")
st.caption("Powered by LangChain, LangGraph, Tavily, and Gemini")

query = st.text_input("Enter your Search query:")
if st.button("Start Search"):
    with st.spinner("Agentic Re-Search in progress..."):
        result = run_research_system(query)
        
        st.subheader("Research Results")
        st.json(result["research_data"])
        
        st.subheader("Final Answer")
        st.markdown(result["final_answer"])