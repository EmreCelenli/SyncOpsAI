# Developer B: POC Plan - Agent Orchestration
## 2-Day Hackathon: Compelling Demo Focus

---

## POC PHILOSOPHY: DEMO > PERFECTION

**Goal:** Build a working demo that WOWs judges, not production code.

**Priorities:**
1. ✅ **Working end-to-end flow** (3 agents communicating)
2. ✅ **Visual dashboard** (real-time agent actions)
3. ✅ **Clear story** (problem → AI solution → business value)
4. ❌ Error handling, tests, scalability
5. ❌ Perfect code, documentation

---

## SIMPLIFIED ARCHITECTURE

```
Sensor Data → Agent 1 (Detect) → Agent 2 (Diagnose) → Agent 3 (Action) → Dashboard
              ↓                    ↓                     ↓
           "Spike!"           "Replace filter"      "Work Order #123"
```

**Key Simplification:** Use LangGraph for agent flow, but keep everything else minimal.

---

## DAY 1 MORNING (4 hours): AGENT 1 + BASIC FLOW

### Task 1: Minimal Project Structure (15 min)
```
poc/
├── agents.py          # All 3 agents in one file
├── state.py           # Simple state dict
├── data.py            # Hardcoded test data
├── dashboard.py       # Streamlit UI
└── main.py            # Run demo
```

### Task 2: Simple State Schema (30 min)
```python
# state.py - Keep it simple!
from typing import TypedDict

class State(TypedDict):
    # Input
    equipment_id: str
    sensor_value: float
    
    # Agent 1 output
    anomaly: bool
    anomaly_type: str
    
    # Agent 2 output
    diagnosis: str
    parts_needed: list
    
    # Agent 3 output
    work_order_id: str
    
    # For dashboard
    messages: list
```

### Task 3: Agent 1 - Simple Threshold Detection (1.5 hours)
```python
# agents.py
def agent_1_detect(state):
    """Agent 1: Detect anomaly with simple threshold"""
    value = state["sensor_value"]
    equipment = state["equipment_id"]
    
    # Hardcoded thresholds for demo
    THRESHOLDS = {
        "HVAC-001": {"temp": 28},
        "MOTOR-001": {"vibration": 3}
    }
    
    if "HVAC" in equipment and value > 28:
        return {
            **state,
            "anomaly": True,
            "anomaly_type": "overheating",
            "messages": [f"🚨 Agent 1: Detected overheating! Temp={value}°C"]
        }
    elif "MOTOR" in equipment and value > 3:
        return {
            **state,
            "anomaly": True,
            "anomaly_type": "vibration",
            "messages": [f"🚨 Agent 1: Detected vibration! Level={value}Hz"]
        }
    else:
        return {
            **state,
            "anomaly": False,
            "messages": [f"✅ Agent 1: Normal operation"]
        }
```

### Task 4: Basic LangGraph Setup (1.5 hours)
```python
# main.py
from langgraph.graph import StateGraph, END

def build_graph():
    graph = StateGraph(State)
    
    # Add agents
    graph.add_node("detect", agent_1_detect)
    graph.add_node("diagnose", agent_2_diagnose)  # Will implement in afternoon
    graph.add_node("action", agent_3_action)      # Will implement in afternoon
    
    # Simple routing
    graph.set_entry_point("detect")
    graph.add_conditional_edges(
        "detect",
        lambda s: "diagnose" if s["anomaly"] else END
    )
    graph.add_edge("diagnose", "action")
    graph.add_edge("action", END)
    
    return graph.compile()

# Test with hardcoded data
if __name__ == "__main__":
    state = {
        "equipment_id": "HVAC-001",
        "sensor_value": 32.0,  # Anomaly!
        "messages": []
    }
    
    result = build_graph().invoke(state)
    print(result["messages"])
```

