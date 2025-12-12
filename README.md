# 🌱 Climate Agriculture Agent

**A Real-World Agentic AI Application** demonstrating complete **Langfuse Observability** integration.

### 🌍 Real-World Use Case
This project simulates a **Climate Data Analyst**—an AI agent designed to analyze the impact of climate change on global agriculture. It interacts with a realistic dataset of **10,000 records** (covering crop yields, CO2 levels, and economic impacts) to answer complex analytical questions, mirroring how AI is used in modern data-driven enterprises.

### 🔭 Learn Langfuse Observability
More than just a demo, this is a **hands-on masterclass** in LLM Observability. You will learn how to use **Langfuse** to:
- **Trace & Visualize**: See exactly what your agent is thinking, from user input to SQL generation to final answer.
- **Debug with Confidence**: Identify why an agent failed or hallucinated by inspecting the full trace.
- **Monitor Costs & Latency**: Track token usage and performance in real-time.
- **Implement Quality Loops**: Use automated scores and user feedback to continuously improve your agent.

This is a production-ready reference implementation showcasing:
- How to build observable AI agents with Langfuse
- Best practices for LLM observability (tracing, scoring, prompts)
- Clean architecture with separated concerns
- Generic observability wrapper for any Agno agent

> [!IMPORTANT]
> **Educational Purpose Only**: This CLI chatbot is designed as a learning resource for observability of the Agentic AI system using Langfuse. While the *patterns* are production-ready, this specific application is a demonstration and not intended for production deployment.

## 🚀 Quick Start

### Prerequisites

#### 1. Langfuse Setup

This project uses **self-hosted Langfuse** via Docker. Choose one option:

**Option A: Self-Hosted Langfuse (Recommended for this demo)**

```bash
# Navigate to langfuse directory after cloning git repo of langfuse
cd langfuse

# Start Langfuse with Docker Compose
docker-compose up -d

# Access at: http://localhost:3000
```

**Option B: Langfuse Cloud**

Sign up at: https://cloud.langfuse.com (free tier available)

#### 2. Get Langfuse API Keys

**For Self-Hosted:**
1. Open http://localhost:3000
2. Create an account or sign in
3. Create a new project
4. Go to **Settings** → **API Keys**
5. Click **"Create new API key"**
6. Copy the **Public Key** (`pk-lf-...`) and **Secret Key** (`sk-lf-...`)

**For Langfuse Cloud:**
1. Sign up at https://cloud.langfuse.com
2. Create a project
3. Go to **Project Settings** → **API Keys**
4. Generate new keys
5. Copy both keys

### Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp env.template .env

# 3. Edit .env with your keys
# For self-hosted:
LANGFUSE_HOST=http://localhost:3000
LANGFUSE_PUBLIC_KEY=pk-lf-...  # From step above
LANGFUSE_SECRET_KEY=sk-lf-...  # From step above

# For cloud:
LANGFUSE_HOST=https://cloud.langfuse.com
# (or https://us.cloud.langfuse.com for US region)

# Also add OpenAI key:
OPENAI_API_KEY=sk-proj-...
AGENT_MODEL=any-openai-model # any openai model name
# Optional: Custom API Base URL - To use local llms via ollama or lm studio
API_BASE_URL=http://localhost:11434/v1

# 4. Create database
python scripts/ingest_data.py

# 5. Run the agent
python main.py
```

## 🎯 Purpose

This project serves as a **complete example** of integrating Langfuse observability into an Agentic AI application, demonstrating:

### Observability Features
- ✅ **Full tracing** - Input/output/tokens/costs tracked via OpenLIT
- ✅ **Quality scoring** - 4 automatic metrics + custom user feedback
- ✅ **Prompt management** - Centralized, versioned instructions
- ✅ **User feedback** - 👍👎 ratings and decimal scores (0-1)

### Technical Features
- ✅ **Agno agent** with SQL database queries (10K records)
- ✅ **Generic wrapper** - Add observability to ANY Agno agent
- ✅ **Clean architecture** - Business logic separated from observability
- ✅ **No tight coupling** - Agents work with OR without Langfuse
- ✅ **Custom scores** - Add your own metrics with your logic
- ✅ **Environment-based config** - All settings in .env

## 📁 Structure

```
climate-agent-observability/
├── main.py                  # Run this!
├── src/
│   ├── agents/             # Agent implementations
│   ├── observability/      # Langfuse integration
│   ├── custom_log/         # Logging
│   ├── tools/              # Database tools
│   ├── config/             # Settings
│   └── utils/              # Validation
├── scripts/                 # Setup scripts
├── data/                    # Database
└── docs/                    # Documentation
```

## 💻 Commands

```bash
python main.py                    # Interactive chat (Session memory enabled)
python main.py --create-prompt    # Setup managed prompt
python main.py --help             # Show help
```

> **Note:** The interactive chat maintains **in-memory history**, allowing for follow-up questions within the same session.

## 🔍 Observability with Langfuse

### Self-Hosted Langfuse

This example uses **self-hosted Langfuse** for complete control and privacy:

```bash
# Start Langfuse (from langfuse directory)
cd ../langfuse
docker-compose up -d

