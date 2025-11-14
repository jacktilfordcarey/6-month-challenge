"""
LillyHelper - AI Tool to Help Understand/Visuals RWE
Clean, professional interface for RWE data analysis and visualization
"""

import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv
import plotly.graph_objects as go
from io import BytesIO
import json

# Try to import AI libraries
try:
    from pptx import Presentation
    PPTX_SUPPORT = True
except ImportError:
    PPTX_SUPPORT = False

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Load environment variables from .env file
load_dotenv()

# Configure page
st.set_page_config(
    page_title="LillyHelper",
    page_icon="📊",
    layout="wide"
)

# Configure AI with fallback support (Groq -> Gemini -> OpenAI)
GROQ_API_KEY = os.getenv('GROQ_API_KEY') or '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'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') or 'AIzaSyA3RdYq2jb-azGi81zltoittLOhz5AyHis'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') or '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'

model = None
active_model = None

# Try Groq first (with SSL verification disabled for corporate networks)
if GROQ_API_KEY and GROQ_AVAILABLE:
    try:
        import httpx
        http_client = httpx.Client(verify=False, timeout=60.0)
        groq_client = Groq(api_key=GROQ_API_KEY, http_client=http_client)
        model = groq_client
        active_model = "groq"
    except:
        pass

# Try Gemini second
if model is None and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        active_model = "gemini"
    except:
        pass

# Try OpenAI third (with SSL verification disabled for corporate networks)
if model is None and OPENAI_API_KEY and OPENAI_AVAILABLE:
    try:
        import httpx
        http_client = httpx.Client(verify=False, timeout=60.0)
        openai_client = OpenAI(api_key=OPENAI_API_KEY, http_client=http_client)
        model = openai_client
        active_model = "openai"
    except:
        pass

def generate_ai_response(prompt):
    """Generate AI response with fallback support"""
    global model, active_model
    
    if model is None:
        return "AI not configured. Please set API keys."
    
    errors_encountered = []
    
    # Try primary model first
    try:
        if active_model == "groq":
            # Use llama-3.1-8b-instant (supported and fast)
            response = model.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000,
                timeout=60
            )
            return response.choices[0].message.content
        
        elif active_model == "gemini":
            response = model.generate_content(prompt)
            return response.text
        
        elif active_model == "openai":
            response = model.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000,
                timeout=30
            )
            return response.choices[0].message.content
    
    except Exception as e:
        error_msg = str(e).lower()
        errors_encountered.append(f"{active_model}: {str(e)}")
        
        # Try Groq fallback (if not already using it) - try multiple times
        if active_model != "groq" and GROQ_API_KEY and GROQ_AVAILABLE:
            for attempt in range(2):  # Try twice
                try:
                    import httpx
                    http_client = httpx.Client(verify=False, timeout=60.0)
                    groq_client = Groq(api_key=GROQ_API_KEY, http_client=http_client)
                    response = groq_client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                        max_tokens=2000
                    )
                    model = groq_client
                    active_model = "groq"
                    return response.choices[0].message.content
                except Exception as groq_error:
                    if attempt == 1:  # Only log on last attempt
                        errors_encountered.append(f"Groq (retry {attempt+1}): {str(groq_error)}")
                    import time
                    time.sleep(1)  # Wait 1 second between retries
        
        # Try Gemini fallback (if not already using it and not quota error)
        if active_model != "gemini" and GEMINI_API_KEY and "quota" not in error_msg and "429" not in error_msg:
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                fallback_model = genai.GenerativeModel('gemini-2.0-flash-exp')
                response = fallback_model.generate_content(prompt)
                model = fallback_model
                active_model = "gemini"
                return response.text
            except Exception as gemini_error:
                errors_encountered.append(f"Gemini: {str(gemini_error)}")
        
        # Try OpenAI fallback (if not already using it)
        if active_model != "openai" and OPENAI_API_KEY and OPENAI_AVAILABLE:
            try:
                import httpx
                http_client = httpx.Client(verify=False, timeout=60.0)
                openai_client = OpenAI(api_key=OPENAI_API_KEY, http_client=http_client)
                response = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=2000
                )
                model = openai_client
                active_model = "openai"
                return response.choices[0].message.content
            except Exception as openai_error:
                errors_encountered.append(f"OpenAI: {str(openai_error)}")
        
        # Return all errors for debugging
        return f"All AI services failed. Errors: {' | '.join(errors_encountered)}"

