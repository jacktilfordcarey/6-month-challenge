# LillyHelper

AI-powered tool for analyzing and visualizing Real-World Evidence (RWE) data.

## Features

- 📊 **Data Analysis**: Upload Excel/CSV files for instant AI-powered insights
- 💬 **Interactive Chatbot**: Ask questions about your data in natural language
- 📈 **Visualizations**: Generate charts and graphs automatically
- 📄 **Professional Summaries**: Export clean, formatted analysis reports
- ♿ **Accessibility**: High contrast mode, text magnifier, and text-to-speech support

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/jacktilfordcarey/6-month-challenge.git
cd 6-month-challenge
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up API keys** (optional - app has fallback keys)

Create a `.env` file:

```
GROQ_API_KEY=your_groq_key_here
GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here
```

## Usage

1. **Start the application**

```bash
streamlit run lillyextractor.py
```

2. **Open your browser** to `http://localhost:8501`

3. **Upload your data** (Excel or CSV file)

4. **Choose an action**:
   - Generate AI analysis
   - Create visualizations
   - Generate professional summary
   - Chat with your data

## Accessibility Features

Access in the sidebar:

- **🔳 High Contrast**: Black background with yellow text for better visibility
- **🔍 Magnifier**: Increase text size by 30%
- **🔊 Text-to-Speech**: Audio playback for analysis results and chat responses

## Supported File Formats

- Excel (`.xlsx`, `.xls`)
- CSV (`.csv`)
- PowerPoint (`.pptx`) - extracts tables and text
- Text (`.txt`, `.md`)
- JSON (`.json`)

## Theme

Clean white and blue theme with professional aesthetics:

- Primary Blue: #2196F3
- Dark Blue: #1565C0
- Light Blue: #E3F2FD
- White: #FFFFFF

## Requirements

- Python 3.8+
- Streamlit 1.30.0+
- Pandas 2.0.0+
- See `requirements.txt` for full list

## AI Models

The app uses a fallback chain for AI:

1. **Groq** (llama-3.1-8b-instant) - Fast and efficient
2. **Google Gemini** (gemini-2.0-flash-exp) - Balanced performance
3. **OpenAI** (gpt-3.5-turbo) - Reliable fallback

## License

MIT License

## Author

Jack Tilford Carey
