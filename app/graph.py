from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html

def graph(entries):
    dt_l = []
    data_l = []
    for entry in entries:
        dt_l.append(entry.dt)
        data_l.append(entry.data)

    plot = figure(width = 800, height=350, x_axis_type="datetime")
    plot.line(dt_l, data_l, color='navy', legend='degrees Celsius')
    plot.title.text = "Living room temperature"
    plot.legend.location = "top_left"
    plot.grid.grid_line_alpha = 0
    plot.xaxis.axis_label = 'Date'
    plot.yaxis.axis_label = 'Temperature'
    plot.ygrid.band_fill_color = "olive"
    plot.ygrid.band_fill_alpha = 0.1
    result = file_html(plot, CDN, "my plot")
    return result
