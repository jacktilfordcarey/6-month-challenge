# Lilly Data Intelligence Hub - Enhanced Features

## 🎯 New Capabilities

### 1. **Multiple File Format Support**

- **Excel/CSV** - Traditional data analysis
- **PowerPoint (.pptx)** - Extracts text and tables from presentations
- **Text Files (.txt, .md)** - Process analysis documents
- **JSON** - Handle structured API data

### 2. **AI-Powered Chatbot** 💬

- Ask questions about your data in natural language
- Get insights, explanations, and recommendations
- Context-aware responses based on uploaded data
- Chat history maintained during session

### 3. **AR-Ready Visualizations** 🥽

- Generate 3D scatter plots optimized for AR viewing
- Export as standalone HTML files
- View on smartphones/tablets with AR capabilities
- Immersive data exploration experience

### 4. **Enhanced Visualizations** 📊

- **3D Scatter Plots** - Interactive exploration with color mapping
- **Distribution Histograms** - Statistical analysis of numeric columns
- **Correlation Heatmaps** - Identify relationships between variables
- **Categorical Bar Charts** - Analyze categorical distributions

### 5. **Intelligent Analysis** 🤖

- AI-powered insights using Google Gemini 2.0
- Healthcare/pharmaceutical context focus
- Actionable recommendations
- Trend identification

### 6. **Comprehensive Downloads** 📥

- Export data as CSV
- Download statistical summaries
- Full analysis reports with chat history
- AR visualization HTML files

## 🚀 How to Use

### Upload Data

1. Select your input type (Data/PowerPoint/Text/JSON)
2. Upload the file
3. View extracted content and data preview

### Get AI Insights

1. Click "Generate AI Insights"
2. Review comprehensive analysis
3. Get recommendations and trends

### Create Visualizations

1. Click "Generate Visualizations"
2. Explore interactive 3D plots
3. Analyze distributions and correlations

### Generate AR Experience

1. Click "Generate AR-Ready 3D Model"
2. Download HTML file
3. Open on phone/tablet for AR viewing

### Ask Questions

1. Use the chat input at the bottom
2. Ask anything about your data
3. Get instant AI-powered answers
4. Chat history saved during session

## 📋 Requirements

```bash
pip install streamlit pandas plotly python-pptx google-generativeai python-dotenv
```

## 🔧 Configuration

Create `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

## 🎨 Lilly Theme

- **Primary Red**: #E41E26
- **Black**: #000000, #0d0d0d
- **Dark Greys**: #1a1a1a, #2d2d2d, #3d3d3d, #4a4a4a

## 🌐 Access

- **Local**: http://localhost:8502
- **Network**: http://192.168.0.240:8502

## 💡 Tips

- For AR viewing, use latest iOS Safari or Android Chrome
- PowerPoint tables automatically converted to DataFrames
- JSON files can be nested - app finds data arrays automatically
- Chat history clears on browser refresh
- Download reports to save insights and chat conversations
