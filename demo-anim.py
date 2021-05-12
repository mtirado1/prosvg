from prosvg import *

white  = '#fff0cf'
black  = '#33583c'
red    = '#fe7853'
blue   = '#50bac0'
yellow = '#ffbc7d'
brown  = '#904236'
green  = '#3ba484'

tau = 2 * math.pi

video = render.Render(600, 600, fps=30, scale=1.5)
video.start('demo/demo-complete.mp4')
video.start('demo/demo-0.mp4')
video.scene.fill(white)

center = video.center + Y(75)

title = Text(P(center.x, 100), 'Programmatic SVG\nwith Python', svg.Font('Lexend Deca', 40, black))
title.align('center')
video.add(title)
video.play(title.fadeIn())


c = Circle(center, 150, svg.FillStroke(yellow, brown, 5))
xAxis = Vector(center - X(200), center + X(200), svg.Stroke(brown, 3).dashArray(5))
yAxis = Vector(center - Y(200), center + Y(200), svg.Stroke(brown, 3).dashArray(5))
dot = Circle(center + R(150, -tau/8), 10, svg.Fill(brown))
v = Vector(center, dot.center, svg.Stroke(brown, 5))
projection = Vector(Y(center.y) + X(dot.center.x), dot.center, svg.Stroke(brown, 3).dashArray(5))
triangle = Polygon([center, projection.p1, dot.center], svg.Fill(red))

video.add(c, triangle, xAxis, yAxis, v, projection, dot)

video.play(
    c.grow(time=3),
    triangle.grow(time=3),
    xAxis.grow(time=3),
    yAxis.grow(time=3),
    v.grow(time=3),
    projection.grow(time=3),
    dot.grow(time=3)
)

video.pause(3)
video.save('demo/frame-0.svg')


rotationTime = 10
video.play(
    dot.rotate(5 * tau, center, time = rotationTime),
    v.rotate(5 * tau, time = rotationTime),

    projection.update(lambda t: P(dot.center.x, center.y), lambda t: dot.center, time=rotationTime),
    triangle.update(lambda t: [center, projection.p1, dot.center], time = rotationTime)

)
video.pause(2)
video.end('demo/demo-0.mp4')

video.play(
    c.move(R(600, 0)),
    triangle.move(R(600, tau / 7)),
    xAxis.move(R(600, 2 * tau /7)),
    yAxis.move(R(600, 3 * tau / 7)),
    v.move(R(600, 4 * tau / 7)),
    projection.move(R(600, 5 * tau /7)),
    dot.move(R(600, 6 * tau / 7))
)

video.remove(c, triangle, xAxis, yAxis, v, projection, dot)
video.pause(2)


center = video.center
c = Circle(center + P(0, -100), 10, svg.Fill(brown))
l = Vector(center, center + P(0, -100), svg.Stroke(red, 5))
p = RegularPolygon(center, center + P(0, -100), 6, svg.Stroke(green, 5))

video.add(p, l, c)


## Basic Transformations
video.start('demo/demo-1.mp4')
video.play (
    title.fadeText('Basic Transformations'),
    c.grow(time=1),
    l.grow(time=2),
    p.grow(time=3)
)

video.save('demo/frame-1.svg')
video.pause()


video.play(c.move(P(100, 0)))
video.play(l.move(P(100, 0)))
video.play(p.move(P(100, 0)))


video.play(l.rotate(tau, l.center).move(X(-100)))
video.play(p.rotate(tau, time=3).move(X(-100)))
video.play(c.move(X(-100)))

video.play(
    title.fadeText('Scale: 0.0'),
    l.rotate(tau/4, time=0.5)
)
video.pause()

video.play(
    l.scale(3, time=5),
    title.textFunction(lambda t: 'Scale: {:.1f}'.format(1 + 2*t), time=5)
)

video.play(
    l.scale(1/3, time=1),
    title.textFunction(lambda t: 'Scale: {:.1f}'.format(l._scale), time=1)
)


video.pause(2)
video.end('demo/demo-1.mp4')

video.play(
    c.move(Y(1000), time=1),
    l.move(Y(1000), time=1.2),
    p.move(Y(1000), time=1.5),
    title.fadeText('Plotting Functions', time=2)
)
video.remove(p, l, c)

video.start('demo/demo-2.mp4')
video.pause()

f = lambda t: -100 * math.sin(2 * tau * t / video.width)
f2 = lambda t: -200 * ((2 * t / video.width)**2 - 0.5*(2 * t / video.width)**3)
plotStyle = svg.Stroke(green, 5).dashArray(10, 5, 5, 5)
plot = Function(video.left, f, 0, video.width, plotStyle)
video.add(plot)
video.play(plot.draw())

video.save('demo/frame-2.svg')

video.pause(2)
video.play(plot.scale(1.5))
video.pause()
video.play(plot.scaleT(2))
video.play(plot.scaleT(0.5))

video.pause(2)

video.play(plot.transformFunction(f2, time=3))

video.pause(2)

video.play(plot.erase())
video.remove(plot)
video.end('demo/demo-2.mp4')

