"""
Base Climate Agriculture Agent - Pure business logic.

This agent has NO observability dependencies and can run standalone.
"""

import logging
from agno.agent import Agent
from agno.models.openai import OpenAIChat

from ..config.settings import AGENT_NAME, AGENT_MODEL, API_BASE_URL
from ..tools.database_tools import query_database

logger = logging.getLogger(__name__)


class BaseClimateAgent:
    """
    Pure agent implementation without observability dependencies.
    
    This is the core business logic that can work independently
    of any monitoring or tracing system.
    """
    
    def __init__(self, instructions: list = None):
        """
        Initialize the base agent.
        
        Args:
            instructions: List of instruction strings for the agent
        """
        logger.info(f"Initializing {AGENT_NAME}")
        
        # Use provided instructions or default
        if instructions is None:
            instructions = self._get_default_instructions()
        
        # Create agent (pure Agno, no Langfuse)
        self.agent = Agent(
            name=AGENT_NAME,
            model=OpenAIChat(
                id=AGENT_MODEL,
                base_url=API_BASE_URL
            ),
            tools=[query_database],
            markdown=True,
            instructions=instructions,
        )
        
        logger.info(f"Base agent initialized successfully")
    
    def execute(self, question: str) -> str:
        """
        Execute a query - pure business logic.
        
        Args:
            question: User's question
            
        Returns:
            Agent's response text
        """
        logger.info(f"Executing query: {question[:50]}...")
        
        # Core agent execution - no observability
        response = self.agent.run(question)
        response_text = response.content
        
        logger.info(f"Query executed successfully")
        
        return response_text
    
    @staticmethod
    def _get_default_instructions():
        """Get default agent instructions."""
        return [
            "You are an expert agricultural data analyst.",
            "You have a 'query_database' tool that executes SQL queries.",
            "ALWAYS use this tool to get actual data - don't just show SQL code!",
            "Table: climate_agriculture_data",
            "Provide clear insights based on the data.",
        ]

