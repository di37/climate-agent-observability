# 🤖 Agents Module

## Overview

Agent implementations with proper separation between business logic and observability.

## Architecture

### Two-Layer Design

```
┌─────────────────────────────────────┐
│     ObservedClimateAgent            │
│     (Observability Wrapper)         │
│  ┌───────────────────────────────┐  │
│  │    BaseClimateAgent           │  │
│  │    (Pure Business Logic)      │  │
│  │                               │  │
│  │  - Query execution            │  │
│  │  - Tool orchestration         │  │
│  │  - Response handling          │  │
│  └───────────────────────────────┘  │
│                                     │
│  + Langfuse tracing                 │
│  + Automatic scoring                │
│  + Prompt management                │
│  + User feedback                    │
└─────────────────────────────────────┘
```

## Files

### 1. `base_agent.py` - Pure Agent Logic

**Purpose:** Core business logic without any observability dependencies

**Class:** `BaseClimateAgent`

**Features:**
- ✅ Pure Agno agent
- ✅ SQL query execution
- ✅ No Langfuse dependencies
- ✅ Testable independently
- ✅ Reusable anywhere

**Usage:**
```python
from src.agents.base_agent import BaseClimateAgent

# Use without any observability
agent = BaseClimateAgent()
response = agent.execute("What are the top countries?")
print(response)
```

**Benefits:**
- Can test without Langfuse
- Can use in other projects
- No coupling to monitoring
- Pure business logic

### 2. `observed_agent.py` - With Observability

**Purpose:** Wrap base agent with Langfuse observability

**Class:** `ObservedClimateAgent`

**Features:**
- ✅ Wraps BaseClimateAgent
- ✅ Adds Langfuse tracing
- ✅ Adds automatic scoring
- ✅ Manages prompts
- ✅ Handles user feedback

**Usage:**
```python
from src.agents.observed_agent import ObservedClimateAgent

# Full observability
agent = ObservedClimateAgent()
result = agent.query("What are the top countries?")
# Returns: {response, trace_id, observation_id}
```

**Benefits:**
- Full Langfuse integration
- Optional observability
- Delegates logic to base agent
- Clean separation

### 3. `climate_agent.py` - DEPRECATED

**Status:** Old monolithic implementation (kept for reference)

**Recommendation:** Use `ObservedClimateAgent` instead

## Comparison

### BaseClimateAgent (Pure)

```python
# No observability dependencies
agent = BaseClimateAgent()
response = agent.execute(question)  # Returns: string

# ✅ Fast
# ✅ Simple
# ✅ Testable
# ❌ No tracking
```

### ObservedClimateAgent (Full Features)

```python
# With observability
agent = ObservedClimateAgent()
result = agent.query(question)  # Returns: {response, trace_id, ...}

# ✅ Full tracking
# ✅ Automatic scores
# ✅ Prompt management
# ✅ User feedback
```

## Design Pattern: Decorator/Wrapper

### Core Logic (Base)

```python
class BaseClimateAgent:
    def execute(self, question):
        # Pure business logic
        response = self.agent.run(question)
        return response.content
```

### Observability Wrapper (Observed)

```python
class ObservedClimateAgent:
    def __init__(self):
        self.base_agent = BaseClimateAgent()  # Delegate to base
        self.langfuse = get_client()
    
    def query(self, question):
        # Add observability wrapper
        with self.langfuse.start_as_current_observation(...):
            response = self.base_agent.execute(question)  # Core logic
            # Add scoring, tracking, etc.
        return {response, trace_id, ...}
```

## Benefits of Separation

### 1. Independent Testing

```python
# Test base agent without Langfuse
def test_agent():
    agent = BaseClimateAgent()
    response = agent.execute("Test query")
    assert "data" in response
```

### 2. Reusable Logic

```python
# Use base agent in another project
from climate_rag.agents import BaseClimateAgent

# Works anywhere!
agent = BaseClimateAgent(custom_instructions)
```

### 3. Optional Observability

```python
# Development - no observability
agent = BaseClimateAgent()

# Production - with observability
agent = ObservedClimateAgent()
```

### 4. Clear Responsibilities

| Class | Responsibility |
|-------|----------------|
| `BaseClimateAgent` | Business logic only |
| `ObservedClimateAgent` | Add observability |

## Usage Examples

### Example 1: Pure Agent (Fast, Simple)

```python
from src.agents import BaseClimateAgent

agent = BaseClimateAgent()
response = agent.execute("How many records?")
print(response)
# Output: "The database contains 10,000 records"
```

### Example 2: With Observability (Full Features)

```python
from src.agents import ObservedClimateAgent
from src.observability.scoring import add_user_feedback_score

agent = ObservedClimateAgent()
result = agent.query("How many records?")

print(result['response'])
print(f"Trace: {result['trace_id']}")

# Add user feedback
add_user_feedback_score(
    agent.langfuse,
    result['trace_id'],
    result['observation_id'],
    "positive"
)
```

### Example 3: Custom Instructions (Pure)

```python
from src.agents import BaseClimateAgent

custom_instructions = [
    "You are a specialized climate analyst.",
    "Focus on precipitation patterns.",
]

agent = BaseClimateAgent(instructions=custom_instructions)
response = agent.execute("Show rainfall trends")
```

### Example 4: Interactive Chat (Full Features)

```python
from src.agents import ObservedClimateAgent

agent = ObservedClimateAgent()
agent.chat()
# Full interactive experience with feedback
```

## Backward Compatibility

For existing code, the alias still works:

```python
# Old way (still works)
from src.agents import ClimateAgricultureAgent
agent = ClimateAgricultureAgent()

# Actually uses ObservedClimateAgent
# Full backward compatibility ✅
```

## Migration Guide

### From Monolithic

**Old:**
```python
from src.agents.climate_agent import ClimateAgricultureAgent
```

**New:**
```python
# For full observability (default)
from src.agents import ObservedClimateAgent as ClimateAgent

# For pure logic (testing)
from src.agents import BaseClimateAgent
```

## Testing Strategy

### Unit Tests (Base Agent)

```python
def test_base_agent():
    """Test agent logic without observability overhead."""
    agent = BaseClimateAgent()
    response = agent.execute("Test query")
    assert response is not None
```

### Integration Tests (Observed Agent)

```python
def test_observed_agent():
    """Test agent with full observability."""
    agent = ObservedClimateAgent()
    result = agent.query("Test query")
    assert 'trace_id' in result
    assert 'response' in result
```

## Summary

### File Structure

```
src/agents/
├── __init__.py           # Exports both classes
├── base_agent.py         # Pure logic (NEW)
├── observed_agent.py     # With observability (NEW)
├── climate_agent.py      # Old monolithic (deprecated)
└── README.md             # This file
```

### Classes

| Class | Dependencies | Use When |
|-------|--------------|----------|
| `BaseClimateAgent` | Agno only | Testing, reuse, development |
| `ObservedClimateAgent` | Agno + Langfuse | Production, full features |

### Design Principle

**Separation of Concerns:**
- Core logic: `BaseClimateAgent`
- Observability: `ObservedClimateAgent` wraps base

**Result:**
- ✅ Testable
- ✅ Reusable
- ✅ Maintainable
- ✅ Professional

---

**Clean separation achieved!** 🎯✅