# Custom CSS for Lilly theme (Red, Black, and Dark Grey)
st.markdown("""
<style>
    /* Main app background - Dark grey for better readability */
    .main {
        background-color: #1a1a1a !important;
        padding: 2rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #2d2d2d !important;
    }
    
    /* App background - Black */
    .stApp {
        background-color: #0d0d0d !important;
    }
    
    /* Header - Black */
    header[data-testid="stHeader"] {
        background-color: #0d0d0d !important;
    }
    
    /* Toolbar - Black */
    [data-testid="stToolbar"] {
        background-color: #0d0d0d !important;
    }
    
    /* Top decoration */
    .stApp > header {
        background-color: #0d0d0d !important;
    }
    
    /* Block container - slightly lighter grey */
    [data-testid="stVerticalBlock"] {
        background-color: transparent !important;
    }
    
    /* All text default to light grey */
    body, p, span, div, label, .stMarkdown, .stText {
        color: #d0d0d0 !important;
    }
    
    /* Headers - Red */
    h1 {
        color: #E41E26 !important;
        font-weight: 700;
        margin-bottom: 0.5rem !important;
    }
    h2, h3 {
        color: #E41E26 !important;
        font-weight: 600;
        margin-top: 2rem !important;
    }
    
    /* Subtitle text */
    .stMarkdown h3 {
        color: #cccccc !important;
        font-weight: 400;
    }
    
    /* Buttons - All buttons red */
    button[kind="primary"],
    button[kind="secondary"],
    .stButton button,
    .stDownloadButton button {
        background-color: #E41E26 !important;
        color: #e8e8e8 !important;
        border: none !important;
        padding: 0.6rem 1.5rem !important;
        font-size: 1rem !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    button[kind="primary"]:hover,
    button[kind="secondary"]:hover,
    .stButton button:hover,
    .stDownloadButton button:hover {
        background-color: #c01820 !important;
        box-shadow: 0 4px 12px rgba(228, 30, 38, 0.4) !important;
        transform: translateY(-1px) !important;
    }
    
    /* File uploader - Dark grey box with red border */
    [data-testid="stFileUploader"] {
        background-color: #2d2d2d !important;
        border: 2px dashed #E41E26 !important;
        border-radius: 8px !important;
        padding: 2rem !important;
    }
    [data-testid="stFileUploader"] label {
        color: #d0d0d0 !important;
        font-size: 1.1rem !important;
    }
    [data-testid="stFileUploader"] section {
        background-color: #2d2d2d !important;
    }
    [data-testid="stFileUploader"] small {
        color: #999999 !important;
    }
    
    /* Dataframe - Dark grey background */
    [data-testid="stDataFrame"] {
        background-color: transparent !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        border: 1px solid #3d3d3d !important;
    }
    .stDataFrame {
        background-color: transparent !important;
    }
    
    /* Dataframe table styling */
    [data-testid="stDataFrame"] table {
        background-color: transparent !important;
    }
    
    /* Table header - dark grey */
    [data-testid="stDataFrame"] thead tr th {
        background-color: #3d3d3d !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #E41E26 !important;
        padding: 0.75rem !important;
    }
    
    /* Keep headers grey on dropdown/filter */
    [data-testid="stDataFrame"] thead tr th:hover {
        background-color: #3d3d3d !important;
    }
    
    [data-testid="stDataFrame"] thead tr th[aria-sort] {
        background-color: #3d3d3d !important;
    }
    
    /* Table body cells - light grey */
    [data-testid="stDataFrame"] tbody tr td {
        background-color: #5a5a5a !important;
        color: #ffffff !important;
        border-bottom: 1px solid #3d3d3d !important;
        padding: 0.5rem !important;
    }
    
    /* Alternating row colors for better readability */
    [data-testid="stDataFrame"] tbody tr:nth-child(even) td {
        background-color: #6a6a6a !important;
    }
    
    /* Hover effect on rows */
    [data-testid="stDataFrame"] tbody tr:hover td {
        background-color: #5a5a5a !important;
    }
    
    /* Index column styling */
    [data-testid="stDataFrame"] tbody tr th {
        background-color: #3d3d3d !important;
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    /* Expander - Dark grey with red accent */
    [data-testid="stExpander"] {
        background-color: #2d2d2d !important;
        border: 1px solid #3d3d3d !important;
        border-radius: 8px !important;
        margin: 1rem 0 !important;
    }
    details[open] > summary {
        border-bottom: 2px solid #E41E26 !important;
        padding-bottom: 0.5rem !important;
    }
    .streamlit-expanderHeader {
        background-color: #2d2d2d !important;
        color: #cccccc !important;
        font-weight: 600 !important;
    }
    
    /* Metrics - Dark grey cards with red accent */
    [data-testid="stMetric"] {
        background-color: #2d2d2d !important;
        padding: 1.2rem !important;
        border-radius: 8px !important;
        border-left: 4px solid #E41E26 !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
    }
    [data-testid="stMetricValue"] {
        color: #E41E26 !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: #cccccc !important;
        font-weight: 500 !important;
    }
    
    /* Info/Success/Error boxes */
    .stAlert {
        background-color: #2d2d2d !important;
        color: #cccccc !important;
        border-left: 5px solid #E41E26 !important;
        border-radius: 6px !important;
        padding: 1rem !important;
    }
    
    /* Success message */
    .stSuccess {
        background-color: #2d2d2d !important;
        color: #cccccc !important;
        border-left: 5px solid #E41E26 !important;
    }
    
    /* Info message */
    .stInfo {
        background-color: #2d2d2d !important;
        color: #cccccc !important;
        border-left: 5px solid #E41E26 !important;
    }
    
    /* Spinner - Red */
    .stSpinner > div {
        border-top-color: #E41E26 !important;
    }
    
    /* Horizontal rule */
    hr {
        border-color: #3d3d3d !important;
        margin: 2rem 0 !important;
    }
    
    /* Code blocks */
    code {
        background-color: #2d2d2d !important;
        color: #E41E26 !important;
        padding: 0.2rem 0.4rem !important;
        border-radius: 4px !important;
    }
    
    /* Remove any remaining white backgrounds */
    section[data-testid="stSidebar"] > div {
        background-color: #2d2d2d !important;
    }
    
    /* Column containers */
    [data-testid="column"] {
        background-color: transparent !important;
    }
    
    /* Links */
    a {
        color: #E41E26 !important;
    }
    a:hover {
        color: #c01820 !important;
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: #2d2d2d !important;
        border-radius: 8px !important;
        border: 1px solid #3d3d3d !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
    }
    
    /* User chat message */
    [data-testid="stChatMessageContent"] {
        color: #d0d0d0 !important;
    }
    
    /* Chat input */
    [data-testid="stChatInput"] {
        background-color: #2d2d2d !important;
        border: 2px solid #E41E26 !important;
        border-radius: 12px !important;
    }
    
    [data-testid="stChatInput"]:focus-within {
        border: 2px solid #E41E26 !important;
        box-shadow: 0 0 0 1px #E41E26 !important;
    }
    
    [data-testid="stChatInput"] > div {
        border-radius: 12px !important;
    }
    
    /* Fix white left border */
    [data-testid="stChatInput"] textarea {
        border-left: none !important;
    }
    
    /* Ensure chat message content is properly styled */
    [data-testid="stChatMessage"] > div {
        border-radius: 8px !important;
    }
    
    [data-testid="stChatInput"] textarea {
        background-color: #2d2d2d !important;
        color: #d0d0d0 !important;
        border: none !important;
    }
    
    [data-testid="stChatInput"] textarea::placeholder {
        color: #888888 !important;
    }
    
    /* Chat input button */
    [data-testid="stChatInput"] button {
        background-color: #E41E26 !important;
        color: #cccccc !important;
    }
    
    /* Text area */
    textarea {
        background-color: #2d2d2d !important;
        color: #d0d0d0 !important;
        border: none !important;
    }
    
    /* Select box styling */
    [data-testid="stSelectbox"] {
        background-color: #2d2d2d !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stSelectbox"] > div {
        border-radius: 8px !important;
    }
    
    [data-testid="stSelectbox"] > div > div {
        background-color: #2d2d2d !important;
        color: #e8e8e8 !important;
        border: 1px solid #3d3d3d !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stSelectbox"] input {
        border-radius: 8px !important;
    }
    
    /* Dropdown arrow color */
    [data-testid="stSelectbox"] svg {
        fill: #ffffff !important;
        color: #ffffff !important;
    }
    
    /* Dropdown menu styling */
    [data-baseweb="popover"] {
        background-color: #2d2d2d !important;
        border-radius: 8px !important;
    }
    
    [data-baseweb="menu"] {
        background-color: #2d2d2d !important;
        border-radius: 8px !important;
    }
    
    [role="option"] {
        background-color: #2d2d2d !important;
        color: #e8e8e8 !important;
        border-radius: 4px !important;
    }
    
    [role="option"]:hover {
        background-color: #3d3d3d !important;
    }
    
    /* Radio button styling */
    [data-testid="stRadio"] label {
        color: #e8e8e8 !important;
    }
    
    [data-testid="stRadio"] > div {
        background-color: #2d2d2d !important;
        padding: 0.5rem !important;
        border-radius: 6px !important;
    }
    
    /* Footer styling */
    footer {
        background-color: #0d0d0d !important;
        color: #888888 !important;
        visibility: visible !important;
    }
    
    footer p {
        color: #888888 !important;
    }
    
    footer div {
        background-color: #0d0d0d !important;
    }
    
    [data-testid="stBottomBlockContainer"] {
        background-color: #1a1a1a !important;
    }
    
    /* Bottom container */
    .main .block-container {
        padding-bottom: 5rem !important;
    }
    
    /* Streamlit footer */
    footer[data-testid="stFooter"] {
        background-color: #0d0d0d !important;
    }
    
    footer[data-testid="stFooter"] > div {
        background-color: #0d0d0d !important;
    }
    
    /* Chat footer area */
    [data-testid="stChatInputContainer"] {
        background-color: #1a1a1a !important;
        border-top: 1px solid #3d3d3d !important;
    }
    
    /* More comprehensive table styling */
    div[data-testid="stDataFrame"] div[data-testid="StyledDataFrameContainer"] {
        background-color: transparent !important;
    }
    
    /* Remove grey box overlays */
    [data-testid="stDataFrame"] > div {
        background-color: transparent !important;
    }
    
    table {
        background-color: transparent !important;
        color: #ffffff !important;
        border-collapse: collapse !important;
    }
    
    thead {
        background-color: #3d3d3d !important;
    }
    
    th {
        background-color: #3d3d3d !important;
        color: #ffffff !important;
    }
    
    td {
        background-color: #5a5a5a !important;
        color: #ffffff !important;
    }
    
    tr:nth-child(even) td {
        background-color: #6a6a6a !important;
    }
    
    /* Streamlit dataframe specific */
    .dataframe {
        background-color: transparent !important;
        color: #ffffff !important;
    }
    
    .dataframe thead th {
        background-color: #3d3d3d !important;
        color: #ffffff !important;
    }
    
    .dataframe tbody td {
        background-color: #5a5a5a !important;
        color: #ffffff !important;
    }
    
    .dataframe tbody tr:nth-child(even) td {
        background-color: #6a6a6a !important;
    }
    
    /* Override any remaining white backgrounds */
    div[class*="stDataFrame"] {
        background-color: transparent !important;
    }
    
    /* Ensure table elements are visible */
    [data-testid="stDataFrame"] * {
        z-index: auto !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;'>
    <h1 style='margin: 0; color: #E41E26;'>LillyHelper</h1>
    <span style='color: #4a4a4a; font-size: 1.5rem;'>AI Tool to Help Personalise/Visualise RWE</span>
</div>
""", unsafe_allow_html=True)

