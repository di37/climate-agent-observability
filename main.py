#!/usr/bin/env python3
"""
Main entry point for Climate Agriculture Agent.

Uses the new separated architecture:
- BaseClimateAgent: Pure business logic (no observability)
- ObservedClimateAgent: Wraps base with Langfuse observability

Features:
- Clean separation of concerns
- Optional observability
- Full Langfuse integration (tracing, scoring, prompt management)
- SQL execution on climate agriculture database
- User feedback support
- Proper logging
"""

import sys
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.config.settings import DB_FILE, LANGFUSE_HOST
from src.custom_log import setup_logging
from src.utils.validators import validate_database, validate_environment
from src.observability.tracing import initialize_langfuse_tracing
from src.observability.prompts import create_agent_prompt
# Import the new separated agents
# BaseClimateAgent = Pure logic, no observability
# ObservedClimateAgent = With full Langfuse integration
from src.agents import ObservedClimateAgent as ClimateAgent

# Setup logging
logger = setup_logging()


def print_banner():
    """Print application banner."""
    print("\n" + "="*80)
    print("🌱 CLIMATE AGRICULTURE AGENT")
    print("="*80)
    print("\n🎯 Features:")
    print("   ✓ Natural language queries")
    print("   ✓ SQL execution on 10,000 climate records")
    print("   ✓ Full Langfuse observability")
    print("   ✓ Automatic quality scoring")
    print("   ✓ User feedback (👍👎)")
    print("   ✓ Centralized prompt management")
    print("   ✓ Logging to file")
    print("="*80 + "\n")


def show_usage():
    """Show usage information."""
    print("\n📖 Usage:")
    print("  python main.py                    # Interactive chat")
    print("  python main.py --demo             # Run demo queries")
    print("  python main.py --create-prompt    # Setup managed prompt")
    print("  python main.py --help             # Show this help")
    print("\n📚 Documentation:")
    print("  docs/QUICK_REFERENCE.md          # Quick commands")
    print("  docs/USER_FEEDBACK_GUIDE.md      # User feedback")
    print("  docs/PROMPT_MANAGEMENT_GUIDE.md  # Prompt management")
    print()


def main():
    """Main application entry point."""
    logger.info("="*60)
    logger.info("Climate Agriculture Agent - Starting")
    logger.info("="*60)
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help', 'help']:
            print_banner()
            show_usage()
            return
    
    # Validate environment
    logger.info("Validating environment...")
    env_check = validate_environment()
    if not env_check["valid"]:
        logger.error(f"Missing environment variables: {env_check['missing']}")
        print("\n❌ Please set up your .env file with:")
        for var in env_check["missing"]:
            print(f"   {var}=...")
        sys.exit(1)
    logger.info("Environment validation passed")
    
    # Validate database
    logger.info(f"Checking database: {DB_FILE}")
    validate_database(DB_FILE)
    logger.info("Database validation passed")
    
    # Initialize Langfuse
    logger.info("Initializing Langfuse tracing...")
    print("\n🔧 Initializing Langfuse with full observability...")
    
    langfuse = initialize_langfuse_tracing()
    
    if not langfuse.auth_check():
        logger.warning("Langfuse authentication failed")
        print("⚠️  Langfuse authentication failed")
        print("   Check LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY")
    else:
        logger.info("Langfuse authenticated successfully")
        print("✅ Langfuse: Tracing, Scoring, Prompts all active")
    
    print(f"✅ Database: {DB_FILE.name}")
    print(f"✅ Logs: {Path('logs/agent.log')}")
    print(f"✅ Dashboard: {LANGFUSE_HOST}\n")
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--demo":
            logger.info("Running demo mode")
            print("📊 Running demo with 3 example queries...\n")
            
            # Run demo inline
            agent = ClimateAgent()
            
            examples = [
                "What are the top 3 countries by average crop yield?",
                "How many extreme weather events occurred in India?",
                "Compare the economic impact of different adaptation strategies",
            ]
            
            logger.info(f"Running {len(examples)} demo queries")
            
            for i, question in enumerate(examples, 1):
                print(f"\n{'='*80}")
                print(f"Query {i}: {question}")
                print('='*80 + "\n")
                
                logger.info(f"Processing query {i}")
                result = agent.query(question)
                
                print(f"{result['response']}")
                print(f"\n📊 Trace: {result['trace_id']}")
                print("="*80)
            
            logger.info("Demo completed successfully")
            print("\n✅ Demo complete! Check Langfuse dashboard.\n")
            
        elif command == "--create-prompt":
            logger.info("Creating/updating managed prompt")
            print("📝 Creating/updating agent prompt in Langfuse...\n")
            create_agent_prompt(langfuse)
            print("\n✅ Done! View your prompt at:")
            print(f"   {LANGFUSE_HOST}/prompts\n")
            
        elif command == "--version":
            print("Climate Agriculture Agent v1.0.0")
            print("Agno + Langfuse + OpenLIT integration\n")
            
        else:
            logger.warning(f"Unknown command: {command}")
            show_usage()
    else:
        # Interactive chat mode
        logger.info("Starting interactive chat mode")
        print_banner()
        
        agent = ClimateAgent()
        agent.chat()
    
    logger.info("Application shutting down")
    logger.info("="*60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        print("\n\n👋 Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n❌ Unexpected error: {e}\n")
        sys.exit(1)

