
# DearPyGUI plots and helpers

A set of scripts with customised graphs and plots in DearPyGUI.

Each example under `examples/` defines a small **`PlotConfig`** dataclass (see the module’s `CONFIG`) so you can change titles, sizes, colors, and data ranges without hunting through layout code.

## Examples

- **`examples.bar_series`** — Grouped bar chart (student scores).
- **`examples.shape_editor`** — Polygon shape editor on a custom series with drag points.
- **`examples.custom_series_tooltip`** — Custom series with hover feedback and tooltip text.
- **`examples.large_polygon_custom_series`** — Many polygons in a custom-series painter (opens the metrics window).
- **`examples.stem_scatter_theme`** — Stem and scatter series with a shared plot theme.
- **`examples.drag_lines_points`** — Drag lines and drag points on a plot.
- **`examples.timeline_multiaxis`** — Long sine series, multiple Y axes, annotations from `timekeys.txt` at the repo root.
- **`examples.screenshot`** — Save viewport or window frame buffers to PNG files.

### Reproduce

From the repository root, install dependencies (Python 3 with `pip`):

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run an example module (opens a GUI; `timeline_multiaxis` loads `timekeys.txt` at the repo root):

```sh
python3 -m examples.bar_series
python3 -m examples.shape_editor
python3 -m examples.custom_series_tooltip
python3 -m examples.large_polygon_custom_series
python3 -m examples.stem_scatter_theme
python3 -m examples.drag_lines_points
python3 -m examples.timeline_multiaxis
python3 -m examples.screenshot
```

List all examples and the same commands:

```sh
python3 -m examples.index
```
