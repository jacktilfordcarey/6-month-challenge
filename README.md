# RWE Mounjaro Study Analysis Dashboard

A comprehensive data analysis tool with interactive visualizations and AI-powered chatbot for exploring the Real World Evidence (RWE) Mounjaro Study dataset.

## 🌟 Features

### 📊 **Comprehensive Data Analysis**

- Statistical summaries and descriptive analytics
- Treatment effectiveness analysis (Mounjaro vs Lifestyle interventions)
- Demographics analysis by age, gender, and country
- Comorbidities impact assessment
- Patient clustering and segmentation
- Statistical hypothesis testing

### 📈 **Interactive Visualizations**

- Overview dashboards with key metrics
- Treatment effectiveness comparisons
- Weight loss distribution analysis
- Demographic breakdowns
- Correlation heatmaps
- Time series analysis of patient enrollment
- Adverse events analysis
- Patient journey visualization

### 🤖 **AI-Powered Chatbot**

- Natural language queries about the dataset
- Context-aware responses using Google Gemini AI
- Suggested questions for data exploration
- Conversation history tracking
- Statistical insights on demand

### 🔍 **Dataset Explorer**

- Raw data viewing with filtering capabilities
- Column selection and data export
- Data quality assessment
- Missing value analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini AI API key

### Installation

1. **Clone or download the project files:**

   ```bash
   # Ensure you have all the Python files in your working directory:
   # - app.py (main dashboard)
   # - data_analyzer.py (analysis module)
   # - visualizer.py (visualization module)
   # - chatbot.py (AI chatbot module)
   # - rwe_mounjaro_study_1000.csv (dataset)
   ```

2. **Install required packages:**

   ```bash
   pip install streamlit pandas numpy plotly seaborn matplotlib google-generativeai python-dotenv scikit-learn scipy
   ```

3. **Set up your Gemini API key:**

   **Option 1: Environment Variable (Recommended)**

   ```bash
   # On Windows (Command Prompt)
   set GEMINI_API_KEY=AIzaSyBJw42dilm_BS3GchYrKRX5txSVO3AwgHA

   # On Windows (PowerShell)
   $env:GEMINI_API_KEY="AIzaSyBJw42dilm_BS3GchYrKRX5txSVO3AwgHA"

   # On macOS/Linux
   export GEMINI_API_KEY=AIzaSyBJw42dilm_BS3GchYrKRX5txSVO3AwgHA
   ```

   **Option 2: Create a .env file**

   ```
   # Create a file named '.env' in your project directory
   GEMINI_API_KEY=AIzaSyBJw42dilm_BS3GchYrKRX5txSVO3AwgHA
   ```

4. **Run the application:**

   ```bash
   streamlit run app.py
   ```

5. **Open your browser:**
   The application will automatically open in your default browser at `http://localhost:8501`

## 📋 Usage Guide

### 🏠 **Overview Page**

- Quick metrics and key performance indicators
- Geographic distribution of patients
- Treatment outcomes summary
- Key insights generated from the data
- Interactive overview dashboard

### 🔬 **Data Analysis Page**

- **Treatment Effectiveness:** Compare Mounjaro vs Lifestyle interventions
- **Demographics:** Analysis by country, age group, and gender
- **Comorbidities:** Impact of medical conditions on outcomes
- **Statistical Tests:** T-tests, ANOVA, and correlation analysis

### 📊 **Visualizations Page**

Choose from various interactive charts:

- Weight loss analysis with scatter plots and distributions
- Country comparison with multiple metrics
- Time series analysis of patient enrollment
- Adverse events breakdown
- Patient journey BMI progression

### 🤖 **AI Chatbot Page**

- Ask natural language questions about the data
- Get AI-powered insights and explanations
- Use suggested questions for quick analysis
- View conversation history
- Examples of questions you can ask:
  - "How effective is Mounjaro compared to lifestyle intervention?"
  - "Which age group responds best to treatment?"
  - "What are the most common adverse events?"
  - "How does adherence affect treatment outcomes?"

### 🔍 **Dataset Explorer**

- View and filter raw data
- Select specific columns to display
- Download filtered datasets as CSV
- Check data quality and missing values

## 📊 Dataset Information

The RWE Mounjaro Study dataset contains 1,000 patient records with the following key variables:

### Patient Demographics

- **patient_id**: Unique patient identifier
- **age**: Patient age (26-69 years)
- **sex**: Gender (M/F)
- **country**: Study location (Italy, Spain, UK, Germany, France, Netherlands)

### Clinical Measures

