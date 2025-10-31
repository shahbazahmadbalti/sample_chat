#!/bin/bash

echo "🤖 Starting Sample Chatbot..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check for OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY not found in environment"
    echo "Please set your OpenAI API key:"
    echo "export OPENAI_API_KEY=your_api_key_here"
    echo ""
    echo "Or create a .env file with your API key"
fi

# Start the server
echo "🚀 Starting server on http://localhost:8000"
python backend/main.py