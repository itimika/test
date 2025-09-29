"""Flet UI layer for the calculator application."""

from __future__ import annotations

import flet as ft

from .state import CalculatorStateManager


C = ft.Colors


def color(value: ft.Colors | str) -> str:
    """Convert ``Colors`` enum members to string values."""

    return value.value if hasattr(value, "value") else value


class CalculatorApp:
    """Encapsulates calculator controls and behaviour for mounting on a Flet page."""

    def __init__(self) -> None:
        self.state_manager = CalculatorStateManager(update_callback=self._on_state_update)
        self.display_text = ft.Text(
            value="0",
            size=40,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.RIGHT,
            color=color(C.BLACK),
            no_wrap=True,
        )
        self.memory_indicator = ft.Text(
            value="M",
            size=16,
            weight=ft.FontWeight.W_600,
            color=color(C.BLUE_ACCENT),
            visible=False,
        )
        self.control = self._build_layout()

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    def _build_layout(self) -> ft.Control:
        number_style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor=color(C.BLUE_GREY_50),
            color=color(C.BLACK),
            overlay_color=C.with_opacity(0.1, C.BLACK),
        )
        function_style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor=color(C.GREY_300),
            color=color(C.BLACK),
            overlay_color=C.with_opacity(0.1, C.BLACK),
        )
        operator_style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor=color(C.DEEP_ORANGE_ACCENT),
            color=color(C.WHITE),
            overlay_color=C.with_opacity(0.15, C.WHITE),
        )
        equals_style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor=color(C.BLUE_ACCENT),
            color=color(C.WHITE),
            overlay_color=C.with_opacity(0.15, C.WHITE),
        )

        display_panel = ft.Container(
            padding=ft.padding.symmetric(horizontal=16, vertical=20),
            bgcolor=color(C.WHITE),
            border_radius=ft.border_radius.all(16),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=28,
                color=C.with_opacity(0.12, C.BLACK),
                offset=ft.Offset(0, 8),
            ),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.END,
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[self.memory_indicator, ft.Text(value="")],
                    ),
                    self.display_text,
                ],
            ),
        )

        button_specs = [
            ("AC", function_style, 3, self._on_all_clear),
            ("C", function_style, 3, self._on_clear),
            ("%", function_style, 3, self._on_percentage),
            ("÷", operator_style, 3, lambda e: self._on_operator("÷")),
            ("BS", function_style, 3, self._on_backspace),
            ("7", number_style, 3, lambda e: self._on_number("7")),
            ("8", number_style, 3, lambda e: self._on_number("8")),
            ("9", number_style, 3, lambda e: self._on_number("9")),
            ("×", operator_style, 3, lambda e: self._on_operator("×")),
            ("4", number_style, 3, lambda e: self._on_number("4")),
            ("5", number_style, 3, lambda e: self._on_number("5")),
            ("6", number_style, 3, lambda e: self._on_number("6")),
            ("−", operator_style, 3, lambda e: self._on_operator("-")),
            ("1", number_style, 3, lambda e: self._on_number("1")),
            ("2", number_style, 3, lambda e: self._on_number("2")),
            ("3", number_style, 3, lambda e: self._on_number("3")),
            ("+", operator_style, 3, lambda e: self._on_operator("+")),
            ("±", function_style, 3, self._on_plus_minus),
            ("0", number_style, 6, lambda e: self._on_number("0")),
            (".", number_style, 3, self._on_decimal),
            ("=", equals_style, 12, self._on_equals),
        ]

        button_grid = ft.ResponsiveRow(
            columns=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            run_spacing=8,
            spacing=8,
            controls=[
                self._build_button(label, style, col, handler)
                for label, style, col, handler in button_specs
            ],
        )

        main_column = ft.Column(
            spacing=24,
            controls=[display_panel, button_grid],
        )

        container = ft.Container(
            bgcolor=color(C.BLUE_GREY_50),
            padding=ft.padding.all(24),
            content=ft.Container(
                alignment=ft.alignment.center,
                content=ft.Container(
                    width=340,
                    bgcolor=color(C.BLUE_GREY_50),
                    padding=ft.padding.all(12),
                    content=main_column,
                ),
            ),
        )

        return container

    def _build_button(self, text: str, style: ft.ButtonStyle, col: int, handler) -> ft.Control:
        col_map = {size: col for size in ("xs", "sm", "md", "lg", "xl")}
        return ft.Container(
            col=col_map,
            content=ft.ElevatedButton(text=text, style=style, height=60, on_click=handler),
        )

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------
    def mount(self, page: ft.Page) -> None:
        page.add(self.control)
        self._on_state_update()

    # ------------------------------------------------------------------
    # State synchronisation
    # ------------------------------------------------------------------
    def _on_state_update(self) -> None:
        if self.display_text:
            self.display_text.value = self.state_manager.get_display_value()
            self.display_text.update()
        if self.memory_indicator:
            self.memory_indicator.visible = self.state_manager.is_memory_active()
            self.memory_indicator.update()

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------
    def _on_number(self, digit: str) -> None:
        self.state_manager.handle_number_input(digit)

    def _on_operator(self, operator: str) -> None:
        self.state_manager.handle_operator_input(operator)

    def _on_equals(self, _event) -> None:
        self.state_manager.handle_equals()

    def _on_decimal(self, _event) -> None:
        self.state_manager.handle_decimal_input()

    def _on_clear(self, _event) -> None:
        self.state_manager.handle_clear()

    def _on_all_clear(self, _event) -> None:
        self.state_manager.handle_all_clear()

    def _on_backspace(self, _event) -> None:
        self.state_manager.handle_backspace()

    def _on_plus_minus(self, _event) -> None:
        self.state_manager.handle_plus_minus()

    def _on_percentage(self, _event) -> None:
        self.state_manager.handle_percentage()