- **baseline_bmi**: BMI at study start
- **followup_bmi**: BMI at study end
- **weight_change_kg**: Weight change in kilograms
- **diagnosis_date**: Initial diagnosis date
- **start_date/end_date**: Treatment period

### Treatment Information

- **intervention**: Treatment type (Mounjaro or LifestyleOnly)
- **adherence_rate**: Treatment adherence (0-1 scale)
- **outcome**: Treatment result categories
  - Significant Weight Loss
  - Moderate Weight Loss
  - Minimal Change
  - Worsened

### Safety and Comorbidities

- **adverse_event**: Reported side effects
- **hospitalizations**: Number of hospital admissions
- **comorbidities**: Existing medical conditions

## 🔧 Technical Architecture

### Core Modules

1. **DataAnalyzer (`data_analyzer.py`)**

   - Data loading and preprocessing
   - Statistical analysis functions
   - Treatment effectiveness calculations
   - Demographic analysis
   - Hypothesis testing

2. **DataVisualizer (`visualizer.py`)**

   - Interactive Plotly visualizations
   - Multiple chart types and dashboards
   - Responsive design for different screen sizes

3. **GeminiChatbot (`chatbot.py`)**

   - Integration with Google Gemini AI
   - Context-aware conversation handling
   - Question intent analysis
   - Conversation history management

4. **Streamlit App (`app.py`)**
   - Main dashboard interface
   - Page navigation and layout
   - Session state management
   - User interaction handling

### Key Features Implementation

- **Caching**: Uses Streamlit caching for improved performance
- **Error Handling**: Comprehensive error handling for API calls and data issues
- **Responsive Design**: Works on desktop and mobile devices
- **Export Functionality**: Download filtered data and visualizations
- **Real-time Analysis**: Interactive filtering and analysis

## 🤖 AI Chatbot Capabilities

The integrated Gemini AI chatbot can help you with:

### Treatment Analysis

- Compare intervention effectiveness
- Analyze success rates and outcomes
- Discuss statistical significance

### Patient Insights

- Demographic trends and patterns
- Risk factor analysis
- Patient segmentation insights

### Safety Analysis

- Adverse event patterns
- Hospitalization rates
- Safety profile comparisons

### Data Quality

- Missing data patterns
- Data distribution insights
- Study methodology questions

## 📈 Key Insights from the Dataset

Based on the analysis, here are some key findings:

1. **Treatment Effectiveness**: Mounjaro shows superior efficacy compared to lifestyle interventions
2. **Demographics**: Treatment response varies by age group and geographic location
3. **Safety Profile**: Well-characterized adverse event profile with manageable side effects
4. **Adherence Impact**: Higher adherence rates correlate with better outcomes
5. **Comorbidities**: Existing conditions influence treatment response

## 🛠️ Customization Options

### Adding New Visualizations

1. Add new methods to the `DataVisualizer` class
2. Update the visualization selection in `app.py`
3. Test with your dataset

### Extending Analysis

1. Add new analysis methods to `DataAnalyzer`
2. Update the analysis tabs in the dashboard
3. Include new metrics in the chatbot context

### Modifying the Chatbot

1. Update the context in `GeminiChatbot.__init__()`
2. Add new suggested questions
3. Customize the response formatting

## 🔒 Security and Privacy

- **API Key Security**: Store API keys in environment variables
- **Data Privacy**: All data processing happens locally
- **No Data Transmission**: Dataset never leaves your local environment
- **Session Management**: Secure session state handling

## 🚨 Troubleshooting

### Common Issues

1. **"Dataset file not found" error**

   - Ensure `rwe_mounjaro_study_1000.csv` is in the same directory as `app.py`

2. **Gemini API errors**

   - Verify your API key is correct
   - Check your internet connection
   - Ensure you have API quota available

3. **Installation issues**

   - Use a virtual environment
   - Update pip: `pip install --upgrade pip`
   - Install packages one by one if bulk installation fails

4. **Performance issues**
   - Clear Streamlit cache: Settings → Clear Cache
   - Restart the application
   - Check available system memory

### Getting Help

If you encounter issues:

1. Check the Streamlit logs in your terminal
2. Verify all dependencies are installed correctly
3. Ensure Python version compatibility (3.8+)

## 📄 License

This project is provided as-is for educational and research purposes. Please ensure compliance with your organization's data handling policies when using with sensitive healthcare data.

## 🤝 Contributing

To extend or modify the tool:

1. Follow the existing code structure
2. Add comprehensive error handling
3. Update documentation for new features
4. Test thoroughly with the provided dataset

## 📧 Support

For technical support or questions about the implementation, refer to the inline documentation in each module or the Streamlit community resources.
