"""
Simple multi-agent workflow for POC
Task 5: 2 hours - Direct function calls, no LangGraph complexity needed for POC
"""

from datetime import datetime
from data import check_anomaly, get_scenario
from diagnosis import diagnose
import time


class Agent1_TelemetryListener:
    """
    Agent 1: Monitors sensor data and detects anomalies
    """
    
    def __init__(self):
        self.name = "Agent 1: Telemetry Listener"
        self.anomalies_detected = []
    
    def process_sensor_reading(self, equipment_id, sensor_reading):
        """
        Process a sensor reading and detect anomalies
        
        Args:
            equipment_id: Equipment identifier
            sensor_reading: Sensor data dict
        
        Returns:
            dict: Anomaly event if detected, None otherwise
        """
        # Determine scenario from equipment_id
        scenario_map = {
            "HVAC-001": "hvac_overheating",
            "HVAC-002": "hvac_overheating",
            "MOTOR-001": "motor_vibration",
            "MOTOR-002": "motor_vibration"
        }
        
        scenario_name = scenario_map.get(equipment_id, "hvac_overheating")
        
        # Check for anomaly
        is_anomaly, anomaly_type, severity = check_anomaly(scenario_name, sensor_reading)
        
        if is_anomaly:
            anomaly_event = {
                "equipment_id": equipment_id,
                "anomaly_type": anomaly_type,
                "severity": severity,
                "sensor_data": sensor_reading,
                "timestamp": datetime.now().isoformat(),
                "detected_by": self.name
            }
            
            self.anomalies_detected.append(anomaly_event)
            
            return anomaly_event
        
        return None
    
    def get_status(self):
        """Get agent status"""
        return {
            "agent": self.name,
            "anomalies_detected": len(self.anomalies_detected),
            "status": "active"
        }


class Agent2_DiagnosticExpert:
    """
    Agent 2: Analyzes anomalies and generates diagnosis using RAG + LLM
    """
    
    def __init__(self, use_ai=False, use_pinecone=False):
        self.name = "Agent 2: Diagnostic Expert"
        self.use_ai = use_ai
        self.use_pinecone = use_pinecone
        self.diagnoses_generated = []
    
    def process_anomaly(self, anomaly_event):
        """
        Process anomaly and generate diagnosis
        
        Args:
            anomaly_event: Anomaly information from Agent 1
        
        Returns:
            dict: Diagnosis report
        """
        equipment_id = anomaly_event["equipment_id"]
        anomaly_type = anomaly_event["anomaly_type"]
        sensor_data = anomaly_event["sensor_data"]
        
        # Generate diagnosis using RAG + template/AI
        diagnosis = diagnose(
            equipment_id=equipment_id,
            anomaly_type=anomaly_type,
            sensor_data=sensor_data,
            use_ai=self.use_ai,
            use_pinecone=self.use_pinecone
        )
        
        # Add agent metadata
        diagnosis["diagnosed_by"] = self.name
        diagnosis["anomaly_event"] = anomaly_event
        
        self.diagnoses_generated.append(diagnosis)
        
        return diagnosis
    
    def get_status(self):
        """Get agent status"""
        return {
            "agent": self.name,
            "diagnoses_generated": len(self.diagnoses_generated),
            "ai_enabled": self.use_ai,
            "status": "active"
        }


