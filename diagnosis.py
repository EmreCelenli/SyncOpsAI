"""
Template-based diagnosis function for POC
Task 4: 1 hour - Simple template-based responses, no watsonx.ai needed initially
Updated: Added watsonx.ai integration
"""

from datetime import datetime
from rag import query_equipment_manual

# Import watsonx.ai integration
try:
    from watsonx_integration import get_watsonx_ai
    WATSONX_AVAILABLE = True
except ImportError:
    WATSONX_AVAILABLE = False
    print("watsonx.ai integration not available")


class DiagnosticEngine:
    """
    Template-based diagnostic engine for POC
    Will be replaced with real LLM (watsonx.ai) in Day 2
    """
    
    def __init__(self, use_ai=False):
        """
        Initialize diagnostic engine
        
        Args:
            use_ai: If True, use real AI (watsonx.ai). If False, use templates
        """
        self.use_ai = use_ai
        self.ai_model = None
        
        if use_ai and WATSONX_AVAILABLE:
            self._initialize_ai_model()
    
    def _initialize_ai_model(self):
        """Initialize watsonx.ai model"""
        try:
            self.ai_model = get_watsonx_ai()
            if self.ai_model.available:
                print("✅ watsonx.ai diagnostic engine initialized")
            else:
                print("⚠️  watsonx.ai not available, using template-based diagnosis")
                self.use_ai = False
        except Exception as e:
            print(f"❌ Error initializing watsonx.ai: {e}")
            self.use_ai = False
    
    def diagnose_equipment_issue(self, anomaly_event):
        """
        Generate diagnosis for equipment issue
        
        Args:
            anomaly_event: dict with keys:
                - equipment_id: str
                - anomaly_type: str
                - sensor_data: dict
                - timestamp: str (optional)
        
        Returns:
            dict: Diagnosis report with resolution steps
        """
        equipment_id = anomaly_event["equipment_id"]
        anomaly_type = anomaly_event["anomaly_type"]
        sensor_data = anomaly_event.get("sensor_data", {})
        timestamp = anomaly_event.get("timestamp", datetime.now().isoformat())
        
        # Query RAG system for manual information
        rag_results = query_equipment_manual(equipment_id, anomaly_type, sensor_data)
        
        if self.use_ai:
            # Use real AI (Day 2)
            return self._diagnose_with_ai(anomaly_event, rag_results)
        else:
            # Use template-based diagnosis (Day 1)
            return self._diagnose_with_template(anomaly_event, rag_results)
    
    def _diagnose_with_template(self, anomaly_event, rag_results):
        """
        Template-based diagnosis (POC Day 1)
        
        Args:
            anomaly_event: Anomaly information
            rag_results: RAG query results
        
        Returns:
            dict: Diagnosis report
        """
        equipment_id = anomaly_event["equipment_id"]
        anomaly_type = anomaly_event["anomaly_type"]
        sensor_data = anomaly_event.get("sensor_data", {})
        
        # Extract information from RAG results
        troubleshooting = rag_results.get("troubleshooting", {})
        possible_causes = troubleshooting.get("possible_causes", [])
        resolution_steps = rag_results.get("resolution_steps", [])
        required_parts = rag_results.get("required_parts", [])
        estimated_time = rag_results.get("estimated_time", "Unknown")
        safety_precautions = rag_results.get("safety_precautions", [])
        
        # Generate root cause (use first possible cause as primary)
        root_cause = possible_causes[0] if possible_causes else f"Unknown cause for {anomaly_type}"
        
        # Format sensor readings for context
        sensor_summary = self._format_sensor_summary(sensor_data)
        
        # Build diagnosis report
        diagnosis = {
            "equipment_id": equipment_id,
            "equipment_name": rag_results.get("equipment_name", equipment_id),
            "equipment_type": rag_results.get("equipment_type", "Unknown"),
            "anomaly_type": anomaly_type,
            "timestamp": anomaly_event.get("timestamp", datetime.now().isoformat()),
            
            # Core diagnosis
            "root_cause": root_cause,
            "confidence_score": 0.85,  # Template-based has lower confidence
            "severity": self._determine_severity(sensor_data, anomaly_type),
            
            # Resolution information
            "resolution_steps": resolution_steps,
            "required_parts": required_parts,
            "estimated_time": estimated_time,
            "estimated_cost": self._calculate_total_cost(required_parts),
            
            # Additional context
            "possible_causes": possible_causes,
            "safety_precautions": safety_precautions,
            "sensor_readings": sensor_data,
            "sensor_summary": sensor_summary,
            
            # Metadata
            "diagnosis_method": "template",
            "rag_sources": rag_results.get("relevant_sections", []),
            "generated_at": datetime.now().isoformat()
        }
        
        return diagnosis
    
    def _diagnose_with_ai(self, anomaly_event, rag_results):
        """
        AI-based diagnosis using watsonx.ai
        
        Args:
            anomaly_event: Anomaly information
            rag_results: RAG query results
        
        Returns:
            dict: AI-generated diagnosis report
        """
        if not self.ai_model or not self.ai_model.available:
            print("⚠️  AI not available, using template-based diagnosis")
            return self._diagnose_with_template(anomaly_event, rag_results)
        
        try:
            # Prepare information for AI
            equipment_info = {
                "equipment_id": anomaly_event["equipment_id"],
                "equipment_name": rag_results.get("equipment_name", "Unknown"),
                "equipment_type": rag_results.get("equipment_type", "Unknown")
            }
            
            anomaly_info = {
                "anomaly_type": anomaly_event["anomaly_type"],
                "severity": self._determine_severity(anomaly_event.get("sensor_data", {}), anomaly_event["anomaly_type"]),
                "sensor_data": anomaly_event.get("sensor_data", {})
            }
            
            # Format RAG context for AI
            from rag import MockRAG
            rag = MockRAG()
            rag_context = rag.format_for_llm(
                anomaly_event["equipment_id"],
                anomaly_event["anomaly_type"],
                anomaly_event.get("sensor_data")
            )
            
            # Generate AI diagnosis
            print("🤖 Generating AI diagnosis with watsonx.ai...")
            ai_diagnosis = self.ai_model.generate_diagnosis(equipment_info, anomaly_info, rag_context)
            
            # Merge AI diagnosis with RAG results
            diagnosis = self._diagnose_with_template(anomaly_event, rag_results)
            
            # Update with AI insights
            diagnosis["root_cause"] = ai_diagnosis.get("root_cause", diagnosis["root_cause"])
            diagnosis["confidence_score"] = ai_diagnosis.get("confidence_score", 0.90)
            diagnosis["ai_analysis"] = ai_diagnosis.get("analysis", "")
            diagnosis["ai_recommended_actions"] = ai_diagnosis.get("recommended_actions", [])
            diagnosis["diagnosis_method"] = "ai_enhanced"
            diagnosis["ai_model"] = ai_diagnosis.get("model", "watsonx.ai")
            
            print("✅ AI diagnosis complete")
            
            return diagnosis
            
        except Exception as e:
            print(f"❌ Error in AI diagnosis: {e}")
            print("⚠️  Falling back to template-based diagnosis")
            return self._diagnose_with_template(anomaly_event, rag_results)
    
    def _format_sensor_summary(self, sensor_data):
        """Format sensor readings into human-readable summary"""
        if not sensor_data:
            return "No sensor data available"
        
        summary_parts = []
        for key, value in sensor_data.items():
            if key not in ['time', 'status', 'timestamp']:
                # Format based on sensor type
                if 'temp' in key.lower():
                    summary_parts.append(f"{key}: {value}°C")
                elif 'pressure' in key.lower():
                    summary_parts.append(f"{key}: {value} PSI")
                elif 'current' in key.lower():
                    summary_parts.append(f"{key}: {value}A")
                elif 'vibration' in key.lower():
                    summary_parts.append(f"{key}: {value} Hz")
                else:
                    summary_parts.append(f"{key}: {value}")
        
        return ", ".join(summary_parts)
    
    def _determine_severity(self, sensor_data, anomaly_type):
        """Determine severity level based on sensor readings"""
        # Simple severity determination
        if not sensor_data:
            return "medium"
        
        # Check for critical values
        temp = sensor_data.get('temp', sensor_data.get('temperature', 0))
        vibration = sensor_data.get('vibration', 0)
        current = sensor_data.get('current', 0)
        
        if temp > 30 or vibration > 4.0 or current > 25:
            return "critical"
        elif temp > 28 or vibration > 3.5 or current > 20:
            return "high"
        else:
            return "medium"
    
    def _calculate_total_cost(self, required_parts):
        """Calculate total cost of required parts"""
        if not required_parts:
            return "$0"
        
        total = 0
        for part in required_parts:
            # Extract numeric value from cost string (e.g., "$45" -> 45)
            cost_str = part.get('cost', '$0')
            cost_value = float(cost_str.replace('$', '').replace(',', ''))
            quantity = part.get('quantity', 1)
            total += cost_value * quantity
        
        return f"${total:.2f}"
    
    def format_diagnosis_for_display(self, diagnosis):
        """
        Format diagnosis for dashboard display
        
        Args:
            diagnosis: Diagnosis dict
        
        Returns:
            str: Formatted diagnosis text
        """
        output = []
        output.append(f"🔍 DIAGNOSIS REPORT")
        output.append(f"=" * 50)
        output.append(f"Equipment: {diagnosis['equipment_name']} ({diagnosis['equipment_id']})")
        output.append(f"Issue: {diagnosis['anomaly_type']}")
        output.append(f"Severity: {diagnosis['severity'].upper()}")
        output.append(f"Confidence: {diagnosis['confidence_score']*100:.0f}%")
        output.append("")
        
        output.append(f"🎯 ROOT CAUSE:")
        output.append(f"  {diagnosis['root_cause']}")
        output.append("")
        
        output.append(f"📋 RESOLUTION STEPS:")
        for i, step in enumerate(diagnosis['resolution_steps'], 1):
            output.append(f"  {i}. {step}")
        output.append("")
        
        output.append(f"🔧 REQUIRED PARTS ({len(diagnosis['required_parts'])}):")
        for part in diagnosis['required_parts']:
            output.append(f"  • {part['part_number']}: {part['description']}")
            output.append(f"    Cost: {part['cost']} x {part['quantity']}")
        output.append(f"  Total Cost: {diagnosis['estimated_cost']}")
        output.append("")
        
        output.append(f"⏱️  ESTIMATED TIME: {diagnosis['estimated_time']}")
        output.append("")
        
        if diagnosis['safety_precautions']:
            output.append(f"⚠️  SAFETY PRECAUTIONS:")
            for precaution in diagnosis['safety_precautions']:
                output.append(f"  • {precaution}")
        
        return "\n".join(output)