video.start('demo/demo-3.mp4')

## Parametric Equations

f3 = lambda t: 150 * P(math.cos(3 * t), math.sin(2 * t))
f4 = lambda t: R(100, t + tau/4) + R(50, 2 * t + tau/4)
f5 = lambda t: R(100, t + tau/4) + R(50, -4 * t + tau/4)

plotStyle = svg.Stroke(green, 5)
plot = Parametric(video.center, f3, 0, tau, plotStyle)
video.add(plot)
video.play(plot.draw(time=3), title.fadeText('Parametric Equations'))
video.save('demo/frame-3.svg')
video.pause()
video.play(plot.transformFunction(f4))
video.pause()
video.play(plot.transformFunction(f5))
video.pause(2)
video.play(plot.erase(time=3))
video.pause()

video.remove(plot)
video.end('demo/demo-3.mp4')

video.play(title.fadeText('3D Animations'))

video.start('demo/demo-4.mp4')
r = 150

star = Circle(video.center, 25, svg.Fill(red))
axis = Vector(video.center, video.center, svg.Stroke(red, 5).dashArray(5))
planet = Circle(video.center + X(r), 10, svg.Fill(blue))

vx = tau/6
vy = 5*tau/6

def orbitGenerator(vx, vy):
    
    def orbitAnimation(f):
        return lambda t: P3D(
                r * math.cos(t),
                r * math.sin(t),
                0).rotateX(vx * f).rotateY(vy * f).to2D()
    return orbitAnimation

orbit = Parametric(video.center, orbitGenerator(0, 0)(0), 0, tau, svg.Stroke(yellow, 5))

video.add(orbit, star, planet, axis)

video.play(
    orbit.draw(),
    planet.grow(),
    star.grow()
)

video.pause()

video.play(
    planet.rotate(tau, video.center, time=2, ease=easeInLinear)
)

video.play(
    orbit.updateFunction(orbitGenerator(vx, vy), time=10),
    planet.moveAlongPath(lambda t: video.center + orbitGenerator(vx, vy)(easeInOut(t))(5*tau* linearEaseOut(t)), time=10, ease=linear),
    axis.update(
        lambda t: video.center + P3D(0,0,75).rotateX(t * vx).rotateY(t * vy).to2D(),
        lambda t: video.center + P3D(0,0,-75).rotateX(t * vx).rotateY(t * vy).to2D(),
        time=10
    )
)

video.save('demo/frame-4.svg')
video.pause()

video.play(
    planet.shrink(),
    star.shrink(),
    orbit.erase(),
    axis.shrink()
)

video.remove(planet, star, orbit, axis)

video.pause()

video.end('demo/demo-4.mp4')

ax = tau/8
ay = tau * 0.9
def spiralGenerator(ax, ay):
    r = 150
    def spiralAnimation(f):
        func = lambda t: P3D(
            t * r * math.cos(3*t) / tau,
            t * r * math.sin(3*t) / tau,
            (t - tau/2) * r / tau
        ).rotateX(f * ax).rotateY(f * ay).to2D()
        return func
    return spiralAnimation

spiral = Parametric(video.center, spiralGenerator(0,0)(0), 0, tau, svg.Stroke(red, 5), n=60)

axisStyle = svg.Stroke(green, 3).lineCap('round')
xAxis = Vector(video.center - X(200), video.center + X(200), axisStyle)
yAxis = Vector(video.center - Y(200), video.center + Y(200), axisStyle)
zAxis = Vector(video.center, video.center, axisStyle)


video.start('demo/demo-5.mp4')
video.add(xAxis, yAxis, zAxis, spiral)

video.play(
    title.fadeText('3D Equations'),
    spiral.draw(),
    xAxis.grow(),
    yAxis.grow(),
    zAxis.grow()
)

video.play(spiral.erase())
spiral.t1 = tau
spiral.t0 = 0
video.play(
    spiral.draw(time=5).updateFunction(
        spiralGenerator(ax, ay),
        time=10
    ),

    xAxis.update(
        lambda t: video.center + P3D(-200,0,0).rotateX(ax*t).rotateY(ay*t).to2D(),
        lambda t: video.center + P3D(200,0,0).rotateX(ax*t).rotateY(ay*t).to2D(),
        time=10
    ),

    yAxis.update(
        lambda t: video.center + P3D(y=-200).rotateX(ax*t).rotateY(ay*t).to2D(),
        lambda t: video.center + P3D(y=200).rotateX(ax*t).rotateY(ay*t).to2D(),
        time=10
    ),

    zAxis.update(
        lambda t: video.center + P3D(z=-200).rotateX(ax*t).rotateY(ay*t).to2D(),
        lambda t: video.center + P3D(z=200).rotateX(ax*t).rotateY(ay*t).to2D(),
        time=10
    )
)

video.save('demo/frame-5.svg')

video.pause()
video.play(
    spiral.erase(),
    xAxis.shrink(),
    yAxis.shrink(),
    zAxis.shrink()
)
video.end('demo/demo-5.mp4')
video.end()

