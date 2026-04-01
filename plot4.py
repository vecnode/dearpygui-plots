from __future__ import annotations
import dearpygui.dearpygui as dpg

from helpers import run_app

POLYGONS:int = 10_000 # the amount of polygons to be generated
POLYGON = ((0.,0.),(0.,1.),(1.,1.),(1.,0.)) # shape of the polygon
POLYGON_COLOR = (0,0,0)

MAX_RANGE:float = 750.
MIN_RANGE:float = -MAX_RANGE

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
                    color=POLYGON_COLOR,
                    fill=POLYGON_COLOR,
                    thickness=0
                ))
        
        dpg.configure_item(sender, tooltip=False)
        dpg.pop_container_stack()

        dpg.set_value(
            item="txt_output",
            value=len(dpg.get_item_children(sender, 2))
        )


def calculate_points(polygon, difference_x:float, difference_y:float, x0:float, y0:float) -> list[list[float,float]]:
    points = []
    for x_original, y_original in polygon:
        if  MIN_RANGE < (x_new := ((x_original * difference_x) + x0)) < MAX_RANGE \
        and MIN_RANGE < (y_new := ((y_original * difference_y) + y0)) < MAX_RANGE:
            points.append([x_new, y_new])

    return points


def create_items():
    for i in range(POLYGONS):
        polygons.append(
            tuple((x+i,y+i) for x,y in POLYGON)
        )

def build_ui():
    with dpg.group(horizontal=True, horizontal_spacing=375):
        dpg.add_button(
            label="Create items",
            callback=create_items,
            width=100
        )
        dpg.add_text(tag="txt_output")
    with dpg.plot(width=500, height=500, tag="plot"):
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
        title='Plot with large Custom Series Example',
        window_tag="primary_window",
        window_kwargs={"label": "primary_window"},
        set_primary_window_tag="primary_window",
        show_metrics=True,
    )
