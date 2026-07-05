import requests

TIMEOUT_SECONDS = 10
COLS_PER_LEVEL = 3

# Adaptive Card TextBlock only accepts this fixed color palette.
LEVEL_COLORS = {
    "Mua to": "attention",
    "Mua vua": "warning",
    "Mua nhe": "accent",
    "Sap mua": "default",
}


def _table_element(names: list[str], cols: int = COLS_PER_LEVEL) -> dict:
    rows = []
    for i in range(0, len(names), cols):
        chunk = names[i:i + cols]
        cells = [
            {"type": "TableCell", "items": [{"type": "TextBlock", "text": n, "wrap": True, "size": "Small"}]}
            for n in chunk
        ]
        while len(cells) < cols:
            cells.append({"type": "TableCell", "items": []})
        rows.append({"type": "TableRow", "cells": cells})
    return {
        "type": "Table",
        "columns": [{"width": 1} for _ in range(cols)],
        "rows": rows,
        "firstRowAsHeaders": False,
        "gridStyle": "accent",
    }


def _card_skeleton(title: str, body_items: list[dict]) -> dict:
    return {
        "type": "AdaptiveCard",
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.5",
        "body": [
            {"type": "TextBlock", "text": title, "weight": "Bolder", "size": "Medium", "wrap": True},
            *body_items,
        ],
    }


def send_rain_alert(webhook_url: str, title: str, rows: list[tuple[str, list[str]]]) -> None:
    """rows: list of (level, [district names]). Each level gets a header line
    plus a real multi-column Adaptive Card Table."""
    body_items = []
    for level, names in rows:
        body_items.append({
            "type": "TextBlock",
            "text": f"{level} ({len(names)})",
            "weight": "Bolder",
            "color": LEVEL_COLORS.get(level, "default"),
            "spacing": "Medium",
        })
        body_items.append(_table_element(names))

    card = _card_skeleton(title, body_items)
    resp = requests.post(webhook_url, json=card, timeout=TIMEOUT_SECONDS)
    resp.raise_for_status()


def send_text(webhook_url: str, title: str, text: str, color: str = "good") -> None:
    card = _card_skeleton(title, [
        {"type": "TextBlock", "text": text, "wrap": True, "color": color},
    ])
    resp = requests.post(webhook_url, json=card, timeout=TIMEOUT_SECONDS)
    resp.raise_for_status()
