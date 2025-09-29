import streamlit as st
import folium
from streamlit_folium import folium_static
import requests
import json
import time
from sentence_transformers import SentenceTransformer
import chromadb

# Configure page
st.set_page_config(
    page_title="TrafficWise Urban Planner",
    page_icon="🚦",
    layout="wide"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# Initialize vector database and embedding model
@st.cache_resource
def initialize_rag():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    client = chromadb.Client()
    collection = client.get_or_create_collection("traffic_data")
    return model, collection

model, collection = initialize_rag()

# Sidebar configuration
st.sidebar.title("🚦 TrafficWise Urban Planner")
st.sidebar.markdown("Your AI Assistant for Traffic & Urban Planning")

# AI Service Selection
ai_service = st.sidebar.selectbox(
    "Choose AI Service:",
    ["Google Gemini API", "OpenAI API", "Local RAG", "Offline Mode"]
)

# API Configuration
if ai_service == "Google Gemini API":
    api_key = st.sidebar.text_input(
        "Google Gemini API Key:", 
        type="password", 
        help="Get from https://aistudio.google.com/app/apikey"
    )
elif ai_service == "OpenAI API":
    api_key = st.sidebar.text_input("OpenAI API Key:", type="password", help="Get from https://platform.openai.com")

# Temperature slider
temperature = st.sidebar.slider(
    "AI Response Variation:",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1,
    help="Higher values provide more varied suggestions"
)

# Map toggle
show_map = st.sidebar.checkbox("Show Interactive Traffic Map", value=True)

# Upload new documents to the knowledge base
uploaded_file = st.sidebar.file_uploader("Upload Traffic Data", type=["txt", "json"])
if uploaded_file:
    new_data = uploaded_file.read().decode("utf-8")
    embedding = model.encode(new_data)
    collection.add(
        documents=[new_data],
        metadatas=[{"source": "uploaded"}],
        ids=[str(time.time())]
    )
    st.sidebar.success("✅ Data added to knowledge base!")

# RAG-based response generation
def retrieve_documents(query, top_k=3):
    """Retrieve relevant documents from the vector database."""
    query_embedding = model.encode(query)
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return [result["document"] for result in results["documents"]]

def local_rag_response(user_message):
    """Generate a response using RAG."""
    retrieved_docs = retrieve_documents(user_message)
    if not retrieved_docs:
        return "❌ No relevant information found in the knowledge base."
    
    context = "\n".join(retrieved_docs)
    enhanced_prompt = f"""You are a senior traffic and urban planning consultant specializing in Pakistani cities. Use the following knowledge base to answer the query:

### Knowledge Base:
{context}

### Query:
{user_message}

### Response:"""
    
    # Simulate response generation
    return f"""📚 **RAG-Enhanced Response:**

{enhanced_prompt}

{offline_traffic_response(user_message)}"""

# Main interface
col1, col2 = st.columns([3, 1])

with col1:
    st.title("🚦 TrafficWise Urban Planner")
    st.markdown("""
    ### Your AI Assistant for:
    - 🚗 Traffic Route Optimization in Pakistan
    - 🌆 Urban Congestion Solutions
    - 🚦 Traffic Flow Analysis
    - 🛣️ Infrastructure Planning
    - 🚌 Public Transport Integration
    """)

    # Display chat history
    for message in st.session_state.chat_history:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.markdown(f"**👤 You:** {content}")
        else:
            st.markdown(f"**🚦 TrafficWise:** {content}")
        st.markdown("---")

    # Chat input
    def submit_message():
        if st.session_state.user_input:
            user_message = st.session_state.user_input
            st.session_state.chat_history.append({"role": "user", "content": user_message})
            
            with st.spinner('🤖 Analyzing traffic patterns with AI...'):
                if ai_service == "Google Gemini API" and api_key:
                    response = chat_with_gemini(user_message, temperature, api_key, "gemini-1.5-flash")
                elif ai_service == "OpenAI API" and api_key:
                    response = chat_with_openai(user_message, temperature, api_key)
                elif ai_service == "Local RAG":
                    response = local_rag_response(user_message)
                else:
                    response = offline_traffic_response(user_message)
            
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.session_state.user_input = ""

    st.text_input(
        "Ask about traffic routes, urban planning, or congestion solutions in Pakistan...",
        key="user_input",
        on_change=submit_message,
        placeholder="Example: Best route from Lahore to Islamabad during peak hours?"
    )

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []

with col2:
    if show_map:
        st.subheader("🗺️ Pakistan Traffic Map")
        folium_static(generate_pakistan_traffic_map(), width=400, height=500)

# Footer
st.markdown("---")
st.markdown("🚦 **TrafficWise Pakistan** - Powered by RAG | Smart Traffic Solutions for Pakistani Cities")