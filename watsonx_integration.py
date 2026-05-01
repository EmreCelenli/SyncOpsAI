"""
watsonx.ai Integration for POC
Implements real AI diagnosis using IBM Granite models
"""

import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Check if ibm-watsonx-ai is available
try:
    from ibm_watsonx_ai.foundation_models import ModelInference
    from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
    WATSONX_AVAILABLE = True
except ImportError:
    WATSONX_AVAILABLE = False
    print("Warning: ibm-watsonx-ai not installed. Install with: pip install ibm-watsonx-ai")


class WatsonxAI:
    """
    Wrapper for watsonx.ai Granite model integration
    """
    
    def __init__(self):
        self.api_key = os.getenv("WATSONX_API_KEY")
        self.url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        
        self.model = None
        self.available = WATSONX_AVAILABLE and self.api_key is not None
        
        if self.available:
            self._initialize_model()
        else:
            print("watsonx.ai not available - using template-based diagnosis")
    
    def _initialize_model(self):
        """Initialize the Granite model"""
        try:
            # Model parameters for diagnosis generation
            parameters = {
                GenParams.DECODING_METHOD: "greedy",
                GenParams.MAX_NEW_TOKENS: 500,
                GenParams.MIN_NEW_TOKENS: 50,
                GenParams.TEMPERATURE: 0.3,
                GenParams.TOP_K: 50,
                GenParams.TOP_P: 0.9,
                GenParams.REPETITION_PENALTY: 1.1
            }
            
            # Initialize model
            self.model = ModelInference(
                model_id="ibm/granite-13b-chat-v2",  # Using Granite chat model
                params=parameters,
                credentials={
                    "apikey": self.api_key,
                    "url": self.url
                },
                project_id=self.project_id
            )
            
            print("✅ watsonx.ai Granite model initialized successfully")
            
        except Exception as e:
            print(f"❌ Error initializing watsonx.ai: {e}")
            self.available = False
    
    def generate_diagnosis(self, equipment_info, anomaly_info, rag_context):
        """
        Generate AI-powered diagnosis using Granite model
        
        Args:
            equipment_info: dict with equipment details
            anomaly_info: dict with anomaly information
            rag_context: str with RAG-retrieved manual context
        
        Returns:
            dict: AI-generated diagnosis
        """
        if not self.available or self.model is None:
            return self._fallback_diagnosis(equipment_info, anomaly_info)
        
        try:
            # Build prompt
            prompt = self._build_diagnosis_prompt(equipment_info, anomaly_info, rag_context)
            
            # Generate response
            response = self.model.generate_text(prompt=prompt)
            
            # Parse response
            diagnosis = self._parse_diagnosis_response(response, equipment_info, anomaly_info)
            
            return diagnosis
            
        except Exception as e:
            print(f"Error generating AI diagnosis: {e}")
            return self._fallback_diagnosis(equipment_info, anomaly_info)
    
    def _build_diagnosis_prompt(self, equipment_info, anomaly_info, rag_context):
        """Build prompt for Granite model"""
        
        prompt = f"""You are an expert equipment maintenance technician analyzing sensor data and equipment manuals.

EQUIPMENT INFORMATION:
- Equipment ID: {equipment_info.get('equipment_id')}
- Equipment Name: {equipment_info.get('equipment_name')}
- Equipment Type: {equipment_info.get('equipment_type')}

ANOMALY DETECTED:
- Type: {anomaly_info.get('anomaly_type')}
- Severity: {anomaly_info.get('severity', 'unknown')}
- Sensor Readings: {json.dumps(anomaly_info.get('sensor_data', {}), indent=2)}

EQUIPMENT MANUAL INFORMATION:
{rag_context}

TASK:
Based on the sensor readings and equipment manual, provide a detailed diagnosis in JSON format with the following structure:
{{
    "root_cause": "Brief explanation of the root cause",
    "confidence_score": 0.95,
    "analysis": "Detailed analysis of the issue",
    "recommended_actions": ["action 1", "action 2", "action 3"],
    "urgency": "critical/high/medium/low"
}}

Provide ONLY the JSON response, no additional text.
"""
        
        return prompt
    
    def _parse_diagnosis_response(self, response, equipment_info, anomaly_info):
        """Parse AI response into structured diagnosis"""
        
        try:
            # Try to extract JSON from response
            response_text = response.strip()
            
            # Find JSON in response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                ai_diagnosis = json.loads(json_str)
            else:
                # If no JSON found, create structured response from text
                ai_diagnosis = {
                    "root_cause": response_text[:200],
                    "confidence_score": 0.85,
                    "analysis": response_text,
                    "recommended_actions": ["Review AI response", "Consult manual"],
                    "urgency": anomaly_info.get('severity', 'medium')
                }
            
            # Add metadata
            ai_diagnosis['ai_generated'] = True
            ai_diagnosis['model'] = 'ibm/granite-13b-chat-v2'
            ai_diagnosis['equipment_id'] = equipment_info.get('equipment_id')
            ai_diagnosis['anomaly_type'] = anomaly_info.get('anomaly_type')
            
            return ai_diagnosis
            
        except json.JSONDecodeError as e:
            print(f"Error parsing AI response: {e}")
            return {
                "root_cause": "AI analysis in progress",
                "confidence_score": 0.75,
                "analysis": response[:500],
                "recommended_actions": ["Review equipment manual", "Inspect equipment"],
                "urgency": anomaly_info.get('severity', 'medium'),
                "ai_generated": True,
                "parse_error": str(e)
            }
    
    def _fallback_diagnosis(self, equipment_info, anomaly_info):
        """Fallback diagnosis when AI is not available"""
        return {
            "root_cause": f"{anomaly_info.get('anomaly_type')} detected on {equipment_info.get('equipment_id')}",
            "confidence_score": 0.70,
            "analysis": "AI diagnosis not available - using template-based analysis",
            "recommended_actions": [
                "Consult equipment manual",
                "Inspect equipment for visible issues",
                "Contact maintenance technician"
            ],
            "urgency": anomaly_info.get('severity', 'medium'),
            "ai_generated": False,
            "fallback": True
        }
    
    def test_connection(self):
        """Test watsonx.ai connection"""
        if not self.available:
            return {
                "status": "unavailable",
                "message": "watsonx.ai not configured or library not installed"
            }
        
        try:
            # Simple test prompt
            test_prompt = "Respond with 'OK' if you can read this."
            response = self.model.generate_text(prompt=test_prompt)
            
            return {
                "status": "connected",
                "message": "watsonx.ai connection successful",
                "model": "ibm/granite-13b-chat-v2",
                "test_response": response[:100]
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Connection test failed: {str(e)}"
            }


