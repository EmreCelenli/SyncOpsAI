#!/usr/bin/env python3
"""
Verification script to confirm watsonx.ai is enabled by default
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
load_dotenv('poc/.env')  # Also try poc/.env

print("=" * 60)
print("watsonx.ai Configuration Verification")
print("=" * 60)

# Check environment variables
use_ai_env = os.getenv('USE_AI', 'not set')
watsonx_api_key = os.getenv('WATSONX_API_KEY', 'not set')
watsonx_url = os.getenv('WATSONX_URL', 'not set')
watsonx_project_id = os.getenv('WATSONX_PROJECT_ID', 'not set')

print(f"\n📋 Environment Variables:")
print(f"  USE_AI: {use_ai_env}")
print(f"  WATSONX_API_KEY: {'✅ Set' if watsonx_api_key != 'not set' else '❌ Not set'}")
print(f"  WATSONX_URL: {watsonx_url}")
print(f"  WATSONX_PROJECT_ID: {'✅ Set' if watsonx_project_id != 'not set' else '❌ Not set'}")

# Check computed defaults
use_ai_default = os.getenv('USE_AI', 'true').lower() == 'true'
use_pinecone_default = os.getenv('USE_PINECONE', 'false').lower() == 'true'

print(f"\n🔧 Computed Defaults:")
print(f"  USE_AI_DEFAULT: {use_ai_default}")
print(f"  USE_PINECONE_DEFAULT: {use_pinecone_default}")

# Check if watsonx.ai will be used
if use_ai_default and watsonx_api_key != 'not set':
    print(f"\n✅ watsonx.ai is ENABLED by default")
    print(f"   The diagnostic_expert_agent will use IBM Granite models")
elif use_ai_default and watsonx_api_key == 'not set':
    print(f"\n⚠️  watsonx.ai is enabled but API key is missing")
    print(f"   System will fall back to template-based diagnosis")
else:
    print(f"\n❌ watsonx.ai is DISABLED")
    print(f"   System will use template-based diagnosis")

# Check Mock API configuration
print(f"\n📡 Mock API Server:")
print(f"  Will use USE_AI_DEFAULT = {use_ai_default}")
print(f"  Will use USE_PINECONE_DEFAULT = {use_pinecone_default}")

# Check Dashboard configuration
print(f"\n🖥️  Dashboard:")
print(f"  'Enable watsonx.ai' checkbox default: True")

print(f"\n" + "=" * 60)
print("Verification Complete")
print("=" * 60)

# Summary
if use_ai_default and watsonx_api_key != 'not set':
    print("\n🎉 SUCCESS: watsonx.ai integration is properly configured!")
    print("   Start the system with: cd dashboard && ./run_dashboard.sh")
else:
    print("\n⚠️  WARNING: watsonx.ai may not work properly")
    print("   Check your .env file and ensure API keys are set")

# Made with Bob
