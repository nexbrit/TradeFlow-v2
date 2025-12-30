"""
Circuit Breaker - Daily loss protection system.

Monitors daily P&L and triggers protective actions:
- Tiered alerts at 50%, 80%, 100% of daily loss limit
- Automatic position square-off at limit
- Trading block until next day
- Emergency override with password protection
"""

from datetime import datetime, date
from typing import Any, Optional, Dict, List, Callable
from enum import Enum
from dataclasses import dataclass
import threading
import logging
import hashlib

from data.services.capital_service import CapitalService

logger = logging.getLogger(__name__)


class CircuitBreakerStatus(Enum):
    """Circuit breaker status levels."""
    NORMAL = "normal"           # < 50% of limit
    CAUTION = "caution"         # 50-80% of limit
    WARNING = "warning"         # 80-100% of limit
    TRIGGERED = "triggered"     # 100% - trading blocked
    EMERGENCY = "emergency"     # Emergency square-off in progress
    OVERRIDDEN = "overridden"   # Manually overridden (logged)


@dataclass
class DailyLossState:
    """Tracks daily P&L state."""
    date: date
    realized_pnl: float = 0.0
    unrealized_pnl: float = 0.0
    peak_pnl: float = 0.0  # Highest P&L of the day
    lowest_pnl: float = 0.0  # Lowest P&L of the day
    breach_count: int = 0  # Number of times limit approached
    triggered_at: Optional[datetime] = None
    override_active: bool = False
    override_reason: str = ""


