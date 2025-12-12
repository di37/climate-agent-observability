"""Langfuse initialization and tracing setup."""

import logging
from langfuse import get_client

logger = logging.getLogger(__name__)


def initialize_langfuse_tracing():
    """
    Initialize Langfuse tracing using OpenLIT instrumentation.
    This is the proper way to integrate Agno with Langfuse.
    
    Returns:
        Langfuse client instance
    """
    logger.info("Initializing Langfuse client")
    langfuse = get_client()
    
    # Initialize OpenLIT with Langfuse's OTEL tracer
    logger.info("Setting up OpenLIT instrumentation")
    import openlit
    openlit.init(tracer=langfuse._otel_tracer, disable_batch=True)
    
    logger.info("Langfuse tracing initialized successfully")
    return langfuse

