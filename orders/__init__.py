"""
Orders Module
Advanced order types and safety mechanisms for professional F&O trading.

Includes:
- Order confirmation and validation (OrderManager)
- Stop-loss automation (StopLossManager)
- Advanced order types (Bracket, OCO, Trailing, Iceberg)
"""

from .bracket_order import BracketOrder, OrderStatus, create_bracket_order_from_signal
from .trailing_stop import TrailingStop, TrailingStopType, create_trailing_stop_from_position
from .oco_order import OCOOrder, OCOStatus, create_oco_from_range, create_oco_from_current_price
from .iceberg_order import IcebergOrder, IcebergStatus, create_iceberg_from_position_size
from .order_manager import OrderManager, OrderPreview, OrderValidationStatus, OrderBlockReason
from .stop_loss_manager import StopLossManager, StopLossOrder, StopLossType, StopLossStatus

__all__ = [
    # Order Management (Safety)
    'OrderManager',
    'OrderPreview',
    'OrderValidationStatus',
    'OrderBlockReason',

    # Stop-Loss Management (Safety)
    'StopLossManager',
    'StopLossOrder',
    'StopLossType',
    'StopLossStatus',

    # Bracket Orders
    'BracketOrder',
    'OrderStatus',
    'create_bracket_order_from_signal',

    # Trailing Stops
    'TrailingStop',
    'TrailingStopType',
    'create_trailing_stop_from_position',

    # OCO Orders
    'OCOOrder',
    'OCOStatus',
    'create_oco_from_range',
    'create_oco_from_current_price',

    # Iceberg Orders
    'IcebergOrder',
    'IcebergStatus',
    'create_iceberg_from_position_size'
]
