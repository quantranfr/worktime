from kivy.app import App
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
import time
from datetime import timedelta
from kivy.clock import Clock

class MyLayout(BoxLayout):
    def reset(self, *args):
        for id in self.ids:
            widget = self.ids[id]
            widget.reset()
        
class TaskWidget(ToggleButton):
    name = None         # name of the task
    elapsed = 0         # total elapsed time
    last_update = None  # last time the clock is updated
    clock_event = None

    def on_state(self, widget, value):
        if value == "down":
            self.last_update = time.time()
            self.update()
            self.clock_event = Clock.schedule_interval(self.update, 1)
        else:
            self.clock_event.cancel()

    def update(self, *args):
        now = time.time()
        self.elapsed += round(now - self.last_update)
        self.last_update = now
        self.text = self.format_text(self.elapsed) 

    def format_text(self, elapsed):
        """
        input:
            elapsed: elapsed time in seconds
        output:
            task name + elapsed time in 0:00:00 format
        """
        return self.name + "\n" + str(timedelta(seconds=elapsed))

    def reset(self):
        self.state = "normal"
        if self.clock_event:
            self.clock_event.cancel()
        self.elapsed = 0
        self.text = self.name

class WorktimeApp(App):
    def build(self):
        return MyLayout()

if __name__ == "__main__":
    WorktimeApp().run()
