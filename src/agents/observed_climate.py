"""
Observed Climate Agriculture Agent - Uses generic observability wrapper.

This demonstrates how to wrap a specific agent with the generic ObservabilityWrapper.
"""

import logging
from .base_agent import BaseClimateAgent
from ..config.settings import AGENT_NAME, PROMPT_NAME
from ..observability import wrap_agent_with_observability
from ..observability.prompts import get_agent_instructions
from langfuse import get_client

logger = logging.getLogger(__name__)


class ObservedClimateAgent:
    """
    Climate Agriculture Agent wrapped with observability.
    
    Uses the generic ObservabilityWrapper to add full Langfuse integration
    to BaseClimateAgent.
    """
    
    def __init__(self, use_managed_prompts=True, enable_scoring=True):
        """
        Initialize observed climate agent.
        
        Args:
            use_managed_prompts: Fetch instructions from Langfuse
            enable_scoring: Add automatic quality scores
        """
        logger.info(f"Initializing Observed {AGENT_NAME}")
        
        # Get Langfuse client and instructions
        langfuse = get_client()
        instructions, managed_prompt = get_agent_instructions(langfuse, use_managed_prompts)
        
        # Create base agent (pure logic)
        base_agent = BaseClimateAgent(instructions=instructions)
        
        # Wrap with generic observability
        self.wrapper = wrap_agent_with_observability(
            agent=base_agent,
            agent_name=AGENT_NAME,
            enable_scoring=enable_scoring,
            enable_prompts=use_managed_prompts,
            prompt_name=PROMPT_NAME if use_managed_prompts else None
        )
        
        # Expose wrapper properties for convenience
        self.langfuse = self.wrapper.langfuse
        self.managed_prompt = self.wrapper.managed_prompt
        
        logger.info(f"Observed agent initialized successfully")
    
    def query(self, question: str) -> dict:
        """
        Query with observability - delegates to generic wrapper.
        
        Args:
            question: User's question
            
        Returns:
            Dict with response, trace_id, observation_id
        """
        return self.wrapper.execute(input_data=question, execute_method="execute")
    
    def chat(self):
        """Interactive chat session with observability and user feedback."""
        logger.info("Starting interactive chat session")
        
        print("\n" + "="*80)
        print(f"🌱 {AGENT_NAME.upper()}")
        print("="*80)
        print("\n✓ Input & Output tracked")
        print("✓ Tokens & Costs tracked")
        print("✓ Quality Scores automatically added")
        print("✓ Prompts managed via Langfuse")
        print("✓ User feedback supported")
        
        if self.managed_prompt:
            print(f"✓ Using prompt version: {self.managed_prompt.version}")
        
        print("\nCommands:")
        print("  • Type your question")
        print("  • Type 'exit' to quit")
        print("  • After response, type: 👍 👎 or 'feedback' for detailed rating\n")
        
        last_result = None
        
        while True:
            user_input = input("You: ").strip()
            
            # Handle exit
            if user_input.lower() in ['exit', 'quit', 'q']:
                logger.info("Chat session ended by user")
                print("\n✅ Check your Langfuse dashboard:")
                print("   - Traces tab for individual queries")
                print("   - Scores tab for quality metrics (including user feedback)\n")
                break
            
            if not user_input:
                continue
            
            # Handle feedback
            if user_input in ['👍', '👎', 'feedback'] and last_result:
                self._handle_feedback(user_input, last_result)
                continue
            
            # Process query
            try:
                result = self.query(user_input)
                last_result = result
                
                print(f"\n🤖 Agent: {result['response']}")
                print(f"\n📊 Trace ID: {result['trace_id']}")
                print("💭 Rate this response: 👍 👎 or 'feedback' for detailed rating\n")
                
            except Exception as e:
                logger.error(f"Query error: {e}")
                print(f"\n❌ Error: {e}\n")
    
    def _handle_feedback(self, user_input: str, last_result: dict):
        """Handle user feedback - delegates to wrapper."""
        if user_input == '👍':
            self.wrapper.add_user_feedback(
                last_result['trace_id'],
                last_result['observation_id'],
                "positive"
            )
            print("✅ Positive feedback recorded!\n")
            
        elif user_input == '👎':
            self.wrapper.add_user_feedback(
                last_result['trace_id'],
                last_result['observation_id'],
                "negative"
            )
            print("✅ Negative feedback recorded!\n")
            
        elif user_input == 'feedback':
            print("Rate the response (0-1, 0=bad, 1=excellent):")
            rating = input("Rating: ").strip()
            print("Optional comment:")
            comment = input("Comment: ").strip()
            
            try:
                rating_value = float(rating)
                if 0.0 <= rating_value <= 1.0:
                    self.wrapper.add_user_feedback(
                        last_result['trace_id'],
                        last_result['observation_id'],
                        rating,
                        comment
                    )
                    print("✅ Feedback recorded!\n")
                else:
                    print("❌ Rating must be between 0 and 1\n")
            except ValueError:
                print("❌ Invalid rating. Please enter a decimal number (e.g., 0.9)\n")
            except Exception as e:
                logger.error(f"Feedback error: {e}")
                print(f"❌ Error recording feedback: {e}\n")

