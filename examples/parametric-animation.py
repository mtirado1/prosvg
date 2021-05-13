from prosvg import *
from style import *
import math

video = Render(600, 600, fps=30)
video.start('parametric-animation.mp4')
video.scene.fill(white)

xAxis = Vector(video.left, video.right, svg.Stroke(yellow, 3))
yAxis = Vector(video.top, video.bottom, svg.Stroke(yellow, 3))

# Draw the axis
video.add(xAxis, yAxis)
video.play(
    xAxis.grow(),
    yAxis.grow()
).pause()

# Let's start with a parabola

# Returns a point with x and y coordinates
# each unit represents 100 svg units
parabola = lambda x: P(x, -x**2) * 100

func = Parametric(
    video.center,
    parabola,
    -2, 2,
    svg.Stroke(green, 5)
)

video.add(func).play(func.draw())

video.pause()

# Now we create a spiral
tau = 2 * math.pi
spiral = lambda t: R(t/tau, 3*t) * 100
video.play(
    func.transformFunction(
        spiral,
        time=3
    ).changeLimits(
        -2, 2,
         0, tau,
        time=3
    )
)
video.pause()

video.play(func.erase()).pause(3)

# Animating functions

def animation(f):
    k = 1 + 11 * f
    return lambda t: R(100, t) + R(100/k, k*t)

func.f = animation(0)
func.t0 = 0
func.t1 = tau
func.n = 60

video.play(func.draw())
video.pause()

video.play(
    func.updateFunction(animation, time=10, ease=linear)
)

video.pause()

video.end()
