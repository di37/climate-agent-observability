# 🔄 Generic Observability Wrapper Guide

## Overview

The `ObservabilityWrapper` is a **generic, reusable wrapper** that adds full Langfuse observability to **ANY agent** - not just our ClimateAgent!

## 🎯 Key Benefit

**Wrap ANY agent with observability in 2 lines of code!**

```python
from src.observability import wrap_agent_with_observability

observed_agent = wrap_agent_with_observability(your_agent)
result = observed_agent.execute("Your input")
# Full Langfuse tracking automatically!
```

## 📦 What's Included

### `wrapper.py`

**Class:** `ObservabilityWrapper`  
**Function:** `wrap_agent_with_observability()` (factory function)

**Features:**
- ✅ Works with ANY agent
- ✅ Langfuse tracing
- ✅ Automatic scoring
- ✅ Prompt tracking
- ✅ User feedback
- ✅ Configurable

## 🚀 Usage Examples

### Example 1: Wrap Climate Agent

```python
from src.agents import BaseClimateAgent
from src.observability import wrap_agent_with_observability

# Create your agent
base_agent = BaseClimateAgent()

# Wrap with observability
observed = wrap_agent_with_observability(
    agent=base_agent,
    agent_name="Climate Agent",
    enable_scoring=True
)

# Use with full tracking
result = observed.execute("What are the top countries?")
print(result['response'])
print(f"Trace: {result['trace_id']}")
```

### Example 2: Wrap Custom Agno Agent

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from src.observability import wrap_agent_with_observability

# Create ANY Agno agent
my_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    instructions=["You are a helpful assistant"],
    tools=[...],  # Your custom tools
)

# Wrap it!
observed = wrap_agent_with_observability(
    agent=my_agent,
    agent_name="MyCustomAgent",
    enable_scoring=True,
    enable_prompts=True,
    prompt_name="my-custom-prompt"
)

# Use with full Langfuse tracking
result = observed.execute("Your question", execute_method="run")
```

### Example 3: Wrap Third-Party Agent

```python
from some_library import ThirdPartyAgent
from src.observability import wrap_agent_with_observability

# Create third-party agent
agent = ThirdPartyAgent(config=...)

# Wrap with observability
observed = wrap_agent_with_observability(
    agent=agent,
    agent_name="ThirdPartyAgent"
)

# Now you have full Langfuse tracking!
result = observed.execute("Input", execute_method="process")
```

### Example 4: Multiple Agents with Same Wrapper

```python
from src.observability import wrap_agent_with_observability

# Wrap different agents
agent1 = wrap_agent_with_observability(climate_agent, "Climate")
agent2 = wrap_agent_with_observability(weather_agent, "Weather")
agent3 = wrap_agent_with_observability(finance_agent, "Finance")

# All tracked in Langfuse independently!
result1 = agent1.execute("Climate question")
result2 = agent2.execute("Weather question")
result3 = agent3.execute("Finance question")
```

## ⚙️ Configuration Options

### Basic (Defaults)

```python
observed = wrap_agent_with_observability(your_agent)
# Uses defaults:
# - agent_name="Agent"
# - enable_scoring=True
# - enable_prompts=False
```

### Full Configuration

```python
observed = wrap_agent_with_observability(
    agent=your_agent,
    agent_name="MySpecialAgent",      # Custom name
    enable_scoring=True,               # Add quality scores
    enable_prompts=True,               # Track prompt versions
    prompt_name="my-agent-prompt"      # Prompt in Langfuse
)
```

### Minimal (No Scoring/Prompts)

```python
observed = wrap_agent_with_observability(
    agent=your_agent,
    agent_name="SimpleAgent",
    enable_scoring=False,    # Skip scoring
    enable_prompts=False     # Skip prompts
)
# Just basic tracing (input/output/tokens/costs)
```

## 🔧 Flexible Agent Methods

The wrapper supports different agent method names:

```python
# For Agno agents with .run()
result = observed.execute(question, execute_method="run")

