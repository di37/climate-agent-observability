"""
Generic observability wrapper for any Agno agent.

This wrapper adds Langfuse observability to any agent without modifying the agent itself.
"""

import logging
from typing import Optional, Callable
from langfuse import get_client

from .scoring import score_response, add_user_feedback_score
from .prompts import get_agent_instructions

logger = logging.getLogger(__name__)


class ObservabilityWrapper:
    """
    Generic wrapper that adds Langfuse observability to any agent.
    
    This class can wrap ANY agent (Agno or custom) and add:
    - Tracing (input/output/tokens/costs)
    - Automatic quality scoring
    - Prompt version tracking
    - User feedback support
    """
    
    def __init__(
        self,
        agent,
        agent_name: str = "Agent",
        enable_scoring: bool = True,
        enable_prompts: bool = False,
        prompt_name: Optional[str] = None
    ):
        """
        Initialize the observability wrapper.
        
        Args:
            agent: Any agent instance with a run() or execute() method
            agent_name: Display name for logging
            enable_scoring: If True, add automatic quality scores
            enable_prompts: If True, track prompt usage
            prompt_name: Prompt name in Langfuse (if enable_prompts=True)
        """
        logger.info(f"Initializing ObservabilityWrapper for {agent_name}")
        
        # Store the wrapped agent
        self.agent = agent
        self.agent_name = agent_name
        self.enable_scoring = enable_scoring
        self.enable_prompts = enable_prompts
        self.prompt_name = prompt_name
        
        # Initialize Langfuse
        self.langfuse = get_client()
        self.managed_prompt = None
        
        # Fetch managed prompt if enabled
        if enable_prompts and prompt_name:
            try:
                self.managed_prompt = self.langfuse.get_prompt(prompt_name, type="text")
                logger.info(f"Tracking prompt: {prompt_name} (v{self.managed_prompt.version})")
            except Exception as e:
                logger.warning(f"Could not fetch prompt: {e}")
        
        logger.info(f"ObservabilityWrapper initialized for {agent_name}")
    
    def execute(self, input_data: str, execute_method: str = "run") -> dict:
        """
        Execute the wrapped agent with full observability.
        
        Args:
            input_data: Input to the agent (question, prompt, etc.)
            execute_method: Method name to call on agent ("run", "execute", etc.)
            
        Returns:
            Dict with response, trace_id, and observation_id
        """
        logger.info(f"Processing request: {input_data[:50]}...")
        
        # Prepare metadata
        span_metadata = {
            "agent_name": self.agent_name,
            "input": input_data
        }
        
        if self.managed_prompt:
            span_metadata["prompt_name"] = self.managed_prompt.name
            span_metadata["prompt_version"] = self.managed_prompt.version
        
        # Observability wrapper - Langfuse span
        with self.langfuse.start_as_current_observation(
            as_type="span",
            name=f"{self.agent_name}_query",
            input={"input": input_data},
            metadata=span_metadata
        ) as span:
            # Link prompt if available
            if self.managed_prompt:
                try:
                    span.update(prompt=self.managed_prompt)
                except Exception as e:
                    logger.warning(f"Could not link prompt: {e}")
            
            # Execute the wrapped agent (flexible method calling)
            try:
                execute_fn = getattr(self.agent, execute_method)
                response_obj = execute_fn(input_data)
                
                # Handle different response types
                if hasattr(response_obj, 'content'):
                    response_text = response_obj.content  # Agno response
                elif isinstance(response_obj, str):
                    response_text = response_obj  # String response
                else:
                    response_text = str(response_obj)  # Fallback
                    
            except Exception as e:
                logger.error(f"Agent execution error: {e}")
                raise
            
            # Update span with output
            span.update(output={"response": response_text})
            
            # Get trace IDs
            trace_id = span.trace_id
            observation_id = span.id
        
        # Add automatic quality scores (if enabled)
        if self.enable_scoring:
            try:
                score_response(
                    self.langfuse,
                    observation_id,
                    trace_id,
                    response_text,
                    input_data
                )
                logger.debug(f"Scores added to trace {trace_id}")
            except Exception as e:
                logger.error(f"Scoring error: {e}")
        
        logger.info(f"Request completed, trace_id: {trace_id}")
        
        return {
            "response": response_text,
            "trace_id": trace_id,
            "observation_id": observation_id
        }
    
    def add_user_feedback(
        self,
        trace_id: str,
        observation_id: str,
        feedback: str,
        comment: str = ""
    ) -> bool:
        """
        Add user feedback score to a trace.
        
        Args:
            trace_id: The trace ID
            observation_id: The observation ID
            feedback: "positive", "negative", or numeric value (0-1)
            comment: Optional user comment
            
        Returns:
            True if successful, False otherwise
        """
        return add_user_feedback_score(
            self.langfuse,
            trace_id,
            observation_id,
            feedback,
            comment
        )


def wrap_agent_with_observability(
    agent,
    agent_name: str = "Agent",
    enable_scoring: bool = True,
    enable_prompts: bool = False,
    prompt_name: Optional[str] = None
) -> ObservabilityWrapper:
    """
    Factory function to wrap any agent with observability.
    
    Args:
        agent: Any agent instance
        agent_name: Display name
        enable_scoring: Add automatic scores
        enable_prompts: Track prompt versions
        prompt_name: Prompt name in Langfuse
        
    Returns:
        Wrapped agent with observability
        
    Example:
        from agno.agent import Agent
        from src.observability.wrapper import wrap_agent_with_observability
        
        # Create any agent
        my_agent = Agent(model=..., tools=[...])
        
        # Wrap with observability
        observed = wrap_agent_with_observability(
            my_agent,
            agent_name="MyCustomAgent",
            enable_scoring=True
        )
        
        # Use with full observability
        result = observed.execute("Your question")
    """
    return ObservabilityWrapper(
        agent=agent,
        agent_name=agent_name,
        enable_scoring=enable_scoring,
        enable_prompts=enable_prompts,
        prompt_name=prompt_name
    )

