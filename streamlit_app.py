
import streamlit as st
import folium
from streamlit_folium import folium_static
import requests
import json
import time

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
    if not api_key:
        st.sidebar.warning("⚠️ Please enter your Google Gemini API key")
        st.sidebar.markdown("**Get your free API key:**")
        st.sidebar.markdown("1. Visit https://aistudio.google.com/app/apikey")
        st.sidebar.markdown("2. Sign in with Google account")
        st.sidebar.markdown("3. Click 'Create API Key'")
        st.sidebar.markdown("4. Copy and paste here")

elif ai_service == "OpenAI API":
    api_key = st.sidebar.text_input("OpenAI API Key:", type="password", help="Get from https://platform.openai.com")
    if not api_key:
        st.sidebar.warning("⚠️ Please enter your OpenAI API key")

# Model selection for Gemini
gemini_model = st.sidebar.selectbox(
    "Gemini Model:",
    ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"],
    help="Flash is faster, Pro is more capable"
) if ai_service == "Google Gemini API" else "gemini-1.5-flash"

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

def generate_pakistan_traffic_map():
    """Generate an interactive map of Pakistan with traffic information"""
    # Center on Pakistan
    m = folium.Map(location=[30.3753, 69.3451], zoom_start=6)
    
    # Major Pakistani cities with simulated traffic data
    cities = [
        {
            "city": "Lahore", 
            "lat": 31.582045, 
            "lon": 74.329376, 
            "color": "red",
            "traffic": "Heavy",
            "info": "Cultural capital - Heavy traffic during peak hours (7-9 AM, 5-8 PM)"
        },
        {
            "city": "Karachi", 
            "lat": 24.8607, 
            "lon": 67.0011, 
            "color": "darkred",
            "traffic": "Very Heavy",
            "info": "Economic hub - Severe congestion on main arteries"
        },
        {
            "city": "Islamabad", 
            "lat": 33.6844, 
            "lon": 73.0479, 
            "color": "green",
            "traffic": "Moderate",
            "info": "Capital city - Well-planned roads, moderate traffic"
        },
        {
            "city": "Rawalpindi", 
            "lat": 33.5651, 
            "lon": 73.0169, 
            "color": "orange",
            "traffic": "Heavy",
            "info": "Twin city - Connected to Islamabad, busy commercial area"
        },
        {
            "city": "Faisalabad", 
            "lat": 31.4187, 
            "lon": 73.0790, 
            "color": "blue",
            "traffic": "Moderate",
            "info": "Industrial city - Traffic concentrated in textile areas"
        },
        {
            "city": "Peshawar", 
            "lat": 34.0151, 
            "lon": 71.5249, 
            "color": "purple",
            "traffic": "Moderate",
            "info": "Historic city - Congestion in old city areas"
        },
        {
            "city": "Multan", 
            "lat": 30.1575, 
            "lon": 71.5249, 
            "color": "cadetblue",
            "traffic": "Light",
            "info": "City of Saints - Manageable traffic flow"
        }
    ]
    
    # Add markers for each city
    for city in cities:
        popup_html = f"""
        <div style="width: 200px;">
            <h4>{city['city']}</h4>
            <p><b>Traffic Level:</b> {city['traffic']}</p>
            <p>{city['info']}</p>
            <p><i>Click for route suggestions</i></p>
        </div>
        """
        
        folium.Marker(
            [city["lat"], city["lon"]],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{city['city']} - {city['traffic']} Traffic",
            icon=folium.Icon(color=city["color"], icon="car", prefix="fa")
        ).add_to(m)
    
    # Add major highways
    highway_routes = [
        # Grand Trunk Road (Lahore to Peshawar)
        [[31.582045, 74.329376], [33.6844, 73.0479], [34.0151, 71.5249]],
        # Motorway (Lahore to Karachi)
        [[31.582045, 74.329376], [31.4187, 73.0790], [30.1575, 71.5249], [24.8607, 67.0011]]
    ]
    
    colors = ['blue', 'red']
    names = ['GT Road', 'M-1/M-2 Motorway']
    
    for i, route in enumerate(highway_routes):
        folium.PolyLine(
            route,
            color=colors[i],
            weight=4,
            opacity=0.7,
            popup=f"Major Highway: {names[i]}"
        ).add_to(m)
    
    return m