class Agent3_Orchestrator:
    """
    Agent 3: Creates work orders and checks inventory
    """
    
    def __init__(self):
        self.name = "Agent 3: Orchestrator"
        self.work_orders_created = []
        self.work_order_counter = 1000
    
    def process_diagnosis(self, diagnosis):
        """
        Process diagnosis and create work order
        
        Args:
            diagnosis: Diagnosis report from Agent 2
        
        Returns:
            dict: Work order information
        """
        # Generate work order ID
        work_order_id = f"WO-{self.work_order_counter}"
        self.work_order_counter += 1
        
        # Check inventory (mock - always available for POC)
        inventory_status = self._check_inventory(diagnosis["required_parts"])
        
        # Create work order
        work_order = {
            "work_order_id": work_order_id,
            "equipment_id": diagnosis["equipment_id"],
            "equipment_name": diagnosis["equipment_name"],
            "issue": diagnosis["root_cause"],
            "severity": diagnosis["severity"],
            "resolution_steps": diagnosis["resolution_steps"],
            "required_parts": diagnosis["required_parts"],
            "estimated_time": diagnosis["estimated_time"],
            "estimated_cost": diagnosis["estimated_cost"],
            "inventory_status": inventory_status,
            "safety_precautions": diagnosis["safety_precautions"],
            "created_at": datetime.now().isoformat(),
            "created_by": self.name,
            "status": "open",
            "priority": self._determine_priority(diagnosis["severity"])
        }
        
        self.work_orders_created.append(work_order)
        
        return work_order
    
    def _check_inventory(self, required_parts):
        """
        Check inventory for required parts (mock for POC)
        
        Args:
            required_parts: List of required parts
        
        Returns:
            dict: Inventory status
        """
        # Mock implementation - always available for POC
        parts_status = []
        all_available = True
        
        for part in required_parts:
            parts_status.append({
                "part_number": part["part_number"],
                "description": part["description"],
                "required_quantity": part["quantity"],
                "available_quantity": part["quantity"] + 2,  # Mock: always have extra
                "in_stock": True,
                "location": "Warehouse A"
            })
        
        return {
            "all_parts_available": all_available,
            "parts_status": parts_status,
            "checked_at": datetime.now().isoformat()
        }
    
    def _determine_priority(self, severity):
        """Determine work order priority based on severity"""
        priority_map = {
            "critical": "P1 - Critical",
            "high": "P2 - High",
            "medium": "P3 - Medium",
            "low": "P4 - Low"
        }
        return priority_map.get(severity, "P3 - Medium")
    
    def get_status(self):
        """Get agent status"""
        return {
            "agent": self.name,
            "work_orders_created": len(self.work_orders_created),
            "status": "active"
        }


