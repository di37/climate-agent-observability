"""Validation utilities."""

from pathlib import Path
import sys


def validate_database(db_path: Path) -> bool:
    """
    Validate that the database exists.
    
    Args:
        db_path: Path to database file
        
    Returns:
        True if valid, exits otherwise
    """
    if not db_path.exists():
        print(f"❌ Error: Database not found at {db_path}")
        print("   Run: python scripts/ingest_data.py")
        sys.exit(1)
    return True


def validate_environment() -> dict:
    """
    Validate required environment variables.
    
    Returns:
        Dict with validation results
    """
    import os
    
    required = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "LANGFUSE_PUBLIC_KEY": os.getenv("LANGFUSE_PUBLIC_KEY"),
        "LANGFUSE_SECRET_KEY": os.getenv("LANGFUSE_SECRET_KEY"),
    }
    
    missing = [key for key, val in required.items() if not val]
    
    if missing:
        print(f"⚠️  Missing environment variables: {', '.join(missing)}")
        print("   Check your .env file")
        return {"valid": False, "missing": missing}
    
    return {"valid": True, "missing": []}

