# vecnode 28-06-2023

from pathlib import Path

import dearpygui.dearpygui as dpg
from math import sin

from .helpers import run_app

_REPO_ROOT = Path(__file__).resolve().parent.parent

# window

window_width = 1280
window_height = 600

sindatax = []
sindatay = []
for i in range(0, 10000):
    sindatax.append(i / 500)
    sindatay.append(0.5 + 0.5 * sin(50 * i / 1000))


class Button:
    def __init__(self, label):
        with dpg.stage() as self._staging_container_id:
            self._id = dpg.add_button(label=label)
    def set_callback(self, callback):
        dpg.set_item_callback(self._id, callback)
    def get_label(self):
        return dpg.get_item_label(self._id)
    def submit(self, parent):
        dpg.push_container_stack(parent)
        dpg.unstage(self._staging_container_id)
        dpg.pop_container_stack()


# for loop create it up and down
def create_annotations_from_file(file_name, plot_id, color):
    with open(file_name, 'r') as file:
        for i, line in enumerate(file):
            vertical_value = 0.4 if i % 2 == 0 else 0.6
            timecode, text = line.strip().split(',', 1)
            text = text.strip(' "')
            time = sum(int(x) * 60 ** i for i, x in enumerate(reversed(timecode.split(':'))))
            dpg.add_plot_annotation(label=text, default_value=(time, vertical_value), parent=plot_id, color=color, offset=(-0.05, -50), clamped=True)


def callback1(sender, data):
    dpg.set_value("line_min_val", -1)
    dpg.set_value("line_max_val", 1)
    dpg.set_axis_limits("x_axis", 0, 50)



def callback3(sender, data):
    create_annotations_from_file(str(_REPO_ROOT / "timekeys.txt"), "mainplot", color=[255, 255, 255, 255])





table_x_data = [0,0]
table_y_data = [0,0]

def print_val(sender):
    print(dpg.get_value(sender))

def build_ui():
    with dpg.window(label="main_window", tag="main_window", pos=(0,0), no_close=True, no_move=True, no_resize=True, no_title_bar=True, no_collapse=True, no_scrollbar=True, width=window_width, height=window_height):
        with dpg.window(label="second_window", tag="second_window", pos=(0,0), no_close=True, no_move=True, no_resize=True, no_title_bar=True, no_collapse=True, no_scrollbar=True, width=window_width, height=window_height):
            with dpg.group(horizontal=True):
                with dpg.child_window(width=100):
                    dpg.add_button(label="overview", callback=callback1, width=-1)
                    dpg.add_button(label="plot", callback=callback3, width=-1)

                with dpg.child_window(width=-1):
                    with dpg.plot(tag="mainplot", label=" ", height=-1, width=-1, anti_aliased=True, query=True, no_title=True, crosshairs=True):
                        dpg.add_plot_legend()

                        with dpg.plot_axis(dpg.mvXAxis, label="", tag="x_axis", no_tick_labels=True, no_gridlines=False, no_tick_marks=False, lock_min=True): #, lock_min=True)
                            dpg.set_axis_limits_auto("x_axis")
                            dpg.add_line_series(sindatax, sindatay, label="5 + 5 * sin(x)", parent="y_axis", tag="series_tag")

                        dpg.add_drag_line(tag="line_max_val", label="line_min_val", color=[255, 255, 0, 255], vertical=False, default_value=1, callback=print_val)
                        dpg.add_drag_point(tag="dpoint1", label="dpoint1", color=[255, 0, 255, 255], default_value=(1.0, 1.0), callback=print_val)
                        dpg.add_drag_line(tag="line_min_val", label="line_max_val", color=[255, 255, 0, 255], vertical=False, default_value=-1, callback=print_val)
                        dpg.add_drag_point(tag="dpoint2", label="dpoint2", color=[255, 0, 255, 255])

                        dpg.add_plot_annotation(label="sum1", default_value=(0.25, 0.25), offset=(-15, 15), color=[255, 255, 0, 255])

                        with dpg.plot_axis(dpg.mvYAxis, label="", tag="y_axis1", no_tick_labels=True, no_gridlines=False, no_tick_marks=False, lock_min=True, lock_max=True): #, no_gridlines=False):
                            dpg.set_axis_limits(dpg.last_item(), -1.2, 1.2)
                            dpg.add_line_series(table_x_data, table_y_data, label="series_1", tag="series_1")
                            dpg.add_button(label="series_1", user_data = dpg.last_item(), parent=dpg.last_item(), callback=lambda s, a, u: dpg.delete_item(u))

                        with dpg.plot_axis(dpg.mvYAxis, label="", tag="y_axis2", no_tick_labels=True, no_gridlines=False, no_tick_marks=False, lock_min=True, lock_max=True): #, no_gridlines=False):
                            dpg.set_axis_limits(dpg.last_item(), -1.2, 1.2)
                            dpg.add_bar_series([1.0, 5.0, 10.0, 15.0], [1.0, 1.0, 0.5, 0.5], tag="okok1", weight=0.2)


if __name__ == "__main__":
    run_app(
        build_ui,
        title=' ',
        width=window_width,
        height=window_height,
        wrap_window=False,
        set_primary_window_tag="main_window",
    )
