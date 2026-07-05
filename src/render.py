import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

COLS_PER_LEVEL = 3
LEVEL_COLORS = {
    "Mua to": "#c0392b",
    "Mua vua": "#e67e22",
    "Mua nhe": "#2f80c4",
    "Sap mua": "#7f8c8d",
}


def _row_count(n_names: int) -> int:
    return max(1, math.ceil(n_names / COLS_PER_LEVEL))


def render_table_image(rows: list[tuple[str, list[str]]], out_path: Path, title: str = "") -> None:
    """rows: list of (level, [district names]). Each level gets its own header bar
    plus a mini grid table of district names ("table in table")."""
    row_counts = [_row_count(len(names)) for _, names in rows]
    height_ratios = [rc + 1.4 for rc in row_counts]
    fig_height = max(2.5, 0.8 + sum(height_ratios) * 0.35)

    fig = plt.figure(figsize=(9, fig_height))
    if title:
        fig.suptitle(title, fontsize=13, fontweight="bold", y=0.995)

    top = 0.93 if title else 0.98
    outer_gs = GridSpec(len(rows), 1, figure=fig, height_ratios=height_ratios, hspace=0.35, top=top, bottom=0.02)

    for i, (level, names) in enumerate(rows):
        rc = row_counts[i]
        section_gs = outer_gs[i].subgridspec(2, 1, height_ratios=[1.4, rc], hspace=0.05)

        header_ax = fig.add_subplot(section_gs[0])
        header_ax.axis("off")
        color = LEVEL_COLORS.get(level, "#2f6fab")
        header_ax.add_patch(
            plt.Rectangle((0, 0), 1, 1, transform=header_ax.transAxes, facecolor=color, edgecolor="none")
        )
        header_ax.text(
            0.015, 0.5, f"{level}  ({len(names)})",
            transform=header_ax.transAxes, ha="left", va="center",
            fontsize=11, fontweight="bold", color="white",
        )

        body_ax = fig.add_subplot(section_gs[1])
        body_ax.axis("off")
        grid = [names[j:j + COLS_PER_LEVEL] for j in range(0, len(names), COLS_PER_LEVEL)]
        if grid and len(grid[-1]) < COLS_PER_LEVEL:
            grid[-1] = grid[-1] + [""] * (COLS_PER_LEVEL - len(grid[-1]))

        table = body_ax.table(cellText=grid, cellLoc="center", loc="center")
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.7)
        for (r, c), cell in table.get_celld().items():
            is_empty = r >= len(grid) or c >= len(grid[r]) or grid[r][c] == ""
            if is_empty:
                cell.set_edgecolor("white")
                cell.set_facecolor("white")
            else:
                cell.set_edgecolor("#bbbbbb")
                cell.set_facecolor("#f7f7f7" if r % 2 == 0 else "#ffffff")

    fig.savefig(out_path, dpi=160, bbox_inches="tight")
    plt.close(fig)