# For custom agents with .execute()
result = observed.execute(question, execute_method="execute")

# For agents with .process()
result = observed.execute(question, execute_method="process")

# For agents with .query()
result = observed.execute(question, execute_method="query")
```

## 📊 What Gets Tracked

Regardless of which agent you wrap, you get:

### Via Tracing (Automatic)
- ✅ Input text
- ✅ Output text
- ✅ Actual token counts
- ✅ Real costs
- ✅ Latency
- ✅ Model information

### Via Scoring (If enabled)
- ✅ response_length
- ✅ data_backed
- ✅ completeness
- ✅ relevance

### Via Prompts (If enabled)
- ✅ Prompt name
- ✅ Prompt version
- ✅ Configuration

### Via Feedback (Always available)
- ✅ User ratings (👍👎)
- ✅ Custom scores (0-1)
- ✅ Comments

## 🎨 Real-World Examples

### Example: Financial Analysis Agent

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from src.observability import wrap_agent_with_observability

# Create financial agent
financial_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    instructions=["You are a financial analyst..."],
    tools=[stock_data_tool, calculator_tool]
)

# Wrap with observability
observed_financial = wrap_agent_with_observability(
    agent=financial_agent,
    agent_name="Financial Analyst",
    enable_scoring=True,
    enable_prompts=True,
    prompt_name="financial-analyst-instructions"
)

# Use with full tracking
result = observed_financial.execute("What's AAPL's P/E ratio?")
```

### Example: Code Review Agent

```python
# Create code review agent
code_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    instructions=["You are a code reviewer..."],
    tools=[read_file_tool, analyze_code_tool]
)

# Wrap
observed_code = wrap_agent_with_observability(
    agent=code_agent,
    agent_name="Code Reviewer"
)

# Review with tracking
result = observed_code.execute("Review this Python file")
```

### Example: Customer Support Agent

```python
# Create support agent
support_agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),  # Cheaper model
    instructions=["You are a support agent..."],
    tools=[kb_search_tool, ticket_tool]
)

# Wrap
observed_support = wrap_agent_with_observability(
    agent=support_agent,
    agent_name="Support Agent",
    enable_scoring=True  # Track response quality
)

# Handle tickets with tracking
result = observed_support.execute("Customer issue: ...")

# Add user feedback
observed_support.add_user_feedback(
    result['trace_id'],
    result['observation_id'],
    "positive" if issue_resolved else "negative"
)
```

## 🏗️ Architecture

### Generic Wrapper Design

```
ObservabilityWrapper (Generic)
    ├── Wraps: ANY agent
    ├── Adds: Langfuse tracing
    ├── Adds: Automatic scoring
    ├── Adds: Prompt tracking
    └── Adds: User feedback
    
Can wrap:
    ├── Agno agents
    ├── LangChain agents
    ├── Custom agents
    └── Third-party agents
```

### Our Implementation

```
ObservedClimateAgent (Specific)
    └── Uses: ObservabilityWrapper (Generic)
        └── Wraps: BaseClimateAgent (Specific)
```

**Pattern:** Specific agent uses generic wrapper!

## 🎯 Benefits of Generic Wrapper

### 1. Reusability

```python
# Use same wrapper for different agents
wrap_agent_with_observability(climate_agent)
wrap_agent_with_observability(weather_agent)
wrap_agent_with_observability(finance_agent)
```

### 2. Consistency

All wrapped agents get the same observability features:
- Same tracing format
- Same scoring metrics
- Same Langfuse structure

### 3. Maintainability

Fix observability bugs in ONE place:
- Update `wrapper.py`
- All agents benefit

### 4. Easy Integration

Add observability to existing agents:
```python
# Before: No tracking
result = my_agent.run(question)

# After: Full tracking (2 lines added)
from src.observability import wrap_agent_with_observability
observed = wrap_agent_with_observability(my_agent)
result = observed.execute(question)
```

