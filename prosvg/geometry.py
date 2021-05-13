import math
from . import svg

# Ease Functions

def inverse(f):
    return lambda t: (1 - f(t))

def linear(t):
    return t

def easeIn(t):
    return t ** 2

def easeInLinear(t):
    return (1 - t) * t ** 2 + t ** 2

def easeOut(t):
    return 1 - (1 - t) ** 2

def easeInOut(t):
    return easeIn(t) * (1 - t) + easeOut(t) * t

def linearEaseOut(t):
    return t * (1 - t) + easeOut(t) * t

def interpolate(a, b, t, ease=easeInOut):
    if ease == linear:
        return a * (1 - t) + b * t
    else:
        return a * (1 - ease(t)) + b * ease(t)

# Neat SVG Point wrappers

def X(x):
    return svg.Point(x, 0)

def Y(y):
    return svg.Point(0, y)

def P(x, y):
    return svg.Point(x, y)

def R(r, angle):
    return svg.Polar(r, angle)

def P3D(x=0, y=0, z=0):
    return svg.Point3D(x, y, z)

class Animation():
    def __init__(self, action=None, runTime=0, onEnd=None):
        self.runTime = runTime
        self.t = 0
        if action is None:
            self.transition = []
        else:
            self.transition = [(action, runTime, onEnd)]

    def run(self, dt):
        self.t += dt
        if self.t > self.runTime:
            # The animation has ended
            for f in self.transition:
                if f[2] is not None:
                    f[2]()
            self.reset()
            return
        for f in self.transition:
            if self.t <= f[1] + dt:
                f[0](self.t/f[1], dt/f[1])

    def add(self, action, runTime, onEnd=None):
        self.runTime = max(self.runTime, runTime)
        self.transition.append((action, runTime, onEnd)) 

    def reset(self):
        self.t = 0
        self.transition = []
        self.runTime = 0

# An animated object can be animated using an animation
class AnimatedObject():
    def __init__(self):
        self.animation = Animation()

    def fadeIn(self, time=1, ease=easeInOut): # Show an object on screen
        def action(t, dt):
            self.setAttributes({'opacity': ease(t)})
        self.animation = Animation(action, time)
        return self
    
    def fadeOut(self, time=1, ease=easeInOut): # Hides an object
        def action(t, dt):
            self.setAttributes({'opacity': 1 - ease(t)})
        self.animation = Animation(action, time)
        return self

    # Movement functions, needs to implement position(get, set) on children objects
    def move(self, deltaVector, time=1, ease=easeInOut):
        def action(t, dt):
            delta = deltaVector * (ease(t) - ease(t - dt)) 
            self.position += delta
        self.animation.add(action, time)
        return self

    def moveTo(self, dest, time=1, ease=easeInOut):
        return self.move(dest - self.position, time, ease)

    def moveAlongPath(self, path, time=1, ease=easeInOut):
        def action(t, dt):
            self.position = path(ease(t))
        self.animation.add(action, time)
        return self


class Vector(svg.Line, AnimatedObject):
    def __init__(self, p1, p2, style={}):
        self.p1 = p1
        self.p2 = p2
        self._scale = 1
        svg.Line.__init__(self, p1.x, p1.y, p2.x, p2.y, style)
        AnimatedObject.__init__(self)
    def set(self, p1, p2, scale = None):
        self.p1 = p1
        self.p2 = p2
        if not (scale is None):
            self._scale = scale
        delta = p1 + self._scale * (p2 - p1)
        self.setAttributes({
            'x1': p1.x,
            'y1': p1.y,
            'x2': delta.x,
            'y2': delta.y,
        })

    def __abs__(self):
        return abs(self.p2 - self.p1)

    def resize(self, start, end, time=1, ease=easeInOut):
        
        def action(t, dt):
            self.set(self.p1, self.p2, scale = interpolate(start, end, t, ease))
        self.animation.add(action, time)
        return self
    
    def grow(self, time=1, ease=easeInOut):
        return self.resize(0, 1, time, ease)

    def shrink(self, time=1, ease=easeInOut):
        return self.resize(1, 0, time, ease)

    def scale(self, scale, time=1, ease=easeInOut):
        return self.resize(self._scale, self._scale * scale, time, ease)

    def update(self, a, b, time=1, ease=easeInOut):
        def action(t, dt):
            self.set(a(ease(t)), b(ease(t)))
        self.animation.add(action, time)
        return self

    @property # Vector Midpoint
    def center(self):
        return (self.p1 + self.p2 * self._scale) / 2

    @property
    def position(self):
        return self.p1

    @position.setter
    def position(self, pos):
        self.set(pos, pos + (self.p2 - self.p1))

    def rotate(self, angle, center=None, time=1, ease=easeInOut):
        if center is None:
            center = self.p1
        start1 = self.p1 - center
        start2 = self.p2 - center
        def action(t, dt):
            a1 = angle * ease(t)
            a2 = angle * ease(t-dt)
            delta1 = start1.rotate(a1) - start1.rotate(a2)
            delta2 = start2.rotate(a1) - start2.rotate(a2)
            
            self.set(self.p1 + delta1, self.p2 + delta2)
        
        self.animation.add(action, time)
        return self

