# Agent Communication Quick Reference Guide
## LangGraph Message Passing for Multi-Agent System

---

## TL;DR - How to Send Messages to Agents

**Simple Answer:** You don't send messages directly to agents. Instead, you:
1. Create an initial state with your data
2. Pass it to the LangGraph workflow
3. The graph automatically routes messages between agents based on state conditions

```python
# Create initial state with sensor data
state = {
    "sensor_data": {"temperature": 32.5},
    "equipment_id": "HVAC-001",
    "timestamp": "2026-05-01T10:30:00Z"
}

# Run workflow - agents communicate automatically
result = app.invoke(state)

# Get final result
print(result["work_order_id"])
```

---

## Core Concepts

### 1. Shared State (The Message Bus)
All agents read from and write to a shared state dictionary:

```python
class AgentState(TypedDict):
    # Input
    sensor_data: dict
    equipment_id: str
    
    # Agent 1 → Agent 2
    anomaly_detected: bool
    anomaly_type: str
    
    # Agent 2 → Agent 3
    diagnosis_complete: bool
    root_cause: str
    resolution_steps: list[str]
    required_parts: list[dict]
    
    # Agent 3 → Output
    work_order_id: str
    
    # Logs
    messages: list[str]
```

### 2. Agent Nodes (Message Processors)
Each agent is a function that receives state and returns updated state:

```python
def agent_2_diagnostic(state: AgentState) -> AgentState:
    # Read from state (message from Agent 1)
    anomaly_type = state["anomaly_type"]
    
    # Process
    diagnosis = generate_diagnosis(anomaly_type)
    
    # Write to state (message to Agent 3)
    return {
        **state,
        "diagnosis_complete": True,
        "root_cause": diagnosis["root_cause"]
    }
```

### 3. Conditional Routing (Message Flow Control)
The graph decides which agent runs next:

```python
def should_diagnose(state: AgentState) -> str:
    if state["anomaly_detected"]:
        return "diagnostic"  # Route to Agent 2
    return END  # Stop workflow

workflow.add_conditional_edges(
    "telemetry",
    should_diagnose,
    {"diagnostic": "diagnostic", END: END}
)
```

---

## Communication Patterns

### Pattern 1: Sequential Processing
Agent 1 → Agent 2 → Agent 3

```python
# Agent 1 detects anomaly
def agent_1(state):
    return {**state, "anomaly_detected": True, "anomaly_type": "overheating"}

# Agent 2 receives anomaly info automatically
def agent_2(state):
    if state["anomaly_detected"]:
        diagnosis = diagnose(state["anomaly_type"])
        return {**state, "diagnosis_complete": True, "root_cause": diagnosis}
    return state

# Agent 3 receives diagnosis automatically
def agent_3(state):
    if state["diagnosis_complete"]:
        work_order = create_work_order(state["root_cause"])
        return {**state, "work_order_id": work_order}
    return state
```

### Pattern 2: Conditional Branching
Agent 1 → Agent 2 (only if anomaly) → Agent 3 (only if diagnosis)

```python
workflow.add_conditional_edges(
    "agent_1",
    lambda state: "agent_2" if state["anomaly_detected"] else END
)

workflow.add_conditional_edges(
    "agent_2",
    lambda state: "agent_3" if state["diagnosis_complete"] else END
)
```

### Pattern 3: Parallel Processing (Advanced)
Multiple agents process simultaneously:

```python
from langgraph.graph import StateGraph

# Create parallel branches
workflow.add_node("check_inventory", check_inventory_agent)
workflow.add_node("notify_team", notification_agent)

# Both run after diagnosis
workflow.add_edge("diagnostic", "check_inventory")
workflow.add_edge("diagnostic", "notify_team")
```

---

## Developer A's Specific Integration

### Your Functions Are Called BY Agent 2

**You provide:**
```python
# Function 1: RAG Query
def query_equipment_manual(equipment_id, anomaly_type, sensor_data):
    # Your RAG implementation
    return {
        "relevant_sections": [...],
        "required_parts": [...]
    }

# Function 2: Diagnosis Generation
def diagnose_equipment_issue(anomaly_event):
    # Your LLM + RAG implementation
    return {
        "root_cause": "...",
        "resolution_steps": [...],
        "required_parts": [...]
    }
```

**Developer B integrates them into Agent 2:**
```python
def agent_2_diagnostic(state: AgentState) -> AgentState:
    # Developer B calls your functions
    rag_results = query_equipment_manual(
        state["equipment_id"],
        state["anomaly_type"],
        state["sensor_data"]
    )
    
    diagnosis = diagnose_equipment_issue({
        "equipment_id": state["equipment_id"],
        "anomaly_type": state["anomaly_type"],
        "sensor_data": state["sensor_data"],
        "rag_context": rag_results
    })
    
    # Developer B updates state
    return {
        **state,
        "diagnosis_complete": True,
        "root_cause": diagnosis["root_cause"],
        "resolution_steps": diagnosis["resolution_steps"],
        "required_parts": diagnosis["required_parts"]
    }
```

