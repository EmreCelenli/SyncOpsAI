# 2-Day Hackathon: Proof-of-Concept Plan
## Developer A - Compelling Demo Focus

---

## POC PHILOSOPHY: DEMO > PERFECTION

**Goal:** Build a working demo that showcases the concept, not production-ready code.

**Priorities:**
1. ✅ **Working end-to-end flow** (even if hardcoded)
2. ✅ **Visual impact** (dashboard showing AI in action)
3. ✅ **Clear value proposition** (automation saves time/money)
4. ❌ Error handling, scalability, edge cases
5. ❌ Perfect code quality, tests, documentation

---

## DAY 1: MINIMUM VIABLE DEMO

### Morning (4 hours) - Quick Data Setup

**Task 1: Hardcoded Sensor Data (30 min)**
```python
# data.py - Just hardcode 2 scenarios
DEMO_SCENARIOS = {
    "hvac_overheating": {
        "equipment_id": "HVAC-001",
        "readings": [
            {"temp": 22, "time": "10:00"},
            {"temp": 28, "time": "10:05"},
            {"temp": 32, "time": "10:10"}  # Anomaly!
        ]
    },
    "motor_vibration": {
        "equipment_id": "MOTOR-001", 
        "readings": [
            {"vibration": 1.5, "time": "10:00"},
            {"vibration": 4.2, "time": "10:05"}  # Anomaly!
        ]
    }
}
```

**Task 2: Fake PDF Content (1 hour)**
```python
# manuals.py - Skip PDF generation, just use text
MANUAL_CONTENT = {
    "HVAC-001": """
    TROUBLESHOOTING: High Temperature (>28°C)
    - Cause: Clogged air filter
    - Fix: Replace filter (Part: AF-2024, $45)
    - Time: 30 minutes
    """,
    "MOTOR-001": """
    TROUBLESHOOTING: Excessive Vibration (>3Hz)
    - Cause: Worn bearings
    - Fix: Replace bearings (Part: RB-500, $120)
    - Time: 2 hours
    """
}
```

**Task 3: Mock RAG (1.5 hours)**
```python
# rag.py - Simple keyword matching, no Pinecone needed
def query_manual(equipment_id, anomaly_type):
    content = MANUAL_CONTENT[equipment_id]
    return {
        "troubleshooting": content,
        "parts": extract_parts(content),
        "steps": extract_steps(content)
    }
```

**Task 4: Mock LLM (1 hour)**
```python
# diagnosis.py - Template-based, no watsonx.ai needed for POC
def diagnose(equipment_id, anomaly_type, manual_content):
    return {
        "root_cause": f"{anomaly_type} detected on {equipment_id}",
        "resolution": manual_content["steps"],
        "parts": manual_content["parts"],
        "estimated_time": "1-2 hours"
    }
```

---

### Afternoon (4 hours) - Integration & Dashboard

**Task 5: Simple Agent Flow (2 hours)**
```python
# agents.py - No LangGraph complexity for POC
def run_workflow(sensor_data):
    # Agent 1: Detect anomaly
    if sensor_data["temp"] > 28:
        anomaly = {"type": "overheating", "equipment": "HVAC-001"}
    
    # Agent 2: Diagnose
    manual = query_manual(anomaly["equipment"], anomaly["type"])
    diagnosis = diagnose(anomaly["equipment"], anomaly["type"], manual)
    
    # Agent 3: Create work order
    work_order = {
        "id": "WO-001",
        "issue": diagnosis["root_cause"],
        "parts": diagnosis["parts"]
    }
    
    return {"anomaly": anomaly, "diagnosis": diagnosis, "work_order": work_order}
```

