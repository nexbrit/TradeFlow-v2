"""
TradeFlow v2
A comprehensive trading platform with live signals, Upstox integration, and pandas screeners
"""

__version__ = "2.0.0"
__author__ = "TradeFlow Team"

from .main import FNOTradingApp
from .api import UpstoxClient
from .signals import SignalGenerator, SignalType
from .screeners import FNOScreener
from .utils import ConfigLoader, setup_logger

__all__ = [
    'FNOTradingApp',
    'UpstoxClient',
    'SignalGenerator',
    'SignalType',
    'FNOScreener',
    'ConfigLoader',
    'setup_logger'
]
