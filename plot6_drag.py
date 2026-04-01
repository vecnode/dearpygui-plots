import dearpygui.dearpygui as dpg

from helpers import run_app


class DraggablePoints:
    def __init__(self, pos, parent, width, height) -> None:
        self.color = [255, 0, 255, 255]
        self.pos = pos
        self.parent = parent
        self.width = width
        self.height = height

    def do(self):
        dpg.add_drag_point(label="dpoint1", color=self.color, parent=self.parent, width=self.width, height=self.height)

x = DraggablePoints([0, 0], "plot1", 10, 10)

def add_points_to_plot(sender, app_data):
    dpg.add_child

def custom_series_callback(sender, app_data):
    x_transformed = app_data[1]
    y_transformed = app_data[2]

    print(len(x_transformed)) #Will always have a length of 4

    dpg.delete_item(sender, children_only=True, slot=2)
    dpg.push_container_stack(sender)
    for i in range(len(x_transformed) - 1):
        p1 = (x_transformed[i], y_transformed[i])
        p2 = (x_transformed[i+1], y_transformed[i+1])
        dpg.draw_line(p1, p2)
    dpg.pop_container_stack()

def build_ui():
    dpg.add_button(label="plot", callback=add_points_to_plot)
    with dpg.plot(tag="plot1", label="plot1", height=400, width=-1):
        dpg.add_plot_legend()
        dpg.add_plot_axis(dpg.mvXAxis, label="x")
        dpg.add_plot_axis(dpg.mvYAxis, label="y")

        # drag lines/points belong to the plot NOT axis
        dpg.add_drag_line(label="dline1", color=[255, 0, 0, 255])
        dpg.add_drag_line(label="dline2", color=[255, 255, 0, 255], vertical=False)
        dpg.add_drag_point(label="dpoint1", color=[255, 0, 255, 255])
        dpg.add_drag_point(label="dpoint2", color=[255, 0, 255, 255])


if __name__ == "__main__":
    run_app(build_ui, window_kwargs={"width": 400})
