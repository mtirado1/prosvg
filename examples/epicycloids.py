from prosvg import *
from style import *


colors = [
red,   black, green, blue,
green, blue,  red,   brown,
brown, green, blue,  red,
blue,  red,   black, green
]

margin = 100
size = 800
centers = []

def parametric(r, k):
    return lambda t: R(r + r/k, t - math.pi/2) + R(r/(k), (k+1)*t + math.pi/2)

img = Render(size, size, fps=30)
img.scene.fill(white)
img.start('epicycloid.mp4')

for y in range(4):
    for x in range(4):
        point = P(
            margin + x * (size - 2 * margin) / 3,
            margin + y * (size - 2 * margin) / 3
        )
        centers.append(point)

plots = []
bigCircles = []
smallCircles = []
dots = []

for i in range(len(colors)):
    k = i + 1
    r = 30
    c1 = Circle(centers[i], r, svg.Fill(yellow))
    c2 = Circle(centers[i] - Y(r + r / k), r / k, svg.Fill(yellow))
    p = Circle(c1.center - Y(r), 2, svg.Fill(black))

    f = Parametric(centers[i], parametric(r, k), 0, 2 * math.pi, svg.Stroke(colors[i], 3), n = 60)
    img.add(c1, c2, p)

    c1.grow()
    c2.grow()
    p.grow()

    plots.append(f)
    bigCircles.append(c1)
    smallCircles.append(c2)
    dots.append(p)

img.play(
    *bigCircles,
    *smallCircles,
    *dots
)

img.pause(2)

img.add(*plots)
img.remove(*dots)
img.add(*dots)

def path(i):
    return lambda t: parametric(30, i+1)(t * 2 * math.pi) + centers[i]

for i in range(16):

    plots[i].draw(time=5)
    dots[i].moveAlongPath(path(i), time = 5)
    smallCircles[i].rotate(2 * math.pi, centers[i], time = 5)

img.play(*plots, *dots, *smallCircles)

img.pause(2)

for i in range(16):
    dots[i].fadeOut()
    bigCircles[i].fadeOut()
    smallCircles[i].fadeOut()

img.play(*dots, *bigCircles, *smallCircles)
img.remove(*dots, *bigCircles, *smallCircles)
img.pause(2)
img.save('epicycloids.svg')

img.end()
