"""
Streamlit dashboard for SyncOps AI POC
Visual demonstration of multi-agent workflow
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from poc.state import create_initial_state
from poc.main import build_graph
from poc.data import DEMO_SCENARIOS


def main():
    """Main dashboard application"""
    
    # Page config
    st.set_page_config(
        page_title="SyncOps AI - Multi-Agent Anomaly Detection",
        page_icon="🤖",
        layout="wide"
    )
    
    # Title
    st.title("🤖 SyncOps AI")
    st.subheader("Multi-Agent Anomaly Detection & Automated Response")
    
    st.markdown("---")
    
    # Sidebar: Scenario selection
    st.sidebar.header("Demo Controls")
    scenario_name = st.sidebar.selectbox(
        "Select Scenario",
        [s["name"] for s in DEMO_SCENARIOS]
    )
    
    # Get selected scenario
    scenario = next(s for s in DEMO_SCENARIOS if s["name"] == scenario_name)
    
    # Display scenario info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Equipment ID", scenario["equipment_id"])
    
    with col2:
        st.metric(
            f"{scenario['sensor_type'].title()} Reading",
            f"{scenario['sensor_value']}"
        )
    
    with col3:
        st.metric("Expected Issue", scenario["expected_anomaly"].title())
    
    st.markdown("---")
    
    # Run button
    if st.button("🚀 Run AI Agents", type="primary", use_container_width=True):
        
        # Create initial state
        state = create_initial_state(
            equipment_id=scenario["equipment_id"],
            sensor_value=scenario["sensor_value"],
            sensor_type=scenario["sensor_type"]
        )
        
        # Progress indicator
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Build workflow
        status_text.text("Building workflow...")
        progress_bar.progress(10)
        workflow = build_graph()
        
        # Execute workflow
        status_text.text("Running agents...")
        progress_bar.progress(30)
        
        result = workflow.invoke(state)
        
        progress_bar.progress(100)
        status_text.text("✅ Workflow complete!")
        
        # Display results
        st.markdown("---")
        st.header("📊 Results")
        
        # Agent activity log
        st.subheader("🔄 Agent Activity Log")
        log_container = st.container()
        
        with log_container:
            for msg in result["messages"]:
                # Color code by agent
                if "Agent 1" in msg:
                    st.info(msg)
                elif "Agent 2" in msg:
                    st.success(msg)
                elif "Agent 3" in msg:
                    st.warning(msg)
                else:
                    st.text(msg)
        
        st.markdown("---")
        
        # Final results
        if result["anomaly"]:
            st.subheader("🚨 Anomaly Detected")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Diagnosis**")
                st.write(result["diagnosis"])
                
                st.markdown("**Parts Needed**")
                for part in result["parts_needed"]:
                    st.write(f"- {part}")
                
                st.markdown("**Estimated Time**")
                st.write(result["estimated_time"])
            
            with col2:
                st.markdown("**Work Order**")
                st.code(result["work_order_id"], language=None)
                
                st.markdown("**Parts Availability**")
                if result["parts_available"]:
                    st.success("✅ All parts in stock")
                else:
                    st.warning("⚠️ Some parts on backorder")
                
                st.markdown("**Next Steps**")
                st.write("1. Assign to technician")
                st.write("2. Schedule maintenance")
                st.write("3. Monitor repair progress")
            
            # Business value
            st.markdown("---")
            st.subheader("💰 Business Impact")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Response Time", "< 1 second", delta="-99% vs manual")
            
            with col2:
                st.metric("Downtime Prevented", "4 hours", delta="Proactive detection")
            
            with col3:
                st.metric("Cost Savings", "$2,400", delta="Labor + downtime")
        
        else:
            st.success("✅ No anomalies detected - Equipment operating normally")
    
    # Sidebar: Info
    st.sidebar.markdown("---")
    st.sidebar.header("About")
    st.sidebar.info(
        """
        **SyncOps AI** uses 3 AI agents to:
        
        1. 🔍 **Agent 1**: Detect anomalies in real-time
        2. 🧠 **Agent 2**: Diagnose root causes using AI
        3. 📋 **Agent 3**: Create work orders automatically
        
        **Technology Stack:**
        - LangGraph for agent orchestration
        - watsonx.ai for diagnosis
        - watsonx Orchestrate for automation
        """
    )
    
    st.sidebar.markdown("---")
    st.sidebar.caption("POC Demo - 2-Day Hackathon")


if __name__ == "__main__":
    main()

# Made with Bob
