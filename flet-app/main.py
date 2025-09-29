#!/usr/bin/env python3
"""
Flet Calculator App - Main Entry Point

A simple calculator application built with Flet (Python).
Supports basic arithmetic operations and runs in web browsers.
"""

import flet as ft

from app.ui import CalculatorApp

C = ft.Colors


def color(value: ft.Colors | str) -> str:
    return value.value if hasattr(value, "value") else value


def main(page: ft.Page) -> None:
    """Configure the page and mount the calculator UI."""

    page.title = "Flet Calculator"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = color(C.BLUE_GREY_100)
    page.padding = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_min_width = 360
    page.window_min_height = 520
    page.window_width = 380
    page.window_height = 620
    page.window_resizable = False

    page.theme = ft.Theme(color_scheme_seed=color(C.BLUE_ACCENT))

    calculator = CalculatorApp()
    calculator.mount(page)


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550, host="127.0.0.1")
