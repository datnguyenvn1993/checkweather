import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

WRAP_WIDTH = 48


def render_table_image(rows: list[tuple[str, str]], out_path: Path, title: str = "") -> None:
    """rows: list of (level, comma-joined district names). Renders a 2-column table PNG."""
    wrapped_rows = []
    line_counts = []
    for level, names in rows:
        wrapped = "\n".join(textwrap.wrap(names, width=WRAP_WIDTH)) or "-"
        wrapped_rows.append((level, wrapped))
        line_counts.append(wrapped.count("\n") + 1)

    total_lines = sum(line_counts) + 1  # +1 for header row
    fig_height = max(2.0, 0.6 + total_lines * 0.32)
    fig, ax = plt.subplots(figsize=(9, fig_height))
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=13, fontweight="bold", pad=16)

    table = ax.table(
        cellText=wrapped_rows,
        colLabels=["Muc do mua", "Cac quan/huyen"],
        cellLoc="left",
        colLoc="left",
        loc="center",
        colWidths=[0.22, 0.78],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#bbbbbb")
        cell.PAD = 0.02
        if row == 0:
            cell.set_text_props(weight="bold", color="white")
            cell.set_facecolor("#2f6fab")
            cell.set_height(cell.get_height() * 1.3)
        else:
            n_lines = line_counts[row - 1]
            cell.set_height(cell.get_height() * n_lines * 1.25)
            cell.set_facecolor("#f2f2f2" if row % 2 == 0 else "#ffffff")

    fig.tight_layout()
    fig.savefig(out_path, dpi=160, bbox_inches="tight")
    plt.close(fig)
