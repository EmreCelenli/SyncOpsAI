# SyncOps AI - POC Implementation
## Multi-Agent Anomaly Detection System

---

## Quick Start

### 1. Install Dependencies
```bash
cd poc
pip install -r requirements.txt
```

### 2. Run Command-Line Demo
```bash
python main.py
```

### 3. Run Dashboard
```bash
streamlit run dashboard.py
```

---

## Project Structure

```
poc/
├── state.py           # State schema for agent communication
├── data.py            # Demo scenarios and test data
├── agents.py          # All 3 agents implementation
├── main.py            # LangGraph workflow and CLI
├── dashboard.py       # Streamlit UI for demo
├── integration.py     # Developer A integration interface
├── demo_script.md     # Presentation guide
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

---

## Architecture

### Multi-Agent Workflow

```
Sensor Data → Agent 1 (Detect) → Agent 2 (Diagnose) → Agent 3 (Action) → Work Order
              ↓                    ↓                     ↓
           "Spike!"           "Replace filter"      "WO-ABC123"
```

### Agent Responsibilities

**Agent 1: Telemetry Listener**
- Receives sensor data
- Detects anomalies using threshold-based detection
- Outputs: anomaly type, severity

**Agent 2: Diagnostic Expert**
- Receives anomaly event
- Queries equipment manuals (RAG)
- Generates diagnosis using LLM
- Outputs: root cause, parts needed, estimated time

**Agent 3: Orchestrator**
- Receives diagnosis
- Creates work order (watsonx Orchestrate)
- Checks inventory (watsonx Orchestrate)
- Outputs: work order ID, parts availability

---

## Demo Scenarios

### Scenario 1: HVAC Overheating
- Equipment: HVAC-001
- Sensor: Temperature = 32°C (threshold: 28°C)
- Expected: Clogged air filter diagnosis

### Scenario 2: Motor Vibration
- Equipment: MOTOR-001
- Sensor: Vibration = 4.2 Hz (threshold: 3.0 Hz)
- Expected: Worn bearings diagnosis

---

## Developer A Integration

### Day 1 End Deliverables

Developer A should provide these 2 functions:

```python
# developer_a_functions.py

def query_manual(equipment_id: str, anomaly_type: str) -> dict:
    """Query equipment manual using RAG"""
    return {
        "troubleshooting": str,
        "parts": list[str],
        "steps": list[str]
    }

def diagnose(equipment_id: str, anomaly_type: str, manual_content: dict) -> dict:
    """Generate diagnosis using LLM"""
    return {
        "root_cause": str,
        "parts": list[str],
        "time": str
    }
```

### Day 2 Morning Integration

1. Developer A creates `developer_a_functions.py`
2. Update `agents.py`:
   ```python
   from developer_a_functions import query_manual, diagnose
   ```
3. Test: `python main.py`

See `integration.py` for detailed instructions.

---

## Testing

### Test Command-Line Flow
```bash
python main.py
```

Expected output:
- Both scenarios run successfully
- Agent messages display correctly
- Work orders created with unique IDs

### Test Dashboard
```bash
streamlit run dashboard.py
```

Expected behavior:
- Dashboard loads without errors
- Both scenarios selectable
- Agents execute when button clicked
- Results display correctly

### Test Developer A Integration
```bash
python integration.py
```

Expected output:
- Test cases for both scenarios
- Validates function signatures
- Checks return values

---

## Technology Stack

- **LangGraph**: Multi-agent orchestration
- **Streamlit**: Dashboard UI
- **watsonx.ai**: LLM for diagnosis (Developer A)
- **watsonx Orchestrate**: Work order automation
- **Pinecone**: Vector store for RAG (Developer A)

---

## POC Limitations

This is a proof-of-concept focused on demo impact, not production code:

### What Works:
✅ End-to-end agent workflow
✅ Real-time anomaly detection
✅ Visual dashboard
✅ Clear business value demonstration

### What's Simplified:
- Threshold-based detection (not ML)
- Mock watsonx Orchestrate calls
- Hardcoded test scenarios
- No error handling for edge cases
- No authentication/security
- No scalability considerations

### For Production:
- Implement statistical anomaly detection (3-sigma, drift, flatline)
- Connect to real watsonx Orchestrate API
- Add comprehensive error handling
- Implement user authentication
- Add logging and monitoring
- Scale to handle multiple equipment streams
- Add unit tests and integration tests

---

## Demo Preparation

### Before Demo:
1. Test both scenarios 3 times
2. Verify dashboard loads in < 5 seconds
3. Check all agent messages display
4. Confirm work order IDs are unique
5. Practice 3-minute pitch (see `demo_script.md`)

### During Demo:
1. Start with problem statement
2. Run live demo (don't just talk)
3. Highlight agent collaboration
4. Show business value metrics
5. Be ready for Q&A

### Backup Plan:
- Screenshots of successful runs
- Pre-recorded video
- Architecture diagram

---

## Troubleshooting

### Dashboard won't start
```bash
# Check Streamlit is installed
pip install streamlit

# Run with verbose output
streamlit run dashboard.py --logger.level=debug
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### LangGraph errors
```bash
# Check LangGraph version
pip show langgraph

# Should be >= 0.2.0
```

---

## File Sizes

- `state.py`: ~60 lines
- `data.py`: ~30 lines
- `agents.py`: ~240 lines
- `main.py`: ~130 lines
- `dashboard.py`: ~175 lines
- `integration.py`: ~160 lines

**Total: ~800 lines** (vs 2000+ for production)

---

## Success Metrics

**Demo is successful if:**
- ✅ Workflow runs end-to-end without errors
- ✅ Judges understand the value proposition
- ✅ Dashboard is visually appealing
- ✅ Can answer "How does this save time/money?"

**Demo fails if:**
- ❌ Code crashes during presentation
- ❌ Agents don't communicate
- ❌ Value proposition is unclear
- ❌ Dashboard is confusing

---

## Next Steps

### After Hackathon:
1. Implement real statistical anomaly detection
2. Connect to real watsonx Orchestrate
3. Add more equipment types
4. Implement historical data analysis
5. Add user authentication
6. Deploy to cloud platform

### For Production:
1. Comprehensive testing suite
2. Error handling and logging
3. Scalability improvements
4. Security hardening
5. Documentation
6. CI/CD pipeline

---

## Contact

For questions or issues:
- Developer B: Agent orchestration, LangGraph, dashboard
- Developer A: RAG system, LLM integration, diagnosis

---

## License

POC Demo - 2-Day Hackathon Project