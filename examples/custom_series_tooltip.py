"""Custom series with per-point drawing and a hover-driven tooltip.

Run with: ``python -m examples.custom_series_tooltip``. Edit ``CONFIG`` to
change sample data, plot size, and window tags.
"""

from dataclasses import dataclass

import dearpygui.dearpygui as dpg

from .helpers import run_app


@dataclass
class PlotConfig:
    viewport_title: str = "DearPyGui Plot Example"
    window_label: str = "Tutorial"
    window_tag: str = "plot3_window"
    plot_label: str = "Custom Series"
    plot_height: int = 400
    x_data: tuple[float, ...] = (0.0, 1.0, 2.0, 4.0, 5.0)
    y_data: tuple[float, ...] = (0.0, 10.0, 20.0, 40.0, 50.0)


CONFIG = PlotConfig()

x_data = list(CONFIG.x_data)
y_data = list(CONFIG.y_data)

def callback(sender, app_data):

    _helper_data = app_data[0]
    transformed_x = app_data[1]
    transformed_y = app_data[2]
    #transformed_y1 = app_data[3] # for channel = 3
    #transformed_y2 = app_data[4] # for channel = 4
    #transformed_y3 = app_data[5] # for channel = 5
    mouse_x_plot_space = _helper_data["MouseX_PlotSpace"]   # not used in this example
    mouse_y_plot_space = _helper_data["MouseY_PlotSpace"]   # not used in this example
    mouse_x_pixel_space = _helper_data["MouseX_PixelSpace"]
    mouse_y_pixel_space = _helper_data["MouseY_PixelSpace"]
    dpg.delete_item(sender, children_only=True, slot=2)
    dpg.push_container_stack(sender)
    dpg.configure_item("demo_custom_series", tooltip=False)
    for i in range(0, len(transformed_x)):
        dpg.draw_text((transformed_x[i]+15, transformed_y[i]-15), str(i), size=20)
        dpg.draw_circle((transformed_x[i], transformed_y[i]), 15, fill=(50+i*5, 50+i*50, 0, 255))
        if mouse_x_pixel_space < transformed_x[i]+15 and mouse_x_pixel_space > transformed_x[i]-15 and mouse_y_pixel_space > transformed_y[i]-15 and mouse_y_pixel_space < transformed_y[i]+15:
            dpg.draw_circle((transformed_x[i], transformed_y[i]), 30)
            dpg.configure_item("demo_custom_series", tooltip=True)
            dpg.set_value("custom_series_text", "Current Point: " + str(i))
    dpg.pop_container_stack()

def build_ui():
    dpg.add_text("Hover an item for a custom tooltip!")
    with dpg.plot(label=CONFIG.plot_label, height=CONFIG.plot_height, width=-1):
        dpg.add_plot_legend()
        dpg.add_plot_axis(dpg.mvXAxis)
        with dpg.plot_axis(dpg.mvYAxis):
            with dpg.custom_series(x_data, y_data, 2, label="Custom Series", callback=callback, tag="demo_custom_series"):
                dpg.add_text("Current Point: ", tag="custom_series_text")
            dpg.fit_axis_data(dpg.top_container_stack())


if __name__ == "__main__":
    run_app(
        build_ui,
        title=CONFIG.viewport_title,
        window_label=CONFIG.window_label,
        window_tag=CONFIG.window_tag,
        set_primary_window_tag=CONFIG.window_tag,
    )
