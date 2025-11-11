"""
Data Analyzer Module for Mounjaro Study Analysis

This module provides comprehensive data analysis capabilities for the RWE Mounjaro Study dataset.
It includes statistical analysis, data preprocessing, and insights generation functions.
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

class DataAnalyzer:
    """Comprehensive data analysis class for RWE Mounjaro Study data."""
    
    def __init__(self, csv_path):
        """Initialize the analyzer with the dataset."""
        self.csv_path = csv_path
        self.df = None
        self.load_data()
        self.preprocess_data()
    
    def load_data(self):
        """Load and perform initial data validation."""
        try:
            self.df = pd.read_csv(self.csv_path)
            print(f"Data loaded successfully. Shape: {self.df.shape}")
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def preprocess_data(self):
        """Preprocess the data for analysis."""
        if self.df is None:
            return
        
        # Convert date columns to datetime
        date_columns = ['diagnosis_date', 'start_date', 'end_date']
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col])
        
        # Calculate treatment duration in days
        self.df['treatment_duration_days'] = (self.df['end_date'] - self.df['start_date']).dt.days
        
        # Calculate BMI change
        self.df['bmi_change'] = self.df['followup_bmi'] - self.df['baseline_bmi']
        
        # Calculate percentage weight change
        self.df['weight_change_percentage'] = (self.df['weight_change_kg'] / 
                                             (self.df['weight_change_kg'] + 80)) * 100  # Assuming average baseline weight
        
        # Clean comorbidities - split and count
        self.df['comorbidity_count'] = self.df['comorbidities'].apply(
            lambda x: 0 if pd.isna(x) or x == 'None' else len([c.strip() for c in str(x).split(';') if c.strip() != 'None'])
        )
        
        # Create binary outcome variables
        self.df['significant_weight_loss'] = (self.df['outcome'] == 'Significant Weight Loss').astype(int)
        self.df['moderate_weight_loss'] = (self.df['outcome'] == 'Moderate Weight Loss').astype(int)
        self.df['any_weight_loss'] = self.df['outcome'].isin(['Significant Weight Loss', 'Moderate Weight Loss']).astype(int)
        
        # Create age groups
        self.df['age_group'] = pd.cut(self.df['age'], 
                                    bins=[0, 30, 40, 50, 60, 100], 
                                    labels=['<30', '30-39', '40-49', '50-59', '60+'])
        
        # Create BMI categories
        self.df['baseline_bmi_category'] = pd.cut(self.df['baseline_bmi'],
                                                bins=[0, 25, 30, 35, 100],
                                                labels=['Normal/Overweight', 'Obese I', 'Obese II', 'Obese III'])
    
    def get_basic_statistics(self):
        """Generate comprehensive basic statistics."""
        stats_dict = {
            'dataset_overview': {
                'total_patients': len(self.df),
                'unique_countries': self.df['country'].nunique(),
                'countries': list(self.df['country'].unique()),
                'intervention_types': list(self.df['intervention'].unique()),
                'date_range': {
                    'start': self.df['start_date'].min().strftime('%Y-%m-%d'),
                    'end': self.df['end_date'].max().strftime('%Y-%m-%d')
                }
            },
            'demographics': {
                'age_stats': {
                    'mean': round(self.df['age'].mean(), 1),
                    'median': self.df['age'].median(),
                    'std': round(self.df['age'].std(), 1),
                    'min': self.df['age'].min(),
                    'max': self.df['age'].max()
                },
                'gender_distribution': self.df['sex'].value_counts().to_dict(),
                'country_distribution': self.df['country'].value_counts().to_dict(),
                'age_group_distribution': self.df['age_group'].value_counts().to_dict()
            },
            'clinical_measures': {
                'baseline_bmi': {
                    'mean': round(self.df['baseline_bmi'].mean(), 1),
                    'median': round(self.df['baseline_bmi'].median(), 1),
                    'std': round(self.df['baseline_bmi'].std(), 1)
                },
                'followup_bmi': {
                    'mean': round(self.df['followup_bmi'].mean(), 1),
                    'median': round(self.df['followup_bmi'].median(), 1),
                    'std': round(self.df['followup_bmi'].std(), 1)
                },
                'weight_change': {
                    'mean': round(self.df['weight_change_kg'].mean(), 1),
                    'median': round(self.df['weight_change_kg'].median(), 1),
                    'std': round(self.df['weight_change_kg'].std(), 1)
                },
                'adherence_rate': {
                    'mean': round(self.df['adherence_rate'].mean(), 2),
                    'median': round(self.df['adherence_rate'].median(), 2),
                    'std': round(self.df['adherence_rate'].std(), 2)
                }
            },
            'outcomes': {
                'outcome_distribution': self.df['outcome'].value_counts().to_dict(),
                'intervention_distribution': self.df['intervention'].value_counts().to_dict(),
                'adverse_events': {
                    'total_with_ae': len(self.df[self.df['adverse_event'] != 'None']),
                    'ae_types': self.df[self.df['adverse_event'] != 'None']['adverse_event'].value_counts().to_dict()
                },
                'hospitalizations': {
                    'mean': round(self.df['hospitalizations'].mean(), 1),
                    'distribution': self.df['hospitalizations'].value_counts().to_dict()
                }
            }
        }
        return stats_dict
    
    def analyze_treatment_effectiveness(self):
        """Analyze treatment effectiveness by intervention type."""
        effectiveness = {}
        
        for intervention in self.df['intervention'].unique():
            subset = self.df[self.df['intervention'] == intervention]
            
            effectiveness[intervention] = {
                'n_patients': len(subset),
                'mean_weight_loss': round(subset['weight_change_kg'].mean(), 2),
                'mean_bmi_change': round(subset['bmi_change'].mean(), 2),
                'significant_weight_loss_rate': round(
                    (subset['outcome'] == 'Significant Weight Loss').mean() * 100, 1
                ),
                'any_weight_loss_rate': round(subset['any_weight_loss'].mean() * 100, 1),
                'mean_adherence': round(subset['adherence_rate'].mean(), 2),
                'adverse_event_rate': round(
                    (subset['adverse_event'] != 'None').mean() * 100, 1
                ),
                'hospitalization_rate': round(
                    (subset['hospitalizations'] > 0).mean() * 100, 1
                )
            }
        
        return effectiveness
    
    def analyze_by_demographics(self):
        """Analyze outcomes by demographic factors."""
        demographics_analysis = {}
        
        # By country
        demographics_analysis['by_country'] = {}
        for country in self.df['country'].unique():
            subset = self.df[self.df['country'] == country]
            demographics_analysis['by_country'][country] = {
                'n_patients': len(subset),
                'mean_weight_loss': round(subset['weight_change_kg'].mean(), 2),
                'success_rate': round(subset['any_weight_loss'].mean() * 100, 1),
                'mounjaro_usage': round((subset['intervention'] == 'Mounjaro').mean() * 100, 1)
            }
        
        # By age group
        demographics_analysis['by_age_group'] = {}
        for age_group in self.df['age_group'].unique():
            if pd.notna(age_group):
                subset = self.df[self.df['age_group'] == age_group]
                demographics_analysis['by_age_group'][str(age_group)] = {
                    'n_patients': len(subset),
                    'mean_weight_loss': round(subset['weight_change_kg'].mean(), 2),
                    'success_rate': round(subset['any_weight_loss'].mean() * 100, 1),
                    'mean_adherence': round(subset['adherence_rate'].mean(), 2)
                }
        
        # By gender
        demographics_analysis['by_gender'] = {}
        for gender in self.df['sex'].unique():
            subset = self.df[self.df['sex'] == gender]
            demographics_analysis['by_gender'][gender] = {
                'n_patients': len(subset),
                'mean_weight_loss': round(subset['weight_change_kg'].mean(), 2),
                'success_rate': round(subset['any_weight_loss'].mean() * 100, 1),
                'mean_baseline_bmi': round(subset['baseline_bmi'].mean(), 1)
            }
        
        return demographics_analysis
    
    def analyze_comorbidities_impact(self):
        """Analyze impact of comorbidities on outcomes."""
        comorbidity_analysis = {}
        
        # Overall impact of comorbidity count
        comorbidity_analysis['by_count'] = {}
        for count in sorted(self.df['comorbidity_count'].unique()):
            subset = self.df[self.df['comorbidity_count'] == count]
            comorbidity_analysis['by_count'][f'{count}_comorbidities'] = {
                'n_patients': len(subset),
                'mean_weight_loss': round(subset['weight_change_kg'].mean(), 2),
                'success_rate': round(subset['any_weight_loss'].mean() * 100, 1),
                'mean_adherence': round(subset['adherence_rate'].mean(), 2)
            }
        
        # Specific comorbidities analysis
        common_comorbidities = [
            'Type 2 Diabetes', 'Hypertension', 'Sleep Apnea', 
            'Cardiac Disease', 'High Cholesterol', 'Obesity', 'PCOS'
        ]
        
        comorbidity_analysis['by_type'] = {}
        for comorbidity in common_comorbidities:
            has_condition = self.df['comorbidities'].str.contains(comorbidity, na=False)
            subset_with = self.df[has_condition]
            subset_without = self.df[~has_condition]
            
            if len(subset_with) > 0 and len(subset_without) > 0:
                comorbidity_analysis['by_type'][comorbidity] = {
                    'with_condition': {
                        'n_patients': len(subset_with),
                        'mean_weight_loss': round(subset_with['weight_change_kg'].mean(), 2),
                        'success_rate': round(subset_with['any_weight_loss'].mean() * 100, 1)
                    },
                    'without_condition': {
                        'n_patients': len(subset_without),
                        'mean_weight_loss': round(subset_without['weight_change_kg'].mean(), 2),
                        'success_rate': round(subset_without['any_weight_loss'].mean() * 100, 1)
                    }
                }
        
        return comorbidity_analysis
    
    def statistical_tests(self):
        """Perform statistical tests for key comparisons."""
        tests = {}
        
        # Compare Mounjaro vs LifestyleOnly
        mounjaro_group = self.df[self.df['intervention'] == 'Mounjaro']['weight_change_kg']
        lifestyle_group = self.df[self.df['intervention'] == 'LifestyleOnly']['weight_change_kg']
        
        t_stat, p_value = stats.ttest_ind(mounjaro_group, lifestyle_group)
        tests['mounjaro_vs_lifestyle'] = {
            'test_type': 'Independent t-test',
            't_statistic': round(t_stat, 3),
            'p_value': round(p_value, 6),
            'significant': p_value < 0.05,
            'interpretation': 'Mounjaro shows significantly different weight loss compared to lifestyle intervention' if p_value < 0.05 else 'No significant difference between interventions'
        }
        
        # Correlation between adherence and weight loss
        correlation_coef, correlation_p = stats.pearsonr(
            self.df['adherence_rate'], 
            self.df['weight_change_kg']
        )
        tests['adherence_weight_correlation'] = {
            'test_type': 'Pearson correlation',
            'correlation_coefficient': round(correlation_coef, 3),
            'p_value': round(correlation_p, 6),
            'significant': correlation_p < 0.05,
            'interpretation': f'{"Strong" if abs(correlation_coef) > 0.7 else "Moderate" if abs(correlation_coef) > 0.3 else "Weak"} correlation between adherence and weight loss'
        }
        
        # ANOVA for outcomes across countries
        country_groups = [self.df[self.df['country'] == country]['weight_change_kg'] 
                         for country in self.df['country'].unique()]
        f_stat, anova_p = stats.f_oneway(*country_groups)
        tests['country_weight_loss_anova'] = {
            'test_type': 'One-way ANOVA',
            'f_statistic': round(f_stat, 3),
            'p_value': round(anova_p, 6),
            'significant': anova_p < 0.05,
            'interpretation': 'Significant differences in weight loss across countries' if anova_p < 0.05 else 'No significant differences across countries'
        }
        
        return tests
    
    def patient_clustering(self, n_clusters=4):
        """Perform patient clustering based on characteristics."""
        # Prepare features for clustering
        features_for_clustering = [
            'age', 'baseline_bmi', 'adherence_rate', 
            'comorbidity_count', 'treatment_duration_days'
        ]
        
        # Create feature matrix
        X = self.df[features_for_clustering].fillna(0)
        
        # Perform clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.df['cluster'] = kmeans.fit_predict(X)
        
        # Analyze clusters
        cluster_analysis = {}
        for cluster in range(n_clusters):
            subset = self.df[self.df['cluster'] == cluster]
            cluster_analysis[f'Cluster_{cluster}'] = {
                'n_patients': len(subset),
                'characteristics': {
                    'mean_age': round(subset['age'].mean(), 1),
                    'mean_baseline_bmi': round(subset['baseline_bmi'].mean(), 1),
                    'mean_adherence': round(subset['adherence_rate'].mean(), 2),
                    'mean_comorbidities': round(subset['comorbidity_count'].mean(), 1)
                },
                'outcomes': {
                    'mean_weight_loss': round(subset['weight_change_kg'].mean(), 2),
                    'success_rate': round(subset['any_weight_loss'].mean() * 100, 1),
                    'mounjaro_usage': round((subset['intervention'] == 'Mounjaro').mean() * 100, 1)
                }
            }
        
        return cluster_analysis
    
    def generate_insights(self):
        """Generate key insights from the data."""
        insights = []
        
        # Treatment effectiveness insights
        effectiveness = self.analyze_treatment_effectiveness()
        mounjaro_success = effectiveness.get('Mounjaro', {}).get('significant_weight_loss_rate', 0)
        lifestyle_success = effectiveness.get('LifestyleOnly', {}).get('significant_weight_loss_rate', 0)
        
        if mounjaro_success > lifestyle_success:
            insights.append(f"Mounjaro shows {mounjaro_success - lifestyle_success:.1f}% higher significant weight loss rate compared to lifestyle intervention alone.")
        
        # Adherence insights
        high_adherence = self.df[self.df['adherence_rate'] > 0.8]
        low_adherence = self.df[self.df['adherence_rate'] <= 0.8]
        
        if len(high_adherence) > 0 and len(low_adherence) > 0:
            high_success = high_adherence['any_weight_loss'].mean() * 100
            low_success = low_adherence['any_weight_loss'].mean() * 100
            insights.append(f"Patients with high adherence (>80%) show {high_success - low_success:.1f}% higher success rate.")
        
        # Age-related insights
        demographics = self.analyze_by_demographics()
        age_groups = demographics.get('by_age_group', {})
        if age_groups:
            best_age_group = max(age_groups.items(), key=lambda x: x[1]['success_rate'])
            insights.append(f"Age group {best_age_group[0]} shows the highest success rate at {best_age_group[1]['success_rate']}%.")
        
        # Comorbidity insights
        comorbidity_analysis = self.analyze_comorbidities_impact()
        count_analysis = comorbidity_analysis.get('by_count', {})
        if len(count_analysis) > 1:
            no_comorbid = count_analysis.get('0_comorbidities', {})
            multiple_comorbid = count_analysis.get('2_comorbidities', {}) or count_analysis.get('3_comorbidities', {})
            if no_comorbid and multiple_comorbid:
                diff = no_comorbid['success_rate'] - multiple_comorbid['success_rate']
                insights.append(f"Patients with no comorbidities have {diff:.1f}% higher success rate than those with multiple conditions.")
        
        # Country insights
        country_analysis = demographics.get('by_country', {})
        if country_analysis:
            best_country = max(country_analysis.items(), key=lambda x: x[1]['success_rate'])
            insights.append(f"{best_country[0]} shows the highest treatment success rate at {best_country[1]['success_rate']}%.")
        
        # Safety insights
        total_patients = len(self.df)
        ae_patients = len(self.df[self.df['adverse_event'] != 'None'])
        ae_rate = (ae_patients / total_patients) * 100
        insights.append(f"Overall adverse event rate is {ae_rate:.1f}% ({ae_patients} out of {total_patients} patients).")
        
        return insights

    def get_data_summary(self):
        """Get a comprehensive summary of the dataset for the chatbot."""
        summary = {
            'basic_stats': self.get_basic_statistics(),
            'treatment_effectiveness': self.analyze_treatment_effectiveness(),
            'demographics_analysis': self.analyze_by_demographics(),
            'comorbidities_analysis': self.analyze_comorbidities_impact(),
            'statistical_tests': self.statistical_tests(),
            'insights': self.generate_insights()
        }
        return summary