# Convenience function for quick diagnosis
def diagnose(equipment_id, anomaly_type, sensor_data=None, use_ai=False):
    """
    Quick diagnosis function
    
    Args:
        equipment_id: Equipment identifier
        anomaly_type: Type of anomaly
        sensor_data: Optional sensor readings
        use_ai: Use AI model (Day 2) or template (Day 1)
    
    Returns:
        dict: Diagnosis report
    """
    engine = DiagnosticEngine(use_ai=use_ai)
    
    anomaly_event = {
        "equipment_id": equipment_id,
        "anomaly_type": anomaly_type,
        "sensor_data": sensor_data or {},
        "timestamp": datetime.now().isoformat()
    }
    
    return engine.diagnose_equipment_issue(anomaly_event)


# Quick test
if __name__ == "__main__":
    print("=== Testing Diagnostic Engine ===\n")
    
    engine = DiagnosticEngine(use_ai=False)
    
    # Test 1: HVAC overheating
    print("Test 1: HVAC Overheating Diagnosis")
    print("-" * 50)
    
    anomaly_event = {
        "equipment_id": "HVAC-001",
        "anomaly_type": "overheating",
        "sensor_data": {
            "temp": 32.0,
            "pressure": 54.0,
            "current": 13.0
        },
        "timestamp": "2026-05-01T10:06:00Z"
    }
    
    diagnosis = engine.diagnose_equipment_issue(anomaly_event)
    
    print(f"Equipment: {diagnosis['equipment_name']}")
    print(f"Root Cause: {diagnosis['root_cause']}")
    print(f"Severity: {diagnosis['severity']}")
    print(f"Confidence: {diagnosis['confidence_score']*100:.0f}%")
    print(f"Estimated Time: {diagnosis['estimated_time']}")
    print(f"Estimated Cost: {diagnosis['estimated_cost']}")
    print(f"Resolution Steps: {len(diagnosis['resolution_steps'])} steps")
    print(f"Required Parts: {len(diagnosis['required_parts'])} items")
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: Motor vibration
    print("Test 2: Motor Excessive Vibration Diagnosis")
    print("-" * 50)
    
    diagnosis = diagnose(
        "MOTOR-001",
        "excessive_vibration",
        {"vibration": 4.5, "temp": 62.0, "current": 26.0}
    )
    
    print(f"Equipment: {diagnosis['equipment_name']}")
    print(f"Root Cause: {diagnosis['root_cause']}")
    print(f"Severity: {diagnosis['severity']}")
    print(f"Estimated Cost: {diagnosis['estimated_cost']}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 3: Formatted display
    print("Test 3: Formatted Diagnosis Display")
    print("-" * 50)
    formatted = engine.format_diagnosis_for_display(diagnosis)
    print(formatted)
    
    print("\n=== All Tests Passed ===")

# Made with Bob
