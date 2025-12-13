@echo off
REM Easy Downloader Server Setup Script for Windows

echo 🚀 Setting up Easy Downloader Server...

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Copy environment file
echo ⚙️  Setting up environment variables...
if not exist .env (
    copy .env.example .env
    echo ✅ Created .env file. Please update it with your configuration.
) else (
    echo ℹ️  .env file already exists.
)

REM Create temp directories
echo 📁 Creating temporary directories...
if not exist temp\singlelink mkdir temp\singlelink
if not exist temp\multilink mkdir temp\multilink
if not exist temp\playlist mkdir temp\playlist

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Update .env file with your configuration
echo 2. Set up PostgreSQL database
echo 3. Run: python app.py
echo.

pause
