"""
SyncOpsAI - Streamlit Dashboard
Polished dashboard with charts, animations, and real-time monitoring
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import json

# Page configuration
st.set_page_config(
    page_title="SyncOpsAI - Equipment Monitoring",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .status-normal {
        color: #28a745;
        font-weight: bold;
    }
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    .status-critical {
        color: #dc3545;
        font-weight: bold;
    }
    .agent-step {
        background-color: #e9ecef;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8787"

# Initialize session state
if 'workflow_history' not in st.session_state:
    st.session_state.workflow_history = []
if 'sensor_history' not in st.session_state:
    st.session_state.sensor_history = []
if 'work_orders' not in st.session_state:
    st.session_state.work_orders = []

def call_api(endpoint, method='GET', data=None):
    """Call Mock API endpoint"""
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == 'POST':
            response = requests.post(url, json=data, timeout=5)
        else:
            response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to Mock API. Please start the server: `python mock_apis/app.py`")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def create_gauge_chart(value, title, max_value, threshold_warning, threshold_critical):
    """Create animated gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 20}},
        delta={'reference': threshold_warning},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, threshold_warning], 'color': "lightgreen"},
                {'range': [threshold_warning, threshold_critical], 'color': "yellow"},
                {'range': [threshold_critical, max_value], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': threshold_critical
            }
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    return fig

def create_timeline_chart(history):
    """Create workflow timeline chart"""
    if not history:
        return None
    
    df = pd.DataFrame(history)
    fig = px.scatter(df, x='timestamp', y='severity', 
                     color='anomaly_type',
                     size='cost_numeric',
                     hover_data=['equipment_id', 'work_order_id'],
                     title="Anomaly Timeline")
    fig.update_layout(height=300)
    return fig

def create_cost_chart(history):
    """Create cost breakdown chart"""
    if not history:
        return None
    
    df = pd.DataFrame(history)
    fig = px.bar(df, x='equipment_id', y='cost_numeric',
                 color='severity',
                 title="Repair Costs by Equipment",
                 labels={'cost_numeric': 'Cost ($)'})
    fig.update_layout(height=300)
    return fig

# Header
st.markdown('<div class="main-header">🔧 SyncOpsAI Equipment Monitoring</div>', unsafe_allow_html=True)
st.markdown("**AI-Powered Predictive Maintenance System**")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Equipment selection
    equipment_id = st.selectbox(
        "Select Equipment",
        ["HVAC-001", "HVAC-002", "MOTOR-001", "MOTOR-002"],
        help="Choose equipment to monitor"
    )
    
    # AI Features
    st.subheader("AI Features")
    use_ai = st.checkbox("Enable watsonx.ai", value=False, 
                         help="Use AI-powered diagnosis (requires watsonx.ai)")
    use_pinecone = st.checkbox("Enable Pinecone RAG", value=False,
                               help="Use vector search for manuals (requires Pinecone)")
    
    # Sensor simulation
    st.subheader("Sensor Simulation")
    if equipment_id.startswith("HVAC"):
        temp = st.slider("Temperature (°C)", 20, 100, 75)
        pressure = st.slider("Pressure (PSI)", 30, 60, 45)
        sensor_data = {"temp": temp, "pressure": pressure}
    else:
        vibration = st.slider("Vibration (mm/s)", 0.0, 10.0, 3.0, 0.1)
        temp = st.slider("Temperature (°C)", 40, 100, 70)
        sensor_data = {"vibration": vibration, "temp": temp}
    
    # Run workflow button
    st.markdown("---")
    run_workflow = st.button("🚀 Run Workflow", type="primary", use_container_width=True)
    
    # API Status
    st.markdown("---")
    st.subheader("API Status")
    health = call_api("/health")
    if health:
        st.success("✅ Connected")
        st.caption(f"Service: {health.get('service', 'Unknown')}")
    else:
        st.error("❌ Disconnected")

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📊 Live Monitoring", "🔍 Workflow Details", "📈 Analytics", "📋 Work Orders"])

