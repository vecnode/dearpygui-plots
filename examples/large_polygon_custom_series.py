"""Stress-test custom series: many polygons drawn inside a custom-series callback.

Run with: ``python -m examples.large_polygon_custom_series``. Use ``CONFIG`` to
tune polygon count, colors, axis clamp range, and plot size before clicking
*Create items*.
"""

from __future__ import annotations
from dataclasses import dataclass

import dearpygui.dearpygui as dpg

from .helpers import run_app


@dataclass
class PlotConfig:
    viewport_title: str = "Plot with large Custom Series Example"
    primary_window_tag: str = "primary_window"
    primary_window_label: str = "primary_window"
    polygon_count: int = 10_000
    polygon_template: tuple[tuple[float, float], ...] = ((0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0))
    polygon_color: tuple[int, int, int] = (0, 0, 0)
    max_range: float = 750.0
    plot_width: int = 500
    plot_height: int = 500
    toolbar_spacing: int = 375


CONFIG = PlotConfig()

polygons:list[tuple] = []
drawn_polygons:list[str|int] = []


def custom_series_callback(sender, app_data):
    global drawn_polygons

    # Add mutex here to solve crashing issue
    with dpg.mutex():
        x0 = app_data[1][0]
        y0 = app_data[2][0]
        x1 = app_data[1][1]
        y1 = app_data[2][1]

        difference_x = x1 - x0
        difference_y = y1 - y0

        dpg.delete_item(sender, children_only=True)
        dpg.push_container_stack(sender)

        for polygon in polygons:
            points = calculate_points(polygon,difference_x,difference_y,x0,y0)
            if len(points) >= 3:
                drawn_polygons.append(dpg.draw_polygon(
                    points=points,
                    color=CONFIG.polygon_color,
                    fill=CONFIG.polygon_color,
                    thickness=0
                ))
        
        dpg.configure_item(sender, tooltip=False)
        dpg.pop_container_stack()

        dpg.set_value(
            item="txt_output",
            value=len(dpg.get_item_children(sender, 2))
        )


def calculate_points(polygon, difference_x:float, difference_y:float, x0:float, y0:float) -> list[list[float,float]]:
    lo = -CONFIG.max_range
    hi = CONFIG.max_range
    points = []
    for x_original, y_original in polygon:
        if  lo < (x_new := ((x_original * difference_x) + x0)) < hi \
        and lo < (y_new := ((y_original * difference_y) + y0)) < hi:
            points.append([x_new, y_new])

    return points


def create_items():
    for i in range(CONFIG.polygon_count):
        polygons.append(
            tuple((x+i,y+i) for x,y in CONFIG.polygon_template)
        )

def build_ui():
    with dpg.group(horizontal=True, horizontal_spacing=CONFIG.toolbar_spacing):
        dpg.add_button(
            label="Create items",
            callback=create_items,
            width=100
        )
        dpg.add_text(tag="txt_output")
    with dpg.plot(width=CONFIG.plot_width, height=CONFIG.plot_height, tag="plot"):
        dpg.add_plot_axis(axis=dpg.mvXAxis)
        with dpg.plot_axis(axis=dpg.mvYAxis):
            dpg.add_custom_series(
                x= [0.,1.],
                y= [0.,1.],
                channel_count=2,
                callback=custom_series_callback
            )


if __name__ == '__main__':
    run_app(
        build_ui,
        title=CONFIG.viewport_title,
        window_tag=CONFIG.primary_window_tag,
        window_kwargs={"label": CONFIG.primary_window_label},
        set_primary_window_tag=CONFIG.primary_window_tag,
        show_metrics=True,
    )
