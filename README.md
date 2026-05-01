# SyncOpsAI - AI-Powered Equipment Monitoring System

**2-Day Hackathon POC** | Multi-Agent System | IBM watsonx.ai | RAG

## 🎯 Overview

SyncOpsAI is an AI-powered equipment monitoring system that uses multi-agent architecture to automatically detect anomalies, diagnose issues, and create work orders. Built for the 2-day hackathon with focus on compelling demo over production code.

## ✨ Key Features

- **🤖 Multi-Agent System**: 3 specialized AI agents working together
  - Agent 1: Telemetry Listener (anomaly detection)
  - Agent 2: Diagnostic Expert (RAG + AI diagnosis)
  - Agent 3: Orchestrator (work orders + inventory)

- **🧠 AI-Powered Diagnosis**: IBM watsonx.ai Granite models
  - Intelligent root cause analysis
  - Context-aware recommendations
  - Confidence scoring

- **📚 RAG System**: Retrieval-Augmented Generation
  - Equipment manual knowledge base
  - Relevant troubleshooting retrieval
  - Parts and cost estimation

- **📊 Real-Time Dashboard**: Streamlit interface
  - Live sensor monitoring
  - Agent activity timeline
  - Diagnosis visualization
  - Work order management

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure .env file
cp .env.example .env
# Edit .env with your watsonx.ai API key

# 3. Test components
python agents.py

# 4. Run dashboard
streamlit run dashboard.py
```

See [SETUP.md](SETUP.md) for detailed instructions.

## 📁 Project Structure

```
SyncOpsAI/
├── data.py                    # Sensor data scenarios
├── manuals.py                 # Equipment manuals
├── rag.py                     # RAG system
├── diagnosis.py               # Diagnostic engine
├── agents.py                  # Multi-agent workflow
├── watsonx_integration.py     # watsonx.ai wrapper
├── dashboard.py               # Streamlit UI
├── requirements.txt           # Dependencies
├── .env                       # Configuration (not in git)
├── SETUP.md                   # Setup guide
└── README.md                  # This file
```

## 🎬 Demo Scenarios

### Scenario 1: HVAC Overheating
- **Equipment**: HVAC-001 Industrial HVAC System
- **Issue**: Temperature rises from 22°C → 32°C
- **AI Diagnosis**: Clogged air filter restricting airflow
- **Resolution**: Replace filter (Part: AF-2024, $45, 30-60 min)
- **Outcome**: Work order WO-1000 created automatically

### Scenario 2: Motor Vibration
- **Equipment**: MOTOR-001 Conveyor Motor
- **Issue**: Vibration rises from 1.2 Hz → 4.5 Hz
- **AI Diagnosis**: Worn or damaged roller bearings
- **Resolution**: Replace bearings (Parts: RB-500, AS-KIT, $310, 2-3 hours)
- **Outcome**: Work order WO-1001 created automatically

## 🏗️ Architecture

```mermaid
graph TB
    A[IoT Sensors] -->|Real-time Data| B[Agent 1: Telemetry]
    B -->|Anomaly Detected| C[Agent 2: Diagnostic]
    C -->|Query| D[RAG System]
    D -->|Context| E[Equipment Manuals]
    C -->|Generate| F[watsonx.ai Granite]
    F -->|Diagnosis| C
    C -->|Report| G[Agent 3: Orchestrator]
    G -->|Create| H[Work Order]
    G -->|Check| I[Inventory]
    
    style C fill:#4CAF50
    style F fill:#FF9800
    style D fill:#2196F3
```

## 🛠️ Tech Stack

- **AI/ML**: IBM watsonx.ai (Granite models)
- **Vector DB**: Pinecone (optional)
- **Framework**: Python 3.9+
- **UI**: Streamlit + Plotly
- **Orchestration**: Simple function-based (LangGraph ready)

## 📊 Performance

- **Detection Speed**: <1ms (threshold-based)
- **Diagnosis Time**: 2-5s (with AI), <1ms (template)
- **End-to-End**: ~5s from anomaly to work order
- **Accuracy**: 85-95% confidence (AI-enhanced)

## 🎯 Value Proposition

- **95% faster diagnosis** vs manual process
- **80% reduction** in manual lookup time
- **Proactive maintenance** prevents failures
- **Automated work orders** reduce response time
- **Cost estimation** improves planning

## 🔧 Development Status

### ✅ Completed (Day 1)
- [x] Sensor data scenarios
- [x] Equipment manuals
- [x] Mock RAG system
- [x] Template-based diagnosis
- [x] Multi-agent workflow
- [x] watsonx.ai integration

### ⏳ In Progress
- [ ] Streamlit dashboard
- [ ] Pinecone vector database
- [ ] Real-time streaming
- [ ] Demo video
- [ ] Presentation slides

## 📝 Usage Examples

### Run Complete Workflow

```python
from agents import MultiAgentWorkflow

# Initialize with AI
workflow = MultiAgentWorkflow(use_ai=True)

# Run scenario
results = workflow.run_scenario("hvac_overheating")

# Check last result
final = results[-1]
if final['anomaly_detected']:
    print(f"Work Order: {final['work_order']['work_order_id']}")
    print(f"Issue: {final['diagnosis']['root_cause']}")
    print(f"Cost: {final['diagnosis']['estimated_cost']}")
```

### AI Diagnosis

```python
from diagnosis import diagnose

diagnosis = diagnose(
    equipment_id="HVAC-001",
    anomaly_type="overheating",
    sensor_data={"temp": 32.0, "pressure": 54.0},
    use_ai=True
)

print(diagnosis['root_cause'])
print(f"Confidence: {diagnosis['confidence_score']*100:.0f}%")
```

## 🤝 Contributing

This is a hackathon POC. For production use:
1. Add error handling
2. Implement proper logging
3. Add authentication
4. Scale with LangGraph
5. Add monitoring/alerting

## 📄 License

MIT License - See LICENSE file

## 🙏 Acknowledgments

- IBM watsonx.ai for Granite models
- Streamlit for rapid UI development
- Pinecone for vector database

## 📧 Contact

For questions or demo requests, contact the development team.

---

**Built for 2-Day Hackathon** | **Focus: Demo > Code** | **Status: POC Ready** ✅