with tab1:
    # Live sensor gauges
    st.subheader("Real-Time Sensor Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if equipment_id.startswith("HVAC"):
            fig = create_gauge_chart(sensor_data['temp'], "Temperature (°C)", 100, 75, 85)
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig = create_gauge_chart(sensor_data['vibration'], "Vibration (mm/s)", 10, 3, 5)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if equipment_id.startswith("HVAC"):
            fig = create_gauge_chart(sensor_data['pressure'], "Pressure (PSI)", 60, 45, 50)
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig = create_gauge_chart(sensor_data['temp'], "Temperature (°C)", 100, 80, 90)
            st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        # Status indicator
        st.markdown("### System Status")
        
        # Check for anomaly
        anomaly_check = call_api("/api/tools/detect_anomaly", "POST", {
            "equipment_id": equipment_id,
            "sensor_data": sensor_data
        })
        
        if anomaly_check and anomaly_check.get('success'):
            result = anomaly_check['result']
            if result['anomaly_detected']:
                severity = result['severity']
                if severity == 'critical':
                    st.error(f"🚨 CRITICAL: {result['anomaly_type']}")
                elif severity == 'warning':
                    st.warning(f"⚠️ WARNING: {result['anomaly_type']}")
                else:
                    st.info(f"ℹ️ {result['anomaly_type']}")
            else:
                st.success("✅ Normal Operation")
        
        # Equipment info
        st.metric("Equipment ID", equipment_id)
        st.metric("Uptime", "99.8%")

with tab2:
    st.subheader("Multi-Agent Workflow")
    
    if run_workflow:
        with st.spinner("Running workflow..."):
            # Call workflow API
            workflow_result = call_api("/api/workflow/run", "POST", {
                "equipment_id": equipment_id,
                "sensor_data": sensor_data,
                "use_ai": use_ai,
                "use_pinecone": use_pinecone
            })
            
            if workflow_result and workflow_result.get('success'):
                st.success("✅ Workflow completed successfully!")
                
                # Display workflow steps with animation
                steps = workflow_result.get('steps', [])
                
                for i, step in enumerate(steps):
                    with st.expander(f"Step {step['step']}: {step['agent']}", expanded=True):
                        st.markdown(f"**Action:** {step['action']}")
                        
                        # Display result based on step
                        if step['step'] == 1:
                            result = step['result']
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Anomaly Detected", "Yes" if result['anomaly_detected'] else "No")
                            with col2:
                                st.metric("Severity", result.get('severity', 'N/A'))
                            if result['anomaly_detected']:
                                st.info(f"**Type:** {result['anomaly_type']}")
                        
                        elif step['step'] == 2:
                            result = step['result']
                            st.markdown(f"**Root Cause:** {result.get('root_cause', 'N/A')}")
                            st.markdown("**Resolution Steps:**")
                            for idx, res_step in enumerate(result.get('resolution_steps', []), 1):
                                st.markdown(f"{idx}. {res_step}")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Estimated Cost", result.get('estimated_cost', '$0'))
                            with col2:
                                st.metric("Severity", result.get('severity', 'N/A'))
                        
                        elif step['step'] == 3:
                            result = step['result']
                            st.markdown("**Parts Availability:**")
                            for part in result.get('parts_status', []):
                                status = "✅" if part['available'] else "❌"
                                st.markdown(f"{status} {part['part_number']} - Stock: {part['stock']}")
                        
                        elif step['step'] == 4:
                            result = step['result']
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Work Order ID", result.get('work_order_id', 'N/A'))
                            with col2:
                                st.metric("Priority", result.get('priority', 'N/A'))
                            with col3:
                                st.metric("Status", result.get('status', 'N/A'))
                    
                    # Add delay for animation effect
                    time.sleep(0.3)
                
                # Store in history
                summary = workflow_result.get('summary', {})
                st.session_state.workflow_history.append({
                    'timestamp': datetime.now(),
                    'equipment_id': equipment_id,
                    'anomaly_type': summary.get('anomaly_type', 'N/A'),
                    'severity': summary.get('severity', 'N/A'),
                    'work_order_id': summary.get('work_order_id', 'N/A'),
                    'cost': summary.get('estimated_cost', '$0'),
                    'cost_numeric': float(summary.get('estimated_cost', '$0').replace('$', ''))
                })
            else:
                st.error("❌ Workflow failed")
    else:
        st.info("👆 Click 'Run Workflow' in the sidebar to start")

with tab3:
    st.subheader("Analytics Dashboard")
    
    if st.session_state.workflow_history:
        # Timeline chart
        timeline_fig = create_timeline_chart(st.session_state.workflow_history)
        if timeline_fig:
            st.plotly_chart(timeline_fig, use_container_width=True)
        
        # Cost chart
        cost_fig = create_cost_chart(st.session_state.workflow_history)
        if cost_fig:
            st.plotly_chart(cost_fig, use_container_width=True)
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Workflows", len(st.session_state.workflow_history))
        
        with col2:
            total_cost = sum(w['cost_numeric'] for w in st.session_state.workflow_history)
            st.metric("Total Cost", f"${total_cost:.2f}")
        
        with col3:
            critical_count = sum(1 for w in st.session_state.workflow_history if w['severity'] == 'critical')
            st.metric("Critical Issues", critical_count)
        
        with col4:
            avg_cost = total_cost / len(st.session_state.workflow_history)
            st.metric("Avg Cost", f"${avg_cost:.2f}")
    else:
        st.info("No workflow data yet. Run a workflow to see analytics.")

with tab4:
    st.subheader("Work Orders")
    
    # Fetch work orders from API
    work_orders_response = call_api("/api/work_orders")
    
    if work_orders_response and work_orders_response.get('success'):
        work_orders = work_orders_response.get('work_orders', [])
        
        if work_orders:
            # Display as table
            df = pd.DataFrame(work_orders)
            st.dataframe(df[['work_order_id', 'equipment_id', 'priority', 'status', 'estimated_cost', 'assigned_to']], 
                        use_container_width=True)
            
            # Work order details
            st.markdown("---")
            selected_wo = st.selectbox("Select Work Order for Details", 
                                      [wo['work_order_id'] for wo in work_orders])
            
            if selected_wo:
                wo = next((w for w in work_orders if w['work_order_id'] == selected_wo), None)
                if wo:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Work Order Details**")
                        st.markdown(f"**ID:** {wo['work_order_id']}")
                        st.markdown(f"**Equipment:** {wo['equipment_id']}")
                        st.markdown(f"**Priority:** {wo['priority']}")
                        st.markdown(f"**Status:** {wo['status']}")
                        st.markdown(f"**Cost:** {wo['estimated_cost']}")
                    
                    with col2:
                        st.markdown("**Assignment**")
                        st.markdown(f"**Assigned To:** {wo['assigned_to']}")
                        st.markdown(f"**Created:** {wo['created_at'][:19]}")
                        st.markdown(f"**ETA:** {wo['estimated_completion_hours']} hours")
                        
                        if wo.get('parts_ordered'):
                            st.success("✅ Parts Ordered")
                        else:
                            st.info("ℹ️ No parts required")
        else:
            st.info("No work orders yet. Run a workflow to create one.")
    else:
        st.warning("Could not fetch work orders from API")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🔧 SyncOpsAI v1.0")
with col2:
    st.caption("Powered by IBM watsonx")
with col3:
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Made with Bob
