"""Agent modules."""

from .base_agent import BaseClimateAgent
from .observed_climate import ObservedClimateAgent

# For backward compatibility
ClimateAgricultureAgent = ObservedClimateAgent

__all__ = [
    'BaseClimateAgent',          # Pure agent (no observability)
    'ObservedClimateAgent',      # With observability (uses generic wrapper)
    'ClimateAgricultureAgent',   # Alias for compatibility
]