# Access at:
http://localhost:3000
```

**Benefits of Self-Hosted:**
- ✅ Full data control
- ✅ No external dependencies
- ✅ Free and open-source
- ✅ Custom deployment options

### What Gets Tracked

Every query automatically captures:
- **Input/Output** - Full conversation text
- **Tokens** - Actual usage (not estimates)
- **Costs** - Real calculation based on usage
- **Quality Scores** - 4 automatic metrics (optional)
- **User Feedback** - 👍👎 ratings
- **Prompt Versions** - Which prompt was used
- **Latency** - Response time

### View Results

**Self-Hosted:** http://localhost:3000  
**Cloud:** https://cloud.langfuse.com

**Dashboard Tabs:**
- **Traces** - All queries with full details
- **Scores** - Quality metrics and trends
- **Prompts** - Centralized prompt management

## 🔄 No Tight Coupling - Completely Flexible

### Use Agent Without Observability

```python
from src.agents import BaseClimateAgent

agent = BaseClimateAgent()
response = agent.execute("Question")
# Works independently - no Langfuse needed!
```

### Add Observability Optionally

```python
from src.observability import wrap_agent_with_observability

observed = wrap_agent_with_observability(your_agent, "AgentName")
result = observed.execute("Input")
# Observability added externally - not built into agent!
```

### Add Custom Scores

```python
from langfuse import get_client

langfuse = get_client()
langfuse.create_score(
    trace_id=result['trace_id'],
    observation_id=result['observation_id'],
    name="your_custom_score",
    value=0.95  # Your logic!
)
# Define your own scoring - not forced to use predefined ones!
```

**See `examples/` folder for complete demos.**

## 📚 Documentation

- **README.md** (this file) - Overview
- **docs/GUIDE.md** - Complete user guide
- **env.template** - Configuration template
- **src/*/README.md** - Module documentation

## 🏗️ Architecture

**Two-layer design:**
1. **Base layer** - Pure agent logic (no observability)
2. **Wrapper layer** - Adds Langfuse observability

**Result:** Clean, testable, reusable code.

## 📊 Database

This project uses the **Climate Change Impact on Agriculture** dataset from Kaggle.
**Source:** [Kaggle Dataset](https://www.kaggle.com/datasets/waqi786/climate-change-impact-on-agriculture)

It contains 10,000 records including:
- Year, Country, Region, Crop Type
- Temperature, Precipitation, CO2
- Crop Yield, Economic Impact
- Adaptation Strategies

## 🛠️ Tech Stack

- **Agno** - Agent framework for building AI agents
- **Langfuse** - LLM observability platform (⭐ focus of this example)
- **OpenLIT** - Instrumentation for automatic tracing
- **SQLite** - Database with climate/agriculture data
- **Python 3.11+** - Runtime

## 🎓 What You'll Learn

By exploring this example, you'll understand:

1. **How to integrate Langfuse** into an Agno agent application
2. **How to separate business logic** from observability code
3. **How to create a generic wrapper** that works with any agent
4. **How to implement custom scoring** based on your needs
5. **How to manage prompts centrally** via Langfuse
6. **How to collect and track user feedback**
7. **Best practices** for production-ready LLM observability

## 📊 Langfuse Integration

This example demonstrates the **three pillars of Langfuse observability**:

### 1. Tracing
- Track every query with input, output, tokens, and costs
- Via OpenLIT instrumentation (automatic)
- **Why OpenLIT?** It provides **automatic OpenTelemetry (OTel) instrumentation** for LLM libraries. Instead of manually logging every call, OpenLIT automatically intercepts `openai` (and other) library calls used by Agno and sends the traces to Langfuse.
- Zero manual tracking code needed

### 2. Scoring
- 4 automatic quality metrics (optional)
- Custom scores with your own logic (fully flexible)
- User feedback (👍👎 or 0-1 ratings)

### 3. Prompt Management
- Store prompts in Langfuse (centralized)
- Version control and A/B testing
- Update without code deployment

## 🎓 Learning Resource

This is a **reference implementation** for:
- Integrating Langfuse with Agno agents
- Building observable AI applications
- Implementing production-ready LLM monitoring
- Creating reusable observability patterns

**Use this as:**
- Template for your own agents
- Learning resource for Langfuse
- Example of clean architecture
- Starting point for production apps

## 🔮 Roadmap & Future Work

The following advanced evaluation techniques are currently **in development** and will be covered in future updates:

- 🤖 **LLM-as-a-Judge**: Automated evaluation pipelines using stronger models to critique agent performance.
- 👩‍💻 **Human Annotation**: Workflows for manual review and correction of agent outputs.
- 📚 **Evaluation Datasets**: Curated Golden Datasets for benchmarking and regression testing.

## 📚 Related Resources

- [Langfuse Documentation](https://langfuse.com/docs)
- [Langfuse + Agno Integration](https://langfuse.com/integrations/frameworks/agno-agents)
- [Agno Documentation](https://docs.agno.ai)
- [OpenLIT Documentation](https://docs.openlit.io)

## 📝 License

This is an example/demonstration project for learning Langfuse observability.

---

**🚀 Quick Start:** `python main.py --demo`  
**📖 Full Guide:** `docs/GUIDE.md`  
**🔄 Wrap Your Agent:** `src/observability/WRAPPER_GUIDE.md`  
**💡 Examples:** `examples/` folder

**Built to demonstrate Langfuse observability for Agentic AI applications** 🌱✨
