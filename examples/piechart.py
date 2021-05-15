from prosvg.svg import *
from style import *
import math

values = [20, 30, 10, 5]
colors = [yellow, green, blue, red]

chart = Drawing(600, 600, origin='center')
chart.fill(white)

angle = 0
for i in range(len(values)):
    startAngle = angle
    angle += 2 * math.pi * values[i] / sum(values)

    pieSlice = Path(Fill(colors[i]))
    pieSlice.arc(
        0, 0,               # Center
        150, 150,           # Rx, Ry
        startAngle, angle,  # Angles
        drawSlice = True
    )
    chart.add(pieSlice)

chart.write('piechart.svg')