class CircuitBreaker:
    """
    Daily loss circuit breaker with automatic protection.

    Features:
    - Configurable daily loss limit (% of capital)
    - Real-time P&L monitoring (realized + unrealized)
    - Tiered alert system (50%, 80%, 100%)
    - Automatic square-off at limit
    - Trading block until next session
    - Secure override capability

    Example:
        breaker = CircuitBreaker(capital_service, daily_loss_percent=2.0)

        # Check status
        status = breaker.get_status()
        if status['is_blocked']:
            print("Trading blocked for today")

        # Update with P&L
        breaker.update_pnl(realized=-5000, unrealized=-2000)

        # Register callbacks
        breaker.on_warning(lambda: send_alert("80% loss limit reached"))
        breaker.on_trigger(lambda: square_off_all_positions())
    """

    # Alert thresholds (% of daily limit)
    CAUTION_THRESHOLD = 50.0   # Yellow alert
    WARNING_THRESHOLD = 80.0   # Orange alert, send notification
    TRIGGER_THRESHOLD = 100.0  # Red alert, block trading

    def __init__(
        self,
        capital_service: Optional[CapitalService] = None,
        daily_loss_percent: float = 2.0,
        override_password_hash: Optional[str] = None
    ):
        """
        Initialize circuit breaker.

        Args:
            capital_service: Capital service for position sizing
            daily_loss_percent: Maximum daily loss as % of capital
            override_password_hash: SHA-256 hash of override password
        """
        self._capital = capital_service or CapitalService()
        self._daily_loss_percent = daily_loss_percent
        self._override_hash = override_password_hash

        # State
        self._state = self._get_or_create_state()
        self._status = CircuitBreakerStatus.NORMAL
        self._lock = threading.Lock()

        # Callbacks
        self._on_caution_callbacks: List[Callable] = []
        self._on_warning_callbacks: List[Callable] = []
        self._on_trigger_callbacks: List[Callable] = []
        self._on_emergency_callbacks: List[Callable] = []

    def _get_or_create_state(self) -> DailyLossState:
        """Get or create today's state."""
        today = date.today()
        return DailyLossState(date=today)

    def _reset_if_new_day(self) -> None:
        """Reset state if it's a new trading day."""
        today = date.today()
        if self._state.date != today:
            logger.info("New trading day - resetting circuit breaker")
            self._state = DailyLossState(date=today)
            self._status = CircuitBreakerStatus.NORMAL

    @property
    def daily_loss_limit(self) -> float:
        """Get daily loss limit in rupees."""
        capital = self._capital.get_current_capital()
        return capital * (self._daily_loss_percent / 100)

    @property
    def is_triggered(self) -> bool:
        """Check if circuit breaker is triggered."""
        return self._status in [
            CircuitBreakerStatus.TRIGGERED,
            CircuitBreakerStatus.EMERGENCY
        ]

    @property
    def is_blocked(self) -> bool:
        """Check if trading is blocked."""
        if self._state.override_active:
            return False
        return self.is_triggered

    def update_pnl(
        self,
        realized: float = 0.0,
        unrealized: float = 0.0
    ) -> CircuitBreakerStatus:
        """
        Update P&L and check circuit breaker thresholds.

        Args:
            realized: Realized P&L (closed positions)
            unrealized: Unrealized P&L (open positions MTM)

        Returns:
            Current circuit breaker status
        """
        with self._lock:
            self._reset_if_new_day()

            self._state.realized_pnl = realized
            self._state.unrealized_pnl = unrealized

            total_pnl = realized + unrealized

            # Track peak and trough
            if total_pnl > self._state.peak_pnl:
                self._state.peak_pnl = total_pnl
            if total_pnl < self._state.lowest_pnl:
                self._state.lowest_pnl = total_pnl

            # Calculate loss percentage
            limit = self.daily_loss_limit
            if limit <= 0:
                return self._status

            # Negative P&L = loss
            loss_amount = abs(min(total_pnl, 0))
            loss_percent = (loss_amount / limit) * 100

            # Check thresholds and update status
            old_status = self._status

            if loss_percent >= self.TRIGGER_THRESHOLD:
                self._status = CircuitBreakerStatus.TRIGGERED
                if self._state.triggered_at is None:
                    self._state.triggered_at = datetime.now()
                    self._state.breach_count += 1
                    self._fire_callbacks(self._on_trigger_callbacks)
                    logger.critical(
                        f"CIRCUIT BREAKER TRIGGERED! "
                        f"Loss: ₹{loss_amount:,.0f} ({loss_percent:.1f}% of limit)"
                    )

            elif loss_percent >= self.WARNING_THRESHOLD:
                if self._status != CircuitBreakerStatus.TRIGGERED:
                    self._status = CircuitBreakerStatus.WARNING
                    if old_status != CircuitBreakerStatus.WARNING:
                        self._fire_callbacks(self._on_warning_callbacks)
                        logger.warning(
                            f"Circuit breaker WARNING: "
                            f"Loss at {loss_percent:.1f}% of daily limit"
                        )

            elif loss_percent >= self.CAUTION_THRESHOLD:
                if self._status not in [
                    CircuitBreakerStatus.WARNING,
                    CircuitBreakerStatus.TRIGGERED
                ]:
                    self._status = CircuitBreakerStatus.CAUTION
                    if old_status == CircuitBreakerStatus.NORMAL:
                        self._fire_callbacks(self._on_caution_callbacks)
                        logger.info(
                            f"Circuit breaker CAUTION: "
                            f"Loss at {loss_percent:.1f}% of daily limit"
                        )

            else:
                if not self.is_triggered:
                    self._status = CircuitBreakerStatus.NORMAL

            return self._status

    def _fire_callbacks(self, callbacks: List[Callable]) -> None:
        """Fire registered callbacks."""
        for callback in callbacks:
            try:
                callback()
            except Exception as e:
                logger.error(f"Callback error: {e}")

    def on_caution(self, callback: Callable) -> None:
        """Register callback for caution level."""
        self._on_caution_callbacks.append(callback)

    def on_warning(self, callback: Callable) -> None:
        """Register callback for warning level."""
        self._on_warning_callbacks.append(callback)

    def on_trigger(self, callback: Callable) -> None:
        """Register callback for trigger level."""
        self._on_trigger_callbacks.append(callback)

    def on_emergency(self, callback: Callable) -> None:
        """Register callback for emergency square-off."""
        self._on_emergency_callbacks.append(callback)

    def trigger_emergency_exit(self, reason: str = "") -> bool:
        """
        Manually trigger emergency square-off.

        Args:
            reason: Reason for emergency exit

        Returns:
            True if initiated
        """
        with self._lock:
            self._status = CircuitBreakerStatus.EMERGENCY
            self._state.triggered_at = datetime.now()

            logger.critical(
                f"EMERGENCY SQUARE-OFF INITIATED: {reason}"
            )

            self._fire_callbacks(self._on_emergency_callbacks)
            return True

    def override(
        self,
        password: str,
        reason: str
    ) -> bool:
        """
        Override circuit breaker (with safeguards).

        Requires password and logs the override.
        Override expires at end of day.

        Args:
            password: Override password
            reason: Reason for override (logged)

        Returns:
            True if override successful
        """
        # Verify password
        if self._override_hash:
            provided_hash = hashlib.sha256(password.encode()).hexdigest()
            if provided_hash != self._override_hash:
                logger.warning("Circuit breaker override DENIED: wrong password")
                return False

        with self._lock:
            self._state.override_active = True
            self._state.override_reason = reason
            self._status = CircuitBreakerStatus.OVERRIDDEN

        logger.warning(
            f"Circuit breaker OVERRIDDEN. Reason: {reason}. "
            f"THIS IS LOGGED AND WILL BE REVIEWED."
        )

        return True

    def cancel_override(self) -> None:
        """Cancel active override."""
        with self._lock:
            self._state.override_active = False
            self._state.override_reason = ""
            # Re-evaluate status
            self.update_pnl(
                self._state.realized_pnl,
                self._state.unrealized_pnl
            )

    def get_status(self) -> Dict[str, Any]:
        """
        Get current circuit breaker status for UI.

        Returns:
            Dictionary with status details
        """
        self._reset_if_new_day()

        limit = self.daily_loss_limit
        total_pnl = self._state.realized_pnl + self._state.unrealized_pnl
        loss_amount = abs(min(total_pnl, 0))
        loss_percent = (loss_amount / limit * 100) if limit > 0 else 0
        distance_to_limit = limit - loss_amount

        return {
            'status': self._status.value,
            'is_blocked': self.is_blocked,
            'is_triggered': self.is_triggered,

            # P&L details
            'realized_pnl': self._state.realized_pnl,
            'unrealized_pnl': self._state.unrealized_pnl,
            'total_pnl': total_pnl,
            'peak_pnl': self._state.peak_pnl,
            'lowest_pnl': self._state.lowest_pnl,

            # Limit details
            'daily_loss_limit': limit,
            'daily_loss_percent': self._daily_loss_percent,
            'loss_amount': loss_amount,
            'loss_percent_of_limit': loss_percent,
            'distance_to_limit': distance_to_limit,

            # Thresholds
            'caution_threshold': self.CAUTION_THRESHOLD,
            'warning_threshold': self.WARNING_THRESHOLD,
            'trigger_threshold': self.TRIGGER_THRESHOLD,

            # Alerts
            'is_caution': loss_percent >= self.CAUTION_THRESHOLD,
            'is_warning': loss_percent >= self.WARNING_THRESHOLD,

            # Override
            'override_active': self._state.override_active,
            'override_reason': self._state.override_reason,

            # Metadata
            'breach_count': self._state.breach_count,
            'triggered_at': (
                self._state.triggered_at.isoformat()
                if self._state.triggered_at else None
            ),
            'date': self._state.date.isoformat(),
            'timestamp': datetime.now().isoformat()
        }

    def get_progress_bar_data(self) -> Dict[str, Any]:
        """
        Get data for UI progress bar display.

        Returns:
            Dictionary with progress bar values
        """
        status = self.get_status()

        # Color based on status
        if status['is_triggered']:
            color = 'red'
        elif status['is_warning']:
            color = 'orange'
        elif status['is_caution']:
            color = 'yellow'
        else:
            color = 'green'

        return {
            'percent': min(status['loss_percent_of_limit'], 100),
            'color': color,
            'label': f"₹{status['loss_amount']:,.0f} / ₹{status['daily_loss_limit']:,.0f}",
            'sub_label': f"{status['loss_percent_of_limit']:.1f}% of daily limit"
        }

    def should_allow_order(self) -> Dict[str, Any]:
        """
        Check if new orders should be allowed.

        Returns:
            Dictionary with allow status and reason
        """
        self._reset_if_new_day()

        if self.is_blocked:
            return {
                'allowed': False,
                'reason': 'Circuit breaker triggered - trading blocked',
                'status': self._status.value
            }

        status = self.get_status()

        if status['is_warning']:
            return {
                'allowed': True,
                'warning': 'Approaching daily loss limit - trade with caution',
                'status': self._status.value,
                'loss_percent': status['loss_percent_of_limit']
            }

        if status['is_caution']:
            return {
                'allowed': True,
                'warning': '50% of daily loss limit used',
                'status': self._status.value,
                'loss_percent': status['loss_percent_of_limit']
            }

        return {
            'allowed': True,
            'status': self._status.value,
            'loss_percent': status['loss_percent_of_limit']
        }

    def set_daily_loss_limit(self, percent: float) -> None:
        """
        Update daily loss limit percentage.

        Args:
            percent: New daily loss limit as % of capital
        """
        if percent <= 0 or percent > 20:
            raise ValueError("Daily loss limit must be between 0 and 20%")

        self._daily_loss_percent = percent
        logger.info(f"Daily loss limit updated to {percent}%")

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get circuit breaker statistics.

        Returns:
            Dictionary with historical statistics
        """
        return {
            'current_limit_percent': self._daily_loss_percent,
            'current_limit_amount': self.daily_loss_limit,
            'today_breach_count': self._state.breach_count,
            'today_triggered': self._state.triggered_at is not None,
            'today_peak_pnl': self._state.peak_pnl,
            'today_lowest_pnl': self._state.lowest_pnl,
            'override_used': self._state.override_active
        }
