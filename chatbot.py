"""
Gemini AI Chatbot Module for Mounjaro Study Analysis

This module implements a chatbot using Google's Gemini AI that can answer questions
about the RWE Mounjaro Study dataset with context-aware responses.
"""

import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

class GeminiChatbot:
    """AI Chatbot powered by Google Gemini for dataset Q&A."""
    
    def __init__(self, analyzer, api_key=None):
        """Initialize the chatbot with data analyzer and API key."""
        self.analyzer = analyzer
        self.data_summary = analyzer.get_data_summary()
        
        # Load environment variables
        load_dotenv()
        
        # Configure Gemini API
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyBJw42dilm_BS3GchYrKRX5txSVO3AwgHA')
        
        genai.configure(api_key=self.api_key)
        
        # Try different model names in order of preference (updated based on available models)
        model_names = [
            'models/gemini-2.5-flash',
            'models/gemini-2.0-flash',
            'models/gemini-flash-latest',
            'models/gemini-2.5-flash-lite',
            'models/gemini-2.0-flash-lite',
            'models/gemini-2.5-pro',
            'models/gemini-2.0-pro-exp',
            'models/gemini-pro-latest'
        ]
        self.model = None
        self.model_name = None
        
        for model_name in model_names:
            try:
                self.model = genai.GenerativeModel(model_name)
                # Test the model with a simple request (skip if quota exceeded)
                try:
                    test_response = self.model.generate_content("Hello")
                    print(f"Successfully initialized and tested model: {model_name}")
                    self.model_name = model_name
                    break
                except Exception as test_e:
                    if "429" in str(test_e) or "quota" in str(test_e).lower():
                        print(f"Model {model_name} available but quota exceeded - will use for interface")
                        self.model_name = model_name
                        break
                    else:
                        print(f"Model {model_name} test failed: {str(test_e)}")
                        continue
            except Exception as e:
                print(f"Model {model_name} not available: {str(e)}")
                continue
        
        if self.model is None:
            # Try to list available models for debugging
            try:
                available_models = self.list_available_models()
                print(f"Available models: {available_models}")
                raise Exception(f"No available Gemini models found. Available models: {available_models}. Please check your API key.")
            except:
                raise Exception("No available Gemini models found. Please check your API key and internet connection.")
        
        # Initialize conversation context
        self.context = self._build_context()
        self.conversation_history = []
    
    def _build_context(self):
        """Build comprehensive context from the dataset."""
        context = f"""
You are an AI assistant specialized in analyzing the RWE (Real World Evidence) Mounjaro Study dataset. 
This dataset contains information about {self.data_summary['basic_stats']['dataset_overview']['total_patients']} patients 
from a clinical study examining the effectiveness of Mounjaro (tirzepatide) compared to lifestyle interventions 
for weight management.

DATASET OVERVIEW:
- Total Patients: {self.data_summary['basic_stats']['dataset_overview']['total_patients']}
- Countries: {', '.join(self.data_summary['basic_stats']['dataset_overview']['countries'])}
- Study Period: {self.data_summary['basic_stats']['dataset_overview']['date_range']['start']} to {self.data_summary['basic_stats']['dataset_overview']['date_range']['end']}
- Interventions: {', '.join(self.data_summary['basic_stats']['dataset_overview']['intervention_types'])}

DEMOGRAPHICS:
- Age Range: {self.data_summary['basic_stats']['demographics']['age_stats']['min']}-{self.data_summary['basic_stats']['demographics']['age_stats']['max']} years (Mean: {self.data_summary['basic_stats']['demographics']['age_stats']['mean']})
- Gender Distribution: {json.dumps(self.data_summary['basic_stats']['demographics']['gender_distribution'])}
- Country Distribution: {json.dumps(self.data_summary['basic_stats']['demographics']['country_distribution'])}

CLINICAL MEASURES:
- Baseline BMI: Mean {self.data_summary['basic_stats']['clinical_measures']['baseline_bmi']['mean']}, Median {self.data_summary['basic_stats']['clinical_measures']['baseline_bmi']['median']}
- Follow-up BMI: Mean {self.data_summary['basic_stats']['clinical_measures']['followup_bmi']['mean']}, Median {self.data_summary['basic_stats']['clinical_measures']['followup_bmi']['median']}
- Weight Change: Mean {self.data_summary['basic_stats']['clinical_measures']['weight_change']['mean']} kg, Median {self.data_summary['basic_stats']['clinical_measures']['weight_change']['median']} kg
- Adherence Rate: Mean {self.data_summary['basic_stats']['clinical_measures']['adherence_rate']['mean']}, Median {self.data_summary['basic_stats']['clinical_measures']['adherence_rate']['median']}

TREATMENT EFFECTIVENESS:
{json.dumps(self.data_summary['treatment_effectiveness'], indent=2)}

OUTCOME DISTRIBUTION:
{json.dumps(self.data_summary['basic_stats']['outcomes']['outcome_distribution'])}

STATISTICAL FINDINGS:
{self._format_statistical_tests()}

KEY INSIGHTS:
{chr(10).join(f"- {insight}" for insight in self.data_summary['insights'])}

ADVERSE EVENTS:
- Total patients with adverse events: {self.data_summary['basic_stats']['outcomes']['adverse_events']['total_with_ae']}
- Adverse event types: {json.dumps(self.data_summary['basic_stats']['outcomes']['adverse_events']['ae_types'])}

HOSPITALIZATIONS:
- Mean hospitalizations per patient: {self.data_summary['basic_stats']['outcomes']['hospitalizations']['mean']}
- Distribution: {json.dumps(self.data_summary['basic_stats']['outcomes']['hospitalizations']['distribution'])}

Please provide accurate, helpful, and context-aware responses about this dataset. When answering:
1. Use specific numbers and statistics from the data
2. Explain clinical significance when relevant
3. Compare interventions when appropriate
4. Mention statistical significance when discussing differences
5. Be conversational but professional
6. If you don't have specific data to answer a question, say so clearly
7. Always ground your answers in the actual data provided

You can discuss:
- Treatment effectiveness and outcomes
- Patient demographics and characteristics
- Safety profiles and adverse events
- Statistical comparisons between groups
- Clinical insights and recommendations
- Data quality and limitations
"""
        return context
    
    def _format_statistical_tests(self):
        """Format statistical tests data for context (avoiding JSON serialization issues)."""
        tests = self.data_summary['statistical_tests']
        formatted = ""
        
        for test_name, results in tests.items():
            formatted += f"\n{test_name.replace('_', ' ').title()}:\n"
            formatted += f"  - Test Type: {results['test_type']}\n"
            
            if 'correlation_coefficient' in results:
                formatted += f"  - Correlation Coefficient: {results['correlation_coefficient']}\n"
            elif 't_statistic' in results:
                formatted += f"  - T-statistic: {results['t_statistic']}\n"
            elif 'f_statistic' in results:
                formatted += f"  - F-statistic: {results['f_statistic']}\n"
            
            formatted += f"  - P-value: {results['p_value']}\n"
            formatted += f"  - Significant: {'Yes' if results['significant'] else 'No'}\n"
            formatted += f"  - Interpretation: {results['interpretation']}\n"
        
        return formatted
    
    def ask(self, question, include_history=True):
        """Ask a question and get an AI-powered response."""
        try:
            # Prepare the prompt with context
            if include_history and self.conversation_history:
                history_text = "\n\nPrevious conversation:\n" + "\n".join(
                    f"Q: {item['question']}\nA: {item['answer'][:200]}..." 
                    for item in self.conversation_history[-3:]  # Last 3 exchanges
                )
            else:
                history_text = ""
            
            full_prompt = f"""
{self.context}

{history_text}

Current question: {question}

Please provide a comprehensive answer based on the dataset information above. 
Use specific statistics and be precise in your response.
"""
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            answer = response.text
            
            # Store in conversation history
            self.conversation_history.append({
                'question': question,
                'answer': answer
            })
            
            # Keep only last 10 exchanges to manage context length
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return answer
            
        except Exception as e:
            error_message = str(e)
            if "429" in error_message or "quota" in error_message.lower():
                return f"I apologize, but you've reached the daily quota limit for the Gemini API. This is common with the free tier.\n\n**What this means:**\n- Free tier has daily limits on requests and tokens\n- Your quota will reset in about 24 hours\n- You can monitor usage at: https://ai.dev/usage?tab=rate-limit\n\n**Solutions:**\n1. Wait for quota reset (recommended)\n2. Upgrade to a paid plan for higher limits\n3. Use fewer/shorter questions to conserve quota\n\n**Error details**: Rate limit exceeded - please retry later."
            elif "404" in error_message or "not found" in error_message:
                return f"I apologize, but the AI model is currently unavailable. This might be due to:\n\n1. **API Key Issues**: Please verify your Gemini API key is valid and active\n2. **Model Availability**: The Gemini model might be temporarily unavailable\n3. **Regional Restrictions**: Some Gemini models may not be available in your region\n\n**Error details**: {error_message}\n\n**Suggestion**: Try refreshing the page or contact support if the issue persists."
            else:
                return f"I encountered an unexpected error: {error_message}. Please try rephrasing your question or refresh the page."
    
    def get_suggested_questions(self):
        """Get a list of suggested questions users can ask."""
        questions = [
            # Treatment Effectiveness
            "How effective is Mounjaro compared to lifestyle intervention?",
            "What percentage of patients achieved significant weight loss?",
            "What is the average weight loss for Mounjaro patients?",
            "Are there statistically significant differences between treatments?",
            
            # Demographics and Subgroups
            "Which age group responds best to treatment?",
            "Do men or women have better outcomes?",
            "How do outcomes vary by country?",
            "What is the effect of baseline BMI on treatment success?",
            
            # Safety and Adherence
            "What are the most common adverse events?",
            "How does adherence affect treatment outcomes?",
            "What is the hospitalization rate for each treatment?",
            "Are there any safety concerns with Mounjaro?",
            
            # Clinical Insights
            "How do comorbidities affect treatment outcomes?",
            "What factors predict successful weight loss?",
            "What is the typical patient profile for best outcomes?",
            "How long did patients stay on treatment?",
            
            # Data Analysis
            "What are the key findings from this study?",
            "What correlations exist in the data?",
            "What are the study limitations?",
            "How many patients were included in each country?",
            
            # Specific Metrics
            "What is the mean BMI change for each treatment?",
            "How many patients experienced weight gain?",
            "What percentage of patients had no adverse events?",
            "What is the adherence rate distribution?",
        ]
        return questions
    
    def get_quick_stats(self):
        """Get quick statistics for display."""
        return {
            'total_patients': self.data_summary['basic_stats']['dataset_overview']['total_patients'],
            'mounjaro_success_rate': self.data_summary['treatment_effectiveness']['Mounjaro']['significant_weight_loss_rate'],
            'lifestyle_success_rate': self.data_summary['treatment_effectiveness']['LifestyleOnly']['significant_weight_loss_rate'],
            'mean_weight_loss_mounjaro': self.data_summary['treatment_effectiveness']['Mounjaro']['mean_weight_loss'],
            'mean_weight_loss_lifestyle': self.data_summary['treatment_effectiveness']['LifestyleOnly']['mean_weight_loss'],
            'total_countries': len(self.data_summary['basic_stats']['demographics']['country_distribution']),
            'adverse_event_rate': round(
                (self.data_summary['basic_stats']['outcomes']['adverse_events']['total_with_ae'] / 
                 self.data_summary['basic_stats']['dataset_overview']['total_patients']) * 100, 1
            )
        }
    
    def analyze_question_intent(self, question):
        """Analyze the intent of the user's question to provide better context."""
        question_lower = question.lower()
        
        intents = {
            'effectiveness': ['effective', 'success', 'outcome', 'result', 'work', 'benefit'],
            'safety': ['safe', 'adverse', 'side effect', 'risk', 'hospital', 'event'],
            'demographics': ['age', 'gender', 'country', 'men', 'women', 'group'],
            'statistics': ['mean', 'average', 'percentage', 'rate', 'number', 'how many'],
            'comparison': ['compare', 'versus', 'vs', 'difference', 'better', 'worse'],
            'adherence': ['adherence', 'compliance', 'follow', 'stick'],
            'comorbidities': ['comorbid', 'condition', 'disease', 'diabetes', 'hypertension']
        }
        
        detected_intents = []
        for intent, keywords in intents.items():
            if any(keyword in question_lower for keyword in keywords):
                detected_intents.append(intent)
        
        return detected_intents
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        return "Conversation history cleared."
    
    def get_history_summary(self):
        """Get a summary of the conversation history."""
        if not self.conversation_history:
            return "No conversation history available."
        
        summary = f"Conversation History ({len(self.conversation_history)} exchanges):\n\n"
        for i, item in enumerate(self.conversation_history, 1):
            summary += f"{i}. Q: {item['question']}\n   A: {item['answer'][:100]}...\n\n"
        
        return summary
    
    def list_available_models(self):
        """List available Gemini models for debugging."""
        try:
            models = genai.list_models()
            available_models = []
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    available_models.append(model.name)
            return available_models
        except Exception as e:
            return f"Error listing models: {str(e)}"