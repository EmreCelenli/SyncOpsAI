# SyncOpsAI Dashboard

Polished Streamlit dashboard with real-time monitoring, charts, and animations for the SyncOpsAI equipment monitoring system.

## 🎨 Features

### **Live Monitoring**
- Real-time sensor gauges with color-coded thresholds
- Animated gauge charts for temperature, pressure, vibration
- Instant anomaly detection with severity indicators
- Equipment status dashboard

### **Multi-Agent Workflow**
- Step-by-step workflow visualization
- Animated progress through 4 agent steps
- Detailed results for each agent action
- Work order creation tracking

### **Analytics Dashboard**
- Timeline chart of anomalies over time
- Cost breakdown by equipment
- Summary metrics (total workflows, costs, critical issues)
- Historical trend analysis

### **Work Order Management**
- Complete work order listing
- Detailed work order view
- Priority and status tracking
- Parts availability status

## 📦 Installation

```bash
cd dashboard
pip install -r requirements.txt
```

## 🚀 Running the Dashboard

### 1. Start the Mock API Server (Required)
```bash
# In terminal 1
cd mock_apis
python app.py
# Server runs on http://localhost:8787
```

### 2. Start the Dashboard
```bash
# In terminal 2
cd dashboard
streamlit run app.py
# Dashboard opens at http://localhost:8501
```

## 🎯 Usage Guide

### **Sidebar Configuration**

1. **Select Equipment**
   - Choose from HVAC-001, HVAC-002, MOTOR-001, MOTOR-002
   - Each equipment type has different sensors

2. **AI Features**
   - Enable watsonx.ai for AI-powered diagnosis
   - Enable Pinecone for vector-based RAG search
   - Both features gracefully degrade if unavailable

3. **Sensor Simulation**
   - Adjust sliders to simulate sensor readings
   - HVAC: Temperature & Pressure
   - Motor: Vibration & Temperature
   - Real-time gauge updates

4. **Run Workflow**
   - Click "🚀 Run Workflow" to execute
   - Watch animated step-by-step progress
   - View results in all tabs

### **Dashboard Tabs**

#### **📊 Live Monitoring**
- Real-time sensor gauges
- Color-coded status (green/yellow/red)
- Anomaly detection alerts
- Equipment metrics

#### **🔍 Workflow Details**
- Complete workflow execution
- 4-step agent process:
  1. Telemetry Listener - Anomaly detection
  2. Diagnostic Expert - Root cause analysis
  3. Orchestrator - Inventory check
  4. Orchestrator - Work order creation
- Expandable step details
- Animated progress

#### **📈 Analytics**
- Timeline scatter plot of anomalies
- Cost breakdown bar chart
- Summary metrics cards
- Historical data visualization

#### **📋 Work Orders**
- Table view of all work orders
- Detailed work order information
- Priority and status tracking
- Assignment and ETA details

## 🎨 Visual Features

### **Gauge Charts**
- Animated needle movement
- Color-coded zones (green/yellow/red)
- Threshold indicators
- Real-time value display

### **Timeline Charts**
- Scatter plot with severity colors
- Size indicates cost magnitude
- Hover for detailed information
- Time-based x-axis

### **Cost Charts**
- Bar chart by equipment
- Color-coded by severity
- Comparative analysis
- Total cost tracking

### **Status Indicators**
- ✅ Normal Operation (Green)
- ⚠️ Warning (Yellow)
- 🚨 Critical (Red)
- Real-time updates

## 🔧 Configuration

### **API Endpoint**
Default: `http://localhost:8787`

To change, edit in [`app.py`](app.py):
```python
API_BASE_URL = "http://localhost:8787"
```

### **Equipment Types**
- **HVAC Systems**: Temperature & Pressure sensors
- **Motors**: Vibration & Temperature sensors

### **Thresholds**
Configured in gauge charts:
- **HVAC Temperature**: Warning 75°C, Critical 85°C
- **HVAC Pressure**: Warning 45 PSI, Critical 50 PSI
- **Motor Vibration**: Warning 3 mm/s, Critical 5 mm/s
- **Motor Temperature**: Warning 80°C, Critical 90°C

## 📊 Demo Scenarios

### **Scenario 1: HVAC Overheating**
1. Select HVAC-001
2. Set Temperature to 88°C
3. Set Pressure to 42 PSI
4. Run Workflow
5. Observe critical anomaly detection
6. View diagnosis and work order

### **Scenario 2: Motor Vibration**
1. Select MOTOR-001
2. Set Vibration to 6.0 mm/s
3. Set Temperature to 75°C
4. Run Workflow
5. Observe warning/critical status
6. Review resolution steps

### **Scenario 3: Normal Operation**
1. Select any equipment
2. Keep sensors in green zone
3. Run Workflow
4. Confirm normal status
5. No work order created

## 🎭 Animation Features

- **Gauge Needles**: Smooth animated transitions
- **Workflow Steps**: Sequential reveal with delays
- **Status Changes**: Color transitions
- **Chart Updates**: Smooth data additions
- **Loading Spinners**: During API calls

## 📱 Responsive Design

- Wide layout for maximum screen usage
- Collapsible sidebar
- Responsive columns
- Mobile-friendly (with limitations)

## 🐛 Troubleshooting

### **"Cannot connect to Mock API"**
- Ensure Mock API server is running
- Check port 8787 is not in use
- Verify API_BASE_URL is correct

### **"No data in charts"**
- Run at least one workflow
- Check workflow completed successfully
- Verify data in session state

### **Slow performance**
- Reduce chart update frequency
- Clear workflow history
- Restart Streamlit server

## 🔗 Integration

### **With Mock API**
```python
import requests

response = requests.post(
    'http://localhost:8787/api/workflow/run',
    json={
        'equipment_id': 'HVAC-001',
        'sensor_data': {'temp': 88, 'pressure': 42}
    }
)
```

### **With watsonx Orchestrate**
Replace Mock API calls with watsonx Orchestrate agent invocations when ready for production deployment.

## 📄 Files

- [`app.py`](app.py) - Main dashboard application (445 lines)
- [`requirements.txt`](requirements.txt) - Python dependencies
- [`README.md`](README.md) - This file

## 🎯 Key Metrics Displayed

- **Total Workflows**: Count of executed workflows
- **Total Cost**: Sum of all repair costs
- **Critical Issues**: Count of critical severity anomalies
- **Average Cost**: Mean cost per workflow
- **Equipment Uptime**: Simulated uptime percentage
- **Work Order Status**: Open/Closed/In Progress

## 🚀 Production Deployment

For production use:
1. Replace Mock API with actual watsonx Orchestrate
2. Connect to real IoT sensor streams
3. Integrate with actual work order system
4. Add authentication and authorization
5. Enable HTTPS
6. Configure proper logging
7. Set up monitoring and alerts

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Charts](https://plotly.com/python/)
- [Mock API Documentation](../mock_apis/README.md)
- [watsonx Orchestrate Guide](../orchestrate/README.md)

---

**Built with ❤️ for SyncOpsAI POC Demo**