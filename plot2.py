
from __future__ import annotations
import dearpygui.dearpygui as dpg
from dataclasses import dataclass, field


stored_shapes:dict[str:Shape] = {}
active_drag_points:list[str | int] = []

@dataclass()
class Shape:
    name:str
    color:list[float] = field(default_factory=lambda:[0.,0.,0.,1.])
    points:list[tuple] = field(default_factory=lambda:[[0.,0.],[0.,1.],[1.,1.],[1.,0.]])

    def update_color(self, _, app_data):
        self.color = [n*255 for n in app_data]

    def update_point(self, sender, _, user_data):
        self.points[user_data] = dpg.get_value(sender)[:2]


def select_shape(sender, app_data, user_data):
    global active_drag_points, stored_shapes
    check_box_state = app_data
    selected_shape = user_data

    for drag_point in active_drag_points:
        dpg.delete_item(drag_point)
    active_drag_points.clear()

    if not check_box_state:
        return

    for shape_name, shape in stored_shapes.items(): #type: str, Shape
        if shape_name != selected_shape.name:
            dpg.set_value(item=f"ChkBox_{shape_name}", value=False)

    for index, point in enumerate(selected_shape.points):
        drag_point = dpg.add_drag_point(
            parent="PlotEditor",
            default_value = point,
            user_data = index,
            callback=selected_shape.update_point
        )
        active_drag_points.append(drag_point)

def create_shape():
    global stored_shapes
    shape_name = dpg.get_value("InTxtShapeName")

    if not shape_name or shape_name is None or shape_name in stored_shapes:
        raise ValueError("No valid shape name was give")

    stored_shapes[shape_name] = (new_shape := Shape(name=shape_name))

    with dpg.table_row(parent="TblShapes"):
        with dpg.group(horizontal=True):
            dpg.add_checkbox(
                tag=f"ChkBox_{new_shape.name}",
                user_data=new_shape,
                callback=select_shape
            )
            dpg.add_color_edit(
                no_inputs=True,
                callback=new_shape.update_color
            )
            dpg.add_text(default_value=f"| {new_shape.name}")

    dpg.set_value(item="InTxtShapeName", value="")

def custom_series_painter(sender,app_data):
    global stored_shapes

    x0 = app_data[1][0]
    y0 = app_data[2][0]
    x1 = app_data[1][1]
    y1 = app_data[2][1]

    difference_x = x1 - x0
    difference_y = y1 - y0

    with dpg.mutex():
        dpg.delete_item(sender, children_only=True)
        dpg.push_container_stack(sender)

        for shape in stored_shapes.values():
            points_offset = [
                [((x * difference_x) + x0),((y * difference_y) + y0)]
                for x,y in shape.points
            ]
            dpg.draw_polygon(
                points=points_offset,
                color= shape.color[:3],
                fill=shape.color[:3],
                thickness=0
            )

        dpg.configure_item(sender, tooltip=False)
        dpg.pop_container_stack()

def main():
    dpg.create_context()
    dpg.create_viewport(title="Plot as Shape Editor")

    with dpg.window(tag="PrimaryWindow"):
        with dpg.group(horizontal=True, tag="LytMain"):
            with dpg.group(tag="LytCol1"):
                with dpg.plot(tag="PlotEditor", width=500, height=500):
                    dpg.add_plot_axis(axis=dpg.mvXAxis, tag="PlotAxisX")
                    with dpg.plot_axis(axis=dpg.mvYAxis, tag="PlotAxisY"):
                        dpg.add_custom_series(x= [0.,1.], y= [0.,1.], channel_count=2, callback=custom_series_painter)

            with dpg.group(tag="LytCol2"):
                with dpg.group(tag="LytCol2_NewShape", horizontal=True):
                    dpg.add_text("New shape's name")
                    dpg.add_input_text(
                        tag="InTxtShapeName",
                        on_enter=True,
                        callback=create_shape,
                        width=250
                    )
                    dpg.add_button(
                        tag="BtnCreateShape",
                        label="Create",
                        callback=create_shape
                    )

                with dpg.table(tag="TblShapes", header_row=False):
                    dpg.add_table_column()

    dpg.set_primary_window("PrimaryWindow", True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()


