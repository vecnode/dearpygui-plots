"""Grouped bar series: multiple exam scores per student with custom X ticks.

Run with: ``python -m examples.bar_series``. Adjust ``CONFIG`` to change
viewport title, window size, and plot label without editing layout code.
"""

from dataclasses import dataclass

import dearpygui.dearpygui as dpg

from .helpers import run_app


@dataclass
class PlotConfig:
    viewport_title: str = "Custom Title"
    window_label: str = "Tutorial"
    window_width: int = 400
    window_height: int = 400
    plot_label: str = "Bar Series"


CONFIG = PlotConfig()


def build_ui():
    with dpg.plot(label=CONFIG.plot_label, height=-1, width=-1):
        dpg.add_plot_legend()

        # create x axis
        dpg.add_plot_axis(dpg.mvXAxis, label="Student", no_gridlines=True)
        dpg.set_axis_ticks(dpg.last_item(), (("S1", 11), ("S2", 21), ("S3", 31)))

        # create y axis
        dpg.add_plot_axis(dpg.mvYAxis, label="Score", tag="yaxis_tag")

        # add series to y axis
        dpg.add_bar_series([10, 20, 30], [100, 75, 90], label="Final Exam", weight=1, parent="yaxis_tag")
        dpg.add_bar_series([11, 21, 31], [83, 75, 72], label="Midterm Exam", weight=1, parent="yaxis_tag")
        dpg.add_bar_series([12, 22, 32], [42, 68, 23], label="Course Grade", weight=1, parent="yaxis_tag")


if __name__ == "__main__":
    run_app(
        build_ui,
        title=CONFIG.viewport_title,
        window_label=CONFIG.window_label,
        window_kwargs={"width": CONFIG.window_width, "height": CONFIG.window_height},
    )
