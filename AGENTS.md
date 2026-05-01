# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project-Specific Patterns (Non-Obvious)

### Component Testing
- Each Python module has `if __name__ == "__main__"` test blocks - run directly: `python <module>.py`
- Tests are embedded in source files, not separate test directories
- All modules must be tested from project root (imports assume root as working directory)

### AI Integration Architecture
- `diagnosis.py` has dual-mode operation: template (default) or AI (opt-in via `use_ai=True`)
- watsonx.ai integration gracefully degrades - if unavailable, automatically falls back to templates
- `get_watsonx_ai()` returns singleton instance - don't create multiple WatsonxAI objects
- AI diagnosis merges template results with AI insights (doesn't replace, enhances)

### Equipment ID Mapping (Hidden Coupling)
- `agents.py` hardcodes equipment_id → scenario mapping in Agent1 (lines 33-38)
- Only 4 equipment IDs work: HVAC-001, HVAC-002, MOTOR-001, MOTOR-002
- Adding new equipment requires updating both `data.py` DEMO_SCENARIOS and `agents.py` scenario_map

### RAG System Quirks
- `rag.py` uses keyword matching, not vector similarity (despite name)
- `format_for_llm()` method is specifically designed for watsonx.ai prompt format
- Anomaly type mapping in `query_manual()` (lines 40-48) - aliases like 'high_temperature' → 'overheating'

### Cost Calculation
- `diagnosis.py` parses cost strings like "$45" - format must include $ symbol
- `_calculate_total_cost()` multiplies by quantity - parts list must have 'quantity' field

### Workflow Execution
- `MultiAgentWorkflow.run_workflow()` returns immediately if no anomaly detected (only 1 step)
- Workflow history stored in `workflow_history` list - grows unbounded (no cleanup)
- Agent state is mutable - calling `run_workflow()` multiple times accumulates state

### Environment Variables
- `.env` file MUST be in project root (not in subdirectories)
- `WATSONX_PROJECT_ID` is optional - system works without it but may have limited functionality
- Missing API keys cause silent fallback to template mode (no errors thrown)

## Build/Test Commands

```bash
# Test individual components (from project root)
python data.py           # Test sensor scenarios
python manuals.py        # Test equipment manuals  
python rag.py            # Test RAG system
python diagnosis.py      # Test diagnostic engine
python agents.py         # Test multi-agent workflow
python watsonx_integration.py  # Test AI connection

# Install dependencies
pip install -r requirements.txt

# Run with AI enabled (requires .env configuration)
python -c "from agents import MultiAgentWorkflow; w = MultiAgentWorkflow(use_ai=True); print(w.run_scenario('hvac_overheating'))"
```

## Critical Gotchas

1. **Import Order**: `diagnosis.py` must import `rag` before `watsonx_integration` (circular dependency risk)
2. **Scenario Names**: Use exact strings "hvac_overheating" or "motor_vibration" - no validation, silent failures
3. **Sensor Data Keys**: Different equipment types use different sensor keys (temp vs vibration) - no schema validation
4. **Work Order IDs**: Counter starts at 1000, increments per instance - restarting resets to 1000 (not persistent)
5. **AI Model**: Uses "ibm/granite-13b-chat-v2" hardcoded - changing requires code modification, not config