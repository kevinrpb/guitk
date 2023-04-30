"""Simple Hello World example using guitk """

from guitk import Button, Entry, Event, Label, Layout, Window


# subclass guitk.Window as the starting point for your app's main window
class HelloWindow(Window):
    def config(self):
        """Configure the window"""

        # set the window title
        self.title = "Hello, World"

        # define a layout for the window
        # you must have a class variable named `layout` or you'll get an empty window
        with Layout() as layout:
            Label("What's your name?")
            Entry(key="name")
            Button("Ok")

        self.layout = layout

    # define your event loop
    # every guitk.Window will call self.handle_event to handle GUI events
    # event is a guitk.Event object
    def handle_event(self, event: Event):
        """Called when an event occurs"""
        if event.key == "Ok":
            print(f"Hello {self['name'].value}")


# run your event loop
if __name__ == "__main__":
    HelloWindow().run()