### You Don't Need to Worry About:
- ❌ How Agent 1 sends data to Agent 2
- ❌ How Agent 2 sends data to Agent 3
- ❌ Graph routing logic
- ❌ State management

### You DO Need to Provide:
- ✅ `query_equipment_manual()` function
- ✅ `diagnose_equipment_issue()` function
- ✅ Clear input/output specifications
- ✅ Test cases

---

## Practical Examples

### Example 1: Running the Full Workflow

```python
from langgraph.graph import StateGraph, END

# Build graph (Developer B's responsibility)
workflow = StateGraph(AgentState)
workflow.add_node("telemetry", agent_1_telemetry)
workflow.add_node("diagnostic", agent_2_diagnostic)
workflow.add_node("orchestrator", agent_3_orchestrator)
workflow.set_entry_point("telemetry")
# ... add edges ...
app = workflow.compile()

# Run workflow (anyone can do this)
initial_state = {
    "sensor_data": {"temperature": 32.5, "pressure": 50},
    "equipment_id": "HVAC-001",
    "timestamp": "2026-05-01T10:30:00Z",
    "anomaly_detected": False,
    "diagnosis_complete": False,
    "work_order_created": False,
    "messages": []
}

# Execute - agents communicate automatically
final_state = app.invoke(initial_state)

# Check results
print(f"Anomaly: {final_state['anomaly_type']}")
print(f"Root Cause: {final_state['root_cause']}")
print(f"Work Order: {final_state['work_order_id']}")
print(f"Agent Messages: {final_state['messages']}")
```

### Example 2: Streaming Real-Time Updates

```python
# Stream execution to see each agent's output
for state_update in app.stream(initial_state):
    print(f"State after agent: {state_update}")
    
    # Update dashboard in real-time
    if "anomaly_detected" in state_update and state_update["anomaly_detected"]:
        dashboard.show_alert(state_update["anomaly_type"])
    
    if "diagnosis_complete" in state_update and state_update["diagnosis_complete"]:
        dashboard.show_diagnosis(state_update["root_cause"])
    
    if "work_order_created" in state_update and state_update["work_order_created"]:
        dashboard.show_work_order(state_update["work_order_id"])
```

### Example 3: Processing Multiple Sensor Readings

```python
# Process batch of sensor readings
sensor_readings = [
    {"equipment_id": "HVAC-001", "temperature": 32.5},
    {"equipment_id": "MOTOR-001", "vibration": 4.2},
    {"equipment_id": "HVAC-002", "temperature": 22.0}
]

results = []
for reading in sensor_readings:
    state = {
        "sensor_data": reading,
        "equipment_id": reading["equipment_id"],
        "timestamp": datetime.now().isoformat(),
        "anomaly_detected": False,
        "diagnosis_complete": False,
        "work_order_created": False,
        "messages": []
    }
    
    result = app.invoke(state)
    results.append(result)

# Analyze results
anomalies = [r for r in results if r["anomaly_detected"]]
work_orders = [r for r in results if r["work_order_created"]]
```

---

## Testing Agent Communication

### Test Individual Agents

```python
def test_agent_2_receives_data_from_agent_1():
    # Simulate Agent 1's output
    state_from_agent_1 = {
        "equipment_id": "HVAC-001",
        "anomaly_detected": True,
        "anomaly_type": "overheating",
        "sensor_data": {"temperature": 32.5},
        "messages": ["Agent 1: Anomaly detected"]
    }
    
    # Test Agent 2 receives and processes it
    result = agent_2_diagnostic(state_from_agent_1)
    
    assert result["diagnosis_complete"] == True
    assert "root_cause" in result
    assert len(result["messages"]) == 2  # Agent 1 + Agent 2
```

### Test Full Workflow

```python
def test_end_to_end_communication():
    initial_state = {
        "sensor_data": {"temperature": 32.5},
        "equipment_id": "HVAC-001",
        "timestamp": "2026-05-01T10:30:00Z",
        "anomaly_detected": False,
        "diagnosis_complete": False,
        "work_order_created": False,
        "messages": []
    }
    
    final_state = app.invoke(initial_state)
    
    # Verify data flowed through all agents
    assert final_state["anomaly_detected"] == True
    assert final_state["diagnosis_complete"] == True
    assert final_state["work_order_created"] == True
    assert len(final_state["messages"]) == 3
```

---

## Common Pitfalls & Solutions

### ❌ Pitfall 1: Trying to Call Agents Directly
```python
# WRONG - Don't do this
result = agent_2_diagnostic({"anomaly_type": "overheating"})
```