# Helper functions
def extract_text_from_pptx(file):
    """Extract text and tables from PowerPoint"""
    if not PPTX_SUPPORT:
        return "PowerPoint support not available. Install python-pptx.", []
    
    prs = Presentation(file)
    text_content = []
    tables_data = []
    
    for slide_num, slide in enumerate(prs.slides, 1):
        slide_text = []
        for shape in slide.shapes:
            if hasattr(shape, "text") and shape.text.strip():
                slide_text.append(shape.text)
            
            if shape.has_table:
                table = shape.table
                table_data = []
                for row in table.rows:
                    row_data = [cell.text for cell in row.cells]
                    table_data.append(row_data)
                if table_data:
                    tables_data.append({"slide": slide_num, "data": table_data})
        
        if slide_text:
            text_content.append(f"Slide {slide_num}:\n" + "\n".join(slide_text))
    
    return "\n\n".join(text_content), tables_data

def parse_json_to_dataframe(file):
    """Parse JSON file to DataFrame"""
    try:
        content = json.load(file)
        if isinstance(content, list):
            return pd.DataFrame(content)
        elif isinstance(content, dict):
            for key, value in content.items():
                if isinstance(value, list) and len(value) > 0:
                    return pd.DataFrame(value)
            return pd.DataFrame([content])
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error parsing JSON: {str(e)}")
        return pd.DataFrame()

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'analysis_text' not in st.session_state:
    st.session_state.analysis_text = ''