class MultiAgentWorkflow:
    """
    Orchestrates the multi-agent workflow
    Simple direct function calls - no LangGraph needed for POC
    """
    
    def __init__(self, use_ai=False):
        self.agent1 = Agent1_TelemetryListener()
        self.agent2 = Agent2_DiagnosticExpert(use_ai=use_ai)
        self.agent3 = Agent3_Orchestrator()
        self.workflow_history = []
    
    def run_workflow(self, equipment_id, sensor_reading):
        """
        Run the complete workflow for a sensor reading
        
        Args:
            equipment_id: Equipment identifier
            sensor_reading: Sensor data
        
        Returns:
            dict: Complete workflow result
        """
        workflow_start = datetime.now()
        
        result = {
            "equipment_id": equipment_id,
            "sensor_reading": sensor_reading,
            "workflow_start": workflow_start.isoformat(),
            "steps": []
        }
        
        # Step 1: Agent 1 - Detect anomaly
        step1_start = time.time()
        anomaly_event = self.agent1.process_sensor_reading(equipment_id, sensor_reading)
        step1_duration = time.time() - step1_start
        
        result["steps"].append({
            "step": 1,
            "agent": self.agent1.name,
            "action": "Anomaly detection",
            "duration_ms": int(step1_duration * 1000),
            "result": "Anomaly detected" if anomaly_event else "No anomaly"
        })
        
        if not anomaly_event:
            result["anomaly_detected"] = False
            result["workflow_end"] = datetime.now().isoformat()
            result["total_duration_ms"] = int((datetime.now() - workflow_start).total_seconds() * 1000)
            return result
        
        result["anomaly_detected"] = True
        result["anomaly_event"] = anomaly_event
        
        # Step 2: Agent 2 - Generate diagnosis
        step2_start = time.time()
        diagnosis = self.agent2.process_anomaly(anomaly_event)
        step2_duration = time.time() - step2_start
        
        result["steps"].append({
            "step": 2,
            "agent": self.agent2.name,
            "action": "Diagnosis generation",
            "duration_ms": int(step2_duration * 1000),
            "result": f"Diagnosis complete: {diagnosis['root_cause']}"
        })
        
        result["diagnosis"] = diagnosis
        
        # Step 3: Agent 3 - Create work order
        step3_start = time.time()
        work_order = self.agent3.process_diagnosis(diagnosis)
        step3_duration = time.time() - step3_start
        
        result["steps"].append({
            "step": 3,
            "agent": self.agent3.name,
            "action": "Work order creation",
            "duration_ms": int(step3_duration * 1000),
            "result": f"Work order {work_order['work_order_id']} created"
        })
        
        result["work_order"] = work_order
        
        # Finalize
        result["workflow_end"] = datetime.now().isoformat()
        result["total_duration_ms"] = int((datetime.now() - workflow_start).total_seconds() * 1000)
        result["success"] = True
        
        self.workflow_history.append(result)
        
        return result
    
    def run_scenario(self, scenario_name):
        """
        Run workflow for a complete scenario
        
        Args:
            scenario_name: 'hvac_overheating' or 'motor_vibration'
        
        Returns:
            list: Results for each reading in scenario
        """
        scenario = get_scenario(scenario_name)
        equipment_id = scenario["equipment_id"]
        results = []
        
        for reading in scenario["readings"]:
            result = self.run_workflow(equipment_id, reading)
            results.append(result)
            
            # Small delay for demo effect
            time.sleep(0.1)
        
        return results
    
    def get_system_status(self):
        """Get status of all agents"""
        return {
            "agents": [
                self.agent1.get_status(),
                self.agent2.get_status(),
                self.agent3.get_status()
            ],
            "workflows_executed": len(self.workflow_history),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_workflow_summary(self):
        """Get summary of all workflows"""
        if not self.workflow_history:
            return {"message": "No workflows executed yet"}
        
        total_anomalies = sum(1 for w in self.workflow_history if w.get("anomaly_detected"))
        total_work_orders = len(self.agent3.work_orders_created)
        avg_duration = sum(w.get("total_duration_ms", 0) for w in self.workflow_history) / len(self.workflow_history)
        
        return {
            "total_workflows": len(self.workflow_history),
            "anomalies_detected": total_anomalies,
            "work_orders_created": total_work_orders,
            "average_duration_ms": int(avg_duration),
            "agents_status": self.get_system_status()
        }


# Quick test
if __name__ == "__main__":
    print("=== Testing Multi-Agent Workflow ===\n")
    
    workflow = MultiAgentWorkflow(use_ai=False)
    
    # Test 1: Single sensor reading with anomaly
    print("Test 1: HVAC Overheating - Single Reading")
    print("-" * 50)
    
    sensor_reading = {
        "temp": 32.0,
        "pressure": 54.0,
        "current": 13.0,
        "time": "10:06:00",
        "status": "critical"
    }
    
    result = workflow.run_workflow("HVAC-001", sensor_reading)
    
    print(f"Anomaly Detected: {result['anomaly_detected']}")
    if result['anomaly_detected']:
        print(f"Anomaly Type: {result['anomaly_event']['anomaly_type']}")
        print(f"Root Cause: {result['diagnosis']['root_cause']}")
        print(f"Work Order: {result['work_order']['work_order_id']}")
        print(f"Total Duration: {result['total_duration_ms']}ms")
        print(f"\nWorkflow Steps:")
        for step in result['steps']:
            print(f"  Step {step['step']}: {step['agent']}")
            print(f"    Action: {step['action']}")
            print(f"    Duration: {step['duration_ms']}ms")
            print(f"    Result: {step['result']}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: Normal reading (no anomaly)
    print("Test 2: Normal Reading - No Anomaly")
    print("-" * 50)
    
    normal_reading = {
        "temp": 22.0,
        "pressure": 50.0,
        "current": 10.0,
        "time": "10:00:00",
        "status": "normal"
    }
    
    result = workflow.run_workflow("HVAC-001", normal_reading)
    print(f"Anomaly Detected: {result['anomaly_detected']}")
    print(f"Workflow Steps: {len(result['steps'])}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 3: System status
    print("Test 3: System Status")
    print("-" * 50)
    
    status = workflow.get_system_status()
    print(f"Workflows Executed: {status['workflows_executed']}")
    for agent_status in status['agents']:
        print(f"\n{agent_status['agent']}:")
        print(f"  Status: {agent_status['status']}")
        for key, value in agent_status.items():
            if key not in ['agent', 'status']:
                print(f"  {key}: {value}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 4: Workflow summary
    print("Test 4: Workflow Summary")
    print("-" * 50)
    
    summary = workflow.get_workflow_summary()
    print(f"Total Workflows: {summary['total_workflows']}")
    print(f"Anomalies Detected: {summary['anomalies_detected']}")
    print(f"Work Orders Created: {summary['work_orders_created']}")
    print(f"Average Duration: {summary['average_duration_ms']}ms")
    
    print("\n=== All Tests Passed ===")

# Made with Bob
