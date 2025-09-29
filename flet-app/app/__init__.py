"""
Flet Calculator App Package

This package contains the main components of the calculator application:
- ui: User interface components and layout
- state: Application state management
- logic: Calculation logic and mathematical operations
"""

__version__ = "0.1.0"
__author__ = "Calculator App Team"

# Lightweight re-exports to avoid importing Flet during test collection
from .logic import *  # noqa: F401,F403  (re-export convenience)

__all__ = []  # populated by logic module exports
