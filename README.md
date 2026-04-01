
# DearPyGUI plots and helpers

A set of scripts with customised graphs and plots in DearPyGUI.

### Reproduce

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
