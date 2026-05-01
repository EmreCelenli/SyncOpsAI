# Installation Guide for SyncOps AI POC

## Quick Install (Recommended)

```bash
# 1. Upgrade pip and install build tools first
pip install --upgrade pip setuptools wheel

# 2. Install all dependencies
pip install -r requirements.txt
```

## Step-by-Step Install (If Quick Install Fails)

### Step 1: Install Build Tools
```bash
pip install --upgrade pip
pip install setuptools>=65.0.0
pip install wheel>=0.38.0
```

### Step 2: Install Core Dependencies
```bash
pip install python-dotenv
pip install pandas numpy
```

### Step 3: Install LangGraph and LangChain
```bash
pip install langgraph>=0.2.0
pip install langchain>=0.3.0
pip install langchain-core>=0.3.0
```

### Step 4: Install Streamlit
```bash
pip install streamlit>=1.28.0
pip install plotly>=5.17.0
```

### Step 5: Install watsonx.ai (May take a few minutes)
```bash
pip install ibm-watsonx-ai>=0.2.0
```

### Step 6: Install Pinecone
```bash
pip install pinecone-client>=3.0.0
```

## Troubleshooting

### Error: "setuptools is not available"

**Solution:**
```bash
pip install --upgrade setuptools wheel
pip install -r requirements.txt
```

### Error: "ibm-cos-sdk" fails to install

**Solution:**
```bash
# Install setuptools first
pip install setuptools>=65.0.0

# Then try again
pip install ibm-watsonx-ai
```

### Error: "No module named 'langgraph'"

**Solution:**
```bash
pip install langgraph langchain langchain-core
```

### Error: "Streamlit not found"

**Solution:**
```bash
pip install streamlit plotly
```

## Verify Installation

```bash
# Test Python imports
python -c "import langgraph; print('✅ LangGraph installed')"
python -c "import streamlit; print('✅ Streamlit installed')"
python -c "import pandas; print('✅ Pandas installed')"

# Test watsonx.ai (optional - will show warning if not configured)
python -c "try:
    from ibm_watsonx_ai.foundation_models import ModelInference
    print('✅ watsonx.ai installed')
except ImportError:
    print('⚠️  watsonx.ai not installed')"

# Test Pinecone (optional)
python -c "try:
    import pinecone
    print('✅ Pinecone installed')
except ImportError:
    print('⚠️  Pinecone not installed')"
```

## Configuration

### 1. Create .env file
```bash
cp .env.example .env
```

### 2. Edit .env with your credentials
```bash
# Required for AI-powered diagnosis
WATSONX_API_KEY=your_api_key_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_PROJECT_ID=your_project_id_here

# Required for vector database
PINECONE_API_KEY=your_pinecone_key_here
PINECONE_ENVIRONMENT=your_pinecone_env_here
```

## Test the Installation

### Test 1: Run main workflow
```bash
python main.py
```

Expected output:
- Both scenarios run
- Agent messages display
- Work orders created

### Test 2: Run dashboard
```bash
streamlit run dashboard.py
```

Expected behavior:
- Dashboard opens in browser
- Can select scenarios
- Agents execute when button clicked

### Test 3: Run integration test
```bash
python test_integration.py
```

Expected output:
- All modules import successfully
- Both scenarios complete
- No errors

## Minimal Install (Without AI)

If you just want to test the POC without watsonx.ai or Pinecone:

```bash
# Install only core dependencies
pip install langgraph langchain langchain-core
pip install streamlit plotly
pip install pandas numpy
pip install python-dotenv
```

The system will automatically use mock/template mode.

## Python Version

**Required:** Python 3.9 or higher

Check your version:
```bash
python --version
```

If you need to upgrade:
```bash
# Using conda
conda install python=3.11

# Using pyenv
pyenv install 3.11.0
pyenv global 3.11.0
```

## Common Issues

### Issue: "Command 'python' not found"

**Solution:** Use `python3` instead:
```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

### Issue: "Permission denied"

**Solution:** Use `--user` flag:
```bash
pip install --user -r requirements.txt
```

### Issue: "SSL Certificate Error"

**Solution:** Use trusted host:
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

## Success!

If all tests pass, you're ready to run the demo:

```bash
# Option 1: Command-line demo
python main.py

# Option 2: Visual dashboard
streamlit run dashboard.py
```

## Need Help?

1. Check error messages carefully
2. Verify Python version (3.9+)
3. Try step-by-step install
4. Check internet connection
5. Review `.env` configuration

For more help, see:
- `README.md` - Project overview
- `demo_script.md` - Demo walkthrough
- `INTEGRATION_COMPLETE.md` - Integration details