# Singleton instance
_watsonx_instance = None

def get_watsonx_ai():
    """Get or create watsonx.ai instance"""
    global _watsonx_instance
    if _watsonx_instance is None:
        _watsonx_instance = WatsonxAI()
    return _watsonx_instance


# Quick test
if __name__ == "__main__":
    print("=== Testing watsonx.ai Integration ===\n")
    
    # Initialize
    watsonx = WatsonxAI()
    
    # Test connection
    print("Test 1: Connection Test")
    print("-" * 50)
    result = watsonx.test_connection()
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    if 'test_response' in result:
        print(f"Response: {result['test_response']}")
    
    print("\n" + "="*50 + "\n")
    
    # Test diagnosis generation
    if watsonx.available:
        print("Test 2: Diagnosis Generation")
        print("-" * 50)
        
        equipment_info = {
            "equipment_id": "HVAC-001",
            "equipment_name": "Industrial HVAC System",
            "equipment_type": "HVAC"
        }
        
        anomaly_info = {
            "anomaly_type": "overheating",
            "severity": "critical",
            "sensor_data": {
                "temp": 32.0,
                "pressure": 54.0,
                "current": 13.0
            }
        }
        
        rag_context = """
        TROUBLESHOOTING: High Temperature (>28°C)
        - Cause: Clogged air filter restricting airflow
        - Fix: Replace filter (Part: AF-2024, $45)
        - Time: 30 minutes
        """
        
        diagnosis = watsonx.generate_diagnosis(equipment_info, anomaly_info, rag_context)
        
        print(f"Root Cause: {diagnosis.get('root_cause')}")
        print(f"Confidence: {diagnosis.get('confidence_score', 0)*100:.0f}%")
        print(f"AI Generated: {diagnosis.get('ai_generated', False)}")
        if 'recommended_actions' in diagnosis:
            print(f"Actions: {len(diagnosis['recommended_actions'])} recommended")
    else:
        print("Test 2: Skipped (watsonx.ai not available)")
    
    print("\n=== Tests Complete ===")

# Made with Bob
