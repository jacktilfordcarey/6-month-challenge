"""
Visualization Module for Mounjaro Study Analysis

This module creates interactive visualizations using Plotly for the RWE Mounjaro Study dataset.
It provides comprehensive charts and graphs for data exploration and insights.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class DataVisualizer:
    """Interactive visualization class for RWE Mounjaro Study data."""
    
    def __init__(self, analyzer):
        """Initialize with a DataAnalyzer instance."""
        self.analyzer = analyzer
        self.df = analyzer.df
        
    def create_overview_dashboard(self):
        """Create an overview dashboard with key metrics."""
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['Intervention Distribution', 'Outcome Distribution', 
                           'Weight Loss by Intervention', 'Age Distribution'],
            specs=[[{"type": "pie"}, {"type": "pie"}],
                   [{"type": "box"}, {"type": "histogram"}]]
        )
        
        # Intervention distribution (pie chart)
        intervention_counts = self.df['intervention'].value_counts()
        fig.add_trace(
            go.Pie(labels=intervention_counts.index, values=intervention_counts.values,
                   name="Intervention"),
            row=1, col=1
        )
        
        # Outcome distribution (pie chart)
        outcome_counts = self.df['outcome'].value_counts()
        fig.add_trace(
            go.Pie(labels=outcome_counts.index, values=outcome_counts.values,
                   name="Outcome"),
            row=1, col=2
        )
        
        # Weight loss by intervention (box plot)
        for intervention in self.df['intervention'].unique():
            data = self.df[self.df['intervention'] == intervention]['weight_change_kg']
            fig.add_trace(
                go.Box(y=data, name=intervention, showlegend=False),
                row=2, col=1
            )
        
        # Age distribution (histogram)
        fig.add_trace(
            go.Histogram(x=self.df['age'], nbinsx=20, name="Age", showlegend=False),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="Dataset Overview Dashboard",
            showlegend=True,
            height=800
        )
        
        return fig
    
    def create_weight_loss_analysis(self):
        """Create comprehensive weight loss analysis visualizations."""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['Weight Loss Distribution', 'BMI Change by Intervention',
                           'Weight Loss vs Adherence', 'Success Rate by Country'],
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Weight loss distribution
        fig.add_trace(
            go.Histogram(x=self.df['weight_change_kg'], 
                        nbinsx=30, 
                        name="Weight Loss Distribution",
                        showlegend=False),
            row=1, col=1
        )
        
        # BMI change by intervention
        for intervention in self.df['intervention'].unique():
            data = self.df[self.df['intervention'] == intervention]
            fig.add_trace(
                go.Scatter(x=data['baseline_bmi'], 
                          y=data['bmi_change'],
                          mode='markers',
                          name=f"{intervention}",
                          opacity=0.7),
                row=1, col=2
            )
        
        # Weight loss vs adherence
        fig.add_trace(
            go.Scatter(x=self.df['adherence_rate'], 
                      y=self.df['weight_change_kg'],
                      mode='markers',
                      name="Adherence vs Weight Loss",
                      marker=dict(color=self.df['weight_change_kg'], 
                                colorscale='RdYlBu'),
                      showlegend=False),
            row=2, col=1
        )
        
        # Success rate by country
        country_success = self.df.groupby('country')['any_weight_loss'].mean().reset_index()
        country_success['success_rate'] = country_success['any_weight_loss'] * 100
        
        fig.add_trace(
            go.Bar(x=country_success['country'], 
                   y=country_success['success_rate'],
                   name="Success Rate by Country",
                   showlegend=False),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="Weight Loss Analysis",
            height=800
        )
        
        return fig
    
    def create_intervention_comparison(self):
        """Create detailed intervention comparison charts."""
        effectiveness = self.analyzer.analyze_treatment_effectiveness()
        
        # Prepare data for comparison
        interventions = list(effectiveness.keys())
        metrics = ['mean_weight_loss', 'significant_weight_loss_rate', 
                  'mean_adherence', 'adverse_event_rate']
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['Mean Weight Loss (kg)', 'Significant Weight Loss Rate (%)',
                           'Mean Adherence Rate', 'Adverse Event Rate (%)'],
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
        
        # Mean weight loss
        values = [effectiveness[i]['mean_weight_loss'] for i in interventions]
        fig.add_trace(
            go.Bar(x=interventions, y=values, name="Weight Loss",
                   marker_color=colors[0], showlegend=False),
            row=1, col=1
        )
        
        # Significant weight loss rate
        values = [effectiveness[i]['significant_weight_loss_rate'] for i in interventions]
        fig.add_trace(
            go.Bar(x=interventions, y=values, name="Success Rate",
                   marker_color=colors[1], showlegend=False),
            row=1, col=2
        )
        
        # Mean adherence
        values = [effectiveness[i]['mean_adherence'] for i in interventions]
        fig.add_trace(
            go.Bar(x=interventions, y=values, name="Adherence",
                   marker_color=colors[2], showlegend=False),
            row=2, col=1
        )
        
        # Adverse event rate
        values = [effectiveness[i]['adverse_event_rate'] for i in interventions]
        fig.add_trace(
            go.Bar(x=interventions, y=values, name="Adverse Events",
                   marker_color='#d62728', showlegend=False),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="Intervention Effectiveness Comparison",
            height=600
        )
        
        return fig
    
    def create_demographic_analysis(self):
        """Create demographic analysis visualizations."""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['Success Rate by Age Group', 'Weight Loss by Gender',
                           'BMI Categories Distribution', 'Treatment Duration Analysis'],
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Success rate by age group
        age_success = self.df.groupby('age_group')['any_weight_loss'].mean().reset_index()
        age_success['success_rate'] = age_success['any_weight_loss'] * 100
        age_success = age_success.dropna()
        
        fig.add_trace(
            go.Bar(x=age_success['age_group'].astype(str), 
                   y=age_success['success_rate'],
                   name="Success Rate by Age",
                   showlegend=False),
            row=1, col=1
        )
        
        # Weight loss by gender
        for gender in self.df['sex'].unique():
            data = self.df[self.df['sex'] == gender]['weight_change_kg']
            fig.add_trace(
                go.Box(y=data, name=f"Gender {gender}"),
                row=1, col=2
            )
        
        # BMI categories distribution
        bmi_counts = self.df['baseline_bmi_category'].value_counts()
        fig.add_trace(
            go.Bar(x=bmi_counts.index.astype(str), 
                   y=bmi_counts.values,
                   name="BMI Categories",
                   showlegend=False),
            row=2, col=1
        )
        
        # Treatment duration analysis
        fig.add_trace(
            go.Histogram(x=self.df['treatment_duration_days'], 
                        nbinsx=20,
                        name="Treatment Duration",
                        showlegend=False),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="Demographic Analysis",
            height=800
        )
        
        return fig
    
    def create_correlation_heatmap(self):
        """Create correlation heatmap of numerical variables."""
        # Select numerical columns
        numerical_cols = ['age', 'baseline_bmi', 'followup_bmi', 'weight_change_kg',
                         'adherence_rate', 'hospitalizations', 'comorbidity_count',
                         'treatment_duration_days', 'bmi_change']
        
        corr_matrix = self.df[numerical_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=np.round(corr_matrix.values, 2),
            texttemplate="%{text}",
            textfont={"size": 10},
        ))
        
        fig.update_layout(
            title="Correlation Heatmap of Key Variables",
            width=800,
            height=600
        )
        
        return fig
    
    def create_time_series_analysis(self):
        """Create time series analysis of study enrollment and outcomes."""
        # Treatment start dates over time
        monthly_starts = self.df.groupby([
            self.df['start_date'].dt.to_period('M'),
            'intervention'
        ]).size().reset_index(name='count')
        monthly_starts['start_date'] = monthly_starts['start_date'].astype(str)
        
        fig = px.line(monthly_starts, 
                     x='start_date', 
                     y='count',
                     color='intervention',
                     title='Patient Enrollment Over Time',
                     labels={'start_date': 'Month', 'count': 'Number of Patients'})
        
        fig.update_layout(height=500)
        
        return fig
    
    def create_adverse_events_analysis(self):
        """Create adverse events analysis visualization."""
        # Filter out 'None' adverse events
        ae_df = self.df[self.df['adverse_event'] != 'None'].copy()
        
        if len(ae_df) == 0:
            # Create empty figure if no adverse events
            fig = go.Figure()
            fig.add_annotation(
                text="No adverse events recorded in the dataset",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=['Adverse Events by Type', 'AE Rate by Intervention'],
            specs=[[{"type": "pie"}, {"type": "bar"}]]
        )
        
        # AE types distribution
        ae_counts = ae_df['adverse_event'].value_counts()
        fig.add_trace(
            go.Pie(labels=ae_counts.index, values=ae_counts.values,
                   name="AE Types"),
            row=1, col=1
        )
        
        # AE rate by intervention
        ae_by_intervention = self.df.groupby('intervention').apply(
            lambda x: (x['adverse_event'] != 'None').mean() * 100
        ).reset_index(name='ae_rate')
        
        fig.add_trace(
            go.Bar(x=ae_by_intervention['intervention'], 
                   y=ae_by_intervention['ae_rate'],
                   name="AE Rate",
                   showlegend=False),
            row=1, col=2
        )
        
        fig.update_layout(
            title_text="Adverse Events Analysis",
            height=500
        )
        
        return fig
    
    def create_comorbidities_analysis(self):
        """Create comorbidities analysis visualization."""
        # Count individual comorbidities
        all_comorbidities = []
        for comorbidities in self.df['comorbidities'].dropna():
            if comorbidities != 'None':
                comorbids = [c.strip() for c in str(comorbidities).split(';') 
                           if c.strip() != 'None']
                all_comorbidities.extend(comorbids)
        
        comorbidity_counts = pd.Series(all_comorbidities).value_counts().head(10)
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=['Most Common Comorbidities', 'Comorbidity Count Distribution']
        )
        
        # Most common comorbidities
        fig.add_trace(
            go.Bar(x=comorbidity_counts.values, 
                   y=comorbidity_counts.index,
                   orientation='h',
                   name="Comorbidity Frequency",
                   showlegend=False),
            row=1, col=1
        )
        
        # Comorbidity count distribution
        comorbidity_count_dist = self.df['comorbidity_count'].value_counts().sort_index()
        fig.add_trace(
            go.Bar(x=comorbidity_count_dist.index, 
                   y=comorbidity_count_dist.values,
                   name="Count Distribution",
                   showlegend=False),
            row=1, col=2
        )
        
        fig.update_layout(
            title_text="Comorbidities Analysis",
            height=500
        )
        
        return fig
    
    def create_country_comparison(self):
        """Create detailed country comparison analysis."""
        country_analysis = self.analyzer.analyze_by_demographics()['by_country']
        
        countries = list(country_analysis.keys())
        metrics_data = {
            'Success Rate (%)': [country_analysis[c]['success_rate'] for c in countries],
            'Mean Weight Loss (kg)': [country_analysis[c]['mean_weight_loss'] for c in countries],
            'Mounjaro Usage (%)': [country_analysis[c]['mounjaro_usage'] for c in countries]
        }
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['Success Rate by Country', 'Mean Weight Loss by Country',
                           'Mounjaro Usage by Country', 'Patient Distribution'],
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"type": "pie"}]]
        )
        
        # Success rate by country
        fig.add_trace(
            go.Bar(x=countries, 
                   y=metrics_data['Success Rate (%)'],
                   name="Success Rate",
                   marker_color='lightblue',
                   showlegend=False),
            row=1, col=1
        )
        
        # Mean weight loss by country
        fig.add_trace(
            go.Bar(x=countries, 
                   y=metrics_data['Mean Weight Loss (kg)'],
                   name="Weight Loss",
                   marker_color='lightgreen',
                   showlegend=False),
            row=1, col=2
        )
        
        # Mounjaro usage by country
        fig.add_trace(
            go.Bar(x=countries, 
                   y=metrics_data['Mounjaro Usage (%)'],
                   name="Mounjaro Usage",
                   marker_color='orange',
                   showlegend=False),
            row=2, col=1
        )
        
        # Patient distribution pie chart
        country_counts = self.df['country'].value_counts()
        fig.add_trace(
            go.Pie(labels=country_counts.index, 
                   values=country_counts.values,
                   name="Patient Distribution"),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="Country Comparison Analysis",
            height=800
        )
        
        return fig
    
    def create_patient_journey_analysis(self):
        """Create patient journey analysis showing BMI progression."""
        # Sample of patients for journey visualization
        sample_patients = self.df.sample(min(50, len(self.df)), random_state=42)
        
        fig = go.Figure()
        
        # Add baseline to follow-up BMI lines
        for idx, row in sample_patients.iterrows():
            color = 'green' if row['weight_change_kg'] < -5 else 'red' if row['weight_change_kg'] > 0 else 'orange'
            fig.add_trace(
                go.Scatter(
                    x=['Baseline', 'Follow-up'],
                    y=[row['baseline_bmi'], row['followup_bmi']],
                    mode='lines+markers',
                    line=dict(color=color, width=1),
                    opacity=0.6,
                    showlegend=False,
                    hovertemplate=f"Patient {row['patient_id']}<br>" +
                                 f"Weight Change: {row['weight_change_kg']:.1f} kg<br>" +
                                 f"Intervention: {row['intervention']}<extra></extra>"
                )
            )
        
        # Add average lines
        avg_baseline = self.df['baseline_bmi'].mean()
        avg_followup = self.df['followup_bmi'].mean()
        
        fig.add_trace(
            go.Scatter(
                x=['Baseline', 'Follow-up'],
                y=[avg_baseline, avg_followup],
                mode='lines+markers',
                line=dict(color='black', width=4),
                name='Average BMI',
                marker=dict(size=10)
            )
        )
        
        fig.update_layout(
            title="Patient BMI Journey (Sample of 50 Patients)",
            xaxis_title="Time Point",
            yaxis_title="BMI",
            height=600
        )
        
        return fig