if 'chatbot_messages' not in st.session_state:
    st.session_state.chatbot_messages = []

# Input method selection
input_method = st.radio(
    "Choose input method:",
    ["Upload File", "Enter Text Directly"],
    horizontal=True
)

uploaded_file = None
text_input = None
file_type = None

if input_method == "Upload File":
    file_type = st.selectbox(
        "Select file type:",
        ["Data File (Excel/CSV)", "PowerPoint Presentation", "Text Document", "JSON Data"]
    )
    
    if file_type == "Data File (Excel/CSV)":
        uploaded_file = st.file_uploader(
            "Choose an Excel or CSV file",
            type=['xlsx', 'xls', 'csv'],
            help="Upload your data file for analysis"
        )
    elif file_type == "PowerPoint Presentation":
        uploaded_file = st.file_uploader(
            "Choose a PowerPoint file",
            type=['pptx'],
            help="Upload PowerPoint with data tables or analysis"
        )
    elif file_type == "Text Document":
        uploaded_file = st.file_uploader(
            "Choose a text file",
            type=['txt', 'md'],
            help="Upload text document with analysis or data"
        )
    else:  # JSON Data
        uploaded_file = st.file_uploader(
            "Choose a JSON file",
            type=['json'],
            help="Upload JSON file with structured data"
        )
else:
    text_input = st.text_area(
        "Enter your data or analysis:",
        height=300,
        placeholder="Paste your text, data, or analysis here...\n\nYou can paste:\n- CSV data\n- Analysis text\n- Research findings\n- Any text for AI analysis",
        help="Enter any text for AI analysis and insights"
    )
    file_type = "Text Input"

