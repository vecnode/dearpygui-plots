"""Stem and scatter series sharing a plot theme (markers and colors).

Run with: ``python -m examples.stem_scatter_theme``. Adjust ``CONFIG`` for viewport
title, window size, sample count, and plot label.
"""

from dataclasses import dataclass

import dearpygui.dearpygui as dpg
from math import sin

from .helpers import run_app


@dataclass
class PlotConfig:
    viewport_title: str = "Custom Title"
    window_label: str = "Tutorial"
    window_width: int = 500
    window_height: int = 400
    sample_count: int = 100
    plot_label: str = "Line Series"


CONFIG = PlotConfig()


def build_ui():
    n = CONFIG.sample_count
    sindatax = []
    sindatay = []
    for i in range(0, n):
        sindatax.append(i / n)
        sindatay.append(0.5 + 0.5 * sin(50 * i / n))
    sindatay2 = []
    for i in range(0, n):
        sindatay2.append(2 + 0.5 * sin(50 * i / n))

    # create a theme for the plot
    with dpg.theme(tag="plot_theme"):
        with dpg.theme_component(dpg.mvStemSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (150, 255, 0), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_style(dpg.mvPlotStyleVar_Marker, dpg.mvPlotMarker_Diamond, category=dpg.mvThemeCat_Plots)
            dpg.add_theme_style(dpg.mvPlotStyleVar_MarkerSize, 7, category=dpg.mvThemeCat_Plots)

        with dpg.theme_component(dpg.mvScatterSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (60, 150, 200), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_style(dpg.mvPlotStyleVar_Marker, dpg.mvPlotMarker_Square, category=dpg.mvThemeCat_Plots)
            dpg.add_theme_style(dpg.mvPlotStyleVar_MarkerSize, 4, category=dpg.mvThemeCat_Plots)

    # create plot
    with dpg.plot(tag="plot", label=CONFIG.plot_label, height=-1, width=-1):
        # optionally create legend
        dpg.add_plot_legend()
        # REQUIRED: create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis, label="x")
        dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="yaxis")

        # series belong to a y axis
        dpg.add_stem_series(sindatax, sindatay, label="0.5 + 0.5 * sin(x)", parent="yaxis", tag="series_data")
        dpg.add_scatter_series(sindatax, sindatay2, label="2 + 0.5 * sin(x)", parent="yaxis", tag="series_data2")

        # apply theme to series
        dpg.bind_item_theme("series_data", "plot_theme")
        dpg.bind_item_theme("series_data2", "plot_theme")


if __name__ == "__main__":
    run_app(
        build_ui,
        title=CONFIG.viewport_title,
        window_label=CONFIG.window_label,
        window_kwargs={"width": CONFIG.window_width, "height": CONFIG.window_height},
    )
