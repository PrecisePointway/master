"""Vortex routing feature flags.

All Vortex-related enforcement MUST be gated behind these flags.
Simulation MAY run regardless of flag state.
"""

# Draft status flag: while False, Vortex Law is DRAFT ONLY.
FEATURE_VORTEX: bool = False
