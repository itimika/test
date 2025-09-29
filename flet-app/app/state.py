"""State management for the Flet calculator application."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Callable, List, Optional

from .logic import (
    SUPPORTED_OPERATORS,
    calculate_percentage,
    decimal_to_token,
    ensure_max_length,
    evaluate_expression,
    format_decimal,
    normalize_operator,
    parse_input_value,
    toggle_sign,
)

_MAX_INPUT_DIGITS = 16


@dataclass
class CalculatorState:
    """Container describing the mutable calculator state."""

    display_value: str = "0"
    input_buffer: str = ""
    last_operator: Optional[str] = None
    expression_tokens: List[str] = field(default_factory=list)
    should_reset_display: bool = False
    memory_value: Decimal = Decimal("0")
    error_state: bool = False
    just_evaluated: bool = False


class CalculatorStateManager:
    """Implements calculator behaviour and state transitions."""

    def __init__(self, update_callback: Optional[Callable[[], None]] = None) -> None:
        self.state = CalculatorState()
        self._update_callback = update_callback

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _notify(self) -> None:
        if self._update_callback:
            self._update_callback()

    def _current_entry(self) -> str:
        return self.state.input_buffer or self.state.display_value

    def _reset_entry(self) -> None:
        self.state.input_buffer = ""
        self.state.should_reset_display = False
        self.state.just_evaluated = False

    def _set_error(self) -> None:
        self.state.display_value = "Error"
        self.state.input_buffer = ""
        self.state.expression_tokens.clear()
        self.state.last_operator = None
        self.state.should_reset_display = True
        self.state.error_state = True
        self.state.just_evaluated = False
        self._notify()

    def _clear_error(self) -> None:
        if self.state.error_state:
            self.state.error_state = False
            self.state.display_value = "0"
            self.state.input_buffer = ""
            self.state.expression_tokens.clear()
            self.state.last_operator = None
            self.state.should_reset_display = False
            self.state.just_evaluated = False

    def _apply_numeric_entry(self, new_value: str) -> None:
        self.state.input_buffer = new_value
        self.state.display_value = new_value

    def _push_current_value(self) -> Optional[str]:
        raw_value = self._current_entry()
        parsed = parse_input_value(raw_value)
        if parsed is None:
            return None
        token = decimal_to_token(parsed)
        tokens = self.state.expression_tokens
        if not tokens or tokens[-1] in SUPPORTED_OPERATORS:
            tokens.append(token)
        else:
            tokens[-1] = token
        return token

    def _preview_expression(self) -> None:
        tokens = self.state.expression_tokens
        if not tokens:
            return
        if tokens[-1] in SUPPORTED_OPERATORS:
            slice_tokens = tokens[:-1]
        else:
            slice_tokens = tokens
        if not slice_tokens:
            return
        try:
            result = evaluate_expression(slice_tokens)
        except ZeroDivisionError:
            self._set_error()
            return
        self.state.display_value = format_decimal(result)

    # ------------------------------------------------------------------
    # Public interface invoked by the UI
    # ------------------------------------------------------------------
    def handle_number_input(self, digit: str) -> None:
        if self.state.error_state:
            self._clear_error()

        if self.state.should_reset_display or self.state.just_evaluated:
            if self.state.just_evaluated:
                self.state.expression_tokens.clear()
                self.state.last_operator = None
            self._reset_entry()
            self.state.display_value = "0"

        buffer = self.state.input_buffer or self.state.display_value
        if buffer == "0":
            buffer = digit
        else:
            prospective = buffer + digit
            if not ensure_max_length(prospective, max_digits=_MAX_INPUT_DIGITS):
                return
            buffer = prospective

        self._apply_numeric_entry(buffer)
        self._notify()

    def handle_decimal_input(self) -> None:
        if self.state.error_state:
            self._clear_error()

        if self.state.should_reset_display or self.state.just_evaluated:
            if self.state.just_evaluated:
                self.state.expression_tokens.clear()
                self.state.last_operator = None
            self._reset_entry()
            self._apply_numeric_entry("0.")
        else:
            buffer = self.state.input_buffer or self.state.display_value
            if "." in buffer:
                return
            prospective = buffer + "."
            if not ensure_max_length(prospective, max_digits=_MAX_INPUT_DIGITS + 1):
                return
            self._apply_numeric_entry(prospective)

        self._notify()

    def handle_operator_input(self, operator: str) -> None:
        if self.state.error_state:
            return

        normalized = normalize_operator(operator)
        if normalized is None:
            return

        if (
            self.state.should_reset_display
            and not self.state.input_buffer
            and self.state.expression_tokens
            and self.state.expression_tokens[-1] in SUPPORTED_OPERATORS
        ):
            self.state.expression_tokens[-1] = normalized
            self.state.last_operator = operator
            self._notify()
            return

        token = self._push_current_value()
        if token is None:
            self._set_error()
            return

        tokens = self.state.expression_tokens
        if tokens and tokens[-1] in SUPPORTED_OPERATORS and self.state.should_reset_display:
            tokens[-1] = normalized
        else:
            tokens.append(normalized)

        self.state.last_operator = operator
        self.state.should_reset_display = True
        self.state.input_buffer = ""
        self.state.just_evaluated = False

        self._preview_expression()
        self._notify()

    def handle_equals(self) -> None:
        if self.state.error_state:
            return

        token = self._push_current_value()
        if token is None and self.state.expression_tokens:
            # If we fail to parse but have tokens, treat as error
            self._set_error()
            return

        tokens = self.state.expression_tokens
        if not tokens:
            # Nothing to evaluate – normalise display
            parsed = parse_input_value(self.state.display_value)
            if parsed is not None:
                self.state.display_value = format_decimal(parsed)
            self.state.input_buffer = ""
            self.state.just_evaluated = True
            self.state.should_reset_display = True
            self._notify()
            return

        if tokens[-1] in SUPPORTED_OPERATORS:
            tokens.pop()  # dangling operator – drop it
        try:
            result = evaluate_expression(tokens)
        except ZeroDivisionError:
            self._set_error()
            return

        self.state.display_value = format_decimal(result)
        self.state.expression_tokens = [decimal_to_token(result)]
        self.state.last_operator = None
        self.state.input_buffer = ""
        self.state.should_reset_display = True
        self.state.just_evaluated = True
        self._notify()

    def handle_clear(self) -> None:
        if self.state.error_state:
            self._clear_error()
        self.state.display_value = "0"
        self.state.input_buffer = ""
        self.state.should_reset_display = False
        self.state.just_evaluated = False
        self._notify()

    def handle_all_clear(self) -> None:
        self.state = CalculatorState()
        self._notify()

    def handle_backspace(self) -> None:
        if self.state.error_state:
            self.handle_all_clear()
            return

        if self.state.should_reset_display or self.state.just_evaluated:
            self.handle_clear()
            return

        buffer = self.state.input_buffer or self.state.display_value
        if len(buffer) <= 1:
            self._apply_numeric_entry("0")
        else:
            buffer = buffer[:-1]
            if buffer in {"-", ""}:
                buffer = "0"
            self._apply_numeric_entry(buffer)

        self._notify()

    def handle_plus_minus(self) -> None:
        if self.state.error_state:
            return

        parsed = parse_input_value(self._current_entry())
        if parsed is None:
            return

        toggled = toggle_sign(parsed)
        token = decimal_to_token(toggled)
        self._apply_numeric_entry(token)
        self.state.just_evaluated = False
        self.state.should_reset_display = False
        self._notify()

    def handle_percentage(self) -> None:
        if self.state.error_state:
            return

        parsed = parse_input_value(self._current_entry())
        if parsed is None:
            return

        percent_value = calculate_percentage(parsed)
        token = decimal_to_token(percent_value)
        self._apply_numeric_entry(token)
        self.state.just_evaluated = False
        self.state.should_reset_display = False
        self._notify()

    # ------------------------------------------------------------------
    # Memory functions (optional for stretch goals)
    # ------------------------------------------------------------------
    def handle_memory_clear(self) -> None:
        self.state.memory_value = Decimal("0")
        self._notify()

    def handle_memory_recall(self) -> None:
        if self.state.error_state:
            self._clear_error()
        token = decimal_to_token(self.state.memory_value)
        self._apply_numeric_entry(token)
        self.state.should_reset_display = False
        self.state.just_evaluated = False
        self._notify()

    def handle_memory_add(self) -> None:
        parsed = parse_input_value(self._current_entry())
        if parsed is None:
            return
        self.state.memory_value += parsed
        self._notify()

    def handle_memory_subtract(self) -> None:
        parsed = parse_input_value(self._current_entry())
        if parsed is None:
            return
        self.state.memory_value -= parsed
        self._notify()

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------
    def get_display_value(self) -> str:
        return self.state.display_value

    def is_memory_active(self) -> bool:
        return self.state.memory_value != Decimal("0")