def chat_with_gemini(user_message, temperature, api_key, model):
    """Chat with Google Gemini API"""
    enhanced_prompt = f"""You are a traffic and urban planning expert for Pakistan. Help with the following query: {user_message}

    Consider Pakistani context including:
    - Local traffic patterns and peak hours (7-9 AM, 5-8 PM)
    - Public transport systems (Metro Bus, Orange Line, BRT)
    - Weather impacts (monsoon season July-Sept, fog Dec-Feb)
    - Cultural and religious events affecting traffic (Friday prayers, Ramadan, Eid)
    - Infrastructure challenges and ongoing development projects
    - Major cities: Karachi, Lahore, Islamabad, Rawalpindi, Faisalabad, Peshawar
    - Highway systems: Motorways (M-1, M-2, M-3), GT Road, National Highways
    
    Provide practical, actionable advice specific to Pakistani traffic conditions.
    """
    
    # Gemini API endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    # Prepare the request payload
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": enhanced_prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": temperature,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 1024,
        },
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 400:
            error_detail = response.json()
            return f"❌ Gemini API Error 400: {error_detail.get('error', {}).get('message', 'Bad request - check your API key and request format')}"
        elif response.status_code == 403:
            return "❌ API Error 403: Invalid API key or insufficient permissions. Please check your Gemini API key."
        elif response.status_code == 429:
            return "❌ Rate Limit: Too many requests. Please wait a moment and try again."
        elif response.status_code == 404:
            return f"❌ Model not found: {model}. Try using 'gemini-pro' or 'gemini-1.5-flash'"
        
        response.raise_for_status()
        response_data = response.json()
        
        # Extract the generated text from Gemini response
        if 'candidates' in response_data and len(response_data['candidates']) > 0:
            candidate = response_data['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                return candidate['content']['parts'][0]['text']
            else:
                return "❌ Unexpected response format from Gemini API"
        else:
            return "❌ No response generated. The content might have been blocked by safety filters."
            
    except requests.exceptions.Timeout:
        return "❌ Request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"❌ Connection Error: {str(e)}"
    except json.JSONDecodeError:
        return "❌ Invalid response format from Gemini API"
    except Exception as e:
        return f"❌ Unexpected Error: {str(e)}"

def chat_with_openai(user_message, temperature, api_key):
    """Chat with OpenAI API"""
    enhanced_prompt = f"""As a traffic and urban planning expert for Pakistan, help with: {user_message}"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": enhanced_prompt}],
        "temperature": temperature,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ OpenAI Error: {str(e)}"

def offline_traffic_response(user_message):
    """Provide offline traffic responses using rule-based logic"""
    user_message_lower = user_message.lower()
    
    # Route suggestions
    if any(word in user_message_lower for word in ['route', 'road', 'path', 'way']):
        return """🛣️ **Route Planning Tips for Pakistan:**

**Major Cities Routes:**
- **Lahore to Islamabad**: Use Motorway M-2 (3.5 hours) - fastest option
- **Karachi to Lahore**: M-9 to M-2 Motorway (18-20 hours) - avoid GT Road
- **Islamabad to Peshawar**: M-1 Motorway (2 hours) - safer than GT Road

**Peak Hours to Avoid:**
- Morning: 7:00-9:30 AM
- Evening: 4:30-7:30 PM
- Friday: 12:00-2:00 PM (Jumma prayers)

**Monsoon Season (July-September):**
- Check weather before traveling
- Avoid underpass areas in Karachi, Lahore
- Keep emergency kit in car"""

    elif any(word in user_message_lower for word in ['congestion', 'traffic jam', 'heavy traffic']):
        return """🚦 **Congestion Management:**

**Most Congested Areas:**
- Karachi: Shahrah-e-Faisal, I.I. Chundrigar Road
- Lahore: Mall Road, Canal Road, Ring Road
- Islamabad: Blue Area, Margalla Road during office hours

**Solutions:**
1. **Use Apps**: Google Maps, Careem for real-time traffic
2. **Alternative Transport**: Metro Bus (Lahore, Rawalpindi, Islamabad)
3. **Time Management**: Travel 30 minutes earlier/later
4. **Carpooling**: Share rides during peak hours"""

    elif any(word in user_message_lower for word in ['public transport', 'metro', 'bus']):
        return """🚌 **Public Transport in Pakistan:**

**Metro Systems:**
- **Lahore**: Orange Line Metro Train + Metro Bus
- **Rawalpindi-Islamabad**: Metro Bus Service
- **Karachi**: Green Line BRT (operational)

**Benefits:**
- Cost-effective (Rs. 15-40 per ride)
- Dedicated lanes avoid traffic
- Air-conditioned comfort
- Environmentally friendly

**Tips:**
- Buy rechargeable cards for convenience
- Avoid peak hours if possible
- Check route maps on official apps"""

    else:
        return """🚦 **TrafficWise Pakistan - General Tips:**

**Smart Travel:**
- Use GPS navigation (Google Maps, Waze)
- Check traffic conditions before leaving
- Keep fuel tank at least half full
- Carry emergency contact numbers

**Safety First:**
- Follow speed limits (120 km/h on motorways)
- Use seat belts always
- Avoid using phone while driving
- Keep vehicle documents updated

**Cultural Considerations:**
- Prayer times affect traffic flow
- Ramadan timings change traffic patterns
- Wedding seasons (winter) increase congestion

How can I help you with specific route or traffic planning?"""

def local_rag_response(user_message):
    """Simulate RAG-based response using local knowledge base"""
    return f"""📚 **RAG-Enhanced Response:**

Based on local traffic knowledge base for your query: "{user_message}"

This would typically use:
- Local traffic pattern data
- Historical congestion information  
- Weather impact analysis
- Event-based traffic predictions

**To implement full RAG:**
1. Use vector database (Pinecone, Weaviate)
2. Embed traffic documents with sentence-transformers
3. Retrieve relevant documents
4. Generate response with local LLM

**Current simulation:** Offline rule-based response with Pakistan context.

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
                # Choose response method based on selected service
                if ai_service == "Google Gemini API" and 'api_key' in locals() and api_key:
                    response = chat_with_gemini(user_message, temperature, api_key, gemini_model)
                elif ai_service == "OpenAI API" and 'api_key' in locals() and api_key:
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

    # API Status indicator
    if ai_service == "Google Gemini API":
        if 'api_key' in locals() and api_key:
            st.success("✅ Google Gemini API connected")
        else:
            st.warning("⚠️ Please enter your Gemini API key in the sidebar")

with col2:
    if show_map:
        st.subheader("🗺️ Pakistan Traffic Map")
        folium_static(generate_pakistan_traffic_map(), width=400, height=500)

# Sidebar information
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 🚗 Pakistan Traffic Guidelines:

**📍 Major Routes:**
- **GT Road**: Historic but congested
- **Motorways**: M-1, M-2, M-3, M-4 - fastest
- **National Highways**: N-5, N-25, N-35

**⏰ Peak Hours:**
- Morning: 7:00-9:30 AM
- Evening: 4:30-7:30 PM
- Friday: 12:00-2:00 PM

**🌦️ Weather Impact:**
- Monsoon: July-September
- Fog: December-February
- Heat waves: May-June

**🚨 Emergency Numbers:**
- Motorway Police: 130
- Highway Police: 1915
- Rescue 1122: 1122
""")

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 🆓 **Google Gemini Benefits:**

✅ **Free Tier Available**
✅ **15 requests per minute**
✅ **1 million tokens per day**
✅ **Advanced reasoning**
✅ **Multimodal capabilities**

### 🔧 **Setup Instructions:**
1. Visit https://aistudio.google.com
2. Sign in with Google
3. Create API key
4. Paste in sidebar
5. Start chatting!

### 🔄 **Alternative Options:**
- **Offline Mode**: No API needed
- **Local RAG**: Vector database
- **OpenAI**: Paid but powerful
""")

# Footer
st.markdown("---")
st.markdown("🚦 **TrafficWise Pakistan** - Powered by Google Gemini AI | Smart Traffic Solutions for Pakistani Cities")