## 📈 Extending the Wrapper

### Add Custom Tracking

```python
# src/observability/wrapper.py
class ObservabilityWrapper:
    def execute(self, input_data):
        # Existing code...
        
        # Add custom tracking
        span.update(metadata={
            "user_id": get_current_user(),
            "session_id": get_session_id(),
            "custom_metric": calculate_metric()
        })
```

### Add Custom Scores

```python
# After wrapping
result = observed.execute(question)

# Add custom scores
langfuse.create_score(
    trace_id=result['trace_id'],
    name="custom_metric",
    value=0.85
)
```

## 🧪 Testing

### Test Generic Wrapper

```python
def test_wrapper_with_any_agent():
    """Wrapper works with any agent."""
    
    # Create simple agent
    simple_agent = Agent(model=..., instructions=[...])
    
    # Wrap it
    observed = wrap_agent_with_observability(simple_agent)
    
    # Test
    result = observed.execute("Test")
    assert 'response' in result
    assert 'trace_id' in result
```

### Test With Mock Agent

```python
class MockAgent:
    def run(self, input):
        return type('obj', (object,), {'content': 'Mock response'})

# Wrap mock
observed = wrap_agent_with_observability(MockAgent())
result = observed.execute("Test", execute_method="run")
# Works!
```

## 📚 API Reference

### ObservabilityWrapper Class

```python
class ObservabilityWrapper:
    def __init__(
        self,
        agent,                          # Any agent instance
        agent_name: str = "Agent",      # Display name
        enable_scoring: bool = True,    # Add quality scores
        enable_prompts: bool = False,   # Track prompts
        prompt_name: Optional[str] = None  # Prompt name
    )
    
    def execute(
        self,
        input_data: str,                # Input to agent
        execute_method: str = "run"     # Method to call
    ) -> dict:  # Returns {response, trace_id, observation_id}
    
    def add_user_feedback(
        self,
        trace_id: str,
        observation_id: str,
        feedback: str,
        comment: str = ""
    ) -> bool
```

### Factory Function

```python
def wrap_agent_with_observability(
    agent,                              # Any agent
    agent_name: str = "Agent",
    enable_scoring: bool = True,
    enable_prompts: bool = False,
    prompt_name: Optional[str] = None
) -> ObservabilityWrapper
```

## 💡 Best Practices

### 1. Name Your Agents

```python
# ✅ Good - Clear identification in Langfuse
observed = wrap_agent_with_observability(
    agent,
    agent_name="Financial Analyst"
)

# ❌ Bad - Generic name
observed = wrap_agent_with_observability(agent)  # "Agent"
```

### 2. Enable Scoring for User-Facing Agents

```python
# User-facing: Enable scoring
wrap_agent_with_observability(agent, enable_scoring=True)

# Internal/System: Skip scoring
wrap_agent_with_observability(agent, enable_scoring=False)
```

### 3. Use Prompts for Versioning

```python
# Production: Track prompt versions
wrap_agent_with_observability(
    agent,
    enable_prompts=True,
    prompt_name="my-production-prompt"
)
```

## 🎉 Summary

### What You Can Do

✅ **Wrap ANY Agno agent** with 2 lines of code  
✅ **Get full Langfuse tracking** automatically  
✅ **Reuse wrapper** across multiple agents  
✅ **Configure features** per agent  
✅ **Keep agents clean** - no observability in agent code  

### Files

- **`wrapper.py`** - Generic wrapper implementation
- **`observed_climate.py`** - Example using the wrapper
- **`WRAPPER_GUIDE.md`** - This guide

### Import

```python
from src.observability import (
    ObservabilityWrapper,              # Class
    wrap_agent_with_observability,     # Factory function
)
```

### Quick Start

```python
from src.observability import wrap_agent_with_observability

observed = wrap_agent_with_observability(your_agent, "YourAgentName")
result = observed.execute("Input")
```

---

**Generic wrapper - works with ANY agent!** 🔄✅

