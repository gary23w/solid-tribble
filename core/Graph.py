import pygal
from pygal.style import Style

class Graph():
    def __init__(self, data = [{}], *args):
        self.data = data

    def graph1(self):
        custom_style = Style(
            colors=('#0343df', '#e50000', '#ffff14', '#929591'),
            font_family =
            'Roboto,Helvetica,Arial,sans-serif',
             background = 'transparent',
             label_font_size = 14,
        )
        c = pygal.Bar(
            title="Twitter Data Analyzer",
            style=custom_style,
            y_title='CORPS',
            width=1200,
            x_label_rotation=270,
        )
        for i in self.data:
            c.add(i)

        c.x_labels = ""

        c.render_to_file('graph.svg')