class Circle(svg.Circle, AnimatedObject):
    def __init__(self, center, r, style={}):
        self.center = center
        self.r = r
        svg.Circle.__init__(self, center.x, center.y, r, style)
        AnimatedObject.__init__(self)
    def set(self, center, r):
        self.center = center
        self.r = r
        self.setAttributes({
            'cx': center.x,
            'cy': center.y,
            'r': r
        })

    def resize(self, start=None, end=10, time=1, ease=easeInOut):
        if start == None:
            start = self.r
        orig = self.r
        def action(t, dt):
            r = start * (1 - ease(t)) + end * ease(t)
            self.set(self.center, r)

        self.animation.add(action, time)
        return self

    def grow(self, time=1, ease=easeInOut): # Hides an object
        return self.resize(0, self.r, time, ease)

    def shrink(self, time=1, ease=easeInOut):
        return self.resize(self.r, 0, time, ease)

    def scale(self, scale, time=1, ease=easeInOut):
        return self.resize(self.r, self.r * scale, time, ease)

    @property
    def position(self):
        return self.center
    @position.setter
    def position(self, pos):
        self.set(pos, self.r)

    def rotate(self, angle, center, time=1, ease=easeInOut):
        start = self.center - center

        def action(t, dt):
            delta = start.rotate(angle * ease(t)) - start.rotate(angle * ease(t - dt))
            self.set(self.center + delta , self.r)
        self.animation.add(action, time)
        return self

class Parametric(svg.Path, AnimatedObject):
    def __init__(self, origin, f, t0, t1, style={}, n=30):
        svg.Path.__init__(self, style)
        AnimatedObject.__init__(self)
        self.set(origin, f, t0, t1, n)

    def set(self, origin, f, t0, t1, n=30):
        self.origin = origin
        self.f = f
        self.t0 = t0
        self.t1 = t1
        self.n = n
        self.clear()
        parametric = lambda t: f(t) + self.origin
        self.parametric(parametric, t0, t1, n)

    # Transforms a Function (interpolation)
    def transformFunction(self, newFunction, time=1, ease=easeInOut):
        oldFunction = self.f
        def action(t, dt):
            f = lambda x: interpolate(oldFunction(x), newFunction(x), t, ease)

            self.set(self.origin, f, self.t0, self.t1, self.n)
        def onEnd():
            f = newFunction
            self.set(self.origin, newFunction, self.t0, self.t1, self.n)

        self.animation.add(action, time, onEnd)
        return self

    # Transforms a function (using another function)
    def updateFunction(self, functionGenerator, time=1, ease=easeInOut):
        def action(t, dt):
            function = functionGenerator(ease(t))
            self.set(self.origin, function, self.t0, self.t1, self.n)
        self.animation.add(action, time)
        return self

    def changeLimits(self, x0, x1, x2, x3, time=1, ease=easeInOut):
        def action(t, dt):
            current_x0 = interpolate(x0, x2, t, ease) 
            current_x1 = interpolate(x1, x3, t, ease) 
            self.set(self.origin, self.f, current_x0, current_x1, self.n)
        self.animation.add(action, time)
        return self

    def draw(self, time=1, start=None, end=None, ease=easeInOut):
        if start is None:
            start = self.t0
        if end is None:
            end = self.t1
        return self.changeLimits(self.t0, start, self.t0, end, time, ease)

    def erase(self, time=1, start=None, end=None, ease=easeInOut):
        if start is None:
            start = self.t0
        if end is None:
            end = self.t1
        return self.changeLimits(start, self.t1, end, self.t1, time, ease)


    # Shifts on X axis
    def shift(self, dx, time=1, ease=easeInOut):
        k = self.f
        def generator(t):
            return lambda x: k(x + t * dx)
        return self.updateFunction(generator)

    # Scales on Y axis
    def scale(self, a, time=1, ease=easeInOut):
        k = self.f
        return self.transformFunction(lambda t: a * k(t), time, ease)

    def scaleT(self, a, time=1, ease=easeInOut):
        k = self.f
        def generator(t):
            return lambda x: k((1 + (a-1) * t) * x)
        return self.updateFunction(generator)

