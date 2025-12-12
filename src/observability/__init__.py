"""
Observability module for Langfuse integration.

This module contains all tracing, scoring, and prompt management functionality
for complete LLM observability.

Modules:
- tracing: Langfuse initialization and OpenLIT setup
- scoring: Automatic quality scoring and user feedback
- prompts: Centralized prompt management
- wrapper: Generic wrapper for any agent
"""

from .tracing import initialize_langfuse_tracing
from .scoring import score_response, add_user_feedback_score
from .prompts import create_agent_prompt, get_agent_instructions
from .wrapper import ObservabilityWrapper, wrap_agent_with_observability

__all__ = [
    # Tracing
    'initialize_langfuse_tracing',
    
    # Scoring
    'score_response',
    'add_user_feedback_score',
    
    # Prompts
    'create_agent_prompt',
    'get_agent_instructions',
    
    # Wrapper
    'ObservabilityWrapper',
    'wrap_agent_with_observability',
]



