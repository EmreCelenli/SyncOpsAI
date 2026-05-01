"""
Main workflow orchestration using LangGraph
"""

from langgraph.graph import StateGraph, END
from poc.state import State, create_initial_state
from poc.agents import agent_1_detect, agent_2_diagnose, agent_3_action
from poc.data import DEMO_SCENARIOS


def build_graph():
    """
    Build LangGraph workflow with 3 agents.
    
    Flow:
        START → Agent 1 (Detect) → Agent 2 (Diagnose) → Agent 3 (Action) → END
    
    Routing:
        - Agent 1 → Agent 2: Only if anomaly detected
        - Agent 2 → Agent 3: Always (if we reach Agent 2)
        - Agent 3 → END: Always
    """
    # Create graph with State schema
    graph = StateGraph(State)
    
    # Add agent nodes
    graph.add_node("detect", agent_1_detect)
    graph.add_node("diagnose", agent_2_diagnose)
    graph.add_node("action", agent_3_action)
    
    # Set entry point
    graph.set_entry_point("detect")
    
    # Define routing logic
    def route_after_detect(state: State) -> str:
        """Route to diagnose if anomaly detected, otherwise end"""
        if state["anomaly"]:
            return "diagnose"
        return END
    
    # Add edges
    graph.add_conditional_edges(
        "detect",
        route_after_detect,
        {
            "diagnose": "diagnose",
            END: END
        }
    )
    graph.add_edge("diagnose", "action")
    graph.add_edge("action", END)
    
    # Compile graph
    return graph.compile()


def run_scenario(scenario: dict, verbose: bool = True):
    """
    Run a single demo scenario through the workflow.
    
    Args:
        scenario: Scenario dict from DEMO_SCENARIOS
        verbose: Print agent messages
    
    Returns:
        Final state after workflow execution
    """
    if verbose:
        print(f"\n{'='*60}")
        print(f"🚀 Running Scenario: {scenario['name']}")
        print(f"{'='*60}\n")
    
    # Create initial state
    state = create_initial_state(
        equipment_id=scenario["equipment_id"],
        sensor_value=scenario["sensor_value"],
        sensor_type=scenario["sensor_type"]
    )
    
    # Build and run workflow
    workflow = build_graph()
    result = workflow.invoke(state)
    
    # Print results
    if verbose:
        print("\n--- Agent Activity Log ---")
        for msg in result["messages"]:
            print(msg)
        
        print("\n--- Final Results ---")
        print(f"Anomaly Detected: {result['anomaly']}")
        if result['anomaly']:
            print(f"Anomaly Type: {result['anomaly_type']}")
            print(f"Diagnosis: {result['diagnosis']}")
            print(f"Parts Needed: {', '.join(result['parts_needed'])}")
            print(f"Estimated Time: {result['estimated_time']}")
            print(f"Work Order: {result['work_order_id']}")
            print(f"Parts Available: {result['parts_available']}")
        
        print(f"\n{'='*60}\n")
    
    return result


def run_all_scenarios():
    """Run all demo scenarios"""
    print("\n" + "="*60)
    print("🤖 SyncOps AI - Multi-Agent Anomaly Detection POC")
    print("="*60)
    
    results = []
    for scenario in DEMO_SCENARIOS:
        result = run_scenario(scenario)
        results.append(result)
    
    # Summary
    print("\n" + "="*60)
    print("📊 Summary")
    print("="*60)
    print(f"Total Scenarios: {len(results)}")
    print(f"Anomalies Detected: {sum(1 for r in results if r['anomaly'])}")
    print(f"Work Orders Created: {sum(1 for r in results if r['work_order_id'])}")
    print("="*60 + "\n")
    
    return results


if __name__ == "__main__":
    # Run all demo scenarios
    run_all_scenarios()

# Made with Bob