**Task 6: Visual Dashboard (2 hours)**
```python
# dashboard.py - Streamlit for quick UI
import streamlit as st

st.title("🤖 AI Equipment Monitor")

# Show sensor data
st.metric("HVAC-001 Temperature", "32°C", "🔴 ALERT")

# Show AI diagnosis
st.subheader("AI Diagnosis")
st.success("Root Cause: Clogged air filter")
st.info("Required Part: AF-2024 ($45)")
st.warning("Estimated Time: 30 minutes")

# Show work order
st.subheader("Work Order Created")
st.code("WO-001: Replace HVAC-001 air filter")
```

---

## DAY 2: POLISH & DEMO PREP

### Morning (3 hours) - Add "AI Magic"

**Task 7: Add Real watsonx.ai Call (1.5 hours)**
```python
# Only add real AI where it's visible in demo
from ibm_watsonx_ai import ModelInference

def diagnose_with_ai(anomaly, manual_content):
    prompt = f"Equipment {anomaly['equipment']} has {anomaly['type']}. Manual says: {manual_content}. Diagnose:"
    
    response = model.generate(prompt)
    
    # Parse response (keep it simple)
    return {"root_cause": response, "confidence": 0.95}
```

**Task 8: Add One Real RAG Query (1.5 hours)**
```python
# Just show Pinecone working once
from pinecone import Pinecone

pc = Pinecone(api_key="...")
index = pc.Index("demo")

# Upload just 2 manual chunks
index.upsert([
    {"id": "hvac-1", "values": embed("HVAC troubleshooting..."), "metadata": {"equipment": "HVAC-001"}},
    {"id": "motor-1", "values": embed("Motor troubleshooting..."), "metadata": {"equipment": "MOTOR-001"}}
])

# Query in demo
results = index.query(vector=embed("overheating"), top_k=1)
```

---

### Afternoon (5 hours) - Demo Perfection

**Task 9: Make Dashboard Impressive (2 hours)**
```python
# Add animations, colors, charts
import plotly.express as px

# Animated sensor chart
fig = px.line(sensor_history, x="time", y="temperature")
fig.add_hline(y=28, line_dash="dash", line_color="red")
st.plotly_chart(fig)

# Agent activity timeline
st.subheader("🤖 AI Agent Activity")
st.write("⏱️ 10:10:05 - Agent 1: Anomaly detected")
st.write("⏱️ 10:10:08 - Agent 2: Querying equipment manual...")
st.write("⏱️ 10:10:12 - Agent 2: Diagnosis complete")
st.write("⏱️ 10:10:15 - Agent 3: Work order WO-001 created")
```

**Task 10: Rehearse Demo Script (1 hour)**
```
DEMO SCRIPT (5 minutes):

1. "Here's our factory with 2 pieces of equipment" [Show dashboard]
2. "Watch what happens when temperature spikes" [Click button to inject anomaly]
3. "Agent 1 detects the anomaly in real-time" [Show alert]
4. "Agent 2 queries the equipment manual using RAG" [Show Pinecone query]
5. "Agent 2 uses IBM Granite AI to diagnose the issue" [Show LLM response]
6. "Agent 3 automatically creates a work order" [Show work order]
7. "Total time: 10 seconds. Manual process: 30+ minutes" [Show value prop]
```

**Task 11: Create Slides (1 hour)**
```
SLIDE 1: Problem
- Manual equipment monitoring is slow
- Technicians waste time searching manuals
- Delayed response = costly downtime

SLIDE 2: Solution
- AI agents monitor equipment 24/7
- RAG retrieves relevant manual sections instantly
- LLM diagnoses issues automatically
- Work orders created in seconds

SLIDE 3: Demo
[Live demo]

SLIDE 4: Tech Stack
- LangGraph for multi-agent orchestration
- IBM watsonx.ai (Granite models)
- Pinecone for vector search
- IBM Docling for document parsing

SLIDE 5: Impact
- 95% faster diagnosis
- 80% reduction in manual lookup time
- Proactive maintenance prevents failures
```

**Task 12: Final Testing (1 hour)**
- Run demo 5 times to ensure it works
- Have backup screenshots if live demo fails
- Test on presentation laptop

---

## SHORTCUTS FOR POC

