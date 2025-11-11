"""
Main Streamlit Dashboard Application for Mounjaro Study Analysis

This is the main application that combines data analysis, visualizations, and AI chatbot
into an interactive dashboard for exploring the RWE Mounjaro Study dataset.
"""

import streamlit as st
import pandas as pd
import os
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

# Import custom modules
from data_analyzer import DataAnalyzer
from visualizer import DataVisualizer
from chatbot import GeminiChatbot

# Page configuration
st.set_page_config(
    page_title="RWE Mounjaro Study Analysis Dashboard",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize accessibility settings
if 'accessibility' not in st.session_state:
    st.session_state.accessibility = {
        'high_contrast': False,
        'large_text': False,
        'reduced_motion': False,
        'screen_reader': False,
        'keyboard_navigation': False
    }

# Base CSS will be applied, accessibility CSS will be added dynamically in main()

st.markdown(f"""
<style>
    .main-header {{
        font-size: 2.2rem;
        color: #2c3e50;
        font-weight: 600;
        padding: 1.5rem 0;
        border-bottom: 2px solid #3498db;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
        padding-left: 1rem;
        border-radius: 8px;
        role: banner;
    }}
    
    /* Accessibility enhancements */
    .accessible-button {{
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 500;
        border-radius: 8px;
        border: 2px solid transparent;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    .accessible-button:focus {{
        outline: 3px solid #007bff;
        outline-offset: 2px;
    }}
    

    

    
    .accessibility-controls {{
        position: fixed;
        top: 10px;
        right: 10px;
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        z-index: 1000;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    
    .ar-viewer {{
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        color: white;
        position: relative;
        overflow: hidden;
    }}
    
    .ar-viewer::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: repeating-linear-gradient(
            45deg,
            transparent,
            transparent 10px,
            rgba(255,255,255,0.1) 10px,
            rgba(255,255,255,0.1) 20px
        );
        animation: ar-scan 3s linear infinite;
    }}
    
    @keyframes ar-scan {{
        0% {{ transform: translateX(-100%) translateY(-100%); }}
        100% {{ transform: translateX(100%) translateY(100%); }}
    }}
    
    .ar-controls {{
        background: rgba(0,0,0,0.8);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    .data-cube {{
        perspective: 1000px;
        height: 400px;
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    
    .cube {{
        width: 200px;
        height: 200px;
        position: relative;
        transform-style: preserve-3d;
        animation: rotate3d 10s infinite linear;
    }}
    
    .cube-face {{
        position: absolute;
        width: 200px;
        height: 200px;
        background: rgba(52, 152, 219, 0.8);
        border: 2px solid #3498db;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
        color: white;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }}
    
    .cube-face.front {{ transform: rotateY(0deg) translateZ(100px); }}
    .cube-face.back {{ transform: rotateY(180deg) translateZ(100px); }}
    .cube-face.right {{ transform: rotateY(90deg) translateZ(100px); }}
    .cube-face.left {{ transform: rotateY(-90deg) translateZ(100px); }}
    .cube-face.top {{ transform: rotateX(90deg) translateZ(100px); }}
    .cube-face.bottom {{ transform: rotateX(-90deg) translateZ(100px); }}
    
    @keyframes rotate3d {{
        from {{ transform: rotateX(0deg) rotateY(0deg); }}
        to {{ transform: rotateX(360deg) rotateY(360deg); }}
    }}
    
    .metric-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }}
    
    .navigation-card {{
        background: white;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin-bottom: 1rem;
        overflow: hidden;
    }}
    
    .nav-button {{
        display: block;
        width: 100%;
        padding: 1rem;
        border: none;
        background: white;
        text-align: left;
        cursor: pointer;
        transition: all 0.2s ease;
        border-bottom: 1px solid #f1f3f4;
    }}
    
    .nav-button:hover {{
        background: #f8f9fa;
        color: #2c3e50;
    }}
    
    .nav-button.active {{
        background: #3498db;
        color: white;
        font-weight: 600;
    }}
    
    .section-header {{
        color: #2c3e50;
        font-size: 1.4rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #ecf0f1;
    }}
    
    .info-box {{
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }}
    
    .success-box {{
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #28a745;
    }}
    
    .warning-box {{
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #ffc107;
    }}
    
    .tabs-container {{
        background: white;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        overflow: hidden;
        margin: 1rem 0;
    }}
    
    .stSelectbox > div > div {{
        background: white;
        border: 1px solid #ced4da;
        border-radius: 6px;
    }}
    
    .stButton > button {{
        background: #3498db;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }}
    
    .stButton > button:hover {{
        background: #2980b9;
        transform: translateY(-1px);
    }}
    
    .sidebar .stSelectbox {{
        margin-bottom: 1rem;
    }}
    
    .quick-stats {{
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }}
    
    /* Full Screen AR Styles */
    .fullscreen-ar {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.95);
        z-index: 9999;
        overflow: auto;
    }}
    
    .fullscreen-controls {{
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        background: rgba(255, 255, 255, 0.9);
        padding: 10px;
        border-radius: 8px;
    }}
    
    .ar-fullscreen-viewer {{
        width: 100%;
        height: 100vh;
        padding: 20px;
        box-sizing: border-box;
    }}
    
    /* Enhanced Accessibility Styles */
    .accessibility-font-small {{ font-size: 0.95em !important; }}
    .accessibility-font-normal {{ font-size: 1em !important; }}
    .accessibility-font-large {{ font-size: 1em !important; }}
    .accessibility-font-extra-large {{ font-size: 1.01em !important; }}
    
    .high-contrast-mode {{
        background: #000 !important;
        color: #fff !important;
    }}
    
    .high-contrast-mode .metric-card {{
        background: #222 !important;
        color: #fff !important;
        border: 2px solid #fff !important;
    }}
    
    .high-contrast-mode .info-box {{
        background: #333 !important;
        color: #fff !important;
        border-left-color: #fff !important;
    }}
    
    .reduced-motion * {{
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }}
    
    /* Focus indicators for better keyboard navigation */
    .stSelectbox > div > div:focus-within,
    .stSlider > div > div:focus-within,
    .stCheckbox > div:focus-within {{
        outline: 3px solid #007bff;
        outline-offset: 2px;
        border-radius: 4px;
    }}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the dataset."""
    csv_path = "rwe_mounjaro_study_1000.csv"
    if not os.path.exists(csv_path):
        st.error(f"Dataset file '{csv_path}' not found. Please ensure the file is in the current directory.")
        st.stop()
    return csv_path

@st.cache_resource
def initialize_analyzer(csv_path):
    """Initialize and cache the data analyzer."""
    return DataAnalyzer(csv_path)

@st.cache_resource
def initialize_visualizer(_analyzer):
    """Initialize and cache the visualizer."""
    return DataVisualizer(_analyzer)

def initialize_chatbot(analyzer):
    """Initialize the chatbot (not cached due to API calls)."""
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = GeminiChatbot(analyzer)
    return st.session_state.chatbot

def main():
    """Main application function."""
    
    # Custom Dataset Upload in sidebar
    with st.sidebar.expander("📂 Custom Dataset Upload", expanded=False):
        st.markdown("**Upload Your Own CSV File:**")
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload your own dataset to analyze. Must be in CSV format."
        )
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                st.session_state.custom_csv_path = tmp_file.name
                st.session_state.custom_csv_name = uploaded_file.name
            
            st.success(f"✅ Loaded: {uploaded_file.name}")
            st.info(f"📊 Size: {len(uploaded_file.getvalue())} bytes")
            
            if st.button("🔄 Use This Dataset", key="use_custom"):
                st.session_state.use_custom_dataset = True
                st.rerun()
        
        # Show current dataset info
        if 'use_custom_dataset' in st.session_state and st.session_state.use_custom_dataset:
            st.markdown("**Current Dataset:**")
            st.markdown(f"📁 {st.session_state.get('custom_csv_name', 'Custom Upload')}")
            
            if st.button("🔙 Return to Default Dataset", key="use_default"):
                st.session_state.use_custom_dataset = False
                if 'custom_csv_path' in st.session_state:
                    try:
                        os.remove(st.session_state.custom_csv_path)
                    except:
                        pass
                st.rerun()
        else:
            st.markdown("**Current Dataset:**")
            st.markdown("📁 RWE Mounjaro Study (Default)")
    
    # Accessibility controls in sidebar
    with st.sidebar.expander("🔧 Accessibility Settings"):
        st.markdown("**Visual Accessibility:**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.checkbox("High Contrast", value=st.session_state.accessibility['high_contrast']):
                st.session_state.accessibility['high_contrast'] = True
            else:
                st.session_state.accessibility['high_contrast'] = False
        
        with col2:
            if st.checkbox("Reduced Motion", value=st.session_state.accessibility['reduced_motion']):
                st.session_state.accessibility['reduced_motion'] = True
            else:
                st.session_state.accessibility['reduced_motion'] = False
            
            if st.checkbox("Screen Reader Mode", value=st.session_state.accessibility['screen_reader']):
                st.session_state.accessibility['screen_reader'] = True
            else:
                st.session_state.accessibility['screen_reader'] = False
        
        if st.button("Reset Accessibility", key="reset_accessibility"):
            for key in st.session_state.accessibility:
                st.session_state.accessibility[key] = False
            st.rerun()
    
    # Apply dynamic accessibility CSS
    accessibility_css = ""
    if st.session_state.accessibility['high_contrast']:
        accessibility_css += """
        <style>
        .main-header { background: #000 !important; color: #fff !important; }
        .metric-card { background: #000 !important; color: #fff !important; border: 2px solid #fff !important; }
        .info-box { background: #333 !important; color: #fff !important; }
        .stApp { background-color: #000 !important; color: #fff !important; }
        </style>
        """



    if st.session_state.accessibility['reduced_motion']:
        accessibility_css += """
        <style>
        * { animation: none !important; transition: none !important; }
        .stButton > button:hover { transform: none !important; }
        </style>
        """
    
    if accessibility_css:
        st.markdown(accessibility_css, unsafe_allow_html=True)
    
    # Header with semantic markup
    st.markdown('<h1 class="main-header" id="main-content" role="banner">RWE Mounjaro Study Analysis Dashboard</h1>', 
                unsafe_allow_html=True)
    
    # Initialize components - check for custom dataset
    if 'use_custom_dataset' in st.session_state and st.session_state.use_custom_dataset:
        if 'custom_csv_path' in st.session_state:
            csv_path = st.session_state.custom_csv_path
            st.info(f"📊 Analyzing custom dataset: {st.session_state.get('custom_csv_name', 'Custom Upload')}")
        else:
            csv_path = load_data()
    else:
        csv_path = load_data()
    
    try:
        analyzer = initialize_analyzer(csv_path)
        visualizer = initialize_visualizer(analyzer)
    except Exception as e:
        st.error(f"❌ Error loading dataset: {str(e)}")
        st.warning("Please ensure your CSV file has the required columns or return to the default dataset.")
        st.stop()
    
    # Sidebar Navigation
    st.sidebar.markdown('<div class="navigation-card" id="navigation" role="navigation">', unsafe_allow_html=True)
    st.sidebar.markdown("## Navigation")
    
    # Page selection with cleaner labels and AR option
    pages = {
        "Study Overview": "overview",
        "Data Analysis": "analysis", 
        "Visualizations": "visualizations",
        "AR Data Viewer": "ar_viewer",
        "AI Assistant": "chatbot",
        "Dataset Explorer": "explorer"
    }
    
    selected_page = st.sidebar.selectbox(
        "Navigate to:",
        list(pages.keys()),
        index=0
    )
    
    current_page = pages[selected_page]
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Quick stats sidebar
    st.sidebar.markdown('<div class="quick-stats">', unsafe_allow_html=True)
    st.sidebar.markdown("## Key Metrics")
    basic_stats = analyzer.get_basic_statistics()
    
    # Display metrics in a cleaner format
    st.sidebar.metric("Total Patients", basic_stats['dataset_overview']['total_patients'])
    st.sidebar.metric("Countries Included", basic_stats['dataset_overview']['unique_countries'])
    
    mounjaro_rate = analyzer.analyze_treatment_effectiveness()['Mounjaro']['significant_weight_loss_rate']
    st.sidebar.metric("Mounjaro Success Rate", f"{mounjaro_rate}%")
    
    ae_rate = round((basic_stats['outcomes']['adverse_events']['total_with_ae'] / 
                    basic_stats['dataset_overview']['total_patients']) * 100, 1)
    st.sidebar.metric("Adverse Event Rate", f"{ae_rate}%")
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Main content based on selected page
    if current_page == "overview":
        show_overview_page(analyzer, visualizer, basic_stats)
    elif current_page == "analysis":
        show_analysis_page(analyzer, visualizer)
    elif current_page == "visualizations":
        show_visualizations_page(visualizer)
    elif current_page == "ar_viewer":
        show_ar_viewer_page(analyzer, visualizer)
    elif current_page == "chatbot":
        show_chatbot_page(analyzer)
    elif current_page == "explorer":
        show_explorer_page(analyzer)

def show_overview_page(analyzer, visualizer, basic_stats):
    """Show the overview page."""
    st.markdown('<h2 class="section-header">Study Overview</h2>', unsafe_allow_html=True)
    
    # Key metrics in cards
    col1, col2, col3, col4 = st.columns(4)
    
    effectiveness = analyzer.analyze_treatment_effectiveness()
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Total Patients", 
            basic_stats['dataset_overview']['total_patients'],
            delta=f"{len(analyzer.df[analyzer.df['intervention'] == 'Mounjaro'])} on Mounjaro"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        mounjaro_weight_loss = effectiveness['Mounjaro']['mean_weight_loss']
        lifestyle_weight_loss = effectiveness['LifestyleOnly']['mean_weight_loss']
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Mounjaro Avg Weight Loss", 
            f"{mounjaro_weight_loss} kg",
            delta=f"{mounjaro_weight_loss - lifestyle_weight_loss:.1f} kg vs Lifestyle"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        mounjaro_success = effectiveness['Mounjaro']['significant_weight_loss_rate']
        lifestyle_success = effectiveness['LifestyleOnly']['significant_weight_loss_rate']
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Mounjaro Success Rate", 
            f"{mounjaro_success}%",
            delta=f"{mounjaro_success - lifestyle_success:.1f}% vs Lifestyle"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Study Duration", 
            f"{(analyzer.df['end_date'].max() - analyzer.df['start_date'].min()).days} days",
            delta="Multi-year study"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Overview visualizations
    st.markdown('<h3 class="section-header">Geographic and Outcome Distribution</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Geographic Distribution**")
        country_dist = basic_stats['demographics']['country_distribution']
        country_df = pd.DataFrame(
            list(country_dist.items()), 
            columns=['Country', 'Patients']
        )
        st.bar_chart(country_df.set_index('Country'), height=300)
    
    with col2:
        st.markdown("**Treatment Outcomes**")
        outcome_dist = basic_stats['outcomes']['outcome_distribution']
        outcome_df = pd.DataFrame(
            list(outcome_dist.items()), 
            columns=['Outcome', 'Count']
        )
        st.bar_chart(outcome_df.set_index('Outcome'), height=300)
    
    # Key insights
    st.markdown('<h3 class="section-header">Key Clinical Insights</h3>', unsafe_allow_html=True)
    insights = analyzer.generate_insights()
    
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    for i, insight in enumerate(insights, 1):
        st.markdown(f"**{i}.** {insight}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Overview dashboard
    st.markdown('<h3 class="section-header">Comprehensive Overview Dashboard</h3>', unsafe_allow_html=True)
    fig_overview = visualizer.create_overview_dashboard()
    st.plotly_chart(fig_overview, width="stretch")

def show_analysis_page(analyzer, visualizer):
    """Show the detailed analysis page."""
    st.markdown('<h2 class="section-header">Detailed Clinical Analysis</h2>', unsafe_allow_html=True)
    
    # Analysis tabs with cleaner names
    tab1, tab2, tab3, tab4 = st.tabs([
        "Treatment Effectiveness", 
        "Demographics Analysis", 
        "Comorbidities Impact", 
        "Statistical Testing"
    ])
    
    with tab1:
        st.markdown("**Comparative Treatment Analysis**")
        effectiveness = analyzer.analyze_treatment_effectiveness()
        
        # Create comparison table with better formatting
        st.markdown("##### Treatment Effectiveness Comparison")
        eff_df = pd.DataFrame(effectiveness).T
        st.dataframe(
            eff_df.style.format({
                'mean_weight_loss': '{:.2f} kg',
                'mean_bmi_change': '{:.2f}',
                'significant_weight_loss_rate': '{:.1f}%',
                'any_weight_loss_rate': '{:.1f}%',
                'mean_adherence': '{:.2f}',
                'adverse_event_rate': '{:.1f}%',
                'hospitalization_rate': '{:.1f}%'
            }),
            width="stretch"
        )
        
        # Intervention comparison chart
        st.markdown("##### Visual Comparison")
        fig_intervention = visualizer.create_intervention_comparison()
        st.plotly_chart(fig_intervention, width="stretch")
    
    with tab2:
        st.markdown("**Patient Demographics and Outcomes**")
        demographics = analyzer.analyze_by_demographics()
        
        # Country analysis
        st.markdown("##### Analysis by Country")
        country_df = pd.DataFrame(demographics['by_country']).T
        st.dataframe(
            country_df.style.format({
                'mean_weight_loss': '{:.2f} kg',
                'success_rate': '{:.1f}%',
                'mounjaro_usage': '{:.1f}%'
            }),
            width="stretch"
        )
        
        # Age group analysis
        st.markdown("##### Analysis by Age Group")
        age_df = pd.DataFrame(demographics['by_age_group']).T
        st.dataframe(
            age_df.style.format({
                'mean_weight_loss': '{:.2f} kg',
                'success_rate': '{:.1f}%',
                'mean_adherence': '{:.2f}'
            }),
            width="stretch"
        )
        
        # Demographics visualization
        st.markdown("##### Demographics Visual Analysis")
        fig_demographics = visualizer.create_demographic_analysis()
        st.plotly_chart(fig_demographics, width="stretch")
    
    with tab3:
        st.markdown("#### Comorbidities Impact Analysis")
        comorbidities = analyzer.analyze_comorbidities_impact()
        
        # By comorbidity count
        st.markdown("##### By Number of Comorbidities")
        count_df = pd.DataFrame(comorbidities['by_count']).T
        st.dataframe(
            count_df.style.format({
                'mean_weight_loss': '{:.2f} kg',
                'success_rate': '{:.1f}%',
                'mean_adherence': '{:.2f}'
            }),
            width="stretch"
        )
        
        # Specific comorbidities comparison
        if 'by_type' in comorbidities:
            st.markdown("##### Specific Comorbidities Impact")
            for condition, data in comorbidities['by_type'].items():
                with st.expander(f"Impact of {condition}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**With Condition:**")
                        st.write(f"Patients: {data['with_condition']['n_patients']}")
                        st.write(f"Mean Weight Loss: {data['with_condition']['mean_weight_loss']:.2f} kg")
                        st.write(f"Success Rate: {data['with_condition']['success_rate']:.1f}%")
                    
                    with col2:
                        st.markdown("**Without Condition:**")
                        st.write(f"Patients: {data['without_condition']['n_patients']}")
                        st.write(f"Mean Weight Loss: {data['without_condition']['mean_weight_loss']:.2f} kg")
                        st.write(f"Success Rate: {data['without_condition']['success_rate']:.1f}%")
        
        # Comorbidities visualization
        fig_comorbidities = visualizer.create_comorbidities_analysis()
        st.plotly_chart(fig_comorbidities, width="stretch")
    
    with tab4:
        st.markdown("#### Statistical Tests")
        tests = analyzer.statistical_tests()
        
        for test_name, results in tests.items():
            with st.expander(f"{test_name.replace('_', ' ').title()}"):
                st.write(f"**Test Type:** {results['test_type']}")
                
                if 'correlation_coefficient' in results:
                    st.write(f"**Correlation Coefficient:** {results['correlation_coefficient']}")
                elif 't_statistic' in results:
                    st.write(f"**T-statistic:** {results['t_statistic']}")
                elif 'f_statistic' in results:
                    st.write(f"**F-statistic:** {results['f_statistic']}")
                
                st.write(f"**P-value:** {results['p_value']}")
                st.write(f"**Significant:** {'Yes' if results['significant'] else 'No'}")
                st.write(f"**Interpretation:** {results['interpretation']}")
        
        # Correlation heatmap
        st.markdown("##### Variable Correlation Analysis")
        fig_correlation = visualizer.create_correlation_heatmap()
        st.plotly_chart(fig_correlation, width="stretch")

def show_visualizations_page(visualizer):
    """Show the visualizations page."""
    st.markdown('<h2 class="section-header">Interactive Data Visualizations</h2>', unsafe_allow_html=True)
    
    # Visualization selection with better organization
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("**Select a visualization type to explore different aspects of the study data:**")
    st.markdown('</div>', unsafe_allow_html=True)
    
    viz_options = {
        "Weight Loss Analysis": "weight_loss",
        "Country Comparison": "country",
        "Time Series Analysis": "time_series",
        "Adverse Events Analysis": "adverse_events",
        "Patient Journey Tracking": "patient_journey"
    }
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_viz = st.selectbox(
            "Choose Visualization:",
            list(viz_options.keys()),
            index=0
        )
    
    viz_type = viz_options[selected_viz]
    
    # Add description for each visualization
    descriptions = {
        "weight_loss": "Comprehensive analysis of weight loss patterns across different treatment groups",
        "country": "Geographic comparison of treatment effectiveness and patient characteristics",
        "time_series": "Timeline analysis showing patient enrollment patterns over the study period",
        "adverse_events": "Safety analysis displaying adverse event frequencies and types",
        "patient_journey": "Individual patient trajectories showing BMI changes from baseline to follow-up"
    }
    
    with col2:
        st.markdown(f'<div class="info-box"><strong>About this visualization:</strong><br>{descriptions[viz_type]}</div>', unsafe_allow_html=True)
    
    if viz_type == "weight_loss":
        st.markdown('<h3 class="section-header">Weight Loss Analysis</h3>', unsafe_allow_html=True)
        fig = visualizer.create_weight_loss_analysis()
        st.plotly_chart(fig, width="stretch")
    
    elif viz_type == "country":
        st.markdown('<h3 class="section-header">Country Comparison Analysis</h3>', unsafe_allow_html=True)
        fig = visualizer.create_country_comparison()
        st.plotly_chart(fig, width="stretch")
    
    elif viz_type == "time_series":
        st.markdown('<h3 class="section-header">Study Enrollment Timeline</h3>', unsafe_allow_html=True)
        fig = visualizer.create_time_series_analysis()
        st.plotly_chart(fig, width="stretch")
    
    elif viz_type == "adverse_events":
        st.markdown('<h3 class="section-header">Safety Profile Analysis</h3>', unsafe_allow_html=True)
        fig = visualizer.create_adverse_events_analysis()
        st.plotly_chart(fig, width="stretch")
    
    elif viz_type == "patient_journey":
        st.markdown('<h3 class="section-header">Individual Patient BMI Trajectories</h3>', unsafe_allow_html=True)
        st.markdown('<div class="info-box">This visualization tracks individual patient BMI changes from baseline to follow-up (showing a representative sample of 50 patients)</div>', unsafe_allow_html=True)
        fig = visualizer.create_patient_journey_analysis()
        st.plotly_chart(fig, width="stretch")

def show_chatbot_page(analyzer):
    """Show the AI chatbot page."""
    st.markdown('<h2 class="section-header">AI-Powered Data Assistant</h2>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">Ask questions about the Mounjaro study data and receive AI-powered insights and analysis based on the complete dataset.</div>', unsafe_allow_html=True)
    
    # Initialize chatbot
    chatbot = initialize_chatbot(analyzer)
    
    # Quick stats in a clean layout
    st.markdown("**Study Summary Metrics**")
    quick_stats = chatbot.get_quick_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Patients", quick_stats['total_patients'])
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Mounjaro Success", f"{quick_stats['mounjaro_success_rate']}%")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Lifestyle Success", f"{quick_stats['lifestyle_success_rate']}%")
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Countries", quick_stats['total_countries'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    # API Status check in collapsible section
    with st.expander("System Status & Diagnostics"):
        st.markdown("**AI Assistant Status:**")
        if hasattr(chatbot, 'model') and chatbot.model:
            st.markdown('<div class="success-box">AI model initialized and ready</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-box">AI model not initialized - check API configuration</div>', unsafe_allow_html=True)
        
        if st.button("Check Available AI Models"):
            models = chatbot.list_available_models()
            if isinstance(models, list):
                st.markdown("**Available Models:**")
                for model in models:
                    st.write(f"- {model}")
            else:
                st.error(models)
    
    st.markdown("---")
    
    # Main chat interface
    st.markdown('<h3 class="section-header">Interactive Question & Answer</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Initialize chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Chat input section
        st.markdown("**Ask Your Question:**")
        user_question = st.text_input(
            "Type your question here:",
            placeholder="e.g., How effective is Mounjaro compared to lifestyle intervention?",
            label_visibility="collapsed"
        )
        
        col_ask, col_clear = st.columns([3, 1])
        
        with col_ask:
            if st.button("Get AI Analysis", type="primary", width="stretch"):
                if user_question.strip():
                    with st.spinner("Analyzing data and generating response..."):
                        response = chatbot.ask(user_question)
                        st.session_state.chat_history.append({
                            'question': user_question,
                            'answer': response
                        })
                        st.rerun()
        
        with col_clear:
            if st.button("Clear Chat", width="stretch"):
                st.session_state.chat_history = []
                chatbot.clear_history()
                st.success("Chat history cleared!")
        
        # Display chat history
        st.markdown("**Conversation History:**")
        
        if st.session_state.chat_history:
            # Show recent conversations first
            for i, exchange in enumerate(reversed(st.session_state.chat_history[-5:])):
                st.markdown(f'<div class="info-box">', unsafe_allow_html=True)
                st.markdown(f"**Question {len(st.session_state.chat_history)-i}:** {exchange['question']}")
                st.markdown(f"**Answer:** {exchange['answer']}")
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("")
        else:
            st.markdown('<div class="info-box">No conversation history yet. Ask a question to get started with AI-powered insights!</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Suggested Questions**")
        st.markdown("Click any question below to get instant insights:")
        
        suggested_questions = chatbot.get_suggested_questions()
        
        # Categorize suggestions with cleaner labels
        categories = {
            "Treatment Effectiveness": suggested_questions[:4],
            "Patient Demographics": suggested_questions[4:8],
            "Safety Profile": suggested_questions[8:12],
            "Clinical Analysis": suggested_questions[12:16],
            "Study Metrics": suggested_questions[16:20]
        }
        
        for category, questions in categories.items():
            with st.expander(f"**{category}**"):
                for question in questions:
                    if st.button(question, key=f"btn_{hash(question)}", width="stretch"):
                        with st.spinner("Processing your question..."):
                            response = chatbot.ask(question)
                            st.session_state.chat_history.append({
                                'question': question,
                                'answer': response
                            })
                            st.rerun()

def show_explorer_page(analyzer):
    """Show the dataset explorer page."""
    st.markdown('<h2 class="section-header">Dataset Explorer & Raw Data</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-box">Explore and filter the complete study dataset. Use the filters below to focus on specific patient populations or outcomes.</div>', unsafe_allow_html=True)
    
    # Filters section
    st.markdown("**Data Filters:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        countries = ['All Countries'] + list(analyzer.df['country'].unique())
        selected_country = st.selectbox("Country Filter:", countries)
    
    with col2:
        interventions = ['All Treatments'] + list(analyzer.df['intervention'].unique())
        selected_intervention = st.selectbox("Treatment Filter:", interventions)
    
    with col3:
        outcomes = ['All Outcomes'] + list(analyzer.df['outcome'].unique())
        selected_outcome = st.selectbox("Outcome Filter:", outcomes)
    
    # Apply filters
    filtered_df = analyzer.df.copy()
    
    if selected_country != 'All Countries':
        filtered_df = filtered_df[filtered_df['country'] == selected_country]
    
    if selected_intervention != 'All Treatments':
        filtered_df = filtered_df[filtered_df['intervention'] == selected_intervention]
    
    if selected_outcome != 'All Outcomes':
        filtered_df = filtered_df[filtered_df['outcome'] == selected_outcome]
    
    # Display filter results
    st.markdown(f'<div class="success-box">Displaying <strong>{len(filtered_df):,}</strong> of <strong>{len(analyzer.df):,}</strong> total patients based on your filters</div>', unsafe_allow_html=True)
    
    # Column selection with better defaults
    st.markdown("**Column Selection:**")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        display_columns = st.multiselect(
            "Choose columns to display in the table:",
            options=analyzer.df.columns.tolist(),
            default=['patient_id', 'age', 'sex', 'country', 'intervention', 
                    'baseline_bmi', 'followup_bmi', 'weight_change_kg', 'outcome']
        )
    
    with col2:
        # Quick column sets
        if st.button("Select Core Columns", width="stretch"):
            st.session_state.display_columns = ['patient_id', 'age', 'sex', 'country', 'intervention', 'outcome']
        if st.button("Select Clinical Measures", width="stretch"):
            st.session_state.display_columns = ['patient_id', 'baseline_bmi', 'followup_bmi', 'weight_change_kg', 'adherence_rate']
        if st.button("Select All Columns", width="stretch"):
            st.session_state.display_columns = analyzer.df.columns.tolist()
    
    if display_columns:
        st.markdown("**Filtered Dataset:**")
        st.dataframe(
            filtered_df[display_columns],
            width="stretch",
            height=500
        )
        
        # Download options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = filtered_df[display_columns].to_csv(index=False)
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name=f"mounjaro_study_filtered_{len(filtered_df)}_patients.csv",
                mime="text/csv",
                width="stretch"
            )
        
        with col2:
            excel_buffer = pd.ExcelWriter('temp.xlsx')
            filtered_df[display_columns].to_excel(excel_buffer, index=False)
            excel_data = excel_buffer.close()
            
        with col3:
            st.markdown(f"**Records:** {len(filtered_df):,}")
    
    else:
        st.markdown('<div class="warning-box">Please select at least one column to display the data</div>', unsafe_allow_html=True)
    
    # Data quality summary
    st.markdown('<h3 class="section-header">Data Quality Assessment</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Missing Values Analysis:**")
        missing_data = filtered_df.isnull().sum()
        missing_df = pd.DataFrame({
            'Column': missing_data.index,
            'Missing Count': missing_data.values,
            'Missing Percentage': (missing_data.values / len(filtered_df) * 100).round(2)
        })
        missing_df = missing_df[missing_df['Missing Count'] > 0]
        
        if len(missing_df) > 0:
            st.dataframe(missing_df, width="stretch")
        else:
            st.markdown('<div class="success-box">Excellent data quality - no missing values detected!</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Column Data Types:**")
        dtype_df = pd.DataFrame({
            'Column': filtered_df.dtypes.index,
            'Data Type': filtered_df.dtypes.values.astype(str),
            'Non-Null Count': [len(filtered_df) - filtered_df[col].isnull().sum() for col in filtered_df.columns]
        })
        st.dataframe(dtype_df, width="stretch")

def show_ar_viewer_page(analyzer, visualizer):
    """Show the AR data viewer page with full screen and accessibility options."""
    
    # Initialize session state for AR settings
    if 'ar_fullscreen' not in st.session_state:
        st.session_state.ar_fullscreen = False
    if 'ar_high_contrast' not in st.session_state:
        st.session_state.ar_high_contrast = False
    if 'ar_reduced_motion' not in st.session_state:
        st.session_state.ar_reduced_motion = False
    if 'ar_font_size' not in st.session_state:
        st.session_state.ar_font_size = 'normal'
    
    # Header with accessibility controls
    st.markdown('<h2 class="section-header">Augmented Reality Data Visualization</h2>', unsafe_allow_html=True)
    
    # Accessibility Controls Section
    with st.expander("🔧 Accessibility & Display Settings", expanded=False):
        acc_col1, acc_col2, acc_col3, acc_col4 = st.columns(4)
        
        with acc_col1:
            st.session_state.ar_fullscreen = st.checkbox(
                "Full Screen Mode", 
                value=st.session_state.ar_fullscreen,
                help="Expand visualizations to use maximum screen space"
            )
        
        with acc_col2:
            st.session_state.ar_high_contrast = st.checkbox(
                "High Contrast Mode",
                value=st.session_state.ar_high_contrast,
                help="Enable high contrast colors for better visibility"
            )
        
        with acc_col3:
            st.session_state.ar_reduced_motion = st.checkbox(
                "Reduced Motion",
                value=st.session_state.ar_reduced_motion,
                help="Disable animations for motion sensitivity"
            )
        
        with acc_col4:
            st.session_state.ar_font_size = st.selectbox(
                "Font Size",
                ["small", "normal", "large", "extra-large"],
                index=["small", "normal", "large", "extra-large"].index(st.session_state.ar_font_size),
                help="Adjust text size for better readability"
            )
    
    st.markdown('''
    <div class="info-box">
    <strong>Immersive Data Experience:</strong> Explore the Mounjaro study data through innovative AR-style visualizations. 
    This interface provides interactive 3D representations of clinical data patterns and patient outcomes.
    <br><br>
    <strong>Navigation Tips:</strong> Use your mouse to rotate, zoom, and pan through 3D visualizations. 
    Enable accessibility options above for a more comfortable viewing experience.
    </div>
    ''', unsafe_allow_html=True)
    
    # Apply accessibility styles dynamically
    accessibility_classes = []
    if st.session_state.ar_high_contrast:
        accessibility_classes.append("high-contrast-mode")
    if st.session_state.ar_reduced_motion:
        accessibility_classes.append("reduced-motion")
    
    font_class = f"accessibility-font-{st.session_state.ar_font_size.replace('-', '-')}"
    accessibility_classes.append(font_class)
    
    accessibility_class_str = " ".join(accessibility_classes)
    

    
    # Apply full screen styles if enabled
    if st.session_state.ar_fullscreen:
        st.markdown(f'''
        <div class="fullscreen-ar {accessibility_class_str}">
            <div class="fullscreen-controls">
                <div style="background: rgba(255, 255, 255, 0.9); padding: 10px; border-radius: 8px; margin-bottom: 10px;">
                    <strong>🔲 Full Screen AR Mode Active</strong><br>
                    <small>Use the toggle button below to exit full screen</small>
                </div>
            </div>
            <div class="ar-fullscreen-viewer">
        ''', unsafe_allow_html=True)
        
        # Enhanced full screen CSS
        st.markdown('''
        <style>
        .fullscreen-ar {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            background: rgba(0, 0, 0, 0.95) !important;
            z-index: 9999 !important;
            overflow: auto !important;
            padding: 20px !important;
        }
        .ar-fullscreen-viewer {
            height: calc(100vh - 100px) !important;
            width: 100% !important;
        }
        .fullscreen-controls {
            position: fixed !important;
            top: 20px !important;
            right: 20px !important;
            z-index: 10000 !important;
        }
        </style>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="{accessibility_class_str}">', unsafe_allow_html=True)
    
    # AR Controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ar_mode = st.selectbox(
            "AR Visualization Mode:",
            ["3D Data Cube", "Patient Journey Map", "Outcome Constellation"],
            key="ar_mode_select"
        )
    
    with col2:
        # Disable animation speed control if reduced motion is enabled
        if st.session_state.ar_reduced_motion:
            animation_speed = 0.1
            st.write("Animation Speed: Disabled (Reduced Motion Mode)")
        else:
            animation_speed = st.slider("Animation Speed", 0.1, 3.0, 1.0, 0.1, key="ar_animation_speed")
        
    with col3:
        data_perspective = st.selectbox(
            "Data Perspective:",
            ["Treatment Groups", "Country Clusters", "Age Demographics", "Outcome Categories"],
            key="ar_data_perspective"
        )
    
    # Main AR Viewer
    st.markdown('<div class="ar-viewer">', unsafe_allow_html=True)
    
    if ar_mode == "3D Data Cube":
        # Get key statistics for the cube faces
        basic_stats = analyzer.get_basic_statistics()
        effectiveness = analyzer.analyze_treatment_effectiveness()
        
        st.markdown(f'''
        <div class="ar-controls">
            <h3>🎲 Interactive Data Cube</h3>
            <p>Each face of the cube represents a different data dimension. Rotate to explore:</p>
        </div>
        
        <div class="data-cube">
            <div class="cube" style="animation-duration: {10/animation_speed}s;">
                <div class="cube-face front">
                    <div>
                        <div>Total Patients</div>
                        <div style="font-size: 2em;">{basic_stats['dataset_overview']['total_patients']}</div>
                    </div>
                </div>
                <div class="cube-face back">
                    <div>
                        <div>Countries</div>
                        <div style="font-size: 2em;">{basic_stats['dataset_overview']['unique_countries']}</div>
                    </div>
                </div>
                <div class="cube-face right">
                    <div>
                        <div>Mounjaro Success</div>
                        <div style="font-size: 2em;">{effectiveness['Mounjaro']['significant_weight_loss_rate']:.1f}%</div>
                    </div>
                </div>
                <div class="cube-face left">
                    <div>
                        <div>Lifestyle Success</div>
                        <div style="font-size: 2em;">{effectiveness['LifestyleOnly']['significant_weight_loss_rate']:.1f}%</div>
                    </div>
                </div>
                <div class="cube-face top">
                    <div>
                        <div>Avg Weight Loss</div>
                        <div style="font-size: 1.5em;">{effectiveness['Mounjaro']['mean_weight_loss']:.1f} kg</div>
                    </div>
                </div>
                <div class="cube-face bottom">
                    <div>
                        <div>Adverse Events</div>
                        <div style="font-size: 1.5em;">{basic_stats['outcomes']['adverse_events']['total_with_ae']}</div>
                    </div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Interactive controls below cube
        st.markdown("### AR Data Interaction")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Rotate View", key="rotate_cube"):
                st.success("Cube rotation speed updated!")
        
        with col2:
            if st.button("📊 Change Data Layer", key="change_layer"):
                st.info("Data layer updated - see cube faces for new metrics!")
        
        with col3:
            if st.button("🎯 Focus Mode", key="focus_mode"):
                st.warning("Entering focus mode - reduced animations for better accessibility")
    
    elif ar_mode == "Patient Journey Map":
        # Create an immersive patient journey visualization
        st.markdown('''
        <div class="ar-controls">
            <h3>🗺️ Patient Journey AR Map</h3>
            <p>Follow individual patient trajectories through treatment in 3D space</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Sample some patients for visualization
        sample_patients = analyzer.df.sample(20)
        
        # Create a 3D scatter plot using Plotly
        fig = go.Figure(data=[
            go.Scatter3d(
                x=sample_patients['baseline_bmi'],
                y=sample_patients['followup_bmi'], 
                z=sample_patients['weight_change_kg'],
                mode='markers+text+lines',
                marker=dict(
                    size=12,
                    color=sample_patients['weight_change_kg'],
                    colorscale='RdYlGn',
                    colorbar=dict(title="Weight Change (kg)")
                ),
                text=sample_patients['intervention'],
                textposition="top center",
                line=dict(color='rgba(255,255,255,0.6)', width=2),
                name="Patient Journeys"
            )
        ])
        
        # Apply accessibility settings to chart
        title_color = "white" if not st.session_state.ar_high_contrast else "#ffff00"
        bg_color = "rgba(0,0,0,0.9)" if not st.session_state.ar_high_contrast else "#000000"
        
        fig.update_layout(
            title=dict(
                text="AR Patient Journey Map - 3D Treatment Trajectories",
                font=dict(
                    size=18 if st.session_state.ar_font_size == 'normal' else 
                         24 if st.session_state.ar_font_size == 'large' else 
                         28 if st.session_state.ar_font_size == 'extra-large' else 16,
                    color=title_color
                )
            ),
            scene=dict(
                xaxis_title="Baseline BMI",
                yaxis_title="Follow-up BMI", 
                zaxis_title="Weight Change (kg)",
                bgcolor=bg_color,
                xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="white"),
                yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="white"), 
                zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="white")
            ),
            paper_bgcolor=bg_color,
            font=dict(color=title_color),
            height=800 if st.session_state.ar_fullscreen else 600,
            margin=dict(t=40, l=40, r=40, b=40)
        )
        
        chart_height = 900 if st.session_state.ar_fullscreen else 600
        st.plotly_chart(fig, width="stretch", height=chart_height)
    
    else:  # Outcome Constellation
        st.markdown('''
        <div class="ar-controls">
            <h3>⭐ Outcome Constellation View</h3>
            <p>Navigate through patient outcomes mapped as an interactive star field. 
            Each star represents a patient, colored by outcome. Hover over stars for details.</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Add black text styling for AR mode controls
        st.markdown('''
        <style>
        .stSlider label, .stSlider p, .stSlider div {
            color: #000000 !important;
        }
        .stRadio label, .stRadio p, .stRadio div {
            color: #000000 !important;
        }
        .stSelectbox label, .stSelectbox p {
            color: #000000 !important;
        }
        .stMultiSelect label, .stMultiSelect p {
            color: #000000 !important;
        }
        .element-container p, .element-container div {
            color: #000000 !important;
        }
        h4, h5, h6 {
            color: #000000 !important;
        }
        </style>
        ''', unsafe_allow_html=True)
        
        # Enhanced constellation controls
        const_col1, const_col2, const_col3 = st.columns(3)
        
        with const_col1:
            sample_size = st.slider(
                "Number of Patient Stars:",
                min_value=20,
                max_value=200,
                value=100,
                step=20,
                help="Adjust constellation density"
            )
        
        with const_col2:
            star_size = st.slider(
                "Star Size:",
                min_value=4,
                max_value=16,
                value=10,
                step=2,
                help="Adjust marker size"
            )
        
        with const_col3:
            star_opacity = st.slider(
                "Star Brightness:",
                min_value=0.5,
                max_value=1.0,
                value=0.85,
                step=0.05,
                help="Adjust star visibility"
            )
        
        # Create enhanced constellation visualization
        constellation_data = analyzer.df.sample(sample_size)
        
        # Enhanced outcome colors with better contrast
        outcome_colors = {
            'Significant Weight Loss': '#00FF00',  # Bright Green
            'Moderate Weight Loss': '#4169E1',     # Royal Blue  
            'Minimal Weight Loss': '#FFA500',      # Orange
            'Weight Gain': '#FF1493'               # Deep Pink
        }
        
        # Apply accessibility adjustments
        if st.session_state.ar_high_contrast:
            outcome_colors = {
                'Significant Weight Loss': '#00FF00',
                'Moderate Weight Loss': '#00FFFF',
                'Minimal Weight Loss': '#FFFF00',
                'Weight Gain': '#FF00FF'
            }
        
        fig = go.Figure()
        
        for outcome in constellation_data['outcome'].unique():
            outcome_subset = constellation_data[constellation_data['outcome'] == outcome]
            
            # Enhanced hover text
            hover_texts = []
            for idx, row in outcome_subset.iterrows():
                hover_text = f"<b>Patient {row['patient_id']}</b><br>"
                hover_text += f"Age: {row['age']} | Sex: {row['sex']}<br>"
                hover_text += f"Country: {row['country']}<br>"
                hover_text += f"Treatment: {row['intervention']}<br>"
                hover_text += f"<b>Outcome: {outcome}</b><br>"
                hover_text += f"Baseline BMI: {row['baseline_bmi']:.1f}<br>"
                hover_text += f"Follow-up BMI: {row['followup_bmi']:.1f}<br>"
                hover_text += f"Weight Change: {row['weight_change_kg']:.1f} kg"
                hover_texts.append(hover_text)
            
            fig.add_trace(go.Scatter3d(
                x=outcome_subset['baseline_bmi'] + np.random.normal(0, 1.5, len(outcome_subset)),
                y=outcome_subset['followup_bmi'] + np.random.normal(0, 1.5, len(outcome_subset)),
                z=outcome_subset['weight_change_kg'] + np.random.normal(0, 0.5, len(outcome_subset)),
                mode='markers',
                marker=dict(
                    size=star_size,
                    color=outcome_colors.get(outcome, '#FFFFFF'),
                    opacity=star_opacity,
                    symbol='circle',
                    line=dict(color='white', width=0.5)
                ),
                name=f"{outcome} ({len(outcome_subset)})",
                text=hover_texts,
                hovertemplate="%{text}<extra></extra>",
                showlegend=True
            ))
        
        # Enhanced layout
        title_color = "#FFFF00" if st.session_state.ar_high_contrast else "white"
        bg_color = "#000000" if st.session_state.ar_high_contrast else "rgba(0,0,20,0.95)"
        grid_color = "#FFFFFF" if st.session_state.ar_high_contrast else "rgba(100,100,255,0.3)"
        
        fig.update_layout(
            title=dict(
                text=f"AR Outcome Constellation - {sample_size} Patient Stars",
                font=dict(size=18, color=title_color),
                x=0.5,
                xanchor='center'
            ),
            scene=dict(
                bgcolor=bg_color,
                xaxis=dict(
                    title=dict(text="Baseline BMI Space", font=dict(color=title_color)),
                    backgroundcolor="rgba(0,0,0,0)",
                    gridcolor=grid_color
                ),
                yaxis=dict(
                    title=dict(text="Follow-up BMI Space", font=dict(color=title_color)),
                    backgroundcolor="rgba(0,0,0,0)",
                    gridcolor=grid_color
                ),
                zaxis=dict(
                    title=dict(text="Weight Change Dimension", font=dict(color=title_color)),
                    backgroundcolor="rgba(0,0,0,0)",
                    gridcolor=grid_color
                ),
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.3))
            ),
            paper_bgcolor=bg_color,
            font=dict(color=title_color),
            showlegend=True,
            legend=dict(
                bgcolor="rgba(0,0,0,0.7)",
                bordercolor=title_color,
                borderwidth=1,
                font=dict(color=title_color),
                title=dict(text="<b>Treatment Outcomes</b>")
            )
        )
        
        chart_height = 900 if st.session_state.ar_fullscreen else 650
        st.plotly_chart(fig, width="stretch", height=chart_height)
        
        # Enhanced statistics panel
        st.markdown('<h4 style="color: white; margin-top: 20px;">⭐ Constellation Statistics</h4>', unsafe_allow_html=True)
        
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            success_count = len(constellation_data[constellation_data['outcome'] == 'Significant Weight Loss'])
            success_pct = (success_count / len(constellation_data) * 100) if len(constellation_data) > 0 else 0
            st.metric(
                "Success Stars ⭐",
                success_count,
                delta=f"{success_pct:.1f}% of constellation"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with stat_col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            avg_weight_change = constellation_data['weight_change_kg'].mean()
            st.metric(
                "Avg Weight Change",
                f"{avg_weight_change:.1f} kg",
                delta="Constellation average"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with stat_col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            mounjaro_count = len(constellation_data[constellation_data['intervention'] == 'Mounjaro'])
            mounjaro_pct = (mounjaro_count / len(constellation_data) * 100) if len(constellation_data) > 0 else 0
            st.metric(
                "Mounjaro Stars",
                mounjaro_count,
                delta=f"{mounjaro_pct:.1f}% of sample"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with stat_col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            countries = constellation_data['country'].nunique()
            st.metric(
                "Countries",
                countries,
                delta=f"Geographic spread"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Outcome distribution
        st.markdown('<p style="color: white; font-weight: bold; font-size: 16px; margin-top: 15px;">Outcome Distribution:</p>', unsafe_allow_html=True)
        outcome_dist = constellation_data['outcome'].value_counts()
        outcome_dist_df = pd.DataFrame({
            'Outcome': outcome_dist.index,
            'Star Count': outcome_dist.values,
            'Percentage': (outcome_dist.values / len(constellation_data) * 100).round(1)
        })
        
        st.dataframe(
            outcome_dist_df.style.format({
                'Star Count': '{:.0f}',
                'Percentage': '{:.1f}%'
            }),
            width="stretch",
            height=150
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # AR Control Panel
    st.markdown('<h3 class="section-header">AR Control Panel</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<p style="color: #000000; font-weight: bold; font-size: 16px;">🎮 Interaction Mode</p>', unsafe_allow_html=True)
        interaction_mode = st.radio(
            "Choose interaction:",
            ["Observe", "Explore", "Analyze"],
            key="ar_interaction"
        )
    
    with col2:
        st.markdown('<p style="color: #000000; font-weight: bold; font-size: 16px;">🎨 Visual Style</p>', unsafe_allow_html=True)
        visual_style = st.selectbox(
            "AR Theme:",
            ["Futuristic", "Medical", "Minimal", "Cosmic"]
        )
    
    with col3:
        st.markdown('<p style="color: #000000; font-weight: bold; font-size: 16px;">📡 Data Filters</p>', unsafe_allow_html=True)
        country_filter = st.multiselect(
            "Countries:",
            analyzer.df['country'].unique(),
            default=analyzer.df['country'].unique()[:3]
        )
    
    with col4:
        st.markdown('<p style="color: #000000; font-weight: bold; font-size: 16px;">💡 Insights Panel</p>', unsafe_allow_html=True)
        if st.button("Generate AR Insights", key="ar_insights"):
            insights = analyzer.generate_insights()
            insight_text = insights[0] if insights else 'Data patterns detected!'
            st.markdown(f'''
            <div style="
                background: #d4edda; 
                color: #000000; 
                padding: 1rem; 
                border-radius: 6px; 
                border-left: 4px solid #28a745;
                margin-top: 10px;
            ">
                🔍 <strong style="color: #000000;">AR Analysis:</strong> {insight_text}
            </div>
            ''', unsafe_allow_html=True)
    
    # Close the AR viewer container
    if st.session_state.ar_fullscreen:
        st.markdown('</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Add JavaScript for full screen functionality
    st.markdown('''
    <script>
    function exitFullscreen() {
        // This would typically communicate back to Streamlit to update session state
        alert("Press ESC or use the toggle button to exit full screen mode");
    }
    
    // Listen for ESC key to exit full screen
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            exitFullscreen();
        }
    });
    
    // Improve keyboard navigation
    document.addEventListener('DOMContentLoaded', function() {
        const selectboxes = document.querySelectorAll('.stSelectbox');
        selectboxes.forEach(function(selectbox) {
            selectbox.setAttribute('tabindex', '0');
        });
    });
    </script>
    ''', unsafe_allow_html=True)
    
    # Accessibility notes
    if st.session_state.ar_reduced_motion:
        st.markdown('<div class="info-box">🔧 <strong>Reduced Motion Active:</strong> AR animations are simplified for better accessibility</div>', unsafe_allow_html=True)
    
    if st.session_state.ar_high_contrast:
        st.markdown('<div class="success-box">🎨 <strong>High Contrast Mode:</strong> Enhanced visibility colors are active</div>', unsafe_allow_html=True)
    
    # Screen reader description
    st.markdown('''
    <div class="info-box" role="region" aria-label="AR Viewer Description">
    <strong>Accessibility Information:</strong> This AR viewer displays interactive 3D visualizations of the Mounjaro study data. 
    Key metrics include treatment effectiveness rates, patient demographics, and outcome patterns. 
    Use the control panels above to adjust visualization parameters, enable accessibility features, and access data insights.
    Navigation: Use Tab to move between controls, Space/Enter to activate buttons, and arrow keys in dropdowns.
    </div>
    ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