if uploaded_file is not None or (text_input and text_input.strip()):
    try:
        df = None
        extracted_text = None
        
        # Process based on input type
        if text_input and text_input.strip():
            extracted_text = text_input.strip()
            st.success(f"Text input received: {len(extracted_text)} characters")
            
            # Try to parse as CSV
            try:
                from io import StringIO
                df = pd.read_csv(StringIO(extracted_text))
                st.info("Detected CSV format in text - parsed as DataFrame")
            except:
                pass
        
        elif uploaded_file is not None:
            if file_type == "Data File (Excel/CSV)":
                with st.spinner("Loading data..."):
                    if uploaded_file.name.endswith('.csv'):
                        try:
                            df = pd.read_csv(uploaded_file, encoding='utf-8')
                        except UnicodeDecodeError:
                            uploaded_file.seek(0)
                            df = pd.read_csv(uploaded_file, encoding='latin-1')
                    else:
                        df = pd.read_excel(uploaded_file)
                st.success(f"Loaded data: {len(df)} rows x {len(df.columns)} columns")
            
            elif file_type == "PowerPoint Presentation":
                extracted_text, tables = extract_text_from_pptx(uploaded_file)
                st.markdown("### Extracted Content")
                with st.expander("View extracted text", expanded=False):
                    st.text_area("PowerPoint Content", extracted_text, height=300, key="pptx_text")
                
                if tables:
                    st.markdown("### Extracted Tables")
                    for idx, table_info in enumerate(tables):
                        st.markdown(f"**Table from Slide {table_info['slide']}**")
                        table_data = table_info['data']
                        if len(table_data) > 1:
                            df_temp = pd.DataFrame(table_data[1:], columns=table_data[0])
                            st.dataframe(df_temp, use_container_width=True)
                            if df is None:
                                df = df_temp
            
            elif file_type == "Text Document":
                try:
                    extracted_text = uploaded_file.read().decode('utf-8')
                except UnicodeDecodeError:
                    uploaded_file.seek(0)
                    extracted_text = uploaded_file.read().decode('latin-1')
                st.markdown("### Document Content")
                with st.expander("View document text", expanded=False):
                    st.text_area("Text Content", extracted_text, height=300, key="text_content")
            
            elif file_type == "JSON Data":
                df = parse_json_to_dataframe(uploaded_file)
                if not df.empty:
                    st.success(f"Loaded JSON data: {len(df)} records")
        
        # Display data preview
        st.markdown("### Data Preview")
        
        if df is not None and not df.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Rows", f"{len(df):,}")
            with col2:
                st.metric("Total Columns", len(df.columns))
            with col3:
                numeric_cols = df.select_dtypes(include=['number']).columns
                st.metric("Numeric Columns", len(numeric_cols))
            
            with st.expander("View Data Sample", expanded=True):
                st.dataframe(df.head(10), use_container_width=True)
            
            # Column information
            with st.expander("Column Details"):
                col_info = pd.DataFrame({
                    'Column Name': df.columns,
                    'Data Type': [str(dtype) for dtype in df.dtypes.values],
                    'Non-Null Count': df.count().values,
                    'Null Count': df.isnull().sum().values,
                    'Unique Values': [df[col].nunique() for col in df.columns]
                })
                st.dataframe(col_info, use_container_width=True)
        
        elif extracted_text:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Characters", f"{len(extracted_text):,}")
            with col2:
                st.metric("Words", f"{len(extracted_text.split()):,}")
            
            with st.expander("View Content Preview", expanded=True):
                st.markdown(extracted_text[:1000] + ("..." if len(extracted_text) > 1000 else ""))
        
        # Generate summary with AI
        st.markdown("### Cortex AI Analysis")
        if st.button("Ask Cortex to Analyze", type="primary", use_container_width=True):
            if not model:
                st.error("⚠️ API key not configured. Please set GEMINI_API_KEY in .env file")
            else:
                with st.spinner("Cortex is analyzing your data..."):
                    # Prepare data summary - prioritize extracted text for PowerPoint/Text files
                    if extracted_text and file_type in ["PowerPoint Presentation", "Text Document"]:
                        # For PowerPoint and text files, analyze the content, not the tables
                        data_summary = f"""
Content Analysis:
- Type: {file_type}
- Length: {len(extracted_text)} characters

Full Content:
{extracted_text}
"""
                        prompt = f"""You are analyzing this content for a Healthcare Professional (HCP). Personalize your analysis for their clinical perspective and provide:

1. Executive Summary: Key takeaways relevant to clinical practice
2. Clinical Insights: How this information applies to patient care and treatment decisions
3. Actionable Recommendations: Specific steps HCPs can take based on this information
4. Key Concepts Explained: Medical/pharmaceutical concepts in practical terms
5. Evidence & Data Quality: Assessment of the strength and relevance of the information
6. Practice Implications: How this impacts day-to-day healthcare delivery

Present the analysis in a clear, professional format that an HCP would find valuable for clinical decision-making.

{data_summary}
"""
                    elif df is not None and not df.empty:
                        data_summary = f"""
Dataset Overview:
- Total Rows: {len(df)}
- Total Columns: {len(df.columns)}
- Column Names: {', '.join(df.columns.tolist())}

Data Types:
{df.dtypes.to_string()}

Statistical Summary:
{df.describe().to_string()}

Sample Data:
{df.head().to_string()}
"""
                        prompt = f"""You are analyzing this Real-World Evidence (RWE) data for a Healthcare Professional (HCP). Personalize your analysis for clinical practice:

1. Clinical Summary: What does this data tell us about patient outcomes, treatment effectiveness, or healthcare patterns?
2. Patient Impact: How do these findings relate to patient care and treatment decisions?
3. Evidence Quality: Assess the data quality, sample size, and statistical significance
4. Key Metrics: Highlight the most important clinical measures and their implications
5. Actionable Insights: Specific recommendations for HCPs based on this RWE
6. Comparative Analysis: How do these findings compare to established clinical standards or previous studies?
7. Practice Implementation: Practical steps HCPs can take to apply these insights

Present insights in a format that supports evidence-based clinical decision-making.

{data_summary}
"""
                    else:
                        data_summary = "No data available."
                        prompt = f"""No data available to analyze.

{data_summary}
"""
                    
                    try:
                        analysis_text = generate_ai_response(prompt)
                        st.session_state.analysis_text = analysis_text
                        
                        st.markdown("#### Cortex Analysis Results")
                        st.markdown(analysis_text)
                        
                        # Store analysis in session state for visualization
                        st.session_state['analysis_done'] = True
                        st.session_state['analysis_text'] = analysis_text
                        st.session_state['df'] = df
                        
                    except Exception as e:
                        st.error(f"Error generating analysis: {str(e)}")
        
        # Show visualization and professional summary buttons after analysis is done
        if st.session_state.get('analysis_done', False):
            st.markdown("---")
            
            # Professional Summary Generator
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📄 Generate Professional Summary", type="primary", use_container_width=True):
                    with st.spinner("Creating professional summary..."):
                        # Build comprehensive context
                        summary_context = ""
                        
                        if 'analysis_text' in st.session_state and st.session_state.analysis_text:
                            summary_context += f"Analysis:\n{st.session_state.analysis_text}\n\n"
                        
                        if df is not None and not df.empty:
                            summary_context += f"Dataset: {len(df)} rows, {len(df.columns)} columns\n"
                            summary_context += f"Columns: {', '.join(df.columns.tolist())}\n"
                        
                        # Generate professional summary
                        summary_prompt = f"""Create a concise, professional executive summary of this Real-World Evidence (RWE) analysis for Healthcare Professionals.

Context:
{summary_context}

Format your summary with:

**Executive Summary**
[2-3 sentence overview of key findings]

**Key Insights**
• [Most important finding 1]
• [Most important finding 2]
• [Most important finding 3]

**Clinical Implications**
[How these findings impact patient care and treatment decisions]

**Recommendations**
1. [Actionable recommendation 1]
2. [Actionable recommendation 2]
3. [Actionable recommendation 3]

**Data Quality & Limitations**
[Brief assessment of data reliability and any caveats]

Keep it professional, concise, and focused on actionable insights for HCPs."""
                        
                        try:
                            professional_summary = generate_ai_response(summary_prompt)
                            st.session_state['professional_summary'] = professional_summary
                            
                            st.markdown("### 📋 Professional Summary")
                            st.markdown(professional_summary)
                            
                            # Download option for summary
                            summary_report = f"""Professional RWE Analysis Summary
{'=' * 50}

Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
File: {uploaded_file.name if uploaded_file else 'Text Input'}

{professional_summary}

{'=' * 50}
Powered by Lilly Cortex AI
"""
                            st.download_button(
                                label="⬇️ Download Summary (TXT)",
                                data=summary_report.encode('utf-8'),
                                file_name="professional_summary.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                        except Exception as e:
                            st.error(f"Error generating summary: {str(e)}")
            
            with col2:
                # Show existing professional summary if available
                if 'professional_summary' in st.session_state:
                    if st.button("📋 View Saved Summary", use_container_width=True):
                        st.markdown("### 📋 Professional Summary")
                        st.markdown(st.session_state['professional_summary'])
            
            st.markdown("---")
            
            # Only show visualisation button if we have a dataframe
            if df is not None and not df.empty:
                visualize_button = st.button("Generate Visualisations & 3D AR Graphs", use_container_width=True)
                if visualize_button:
                    # Show AI Analysis again
                    st.markdown("### Cortex AI Analysis")
                    st.markdown(st.session_state.get('analysis_text', ''))
                    st.markdown("---")
                    with st.spinner("Creating interactive visualisations..."):
                        st.markdown("### Data Visualisations")
                        
                        # Get numeric and categorical columns
                        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                    
                    if len(numeric_cols) >= 2:
                        # 3D Scatter Plot (AR-ready)
                        st.markdown("#### 3D Interactive Scatter Plot")
                        
                        import plotly.graph_objects as go
                        
                        # Select up to 3 numeric columns for 3D plot
                        x_col = numeric_cols[0]
                        y_col = numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0]
                        z_col = numeric_cols[2] if len(numeric_cols) > 2 else numeric_cols[0]
                        
                        # Color by categorical if available
                        color_col = categorical_cols[0] if categorical_cols else None
                        
                        if color_col:
                            # Create color mapping for categorical column
                            unique_categories = df[color_col].unique()
                            colors = ['#E41E26' if i % 2 == 0 else '#4a4a4a' for i in range(len(unique_categories))]
                            color_map = {cat: colors[i] for i, cat in enumerate(unique_categories)}
                            
                            fig = go.Figure(data=[go.Scatter3d(
                                x=df[x_col],
                                y=df[y_col],
                                z=df[z_col],
                                mode='markers',
                                marker=dict(
                                    size=6,
                                    color=[color_map[val] for val in df[color_col]],
                                    line=dict(color='white', width=0.5)
                                ),
                                text=[f"{color_col}: {val}" for val in df[color_col]],
                                hovertemplate=f'<b>%{{text}}</b><br>{x_col}: %{{x}}<br>{y_col}: %{{y}}<br>{z_col}: %{{z}}<extra></extra>'
                            )])
                        else:
                            fig = go.Figure(data=[go.Scatter3d(
                                x=df[x_col],
                                y=df[y_col],
                                z=df[z_col],
                                mode='markers',
                                marker=dict(
                                    size=6,
                                    color='#E41E26',
                                    line=dict(color='white', width=0.5)
                                ),
                                hovertemplate=f'{x_col}: %{{x}}<br>{y_col}: %{{y}}<br>{z_col}: %{{z}}<extra></extra>'
                            )])
                        
                        fig.update_layout(
                            title=dict(
                                text=f'3D Scatter: {x_col} vs {y_col} vs {z_col}',
                                font=dict(color='#E41E26', size=18)
                            ),
                            scene=dict(
                                xaxis=dict(title=x_col, gridcolor='#3d3d3d', backgroundcolor='#1a1a1a'),
                                yaxis=dict(title=y_col, gridcolor='#3d3d3d', backgroundcolor='#1a1a1a'),
                                zaxis=dict(title=z_col, gridcolor='#3d3d3d', backgroundcolor='#1a1a1a'),
                            ),
                            paper_bgcolor='#1a1a1a',
                            font=dict(color='#ffffff'),
                            height=600
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Distribution plots
                    if numeric_cols:
                        st.markdown("#### Distribution Analysis")
                        
                        for col in numeric_cols[:3]:  # Show first 3 numeric columns
                            fig = go.Figure(data=[go.Histogram(
                                x=df[col],
                                marker_color='#E41E26',
                                marker_line_color='white',
                                marker_line_width=1.5,
                                opacity=0.85
                            )])
                            
                            fig.update_layout(
                                title=dict(
                                    text=f'Distribution of {col}',
                                    font=dict(color='#E41E26', size=16)
                                ),
                                xaxis=dict(title=col, gridcolor='#3d3d3d'),
                                yaxis=dict(title='Frequency', gridcolor='#3d3d3d'),
                                paper_bgcolor='#1a1a1a',
                                plot_bgcolor='#1a1a1a',
                                font=dict(color='#ffffff'),
                                showlegend=False,
                                height=400
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                    
                    # Categorical distribution
                    if categorical_cols:
                        st.markdown("#### Categorical Distribution")
                        
                        for cat_col in categorical_cols[:3]:  # Show first 3 categorical columns
                            value_counts = df[cat_col].value_counts().head(10)
                            
                            fig = go.Figure(data=[go.Bar(
                                x=value_counts.values,
                                y=value_counts.index,
                                orientation='h',
                                marker_color='#E41E26',
                                marker_line_color='white',
                                marker_line_width=1.5
                            )])
                            
                            fig.update_layout(
                                title=dict(
                                    text=f'Top Values in {cat_col}',
                                    font=dict(color='#E41E26', size=16)
                                ),
                                xaxis=dict(title='Count', gridcolor='#3d3d3d'),
                                yaxis=dict(title=cat_col, gridcolor='#3d3d3d'),
                                paper_bgcolor='#1a1a1a',
                                plot_bgcolor='#1a1a1a',
                                font=dict(color='#ffffff'),
                                showlegend=False,
                                height=400
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                    
                    # Correlation heatmap if multiple numeric columns
                    if len(numeric_cols) > 1:
                        st.markdown("#### Correlation Matrix")
                        
                        corr_matrix = df[numeric_cols].corr()
                        
                        fig = go.Figure(data=go.Heatmap(
                            z=corr_matrix.values,
                            x=corr_matrix.columns,
                            y=corr_matrix.columns,
                            colorscale=[[0, '#000000'], [0.5, '#ffffff'], [1, '#E41E26']],
                            zmid=0,
                            text=corr_matrix.values.round(2),
                            texttemplate='%{text}',
                            textfont={"size": 10},
                            colorbar=dict(title='Correlation')
                        ))
                        
                        fig.update_layout(
                            title=dict(
                                text='Feature Correlation Heatmap',
                                font=dict(color='#E41E26', size=18)
                            ),
                            paper_bgcolor='#1a1a1a',
                            plot_bgcolor='#1a1a1a',
                            font=dict(color='#ffffff'),
                            height=600
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
        
        # AR Visualisation Export
        st.markdown("---")
        st.markdown("### AR Visualisation Export")
        st.markdown("*Export 3D visualisations for AR viewing*")
        
        if df is not None and not df.empty:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            if len(numeric_cols) >= 2:
                if st.button("Generate AR-Ready 3D Model", type="primary"):
                    with st.spinner("Creating AR visualisation..."):
                        # Create 3D visualization
                        x_col = numeric_cols[0]
                        y_col = numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0]
                        z_col = numeric_cols[2] if len(numeric_cols) > 2 else numeric_cols[0]
                        
                        fig = go.Figure(data=[go.Scatter3d(
                            x=df[x_col],
                            y=df[y_col],
                            z=df[z_col],
                            mode='markers',
                            marker=dict(
                                size=8,
                                color=df[z_col] if z_col in df.columns else '#E41E26',
                                colorscale=[[0, '#000000'], [0.5, '#4a4a4a'], [1, '#E41E26']],
                                line=dict(color='white', width=1),
                                showscale=True
                            ),
                            hovertemplate=f'{x_col}: %{{x}}<br>{y_col}: %{{y}}<br>{z_col}: %{{z}}<extra></extra>'
                        )])
                        
                        fig.update_layout(
                            title=dict(
                                text=f'AR-Ready 3D Visualisation',
                                font=dict(color='#E41E26', size=20)
                            ),
                            scene=dict(
                                xaxis=dict(title=x_col, backgroundcolor='#1a1a1a', gridcolor='#3d3d3d'),
                                yaxis=dict(title=y_col, backgroundcolor='#1a1a1a', gridcolor='#3d3d3d'),
                                zaxis=dict(title=z_col, backgroundcolor='#1a1a1a', gridcolor='#3d3d3d'),
                                camera=dict(
                                    eye=dict(x=1.5, y=1.5, z=1.5)
                                )
                            ),
                            paper_bgcolor='#1a1a1a',
                            font=dict(color='#ffffff'),
                            height=700
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Export HTML for AR
                        html_buffer = BytesIO()
                        fig.write_html(html_buffer)
                        html_buffer.seek(0)
                        
                        st.download_button(
                            label="Download AR Visualisation (HTML)",
                            data=html_buffer,
                            file_name="ar_visualization.html",
                            mime="text/html",
                            help="Open this file on your phone/tablet with AR capabilities"
                        )
                        
                        st.info("**AR Viewing Tip:** Open the downloaded HTML file on a device with AR capabilities (smartphone/tablet). The 3D visualisation can be viewed in augmented reality mode.")
        else:
            st.info("AR visualisations are available for Excel, CSV, and JSON data with numeric columns.")
        
        # Download options
        st.markdown("---")
        st.markdown("### Download Options")
        
        col1, col2, col3 = st.columns(3)
        
        if df is not None and not df.empty:
            with col1:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Data (CSV)",
                    data=csv,
                    file_name="data_export.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Basic statistics
                if len(df.select_dtypes(include=['number']).columns) > 0:
                    stats = df.describe().to_csv().encode('utf-8')
                    st.download_button(
                        label="Download Statistics",
                        data=stats,
                        file_name="data_statistics.csv",
                        mime="text/csv"
                    )
        
        with col3:
            # Download analysis report
            if 'analysis_text' in st.session_state:
                file_name = uploaded_file.name if uploaded_file else "Text Input"
                report = f"""LillyHelper - Analysis Report
=====================================

File: {file_name}
Type: {file_type}
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

Cortex AI Analysis:
{st.session_state['analysis_text']}

Chat History:
"""
                for msg in st.session_state.get('chat_history', []):
                    report += f"\n{msg['role'].upper()}: {msg['content']}"
                
                st.download_button(
                    label="Download Full Report",
                    data=report.encode('utf-8'),
                    file_name="analysis_report.txt",
                    mime="text/plain"
                )
        
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        st.info("Please make sure your file is a valid Excel (.xlsx, .xls) or CSV file")

else:
    # Instructions when no input provided
    st.markdown("### How to use:")
    st.markdown("""
    1. **Choose** between uploading a file or entering text directly
    2. **Upload** your file (Excel, CSV, PowerPoint, Text, JSON) OR **paste** text in the text box
    3. **Review** the data preview and details
    4. **Click** "Ask Cortex to Analyze" to get AI-powered insights
    5. **Ask questions** using the Cortex chatbot
    6. **Generate visualizations** including 3D AR graphs
    7. **Download** your results as needed
    """)
    
    st.markdown("### Supported formats:")
    st.markdown("""
    - **Data Files**: Excel (.xlsx, .xls), CSV
    - **PowerPoint**: .pptx (extracts tables and text)
    - **Text**: .txt, .md files
    - **JSON**: Structured data files
    - **Direct Text Input**: Paste any text for AI analysis
    """)
    
    st.markdown("### What you'll get:")
    st.markdown("""
    - **Quick overview** of your data or content structure
    - **Cortex AI-powered insights** about patterns and trends
    - **Key statistics** for numeric columns
    - **Clinical recommendations** for further analysis
    """)

# Footer
st.markdown("---")
st.markdown("*Powered by Lilly Cortex AI*")

# LillyHelper Chatbot - Sidebar
with st.sidebar:
    st.markdown("### LillyHelper Assistant")
    st.markdown("Ask Cortex about your Real-World Evidence data, clinical insights, or analysis questions.")
    st.markdown("---")
    
    # Custom CSS for chat input styling
    st.markdown("""
    <style>
        /* Custom text input styling for chat */
        div[data-testid="stTextInput"] input {
            background-color: #5a5a5a !important;
            border: none !important;
            border-radius: 25px !important;
            color: #d0d0d0 !important;
            padding: 12px 15px !important;
        }
        div[data-testid="stTextInput"] input:focus {
            border: none !important;
            box-shadow: none !important;
            outline: none !important;
        }
        div[data-testid="stTextInput"] input::placeholder {
            color: #999999 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize voice input state
    if 'voice_input_active' not in st.session_state:
        st.session_state.voice_input_active = False
    
    # Voice input button
    if st.button("Use Voice Input", key="voice_btn", help="Click to speak your question", use_container_width=True):
        st.session_state.voice_input_active = not st.session_state.voice_input_active
        
        voice_input_html = """
        <script>
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'en-US';
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;
            
            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                window.parent.postMessage({type: 'voice_input', text: transcript}, '*');
            };
            
            recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
            };
            
            recognition.start();
        </script>
        """
        st.components.v1.html(voice_input_html, height=0)
    
    # Text input
    prompt = st.text_input(
        "Message",
        placeholder="Ask Cortex anything...",
        key="chat_text_input",
        label_visibility="collapsed"
    )
    
    # Clear chat button
    if st.session_state.chatbot_messages:
        if st.button("Clear Chat History", type="secondary", use_container_width=True, key="clear_chat"):
            st.session_state.chatbot_messages = []
            st.rerun()
    
    st.markdown("---")
    
    # Chat container with scrolling
    chat_container = st.container(height=350)
    
    with chat_container:
        # Display chat history
        for message in st.session_state.chatbot_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"], unsafe_allow_html=True)
    
    # Handle message sending
    if prompt and prompt.strip():
        # Check if this message was already processed
        if 'last_prompt' not in st.session_state or st.session_state.last_prompt != prompt:
            st.session_state.last_prompt = prompt
            
            # Add user message to chat history
            st.session_state.chatbot_messages.append({"role": "user", "content": prompt})
            
            # Build context from analysis if available
            context = ""
            if 'analysis_text' in st.session_state and st.session_state.analysis_text:
                context += f"\n\nPrevious Analysis:\n{st.session_state.analysis_text[:1000]}"
            
            if 'df' in st.session_state and st.session_state.get('df') is not None:
                df = st.session_state['df']
                context += f"\n\nData Context: {len(df)} rows, {len(df.columns)} columns"
                context += f"\nColumns: {', '.join(df.columns.tolist()[:10])}"
            
            # Create HCP-focused prompt
            full_prompt = f"""You are LillyHelper, an AI assistant helping Healthcare Professionals (HCPs) analyze Real-World Evidence (RWE) data.

User Question: {prompt}

{context}

Provide a helpful, professional response tailored for an HCP. Focus on:
- Clinical relevance and practical application
- Evidence-based insights
- Clear, actionable guidance
- Professional medical terminology when appropriate

Response:"""
            
            # Generate AI response
            try:
                with st.spinner("Thinking..."):
                    response = generate_ai_response(full_prompt)
                
                # Add assistant response to chat history
                st.session_state.chatbot_messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
                # Remove the user message if response failed
                if st.session_state.chatbot_messages and st.session_state.chatbot_messages[-1]["role"] == "user":
                    st.session_state.chatbot_messages.pop()
            
            st.rerun()
