"""Langfuse Prompt Management utilities."""

import logging
from ..config.settings import PROMPT_NAME, AGENT_MODEL

logger = logging.getLogger(__name__)


def create_agent_prompt(langfuse):
    """
    Create or update the agent prompt in Langfuse.
    This allows centralized management of agent instructions.
    
    Args:
        langfuse: Langfuse client instance
    """
    try:
        logger.info(f"Creating/updating prompt: {PROMPT_NAME}")
        
        # Create the agent system prompt
        langfuse.create_prompt(
            name=PROMPT_NAME,
            type="text",
            prompt="""You are an expert agricultural data analyst specializing in climate change impacts.

IMPORTANT: You have a 'query_database' tool that executes SQL queries.
ALWAYS use this tool to get actual data - don't just show SQL code!

DATABASE SCHEMA:
Table: climate_agriculture_data
Columns:
  - Year, Country, Region, Crop_Type
  - Average_Temperature_C, Total_Precipitation_mm, CO2_Emissions_MT
  - Crop_Yield_MT_per_HA, Extreme_Weather_Events
  - Irrigation_Access_%, Pesticide_Use_KG_per_HA, Fertilizer_Use_KG_per_HA
  - Soil_Health_Index, Adaptation_Strategies, Economic_Impact_Million_USD

When answering questions:
1. Use the exact table name: climate_agriculture_data
2. Use exact column names as listed above
3. Execute SQL queries to get actual data
4. Provide clear, actionable insights
5. Include specific numbers and statistics
6. Offer recommendations when relevant""",
            labels=["production"],  # Promote to production
            config={
                "model": AGENT_MODEL,
                "temperature": 0.7,
                "max_tokens": 2000,
            },
        )
        
        logger.info(f"Prompt '{PROMPT_NAME}' created/updated successfully")
        return True
        
    except Exception as e:
        logger.warning(f"Prompt creation note: {e} (may already exist)")
        return False


def get_agent_instructions(langfuse, use_managed_prompts=True):
    """
    Fetch agent instructions from Langfuse Prompt Management.
    Falls back to default if prompt doesn't exist.
    
    Args:
        langfuse: Langfuse client instance
        use_managed_prompts: Whether to fetch from Langfuse
        
    Returns:
        Tuple of (instructions list, managed_prompt object or None)
    """
    if not use_managed_prompts:
        logger.info("Using default (non-managed) instructions")
        return get_default_instructions(), None
    
    try:
        # Fetch the prompt from Langfuse
        logger.info(f"Fetching managed prompt: {PROMPT_NAME}")
        prompt = langfuse.get_prompt(PROMPT_NAME, type="text")
        logger.info(f"Using managed prompt version {prompt.version}")
        
        return [prompt.prompt], prompt
        
    except Exception as e:
        logger.warning(f"Could not fetch managed prompt: {e}")
        logger.info("Falling back to default instructions")
        return get_default_instructions(), None


def get_default_instructions():
    """Get default agent instructions."""
    return [
        "You are an expert agricultural data analyst.",
        "You have a 'query_database' tool that executes SQL queries.",
        "ALWAYS use this tool to get actual data - don't just show SQL code!",
        "Table: climate_agriculture_data",
        "Provide clear insights based on the data.",
    ]

