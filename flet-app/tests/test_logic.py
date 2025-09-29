"""Unit tests for calculator logic helpers."""

from decimal import Decimal

import pytest

from app.logic import (
    calculate_percentage,
    decimal_to_token,
    evaluate_expression,
    format_decimal,
    normalize_operator,
    parse_input_value,
    toggle_sign,
)


@pytest.mark.parametrize(
    "tokens, expected",
    [
        (["1", "+", "2"], Decimal("3")),
        (["10", "-", "4"], Decimal("6")),
        (["7", "×", "8"], Decimal("56")),
        (["15", "÷", "3"], Decimal("5")),
    ],
)
def test_basic_operations(tokens, expected):
    """Ensure single-operator expressions compute correctly."""

    assert evaluate_expression(tokens) == expected


def test_operator_precedence_with_chain():
    """Operator precedence should mirror typical calculator rules."""

    result = evaluate_expression(["1", "+", "2", "×", "3"])
    assert result == Decimal("7")

    result = evaluate_expression(["10", "÷", "2", "+", "3", "×", "4", "-", "5"])
    assert result == Decimal("12")


def test_decimal_precision_and_rounding():
    """Decimal arithmetic should avoid binary float artefacts."""

    precise_sum = evaluate_expression(["0.1", "+", "0.2"])
    assert precise_sum == Decimal("0.3")

    formatted = format_decimal(Decimal("2") / Decimal("3"))
    # Rounded half up to ten fractional digits -> 0.6666666667
    assert formatted == "0.6666666667"


def test_percentage_helper():
    """Percentage conversion divides by 100 using Decimal."""

    assert calculate_percentage(Decimal("50")) == Decimal("0.5")
    assert calculate_percentage(Decimal("12.5")) == Decimal("0.125")


def test_zero_division_detection():
    """Division by zero should raise ``ZeroDivisionError``."""

    with pytest.raises(ZeroDivisionError):
        evaluate_expression(["5", "÷", "0"])


def test_large_number_formatting_falls_back_to_scientific():
    """Very large magnitudes should use scientific notation for display."""

    text = format_decimal(Decimal("12345678901234567890"))
    assert "E" in text


def test_parse_input_edge_cases():
    """Parsing should be resilient to incidental input formats."""

    assert parse_input_value("12.") == Decimal("12")
    assert parse_input_value("") == Decimal("0")
    assert parse_input_value("Error") is None


def test_toggle_sign_and_token_normalisation():
    """Sign toggling and token conversion should behave intuitively."""

    value = Decimal("42")
    assert toggle_sign(value) == Decimal("-42")
    assert decimal_to_token(Decimal("5.500")) == "5.5"
    assert normalize_operator("×") == "*"
    assert normalize_operator("÷") == "/"


def test_fractional_edge_case_rounding():
    """Rounding should follow HALF_UP semantics for borderline values."""

    value = Decimal("1.005")
    formatted = format_decimal(value)
    assert formatted == "1.005"

    scaled = format_decimal(value * Decimal("100"))
    assert scaled == "100.5"
