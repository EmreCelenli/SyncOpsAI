# SyncOpsAI - Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the `.env` file and update with your credentials:

```bash
# .env file
WATSONX_API_KEY=your_watsonx_api_key_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_PROJECT_ID=your_project_id_here

# Optional: For Pinecone integration (Day 2)
PINECONE_API_KEY=your_pinecone_key_here
PINECONE_ENVIRONMENT=your_pinecone_env_here
```

### 3. Test Components

Test each component individually:

```bash
# Test sensor data
python data.py

# Test equipment manuals
python manuals.py

# Test RAG system
python rag.py

# Test diagnosis engine
python diagnosis.py

# Test multi-agent workflow
python agents.py

# Test watsonx.ai integration
python watsonx_integration.py
```

### 4. Run Dashboard

```bash
streamlit run dashboard.py
```

## Component Overview

### Core Components (Day 1 - Complete)

1. **data.py** - Hardcoded sensor data scenarios
   - HVAC overheating scenario
   - Motor vibration scenario
   - Anomaly detection logic

2. **manuals.py** - Equipment manual content
   - HVAC-001 manual with troubleshooting
   - MOTOR-001 manual with troubleshooting
   - Parts lists and resolution steps

3. **rag.py** - Mock RAG system
   - Keyword-based manual search
   - Context formatting for LLM
   - Ready for Pinecone upgrade

4. **diagnosis.py** - Diagnostic engine
   - Template-based diagnosis
   - watsonx.ai integration (optional)
   - Cost and time estimation

5. **agents.py** - Multi-agent workflow
   - Agent 1: Telemetry Listener
   - Agent 2: Diagnostic Expert
   - Agent 3: Orchestrator
   - Simple function-based flow

### AI Integration (Day 2)

6. **watsonx_integration.py** - watsonx.ai wrapper
   - Granite model integration
   - AI-powered diagnosis
   - Fallback to template mode

### Dashboard (In Progress)

7. **dashboard.py** - Streamlit UI
   - Real-time sensor monitoring
   - Agent activity timeline
   - Diagnosis display
   - Work order management

## Usage Examples

### Run a Single Scenario

```python
from agents import MultiAgentWorkflow

# Initialize workflow
workflow = MultiAgentWorkflow(use_ai=False)  # Set to True for AI

# Run HVAC scenario
results = workflow.run_scenario("hvac_overheating")

# Check results
for result in results:
    if result['anomaly_detected']:
        print(f"Work Order: {result['work_order']['work_order_id']}")
        print(f"Issue: {result['diagnosis']['root_cause']}")
```

### Use AI Diagnosis

```python
from diagnosis import diagnose

# Diagnose with AI
diagnosis = diagnose(
    equipment_id="HVAC-001",
    anomaly_type="overheating",
    sensor_data={"temp": 32.0, "pressure": 54.0},
    use_ai=True  # Enable watsonx.ai
)

print(f"Root Cause: {diagnosis['root_cause']}")
print(f"Confidence: {diagnosis['confidence_score']*100:.0f}%")
```

### Query Equipment Manual

```python
from rag import query_equipment_manual

# Query manual
result = query_equipment_manual(
    equipment_id="HVAC-001",
    anomaly_type="overheating",
    sensor_data={"temp": 32.0}
)

print(f"Required Parts: {len(result['required_parts'])}")
for part in result['required_parts']:
    print(f"  - {part['part_number']}: {part['description']}")
```

## Troubleshooting

### watsonx.ai Not Available

If you see "watsonx.ai not available":
1. Check `.env` file has correct API key
2. Verify `ibm-watsonx-ai` is installed: `pip install ibm-watsonx-ai`
3. Check internet connection
4. System will automatically fall back to template mode

### Import Errors

If you get import errors:
```bash
pip install --upgrade -r requirements.txt
```

### Dashboard Won't Start

If Streamlit won't start:
```bash
pip install streamlit plotly
streamlit run dashboard.py
```

## Demo Scenarios

### Scenario 1: HVAC Overheating
- Equipment: HVAC-001
- Issue: Temperature rises from 22°C to 32°C
- Expected: Clogged air filter diagnosis
- Parts: AF-2024 ($45)
- Time: 30-60 minutes

### Scenario 2: Motor Vibration
- Equipment: MOTOR-001
- Issue: Vibration rises from 1.2 Hz to 4.5 Hz
- Expected: Worn bearings diagnosis
- Parts: RB-500 ($120), AS-KIT ($45)
- Time: 2-3 hours

## Architecture

```
Sensor Data → Agent 1 (Detect) → Agent 2 (Diagnose) → Agent 3 (Work Order)
                                        ↓
                                    RAG System
                                        ↓
                                  Equipment Manuals
                                        ↓
                                   watsonx.ai (optional)
```

## Next Steps

1. ✅ Complete dashboard implementation
2. ⏳ Add Pinecone vector database
3. ⏳ Add real-time streaming
4. ⏳ Create demo video
5. ⏳ Prepare presentation slides

## Support

For issues or questions:
- Check component tests: `python <component>.py`
- Review error messages in console
- Verify `.env` configuration
- Check `requirements.txt` dependencies