class Function(Parametric):
    def __init__(self, origin, f, x0, x1, style={}, n=30):
        svg.Path.__init__(self, style)
        AnimatedObject.__init__(self)
        self.set(origin, f, x0, x1, n)

    def set(self, origin, f, x0, x1, n=30):
        self.origin = origin
        self.f = f
        self.t0 = x0
        self.t1 = x1
        self.n = n
        parametric = lambda x: svg.Point(x + origin.x, f(x) + origin.y)
        self.clear()
        self.parametric(parametric, x0, x1, n)

class Polygon(svg.Polygon, AnimatedObject):
    def __init__(self, points, style={}):
        self.initialPoints = points
        svg.Polygon.__init__(self, points, style)
        AnimatedObject.__init__(self)
        self.scale=1

    def set(self, points, scale=1):
        self.initialPoints = points
        self.scale = scale
        scaledPoints = [self.center + scale * (p - self.center) for p in points]
        self.points = scaledPoints

    def changeScale(self, start, end, time=1, ease=easeInOut):
        def action(t, dt):
            self.set(self.initialPoints, interpolate(start, end, t, ease))

        self.animation.add(action, time)
        return self

    def grow(self, time=1, ease=easeInOut):
        return self.changeScale(0, 1, time, ease)

    def shrink(self, time=1, ease=easeInOut):
        return self.changeScale(1, 0, time, ease)

    def update(self, pointsFunction, time=1, ease=easeInOut):
        def action(t, dt):
            self.set(pointsFunction(t))
        self.animation.add(action, time)
        return self

    @property
    def position(self):
        return self.center

    @position.setter
    def position(self, pos):
        c = self.center
        self.set([pos + (p - c) for p in self.points])

    def rotate(self, angle, center=None, time=1, ease=easeInOut):
        if center is None:
            center = self.center
        initial = [p - center for p in self.points]
        def action(t, dt):
            points = []
            a1 = angle * ease(t)
            a2 = angle * ease(t - dt)
            for p in range(len(initial)):
                delta = initial[p].rotate(a1) - initial[p].rotate(a2)
                points.append(self.points[p] + delta)

            self.set(points, self.scale)

        self.animation.add(action, time)
        return self

class RegularPolygon(Polygon):
    def __init__(self, center, vertex, sides, style={}):
        reg = svg.RegularPolygon(center.x, center.y, vertex.x, vertex.y, sides)
        points = [svg.Point(*p) for p in reg.points]
        Polygon.__init__(self, points, style)

class Group(svg.Group, AnimatedObject):
    def __init__(self, *elements):
        svg.Group.__init__(self, *elements)
        AnimatedObject.__init__(self)
        self.origin = Point(0, 0)
    
    @property
    def position(self):
        return self.origin
    @position.setter
    def position(self, position):
        self.origin = position
        self.clearTransform()
        self.translate(position.x, position.y)


class Text(svg.Text, AnimatedObject):
    def __init__(self, origin, text, style={}):
        svg.Text.__init__(self, origin.x, origin.y, text, style)
        AnimatedObject.__init__(self)
        self.origin = origin

    def set(self, origin, text):
        self.origin = origin
        self.setAttributes({'x': origin.x, 'y': origin.y})
        self.x = origin.x
        self.y = origin.y
        self.text = text

    @property
    def position(self):
        return self.origin
    @position.setter
    def position(self, pos):
        self.set(pos, self.text)

    def fadeText(self, newText, time=1, ease=easeInOut):
        def action(t, dt):
            startText = self.text
            if ease(t) >= 0.5:
                self.set(self.origin, newText)
                self.setAttributes({'opacity': round(2 * ease(t) - 1, 2)})
            else:
                self.set(self.origin, startText)
                self.setAttributes({'opacity':  round(1 - 2 * ease(t), 2)})

        self.animation.add(action, time)
        return self

    def textFunction(self, f, time=1, ease=easeInOut):
        def action(t, dt):
            self.text = f(round(ease(t), 4))

        self.animation.add(action, time)
        return self

    def integerCount(self, formatString, start, end, time=1, ease=easeInOut):
        function = lambda t: formatString.format(int((1-t) * start + t * end))
        return self.textFunction(function, time, ease)

    def typeText(self, text, time=1, ease=easeInOut):
        function = lambda t: text[0 : int(t * len(text))]
        return self.textFunction(function, time, ease)

    def deleteText(self, time=1, ease=easeInOut):
        text = self.text
        function = lambda t: text[0 : int((1 - t) * len(text))]
        return self.textFunction(function, time, ease)