### Task 5: Hardcoded Test Data (30 min)
```python
# data.py
DEMO_SCENARIOS = [
    {
        "name": "HVAC Overheating",
        "equipment_id": "HVAC-001",
        "sensor_value": 32.0,
        "expected": "Replace air filter"
    },
    {
        "name": "Motor Vibration",
        "equipment_id": "MOTOR-001",
        "sensor_value": 4.2,
        "expected": "Replace bearings"
    }
]
```

**Deliverable:** Agent 1 working with LangGraph routing

---

## DAY 1 AFTERNOON (4 hours): AGENT 2 & 3 + MOCK INTEGRATIONS

### Task 6: Agent 2 Skeleton (1 hour)
```python
# agents.py (continued)
def agent_2_diagnose(state):
    """Agent 2: Diagnose issue (calls Developer A's mock functions)"""
    if not state["anomaly"]:
        return state
    
    equipment = state["equipment_id"]
    anomaly_type = state["anomaly_type"]
    
    # Call Developer A's mock RAG (they provide this)
    manual_info = query_manual_mock(equipment, anomaly_type)
    
    # Call Developer A's mock LLM (they provide this)
    diagnosis = diagnose_mock(equipment, anomaly_type, manual_info)
    
    return {
        **state,
        "diagnosis": diagnosis["root_cause"],
        "parts_needed": diagnosis["parts"],
        "messages": state["messages"] + [
            f"🔍 Agent 2: Diagnosed - {diagnosis['root_cause']}"
        ]
    }

# Mock functions until Developer A provides real ones
def query_manual_mock(equipment, anomaly):
    return {"troubleshooting": "Mock manual content"}

def diagnose_mock(equipment, anomaly, manual):
    if "HVAC" in equipment:
        return {
            "root_cause": "Clogged air filter",
            "parts": ["Air Filter AF-2024"],
            "time": "30 min"
        }
    else:
        return {
            "root_cause": "Worn bearings",
            "parts": ["Bearing RB-500"],
            "time": "2 hours"
        }
```

### Task 7: Agent 3 with Mock watsonx Orchestrate (1.5 hours)
```python
# agents.py (continued)
def agent_3_action(state):
    """Agent 3: Create work order (mock watsonx Orchestrate)"""
    import uuid
    
    # Mock work order creation
    work_order_id = f"WO-{uuid.uuid4().hex[:6].upper()}"
    
    # Mock inventory check
    parts_available = True  # Always true for demo
    
    return {
        **state,
        "work_order_id": work_order_id,
        "messages": state["messages"] + [
            f"📋 Agent 3: Created work order {work_order_id}",
            f"✅ Agent 3: All parts in stock"
        ]
    }
```

### Task 8: Integration Points Documentation (30 min)
```python
# integration.py - Interface for Developer A
"""
Developer A: Provide these 2 functions by end of Day 1:

1. query_manual(equipment_id, anomaly_type) -> dict
   Returns: {"troubleshooting": str, "parts": list, "steps": list}

2. diagnose(equipment_id, anomaly_type, manual_content) -> dict
   Returns: {"root_cause": str, "parts": list, "time": str}

We'll integrate on Day 2 morning by replacing mock functions.
"""
```

### Task 9: Test End-to-End Flow (1 hour)
```python
# test_flow.py
def test_demo_scenarios():
    graph = build_graph()
    
    for scenario in DEMO_SCENARIOS:
        print(f"\n{'='*50}")
        print(f"Testing: {scenario['name']}")
        print(f"{'='*50}")
        
        state = {
            "equipment_id": scenario["equipment_id"],
            "sensor_value": scenario["sensor_value"],
            "messages": []
        }
        
        result = graph.invoke(state)
        
        # Print agent messages
        for msg in result["messages"]:
            print(msg)
        
        # Verify work order created
        assert "work_order_id" in result
        print(f"\n✅ Work Order: {result['work_order_id']}")

if __name__ == "__main__":
    test_demo_scenarios()
```

**Deliverable:** All 3 agents working end-to-end with mock data

---

## DAY 2 MORNING (3 hours): INTEGRATION + DASHBOARD