### ✅ Solution: Use the Workflow
```python
# CORRECT - Let the graph handle routing
state = {"sensor_data": {...}, "equipment_id": "HVAC-001"}
result = app.invoke(state)
```

---

### ❌ Pitfall 2: Modifying State In-Place
```python
# WRONG - Mutating state
def agent_2(state):
    state["diagnosis_complete"] = True  # Mutation!
    return state
```

### ✅ Solution: Return New State
```python
# CORRECT - Return new dict
def agent_2(state):
    return {**state, "diagnosis_complete": True}
```

---

### ❌ Pitfall 3: Forgetting to Set Routing Flags
```python
# WRONG - Agent 3 won't run
def agent_2(state):
    diagnosis = generate_diagnosis()
    return {**state, "root_cause": diagnosis}  # Missing diagnosis_complete!
```

### ✅ Solution: Set All Required Flags
```python
# CORRECT - Set flag for routing
def agent_2(state):
    diagnosis = generate_diagnosis()
    return {
        **state,
        "diagnosis_complete": True,  # Triggers Agent 3
        "root_cause": diagnosis
    }
```

---

## Debugging Agent Communication

### Enable Verbose Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# LangGraph will log state transitions
result = app.invoke(initial_state)
```

### Inspect State at Each Step
```python
for step, state in enumerate(app.stream(initial_state)):
    print(f"\n=== Step {step} ===")
    print(f"Anomaly Detected: {state.get('anomaly_detected')}")
    print(f"Diagnosis Complete: {state.get('diagnosis_complete')}")
    print(f"Work Order Created: {state.get('work_order_created')}")
    print(f"Messages: {state.get('messages')}")
```

### Visualize the Graph
```python
from IPython.display import Image, display

# Generate graph visualization
display(Image(app.get_graph().draw_mermaid_png()))
```

---

## Summary for Developer A

**Your Role in Agent Communication:**
1. Build RAG query function that Agent 2 will call
2. Build diagnosis function that Agent 2 will call
3. Define clear input/output contracts
4. Provide test cases

**You DON'T need to:**
- Implement the LangGraph workflow (Developer B)
- Handle state routing (Developer B)
- Manage agent-to-agent communication (LangGraph handles this)

**Key Handoff:**
```python
# You provide these functions
def query_equipment_manual(equipment_id, anomaly_type, sensor_data):
    """Your RAG implementation"""
    pass

def diagnose_equipment_issue(anomaly_event):
    """Your LLM + RAG implementation"""
    pass

# Developer B integrates them into Agent 2
def agent_2_diagnostic(state):
    rag_results = query_equipment_manual(...)  # Calls your function
    diagnosis = diagnose_equipment_issue(...)   # Calls your function
    return {**state, "diagnosis_complete": True, ...}
```

**Testing Your Functions:**
```python
# Test independently of LangGraph
def test_your_functions():
    # Test RAG query
    rag_result = query_equipment_manual(
        "HVAC-001",
        "overheating",
        {"temperature": 32.5}
    )
    assert "relevant_sections" in rag_result
    
    # Test diagnosis
    diagnosis = diagnose_equipment_issue({
        "equipment_id": "HVAC-001",
        "anomaly_type": "overheating",
        "sensor_data": {"temperature": 32.5}
    })
    assert "root_cause" in diagnosis
    assert "resolution_steps" in diagnosis
```

---

## Quick Reference Card

| Concept | What It Is | Example |
|---------|-----------|---------|
| **State** | Shared data dictionary | `{"anomaly_detected": True, "anomaly_type": "overheating"}` |
| **Agent Node** | Function that processes state | `def agent_2(state): return {...}` |
| **Routing** | Conditional logic for next agent | `if state["anomaly_detected"]: return "diagnostic"` |
| **Invoke** | Run workflow synchronously | `result = app.invoke(state)` |
| **Stream** | Run workflow with real-time updates | `for s in app.stream(state): ...` |
| **Message** | State field passed between agents | `state["root_cause"]` from Agent 2 to Agent 3 |

---

## Need Help?

**Common Questions:**

Q: How do I send data from Agent 2 to Agent 3?
A: Return it in the state dict with `diagnosis_complete=True`

Q: How do I test my RAG function?
A: Call it directly with test data, no LangGraph needed

Q: What if my function fails?
A: Add error handling and return errors in state: `{"errors": ["RAG query failed"]}`

Q: How do I see what's happening?
A: Use `app.stream()` to see state after each agent

**For More Details:**
- See [`developer_a_plan.md`](developer_a_plan.md:1) for full implementation guide
- LangGraph docs: https://langchain-ai.github.io/langgraph/
- Ask Developer B about graph structure and routing logic