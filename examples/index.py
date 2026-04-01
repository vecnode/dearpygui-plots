"""Print available examples and how to run them.

Usage: ``uv run -m examples.index`` (or ``python -m examples.index``) from the repo root.
Descriptions mirror the README *Examples* section.
"""

AVAILABLE_EXAMPLES = {
    "bar_series": "Grouped bar chart (student scores)",
    "shape_editor": "Polygon shape editor (custom series)",
    "custom_series_tooltip": "Custom series with hover tooltip",
    "large_polygon_custom_series": "Many polygons in a custom series (metrics window)",
    "stem_scatter_theme": "Stem and scatter series with theme",
    "drag_lines_points": "Drag lines and points on a plot",
    "timeline_multiaxis": "Timeline annotations and multi-axis plot (reads timekeys.txt)",
    "screenshot": "Viewport / window screenshot demo",
}


def main() -> None:
    print("Available examples (run from repository root):\n")
    for name, blurb in AVAILABLE_EXAMPLES.items():
        print(f"  {name}")
        print(f"    {blurb}")
        print(f"    uv run -m examples.{name}\n")


if __name__ == "__main__":
    main()
