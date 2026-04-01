import dearpygui.dearpygui as dpg


def run_app(
    build_ui,
    *,
    title="DearPyGui Plot Example",
    width=800,
    height=600,
    window_label="Plot Window",
    window_tag=None,
    window_kwargs=None,
    wrap_window=True,
    set_primary_window_tag=None,
    show_metrics=False,
):
    """Create context and viewport, optionally wrap UI in a main window, run the DearPyGui loop."""
    dpg.create_context()
    dpg.create_viewport(title=title, width=width, height=height)

    if wrap_window:
        wargs = dict(window_kwargs or {})
        wargs.setdefault("label", window_label)
        if window_tag is not None:
            wargs["tag"] = window_tag
        with dpg.window(**wargs):
            build_ui()
    else:
        build_ui()

    dpg.setup_dearpygui()
    dpg.show_viewport()

    if set_primary_window_tag is not None:
        dpg.set_primary_window(set_primary_window_tag, True)

    if show_metrics:
        dpg.show_metrics()

    dpg.start_dearpygui()
    dpg.destroy_context()
