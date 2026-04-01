"""Capture the viewport or a single window to PNG files via frame buffers.

Run with: ``python -m examples.screenshot``. Set ``CONFIG`` for viewport title
and output filenames for the demo buttons.
"""

from __future__ import annotations
from dataclasses import dataclass

import dearpygui.dearpygui as dpg
from PIL import Image

from .helpers import run_app


@dataclass
class PlotConfig:
    viewport_title: str = "Screenshot Example"
    inner_window_tag: str = "window"
    inner_window_label: str = "Screenshot Example"
    viewport_png: str = "screenshot_viewport.png"
    window_png: str = "screenshot_window.png"
    window_crop_png: str = "screenshot_window_edit.png"


CONFIG = PlotConfig()


def picture_of_window(_, buffer:dpg.mvBuffer):
    x,y = dpg.get_item_pos(CONFIG.inner_window_tag)
    width = dpg.get_item_width(CONFIG.inner_window_tag)
    height = dpg.get_item_height(CONFIG.inner_window_tag)

    image = Image.frombuffer(
        mode="RGBA",
        size=(buffer.get_width(), buffer.get_height()),
        data=buffer
    )
    image.save(CONFIG.window_png)

    image_edit = image.crop((x,y, width, height))
    image_edit.save(CONFIG.window_crop_png)


def build_ui():
    with dpg.window(tag=CONFIG.inner_window_tag, label=CONFIG.inner_window_label):
        dpg.add_text("Hello world!")
        dpg.add_button(
            label="Press me, to take a screenshot of the viewport",
            callback=lambda : dpg.output_frame_buffer(file=CONFIG.viewport_png)
        )
        dpg.add_button(
            label="Press me, to take a screenshot of this window",
            callback=lambda : dpg.output_frame_buffer(callback=picture_of_window)
        )


if __name__ == "__main__":
    run_app(build_ui, title=CONFIG.viewport_title, wrap_window=False)
