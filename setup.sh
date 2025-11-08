#!/bin/bash

# Leva Backend - Quick Start Script

echo "🚀 Setting up Leva Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please update DATABASE_URL in .env with your PostgreSQL credentials"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update DATABASE_URL in .env file"
echo "2. Make sure PostgreSQL is running"
echo "3. Create a database: createdb leva"
echo "4. Run the server: uvicorn app.main:app --reload"
echo "5. Visit http://localhost:8000/docs for API documentation"