### Task 10: Integrate Developer A's Functions (1 hour)
```python
# Replace mocks in agents.py
from developer_a_functions import query_manual, diagnose

def agent_2_diagnose(state):
    """Now using real RAG + LLM from Developer A"""
    if not state["anomaly"]:
        return state
    
    # Real RAG query
    manual_info = query_manual(
        state["equipment_id"],
        state["anomaly_type"]
    )
    
    # Real LLM diagnosis
    diagnosis = diagnose(
        state["equipment_id"],
        state["anomaly_type"],
        manual_info
    )
    
    return {
        **state,
        "diagnosis": diagnosis["root_cause"],
        "parts_needed": diagnosis["parts"],
        "messages": state["messages"] + [
            f"🔍 Agent 2: {diagnosis['root_cause']}"
        ]
    }
```

### Task 11: Simple Streamlit Dashboard (2 hours)
```python
# dashboard.py
import streamlit as st
from main import build_graph
from data import DEMO_SCENARIOS

st.title("🤖 SyncOps AI - Multi-Agent Anomaly Detection")

# Sidebar: Select scenario
scenario = st.sidebar.selectbox(
    "Demo Scenario",
    [s["name"] for s in DEMO_SCENARIOS]
)

# Get scenario data
selected = next(s for s in DEMO_SCENARIOS if s["name"] == scenario)

# Display equipment info
st.header(f"Equipment: {selected['equipment_id']}")
st.metric("Sensor Reading", f"{selected['sensor_value']}")

# Run button
if st.button("🚀 Run AI Agents"):
    # Create state
    state = {
        "equipment_id": selected["equipment_id"],
        "sensor_value": selected["sensor_value"],
        "messages": []
    }
    
    # Run workflow with progress
    with st.spinner("Running agents..."):
        graph = build_graph()
        result = graph.invoke(state)
    
    # Display results
    st.success("✅ Workflow Complete!")
    
    # Show agent messages
    st.subheader("Agent Activity Log")
    for msg in result["messages"]:
        st.write(msg)
    
    # Show work order
    if result.get("work_order_id"):
        st.subheader("📋 Work Order Created")
        st.info(f"Work Order ID: {result['work_order_id']}")
        st.write(f"**Issue:** {result['diagnosis']}")
        st.write(f"**Parts Needed:** {', '.join(result['parts_needed'])}")
```

**Deliverable:** Working dashboard showing agent flow

---

## DAY 2 AFTERNOON (5 hours): POLISH FOR DEMO

### Task 12: Enhanced Dashboard (2 hours - Together)
```python
# Add visual improvements
- Agent status indicators (🟢 Running, ✅ Complete)
- Timeline visualization of agent execution
- Animated transitions between agents
- Cost savings calculator ("Saved 2 hours of manual diagnosis")
```

### Task 13: Demo Script (1 hour - Developer B)
```markdown
# demo_script.md

## 30-Second Pitch
"SyncOps AI uses 3 AI agents to automatically detect equipment failures, 
diagnose root causes, and create work orders - reducing response time 
from hours to seconds."

## Demo Flow (3 minutes)
1. Show dashboard with normal operation
2. Trigger HVAC overheating scenario
3. Watch agents work in real-time:
   - Agent 1 detects anomaly
   - Agent 2 diagnoses issue using AI
   - Agent 3 creates work order
4. Show final work order with parts list
5. Highlight business value: "Prevented 4-hour downtime"

## Key Talking Points
- Multi-agent collaboration (not just one AI)
- Real-time anomaly detection
- Automated diagnosis using equipment manuals
- Integration with existing systems (watsonx Orchestrate)
```

### Task 14: Final Testing (1 hour - Together)
- Run both scenarios multiple times
- Verify all agent messages display correctly
- Check work order IDs are unique
- Test dashboard responsiveness

### Task 15: Presentation Prep (1 hour - Together)
- Create 3-slide deck:
  1. Problem: Manual equipment monitoring is slow
  2. Solution: 3 AI agents automate the process
  3. Impact: 90% faster response time
