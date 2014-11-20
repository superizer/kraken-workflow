from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.graphics import Line, Rectangle, Color
from widgets import DraggableWidget

class ToolButton(ToggleButton):
    def on_touch_down(self, touch):
        ds = self.parent.drawing_space
        if self.state == 'down' and ds.collide_point(touch.x,touch.y):
            (x,y) = ds.to_widget(touch.x, touch.y)
            self.draw(ds, x, y)
            return True
        return super(ToolButton, self).on_touch_down(touch)

    def draw(self, ds, x, y):
        pass
    
class ToolRectangle(ToolButton):
    def draw(self, ds, x, y):
        h = 60
        w = 150
        ix = x - w/2
        iy = y - h/2
        fx = x + w/2
        fy = y + h/2
        
        widget = self.create_widget(ix,iy,fx,fy)
        (ix,iy) = widget.to_local(ix,iy,relative=True)
        (fx,fy) = widget.to_local(fx,fy,relative=True)
        widget.canvas.add(Color(1, 0, 0, 1))
        widget.canvas.add(Rectangle(pos=(ix, iy), size=(w,h)))
        
        l = Label(text='Component')
        widget.add_widget(l)
        
        ds.add_widget(widget)
    
    def create_widget(self,ix,iy,fx,fy):
        pos = (min(ix, fx), min(iy, fy)) 
        size = (abs(fx-ix), abs(fy-iy))
        return DraggableWidget(pos = pos, size = size)
    
class ToolLine(ToolButton):
    def create_figure(self,ix,iy,fx,fy):
        return Line(points=[ix, iy, fx, fy])

    def create_widget(self,ix,iy,fx,fy):
        pos = (min(ix, fx), min(iy, fy)) 
        size = (abs(fx-ix), abs(fy-iy))
        return DraggableWidget(pos = pos, size = size)

