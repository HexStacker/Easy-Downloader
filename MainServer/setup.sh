#!/bin/bash

# Easy Downloader Server Setup Script

echo "🚀 Setting up Easy Downloader Server..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file
echo "⚙️  Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file. Please update it with your configuration."
else
    echo "ℹ️  .env file already exists."
fi

# Create temp directories
echo "📁 Creating temporary directories..."
mkdir -p temp/singlelink
mkdir -p temp/multilink
mkdir -p temp/playlist

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your configuration"
echo "2. Set up PostgreSQL database"
echo "3. Run: python app.py"
echo ""