- Practice 3-minute demo
- Prepare for Q&A

---

## CRITICAL SUCCESS FACTORS FOR POC

### What Makes a Compelling Demo:
1. ✅ **It works reliably** - No crashes during demo
2. ✅ **Visual impact** - Dashboard shows AI "thinking"
3. ✅ **Clear value** - "Saves 2 hours per incident"
4. ✅ **Simple story** - Problem → AI → Solution

### What We DON'T Need:
- ❌ Error handling for edge cases
- ❌ Unit tests
- ❌ Production-ready code
- ❌ Scalability
- ❌ Security
- ❌ Documentation

### Time Allocation:
- 60% - Core functionality (agents working)
- 30% - Dashboard (visual impact)
- 10% - Demo prep (story + practice)

---

## HANDOFF POINTS WITH DEVELOPER A

### End of Day 1:
**Developer A provides:**
```python
# developer_a_functions.py
def query_manual(equipment_id, anomaly_type):
    """Returns manual content (can be mock or real RAG)"""
    pass

def diagnose(equipment_id, anomaly_type, manual_content):
    """Returns diagnosis (can be template or real LLM)"""
    pass
```

**Developer B provides:**
```python
# Agent interfaces that call these functions
def agent_2_diagnose(state):
    manual = query_manual(...)
    diagnosis = diagnose(...)
    return updated_state
```

### Day 2 Morning:
- 15 min: Developer A shares functions
- 30 min: Developer B integrates
- 15 min: Test together

---

## MINIMAL FILE STRUCTURE

```
syncops-poc/
├── agents.py           # All 3 agents (200 lines)
├── state.py            # State schema (50 lines)
├── data.py             # Test scenarios (30 lines)
├── main.py             # LangGraph setup (50 lines)
├── dashboard.py        # Streamlit UI (100 lines)
├── integration.py      # Developer A interface (20 lines)
├── demo_script.md      # Demo walkthrough
└── requirements.txt    # langgraph, streamlit
```

**Total Code: ~450 lines** (vs 2000+ for production)

---

## DEMO DAY CHECKLIST

### Before Demo:
- [ ] Test both scenarios 3 times
- [ ] Dashboard loads in <5 seconds
- [ ] All agent messages display correctly
- [ ] Work order IDs are unique
- [ ] Practice 3-minute pitch

### During Demo:
- [ ] Start with problem statement
- [ ] Run HVAC scenario live
- [ ] Highlight agent collaboration
- [ ] Show work order output
- [ ] End with business value

### Backup Plan:
- [ ] Screenshots of successful runs
- [ ] Pre-recorded video (if live demo fails)
- [ ] Hardcoded results as fallback

---

## IMPLEMENTATION PRIORITY

### Must Have (Core Demo):
1. Agent 1 detects anomaly ✅
2. Agent 2 diagnoses (even with mock) ✅
3. Agent 3 creates work order ✅
4. Dashboard shows agent flow ✅

### Nice to Have (If Time):
- Real RAG integration
- Real LLM integration
- Animated agent transitions
- Cost savings calculator

### Skip (Not Worth Time):
- Error handling
- Tests
- Documentation
- Multiple equipment types
- Historical data
- User authentication

---

## SUCCESS METRICS

**Demo is successful if:**
1. Workflow runs end-to-end without errors
2. Judges understand the value proposition
3. Dashboard is visually appealing
4. We can answer "How does this save time/money?"

**Demo fails if:**
- Code crashes during presentation
- Agents don't communicate
- Value proposition is unclear
- Dashboard is confusing

---

## FINAL DELIVERABLE

**What judges will see:**
1. Live dashboard with 2 demo scenarios
2. Real-time agent execution
3. Work order creation
4. Clear business value

**What judges won't see:**
- Source code quality
- Test coverage
- Error handling
- Scalability considerations

**Remember:** This is a POC to prove the concept works, not production code!
