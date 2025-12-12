# 🔍 Observability Module

Complete Langfuse observability integration for LLM applications.

## Overview

This module provides all functionality needed for comprehensive LLM observability:
- **Tracing** - Track input, output, tokens, costs
- **Scoring** - Automatic quality metrics + user feedback
- **Prompts** - Centralized prompt management

## Modules

### 1. `tracing.py` - Initialization & Setup

**Purpose:** Set up Langfuse tracing with OpenLIT instrumentation

**Functions:**
- `initialize_langfuse_tracing()` → Langfuse client

**Usage:**
```python
from src.observability.tracing import initialize_langfuse_tracing

langfuse = initialize_langfuse_tracing()
# All agent calls now automatically traced
```

**What It Captures:**
- ✅ Input/output text
- ✅ Actual token usage
- ✅ Real costs
- ✅ Latency
- ✅ Model information

### 2. `scoring.py` - Quality Evaluation

**Purpose:** Add quality scores for evaluation and monitoring

**Functions:**
- `score_response(langfuse, observation_id, trace_id, response, question)`
- `add_user_feedback_score(langfuse, trace_id, observation_id, feedback, comment)`

**Automatic Scores:**
1. **response_length** - How detailed (0-1)
2. **data_backed** - Includes data (0.5 or 1.0)
3. **completeness** - Quality indicators (0-1)
4. **relevance** - Question alignment (0-1)

**User Feedback:**
- 👍 = 1.0 (positive)
- 👎 = 0.0 (negative)
- 0.0-1.0 = Custom rating

**Usage:**
```python
from src.observability.scoring import score_response, add_user_feedback_score

# Automatic scoring
score_response(langfuse, obs_id, trace_id, response, question)

# User feedback
add_user_feedback_score(langfuse, trace_id, obs_id, "positive", "Great!")
```

### 3. `prompts.py` - Prompt Management

**Purpose:** Centralized, versioned prompt management

**Functions:**
- `create_agent_prompt(langfuse)` → Create prompt in Langfuse
- `get_agent_instructions(langfuse, use_managed)` → Fetch instructions
- `get_default_instructions()` → Fallback instructions

**Usage:**
```python
from src.observability.prompts import create_agent_prompt, get_agent_instructions

# Create prompt
create_agent_prompt(langfuse)

# Fetch prompt
instructions, prompt_obj = get_agent_instructions(langfuse, use_managed_prompts=True)
```

**Benefits:**
- Version control
- Update without code changes
- A/B testing
- Track which version used

## Complete Integration Example

```python
from src.observability import (
    initialize_langfuse_tracing,
    score_response,
    add_user_feedback_score,
    create_agent_prompt,
    get_agent_instructions
)

# 1. Initialize tracing
langfuse = initialize_langfuse_tracing()

# 2. Create/fetch prompt
create_agent_prompt(langfuse)
instructions, prompt = get_agent_instructions(langfuse)

# 3. Create agent with instructions
agent = Agent(instructions=instructions)

# 4. Run query and track
with langfuse.start_as_current_observation(...) as span:
    response = agent.run(question)
    trace_id = span.trace_id
    observation_id = span.id

# 5. Add automatic scores
score_response(langfuse, observation_id, trace_id, response, question)

# 6. Add user feedback
add_user_feedback_score(langfuse, trace_id, observation_id, "positive")
```

## Architecture

```
src/observability/
├── __init__.py          # Exports all observability functions
├── tracing.py           # Langfuse + OpenLIT setup
├── scoring.py           # Quality evaluation
└── prompts.py           # Prompt management

Used by:
├── src/agents/          # Agent implementations
├── src/demos/           # Demo runners
└── main.py              # Entry point
```

## What Gets Tracked

### Via Tracing (`tracing.py`)
- Input text
- Output text
- Token counts (actual)
- Costs (calculated)
- Latency
- Model info

### Via Scoring (`scoring.py`)
- response_length
- data_backed
- completeness
- relevance
- user_feedback

### Via Prompts (`prompts.py`)
- Prompt name
- Prompt version
- Prompt content
- Configuration

## Benefits

### 1. Organized
All observability code in one place:
- Easy to find
- Clear purpose
- Logical grouping

### 2. Reusable
Import observability functions anywhere:
```python
from src.observability import initialize_langfuse_tracing
```

### 3. Maintainable
- Modify tracing → `tracing.py`
- Modify scoring → `scoring.py`
- Modify prompts → `prompts.py`

### 4. Testable
Test observability independently:
```python
from src.observability.scoring import score_response
# Unit test scoring logic
```

### 5. Extensible
Easy to add new observability features:
```python
# src/observability/metrics.py
def track_custom_metric(...):
    ...
```

## Integration Points

### Agent Uses Observability

```python
# src/agents/climate_agent.py
from ..observability.prompts import get_agent_instructions
from ..observability.scoring import score_response, add_user_feedback_score
```

### Main Uses Observability

```python
# main.py
from src.observability.tracing import initialize_langfuse_tracing
from src.observability.prompts import create_agent_prompt
```

### Demo Uses Observability

```python
# src/demos/demo_runner.py
# Inherits tracing through agent
# Scores automatically added
```

## Langfuse Dashboard

After using these modules, your dashboard shows:

**Traces Tab:**
- Full conversation flows
- Input/output
- Tokens/costs
- Tool calls

**Scores Tab:**
- Quality metrics
- User feedback
- Moving averages
- Trends

**Prompts Tab:**
- Managed prompts
- Version history
- Usage statistics

## Best Practices

### 1. Initialize Once

```python
# At application start
langfuse = initialize_langfuse_tracing()
```

### 2. Score Everything

```python
# After each query
score_response(langfuse, obs_id, trace_id, response, question)
```

### 3. Manage Prompts Centrally

```python
# Use managed prompts
instructions, prompt = get_agent_instructions(langfuse, use_managed_prompts=True)
```

### 4. Collect User Feedback

```python
# After user rates
add_user_feedback_score(langfuse, trace_id, obs_id, feedback, comment)
```

## Summary

### Structure

```
src/observability/
├── tracing.py    # Initialize Langfuse + OpenLIT
├── scoring.py    # Quality metrics + feedback
└── prompts.py    # Prompt management
```

### Purpose

**Dedicated folder for all LLM observability functionality:**
- ✅ Clear organization
- ✅ Easy to find
- ✅ Reusable
- ✅ Maintainable

### Import

```python
from src.observability import (
    initialize_langfuse_tracing,
    score_response,
    add_user_feedback_score,
    create_agent_prompt,
    get_agent_instructions,
)
```

---

**Complete observability in one organized module!** 🔍✅

