"""Core calculation logic for the Flet calculator app.

This module provides pure functions for performing decimal-safe
calculations with operator precedence, formatting results for
presentation, and parsing user input safely. All arithmetic uses
``Decimal`` with ``ROUND_HALF_UP`` semantics to match a physical
calculator's behaviour and to avoid binary floating point surprises.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, getcontext
from typing import Iterable, List, Optional, Sequence, Union

# Configure global decimal behaviour for the calculator
getcontext().prec = 28  # sufficient precision for typical calculator usage
getcontext().rounding = ROUND_HALF_UP

DecimalLike = Union[str, int, float, Decimal]
Operator = str

SUPPORTED_OPERATORS = {"+", "-", "*", "/"}
_MAX_DECIMAL_PLACES = 10
_DEFAULT_MAX_DIGITS = 12

_OPERATOR_ALIASES = {
    "×": "*",
    "x": "*",
    "X": "*",
    "⋅": "*",
    "÷": "/",
    "／": "/",
    "﹢": "+",
    "﹣": "-",
}

_OPERATOR_PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
}


def normalize_operator(operator: str) -> Optional[Operator]:
    """Normalise various operator glyphs into the internal representation.

    Args:
        operator: Operator provided by UI/user input.

    Returns:
        One of ``+``, ``-``, ``*`` or ``/`` if recognised, otherwise ``None``.
    """

    if not operator:
        return None

    candidate = operator.strip()
    if candidate in SUPPORTED_OPERATORS:
        return candidate

    return _OPERATOR_ALIASES.get(candidate)


def to_decimal(value: DecimalLike) -> Decimal:
    """Convert supported numeric inputs into a ``Decimal`` instance."""

    if isinstance(value, Decimal):
        return value
    if isinstance(value, (int, float)):
        return Decimal(str(value))
    return Decimal(str(value).strip())


def parse_input_value(raw: str) -> Optional[Decimal]:
    """Parse a user-entered string into a ``Decimal``.

    Returns ``None`` if the string represents an error state or cannot be
    parsed. Trailing decimal points (e.g. ``"12."``) are allowed and treated
    as integers.
    """

    if raw is None:
        return None

    text = str(raw).strip()
    if text == "" or text in {"+", "-"}:
        return Decimal("0")

    lowered = text.lower()
    if lowered in {"error", "inf", "-inf", "nan"}:
        return None

    if text.endswith("."):
        text = text[:-1] or "0"

    try:
        return to_decimal(text)
    except (InvalidOperation, ValueError):
        return None


def toggle_sign(value: Decimal) -> Decimal:
    """Return ``value`` with its sign flipped."""

    return -value


def calculate_percentage(value: Decimal) -> Decimal:
    """Return ``value`` expressed as a percentage (divide by 100)."""

    return value / Decimal("100")


def decimal_to_token(value: Decimal) -> str:
    """Convert a ``Decimal`` to a canonical string suitable for expression tokens."""

    if value.is_nan() or value.is_infinite():
        return "0"

    normalized = value.normalize()
    text = format(normalized, "f")

    if "." in text:
        text = text.rstrip("0").rstrip(".")
    if text in {"", "-"}:
        text = "0"

    return text


def _apply_operator(left: Decimal, right: Decimal, operator: Operator) -> Decimal:
    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    if operator == "/":
        if right == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return left / right
    raise ValueError(f"Unsupported operator: {operator}")


def evaluate_expression(tokens: Sequence[Union[str, Decimal]]) -> Decimal:
    """Evaluate an arithmetic expression respecting operator precedence.

    Args:
        tokens: Sequence of alternating operands and operators. Operands can be
            strings or ``Decimal`` instances. Operators may use calculator glyphs
            (e.g. ``×``) and will be normalised automatically.

    Returns:
        ``Decimal`` result of the expression.
    """

    if not tokens:
        return Decimal("0")

    values: List[Decimal] = []
    operators: List[Operator] = []

    def _push_value(token: Union[str, Decimal]):
        values.append(to_decimal(token))

    def _reduce_stack(min_precedence: int = 0) -> None:
        while (
            operators
            and len(values) >= 2
            and _OPERATOR_PRECEDENCE[operators[-1]] >= min_precedence
        ):
            op = operators.pop()
            right = values.pop()
            left = values.pop()
            values.append(_apply_operator(left, right, op))

    for token in tokens:
        if isinstance(token, str):
            op = normalize_operator(token)
            if op:
                current_precedence = _OPERATOR_PRECEDENCE[op]
                _reduce_stack(current_precedence)
                operators.append(op)
                continue
        _push_value(token)

    _reduce_stack()
    return values[-1] if values else Decimal("0")


def format_decimal(value: Decimal, *, max_digits: int = _DEFAULT_MAX_DIGITS) -> str:
    """Format a decimal value for display with optional scientific fallback."""

    if value.is_nan() or value.is_infinite():
        return "Error"

    quantize_exp = Decimal(f"1e-{_MAX_DECIMAL_PLACES}")
    try:
        quantized = value.quantize(quantize_exp)
    except InvalidOperation:
        quantized = value
    normalized = quantized.normalize()

    text = format(normalized, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    if text in {"", "-", "-0"}:
        text = "0"

    digit_count = len(text.replace("-", "").replace(".", ""))
    if digit_count > max_digits and value != 0:
        sci_digits = max(0, max_digits - 6)
        text = f"{value:.{sci_digits}E}"

    return text


def clamp_display(value: Decimal, *, max_digits: int = _DEFAULT_MAX_DIGITS) -> str:
    """Shortcut for callers that only need the formatted string."""

    return format_decimal(value, max_digits=max_digits)


def ensure_max_length(entry: str, *, max_digits: int = _DEFAULT_MAX_DIGITS) -> bool:
    """Return ``True`` if ``entry`` does not exceed the allowed digit budget."""

    plain = entry.replace("-", "").replace(".", "")
    return len(plain) <= max_digits


__all__ = [
    "SUPPORTED_OPERATORS",
    "calculate_percentage",
    "clamp_display",
    "decimal_to_token",
    "ensure_max_length",
    "evaluate_expression",
    "format_decimal",
    "normalize_operator",
    "parse_input_value",
    "to_decimal",
    "toggle_sign",
]
