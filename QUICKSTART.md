# SyncOps AI - Quick Start Guide

## Running the POC

### Option 1: Run from Project Root (Recommended)
```bash
# Run the main workflow
python -m poc.main

# Run the dashboard
streamlit run poc/dashboard.py

# Run integration tests
python -m poc.test_integration
```

### Option 2: Run with Python Module Flag
```bash
# From project root
python -m poc.main
```

## AI Integration Setup

### Current Status
✅ Your `.env` file has valid API keys configured!

### AI Integration (Always Enabled)

1. **Your `.env` file** (in `poc/.env`) has valid credentials:
```bash
# watsonx.ai Configuration
WATSONX_API_KEY=your_api_key_here
WATSONX_URL=https://au-syd.dai.cloud.ibm.com/
WATSONX_PROJECT_ID=your_project_id_here

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_key_here
```

2. **The system automatically uses**:
   - Use IBM Granite-Embedding for RAG
   - Use IBM Granite-Vision-4.1-4B for diagnosis
   - Query equipment manuals from vector database
   - Generate AI-powered root cause analysis

### What You'll See with Real AI

**AI-Powered Diagnosis** (using IBM Granite + Pinecone):
```
Root Cause: [AI-generated analysis based on sensor data + equipment manual]
Parts: [AI-extracted from manual with part numbers and costs]
Time: [AI-estimated based on complexity]
Confidence: [AI confidence score]

Example:
🔍 Agent 2: Diagnosis complete (using watsonx.ai)
   Root Cause: Refrigerant leak detected in compressor unit causing elevated temperature readings
   Parts Needed: Compressor Seal Kit CS-2024 ($85), Refrigerant R-410A ($120)
   Estimated Time: 3-4 hours
```

## Testing AI Integration

### Step 1: Verify Environment
```bash
# Check if .env is loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv('poc/.env'); print('✅ API Key loaded:', bool(os.getenv('WATSONX_API_KEY')))"
```

### Step 2: Test watsonx.ai Connection
```bash
# Run integration test
python -m poc.test_integration
```

Expected output:
```
1. Checking Developer A's modules...
✅ Developer A's modules imported successfully

2. Checking Developer B's modules...
✅ Developer B's modules imported successfully

3. Testing HVAC Overheating Scenario...
🔥 Agent 1: ANOMALY DETECTED!
🔍 Agent 2: Diagnosis complete (using AI)
📋 Agent 3: Work order created
```

### Step 3: Run Full Demo
```bash
# Run all scenarios with AI
python -m poc.main
```

### Step 4: Launch Dashboard
```bash
# Interactive demo with AI
streamlit run poc/dashboard.py
```

## Troubleshooting

### "No module named 'poc'" Error
**Solution**: Always run from project root, not from inside poc/ directory
```bash
# ❌ Wrong
cd poc
python main.py

# ✅ Correct
python -m poc.main
```

### AI Not Working
1. Check `.env` file exists in `poc/` directory
2. Verify API keys are valid (no quotes, no spaces)
3. Check watsonx.ai and Pinecone credentials
4. Run: `python -m poc.test_integration` to see detailed error

### Import Errors
Make sure `poc/__init__.py` exists (it should be created automatically)

## Demo Scenarios

### Scenario 1: HVAC Overheating
- Equipment: HVAC-001
- Sensor: Temperature = 32°C (threshold: 28°C)
- Expected: Overheating anomaly detected
- AI Diagnosis: Analyzes temperature, pressure, current readings

### Scenario 2: Motor Vibration
- Equipment: MOTOR-001  
- Sensor: Vibration = 4.2 Hz (threshold: 3.0 Hz)
- Expected: Vibration anomaly detected
- AI Diagnosis: Analyzes vibration patterns, bearing condition

## Next Steps

1. ✅ Run `python -m poc.main` to see real AI diagnosis
2. ✅ Launch `streamlit run poc/dashboard.py` for interactive demo
3. ✅ Check Agent 2 output to see IBM Granite AI-generated diagnosis
4. ✅ Verify Pinecone vector search is working in the logs

---

**Note**: This is a fully functional system using real IBM watsonx.ai and Pinecone. The system will automatically use AI if credentials are valid, or gracefully fall back to templates if unavailable.