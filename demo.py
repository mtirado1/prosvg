import math
from prosvg.svg import *

# Color definitions
black = '#1c1b19'
white = '#fce8c3'
red   = '#f75341'
blue  = '#0aaeb3'
yellow = '#fbb829'
green = '#98bc37'
magenta = '#ff5c8f'

tau = 2 * math.pi

img = Drawing(800, 600)
img.fill(black)

# Line Paths
axis = Path(Stroke(white, 5))
axis.M(0, img.center.y).H(img.width)
axis.M(img.center.x, 0).v(img.height)

# Circle
A = img.center + Point(100, -100)
circle = Circle(A.x, A.y, 50, Fill(blue))

# Rectangle
rect = Rect(img.center.x - 350, img.center.y - 50, 80, 120, Fill(red))

# Polygons
shape = RegularPolygon(
    *(img.center + Point(-100, 120)),
    *(img.center + Point(-100, 80)),
    5,
    Fill(green)
)

bottomRight = Point(img.width, img.height)
shape2 = Polygon(
    [bottomRight, bottomRight + Point(0, -50), bottomRight + Point(-50,0)],
    Fill(white)
)

# Line
line = Line(
    *(img.center + Point(-150, -150)),
    *(img.center + Point(150, 150)),
    Stroke(green, 5).dashArray(0,10).lineCap('round')
)

# Parametric Equations

def func(t):
    center = img.center + Point(150, 150)
    return center + Polar(100 + 25 * math.cos(6*t), t)
def func2(t):
    center = img.center + Point(-150, -150)
    return center + (Polar(50, t) + Polar(25, 2*t)).rotate(tau/4)

plot = Path(Stroke(yellow, 5))
plot.parametric(func, 0, 2 * math.pi, n=60)

heart = Path(Fill(magenta))
heart.parametric(func2, 0, 2 * math.pi, n=60)

# Text
text = Text(20, 60, 'PROGRAMMATIC\nSVG', Font('Lexend Deca', 40, white))

# Arcs
arc = Path(Fill(white))
arc.Arc(*(img.center + Point(300, -100)), 50, 50, 0, tau*0.75, drawSlice=True)
arc2 = Path(Stroke(white, 5))
arc2.Arc(*(img.center + Point(300, -200)), 50, 50, tau/2, tau, drawSlice=False)
arc2.id = 'clone'

# Some clones created with the <use> tag
arc3 = arc2.clone(x = -20)
arc4 = arc2.clone(x = -40)

# Ellipse
B = img.center + Point(-50, 50)
ellipse = Ellipse(B.x, B.y, 100, 50, FillStroke(white + '80', white, 5))
ellipse.rotate(tau / 12)

# Add Objects
img.add(
    axis, circle, rect,
    shape, shape2,
    plot, line, heart,
    arc, arc2, arc3, arc4,
    ellipse, text
)

# Write to File
img.write('demo.svg')
