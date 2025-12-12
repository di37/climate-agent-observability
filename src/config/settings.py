"""Application configuration."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"
DB_FILE = DATA_DIR / "climate_agriculture.db"
LOG_FILE = LOG_DIR / "agent.log"

# Ensure directories exist
LOG_DIR.mkdir(exist_ok=True)

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

# Agent configuration
AGENT_NAME = os.getenv("AGENT_NAME", "Climate Agriculture Analyst")
AGENT_MODEL = os.getenv("AGENT_MODEL", "gpt-4o-2024-08-06")  # Use specific version for consistency
PROMPT_NAME = os.getenv("PROMPT_NAME", "climate-agent-instructions")

# Database configuration
TABLE_NAME = "climate_agriculture_data"