### What to Skip:
- ❌ PDF generation (use text files)
- ❌ Complex chunking (just split by paragraphs)
- ❌ Production Pinecone setup (use free tier, 2 vectors)
- ❌ Error handling (demo happy path only)
- ❌ Tests (manual testing is enough)
- ❌ Multiple equipment types (2 is enough)
- ❌ Real-time streaming (fake it with sleep())
- ❌ Authentication, security, logging

### What to Fake:
- ✅ Sensor data (hardcoded scenarios)
- ✅ Anomaly detection (simple thresholds)
- ✅ Agent communication (direct function calls, not LangGraph)
- ✅ Inventory check (always return "in stock")
- ✅ Work order system (just print to screen)

### What Must Be Real:
- ✅ One watsonx.ai API call (visible in demo)
- ✅ One Pinecone query (visible in demo)
- ✅ Dashboard showing the flow
- ✅ Clear value proposition

---

## DEMO DAY CHECKLIST

**Before Demo:**
- [ ] Dashboard loads in <5 seconds
- [ ] Demo scenarios work 100% of time
- [ ] Backup screenshots ready
- [ ] Slides loaded on presentation laptop
- [ ] Internet connection tested (for API calls)
- [ ] 5-minute timer set

**During Demo:**
- [ ] Start with problem statement (30 sec)
- [ ] Show dashboard (30 sec)
- [ ] Run Scenario 1: HVAC (2 min)
- [ ] Run Scenario 2: Motor (2 min)
- [ ] Show value proposition (30 sec)
- [ ] Q&A (if time)

**Backup Plan:**
- If API fails: Use pre-recorded video
- If dashboard crashes: Show screenshots
- If laptop dies: Have slides on phone

---

## SUCCESS METRICS FOR POC

**Must Have:**
- ✅ Working demo (even if hardcoded)
- ✅ Visual dashboard showing AI in action
- ✅ Clear before/after comparison
- ✅ One real watsonx.ai call
- ✅ One real Pinecone query

**Nice to Have:**
- ⭐ Animated transitions
- ⭐ Multiple scenarios
- ⭐ Real-time updates
- ⭐ Impressive charts

**Don't Need:**
- ❌ Production-ready code
- ❌ Error handling
- ❌ Tests
- ❌ Documentation
- ❌ Scalability

---

## TIME ALLOCATION

**Day 1:**
- 4 hours: Hardcoded data + mock functions
- 4 hours: Basic dashboard + simple workflow

**Day 2:**
- 3 hours: Add real AI (watsonx.ai + Pinecone)
- 3 hours: Polish dashboard + rehearse
- 2 hours: Slides + final testing

**Total: 16 hours** (realistic for 2-day hackathon)

---

## FINAL DELIVERABLE

**GitHub Repo:**
```
/demo
  - dashboard.py (Streamlit app)
  - data.py (hardcoded scenarios)
  - agents.py (simple workflow)
  - rag.py (mock + one real Pinecone call)
  - diagnosis.py (mock + one real watsonx.ai call)
  - requirements.txt
  - README.md (how to run demo)
  - slides.pdf
```

**README.md:**
```markdown
# AI Equipment Monitor - POC

## Run Demo
1. pip install -r requirements.txt
2. streamlit run dashboard.py
3. Click "Run HVAC Scenario"

## Tech Stack
- IBM watsonx.ai (Granite-Vision-4.1-4B)
- Pinecone Vector Database
- LangGraph Multi-Agent Framework
- Streamlit Dashboard

## Demo Video
[Link to 2-minute demo video]
```

---

## REMEMBER: DEMO > CODE

**Good POC:**
- Shows the concept clearly
- Impresses judges visually
- Demonstrates AI value
- Works reliably in demo

**Bad POC:**
- Perfect code that doesn't demo well
- Complex architecture nobody understands
- Crashes during presentation
- No clear value proposition

**Focus on storytelling, not engineering!** 🎭