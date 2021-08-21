import math
import xml.etree.ElementTree as ET

class Point3D():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def matrix(self, matrix):
        p = (self.x, self.y, self.z, 1)
        ret = [0, 0, 0, 0]
        for row in range(len(matrix)):
            for i in range(len(matrix)):
                ret[row] += matrix[row][i] * p[i]
        return Point3D(ret[0], ret[1], ret[2])

    def transform(self, ax, ay, az, dx, dy, dz):
        cx = math.cos(ax)
        cy = math.cos(ay)
        cz = math.cos(az)
        sx = math.sin(ax)
        sy = math.sin(ay)
        sz = math.sin(az)
        m = (
            (cz * cy, cz*sy*sx - sz*cx, cz*sy*cx + sz*sx, dx),
            (sz * cy, sz*sy*sx + cz*cx, sz*sy*cx - cz*sx, dy),
            (-sy, cy * sx, cy * cx, dz),
            (0, 0, 0, 1)
        )
        return self.matrix(m)
    
    def rotateX(self, angle):
        return self.transform(angle, 0, 0, 0, 0, 0)
    def rotateY(self, angle):
        return self.transform(0, angle, 0, 0, 0, 0)
    def rotateZ(self, angle):
        return self.transform(0, 0, angle, 0, 0, 0)
    rotate = rotateZ

    def unitVector(self):
        return self/abs(self)

    def to2D(self, d=None):
        k = 1
        if d is not None:
            k = d / (d - self.z)

        return k * Point(self.x, self.y)

    def azimuth(self):
        return math.atan2(self.y, self.x)

    def elevation(self):
        d = math.sqrt(self.x**2, self.y**2)
        return math.atan2(self.z, d)

    def __add__(self, other):
        return Point3D(
                self.x + other.x,
                self.y + other.y,
                self.z + other.z
            )

    def __sub__(self, other):
        return Point3D(
                self.x - other.x,
                self.y - other.y,
                self.z - other.z
            )
    def __neg__(self):
        return Point3D(-self.x, -self.y, -self.z)

    def __mul__(self, other):
        return Point3D(
                other * self.x,
                other * self.y,
                other * self.z
            )
    __rmul__ = __mul__

    def __truediv__(self, other):
        return Point3D(
                self.x / other,
                self.y / other,
                self.z / other
            )

    def dot(self, b):
        return self.x * b.x + self.y * b.y + self.z * other.z
    
    def cross(self, b):
        return Point3D(
                self.y * b.z - self.z * b.y,
                self.z * b.x - self.x * b.z,
                self.x * b.y - self.y * b.x
            )

    def __str__(self):
        return '({}, {}, {})'.format(self.x, self.y, self.z)
    def __repr__(self):
        return 'Point3D({}, {}, {})'.format(self.x, self.y, self.z)

    def __getitem__(self, index):
        if index > 2:
            raise IndexError('Higher dimension')
        return (self.x, self.y, self.z)[index]

    def __eq__(self, other):
        if isinstance(other, Point3D):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False



class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def unitVector(self):
        return self / abs(self)

    @property
    def angle(self):
        return math.atan2(self.y, self.x)
    phase = angle

    def rotate(self, angle):
        r = abs(self)
        a = self.angle
        return Point(r * math.cos(angle + a), r * math.sin(angle + a))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    def __neg__(self):
        return Point(-self.x, -self.y)

    def __mul__(self, other):
        if isinstance(other, Point):
            return self.x * other.x + self.y * other.y
        return Point(other * self.x, other * self.y)
    __rmul__ = __mul__

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __repr__(self):
        return 'Point({}, {})'.format(self.x, self.y)

    def __getitem__(self, index):
        if index > 1:
            raise IndexError('Higher dimension')
        return (self.x, self.y)[index]

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False


class Polar(Point):
    def __init__(self, r, angle):
        super().__init__(r * math.cos(angle), r * math.sin(angle))


class Element:
    def __init__(self, tag, attributes={}):
        self.root = ET.Element(tag)
        self.setAttributes(attributes)

    def add(self, *elements):
        for e in elements:
            self.root.append(e.root)

    def remove(self, *elements):
        for e in elements:
            self.root.remove(e.root)

    def setAttributes(self, attributes):
        for key, value in attributes.items():
            if value is None:
                value = 'none'
            self.root.set(key, str(value))

    def set(self, key, value):
        self.root.set(key, str(value))

    def get(self, key):
        return self.root.get(key)

    def __str__(self):
        return ET.tostring(self.root, encoding='unicode')

    def _setId(self, id):
        self.root.set('id', id)
    def _getId(self):
        return self.root.get('id')

    def _setClass(self, className):
        self.root.set('class', className)
    def _getClass(self):
        return self.root.get('class')

    id = property(_getId, _setId)
    className = property(_getClass, _setClass)


class Style(Element):
    def __init__(self, style):
        super().__init__('style')
        self.root.text = style

class Drawing(Element):
    def __init__(self, width, height, origin='default'):
        super().__init__('svg')
        self.width = width
        self.height = height

        viewBox = ''
        if origin == 'default':
            viewBox = '0 0 {} {}'.format(width, height)
            self.center = Point(width/2, height/2)
            self.min = Point(0, 0)
        elif origin == 'center':
            viewBox = '{} {} {} {}'.format(-width/2, -height/2, width, height)
            self.min = Point(-width/2, -height/2)
            self.center = Point(0, 0)

        self.setAttributes({
                'xmlns': 'http://www.w3.org/2000/svg',
                'viewBox': viewBox
            })

    def fill(self, color, attributes = {}):
        background = Rect(self.min.x, self.min.y, self.width, self.height, Fill(color))
        background.setAttributes(attributes)
        self.add(background)
        return background

    def byteString(self):
        return ET.tostring(self.root)

    def write(self, filename):
        f = open(filename, 'w')
        f.write(str(self))
        f.close()

class Figure(Element):
    def __init__(self, tag, attributes={}):
        super().__init__(tag, attributes)

    def transform(self, transformation):
        t = self.root.get('transform')
        if t is None:
            t = ''
        self.root.set('transform', t + transformation)
        return self

    def clearTransform(self):
        self.root.attrib.pop('transform', None)

    def rotate(self, angle, x=None, y=None):
        a = math.degrees(angle)
        if x is None and y is None:
            return self.transform('rotate({})'.format(a))
        else:
            return self.transform('rotate({} {} {})'.format(a, x, y))
    
    def translate(self, dx, dy=None):
        if dy is None:
            return self.transform('translate({})'.format(dx))
        return self.transform('translate({} {})'.format(dx, dy))

    def scale(self, kx, ky=None):
        if ky is None:
            return self.transform('scale({})'.format(kx))
        return self.transform('scale({} {})'.format(kx, ky))

    def matrix(self, a, b, c, d, e, f):
        return self.transform('matrix({} {} {} {} {} {})'.format(a, b, c, d, e, f))

    def skewX(self, angle):
        return self.transform('skewX({})'.format(math.degrees(angle)))
    def skewY(self, angle):
        return self.transform('skewY({})'.format(math.degrees(angle)))

    def clone(self, x=0, y=0):
        use = Element('use')
        if self.id is None:
            raise ValueError('Element id not set')
        use.setAttributes({'href': '#' + self.id, 'x': x, 'y': y})
        return use

class Circle(Figure):
    def __init__(self, cx, cy, r, attributes={}):
        super().__init__('circle')
        self.setAttributes({'cx': cx, 'cy': cy, 'r': r})
        self.setAttributes(attributes)

class Ellipse(Figure):
    def __init__(self, cx, cy, rx, ry, attributes={}):
        super().__init__('ellipse')
        self.setAttributes({'cx': cx, 'cy': cy, 'rx': rx, 'ry': ry})
        self.setAttributes(attributes)

class Path(Figure):
    def __init__(self, attributes={}):
        super().__init__('path', attributes)
        self.d = ''

    def setPath(self):
        self.root.set('d', self.d)
        return self

    def command(self, command, *args):
        precision = 2 # Path precision
        roundedArgs = [round(a, precision) for a in args]
        self.d += command.format(*roundedArgs)
        return self.setPath()

    def M(self, x, y):
        return self.command('M {} {}', x, y)
    def m(self, dx, dy):
        return self.command('m {} {}', dx, dy)
    
    def L(self, x, y):
        return self.command('L {} {}', x, y)
    def l(self, dx, dy):
        return self.command('l {} {}', dx, dy)
    
    def H(self, x):
        return self.command('H {}', x)
    def h(self, dx):
        return self.command('h {}', dx)
    
    def V(self, y):
        return self.command('V {}', y)
    def v(self, dy):
        return self.command('v {}', dy)

    def Z(self):
        self.d += 'Z'
        return self.setPath()

    def C(self, cx1, cy1, cx2, cy2, x2, y2):
        return self.command('C {} {}, {} {}, {} {}', cx1, cy1, cx2, cy2, x2, y2)
    def c(self, cdx1, cdy1, cdx2, cdy2, dx2, dy2):
        return self.command('c {} {}, {} {}, {} {}', cdx1, cdy1, cdx2, cdy2, dx2, dy2)
    def S(self, cx2, cy2, x2, y2):
        return self.command('S {} {}, {} {}', cx2, cy2, x2, y2)
    def s(self, cdx2, cdy2, dx2, dy2):
        return self.command('s {} {}, {} {}', cdx2, cdy2, dx2, dy2)

    def Q(self, cx, cy, x, y):
        return self.command('Q {} {}, {} {}', cx, cy, x, y)
    def q(self, cdx1, cdy1, dx, dy):
        return self.command('Q {} {} {} {}', cdx1, cdy1, dx, dy)
    def T(self, x, y):
        return self.command('T {} {}', x, y)
    def t(self, dx, dy):
        return self.command('t {} {}', dx, dy)

    def A(self, rx, ry, rotation, largeArc, sweep, x, y):
        return self.command('A {} {} {} {} {} {} {}', rx, ry, rotation, int(largeArc), int(sweep), x, y)
    def a(self, rx, ry, rotation, largeArc, sweep, dx, dy):
        return self.command('a {} {} {} {} {} {} {}', rx, ry, rotation, int(largeArc), int(sweep), dx, dy)

    def arc(self, cx, cy, rx, ry, startAngle, endAngle, drawSlice=False):
        center = Point(cx, cy)
        startPoint = Point(rx * math.cos(startAngle), ry * math.sin(startAngle)) + center
        endPoint = Point(rx * math.cos(endAngle), ry * math.sin(endAngle)) + center
       
        if drawSlice:
            self.M(center.x, center.y)
            self.L(startPoint.x, startPoint.y)
        else:
            self.M(startPoint.x, startPoint.y)

        largeArc = abs(endAngle - startAngle) > math.pi
        sweep = 1
        self.A(rx, ry, 0, largeArc, sweep, endPoint.x, endPoint.y)
        
        if drawSlice:
            self.Z()
        return self

    def parametric(self, f, start, end, n, delta=1e-3):
        inc = (end - start) / (n - 1)
        first = True

        for t in range(n-1):
            k  = inc/delta
            try:
                if first:
                    t1 = start + t * inc
                    P0 = Point(*f(t1))
                    d1 = k * (Point(*f(t1 + delta)) - P0)
                    P1 = P0 + d1 / 3
                t2 = start + (t + 1) * inc
                P3 = Point(*f(t2))
                d2 = k * (Point(*f(t2 + delta)) - P3)
                P2 = P3 - d2 / 3

                try:
                    m = d2.y / d2.x
                except ZeroDivisionError:
                    m = 600
                if m > 500:
                    first = True
                elif first:
                    self.M(P0.x, P0.y)
                    self.C(P1.x, P1.y, P2.x, P2.y, P3.x, P3.y)
                    first = False
                else:
                    self.S(P2.x, P2.y, P3.x, P3.y)
            except ValueError:
                first = True

    def clear(self):
        self.d = ''
        self.root.attrib.pop('d', None)


class Line(Figure):
    def __init__(self, x1, y1, x2, y2, attributes={}):
        super().__init__('line')
        self.setAttributes({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})
        self.setAttributes(attributes)


class Rect(Figure):
    def __init__(self, x, y, w, h, attributes={}):
        super().__init__('rect')
        self.setAttributes({'x': x, 'y': y, 'width': w, 'height': h})
        self.setAttributes(attributes)
    def setCornerRadius(self, rx, ry=None):
        if ry is None:
            ry = rx
        self.setAttributes({'rx': rx, 'ry': ry})

class Polygon(Figure):
    def __init__(self, points, attributes={}):
        super().__init__('polygon')
        self.points = points
        self.setAttributes(attributes)

    @property
    def center(self):
        c = Point(0, 0)
        sides = len(self.points)
        for p in self.points:
            c.x += p[0]
            c.y += p[1]
        return c / sides


    def _setPoints(self, points):
        if len(points) < 3:
            raise ValueError('Polygons must have at least three sides.')

        self._points = points
        pointsString = ' '.join(list(map(lambda p: '{},{}'.format(p[0], p[1]), points)))
        self.setAttributes({'points': pointsString})

    def _getPoints(self):
        return self._points

    points = property(_getPoints, _setPoints)

class RegularPolygon(Polygon):
    def __init__(self, cx, cy, px, py, sides, attributes = {}):
        v = Point(px - cx, py - cy)
        r = abs(v)
        angle = v.angle
        c = Point(cx, cy)
        points = []
        for side in range(sides):
            p = c + Polar(r, angle + side * 2 * math.pi / sides)
            points.append(tuple(p))
            
        super().__init__(points, attributes)

class Polyline(Figure):
    def __init__(self, points, attributes={}):
        super().__init('polyline')
        pointsString = ' '.join(list(map(lambda p: '{},{}'.format(p.x, p.y), points)))
        self.setAttributes({'points': pointsString})
        self.setAttributes(attributes)

class Group(Figure):
    def __init__(self, *elements):
        super().__init__('g')
        self.add(*elements)


class ClipPath(Figure):
    def __init__(self, identifier, *elements):
        super().__init__('clipPath')
        self.set('id', identifier)
        self.add(*elements)


class Text(Figure):
    def __init__(self, x, y, text, attributes={}):
        super().__init__('text')
        self.x = x
        self.y = y
        self.lineHeight = 1
        self.text = text
        self.lines = []
        self.setAttributes({'x': x, 'y': y})
        self.setAttributes(attributes)

    def align(self, mode):
        if mode == 'left' or mode == 'start':
            self.root.set('text-anchor', 'start')
        elif mode == 'right' or mode == 'end':
            self.root.set('text-anchor', 'end')
        elif mode == 'center' or mode == 'middle':
            self.root.set('text-anchor', 'middle')
        self.set_text(self.text)
        return self

    def baseline(self, mode):
        if mode == 'top':
            self.root.set('dominant-baseline', 'auto')
        elif mode == 'middle' or mode == 'center':
            self.root.set('dominant-baseline', 'middle')
        elif mode == 'bottom':
            self.root.set('dominant-baseline', 'hanging')
        return self

    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text
        self.lines = []
        # Remove all sub-text elements
        for element in self.root.findall('tspan'):
            self.root.remove(element)

        first = True
        for line in text.split('\n'):
            span = Element('tspan')
            span.root.text = line
            if first:
                span.setAttributes({
                    'x': self.x,
                    'y': self.y
                })
                first = False
            else:
                span.setAttributes({
                    'x': self.x,
                    'dy': str(self.lineHeight) + 'em'
                })
            self.add(span)
            self.lines.append(span)

    text = property(get_text, set_text)

class Image(Figure):
    def __init__(self, x, y, w, h, href):
        super().__init__('image')
        self.setAttributes({
            'x': x,
            'y': y,
            'width': w,
            'height': h,
            'href': href
        })

class Link(Element):
    def __init__(self, url, content=None):
        super().__init__('a')
        self.setAttributes({'href': url})
        if content is not None:
            self.add(content)

# Styles (Fill, Stroke, Font, Opacity)

class FigureStyle(dict):
    def __init__(self, attributes={}):
        for key in attributes.keys():
            self[key] = attributes[key]

    def fill(self, color):
        self['fill'] = color
        return self

    def nonZero(self):
        self['fill-rule'] = 'nonzero'
        return self
    def evenOdd(self):
        self['fill-rule'] = 'evenodd'
        return self

    def stroke(self, color, width):
        self['stroke'] = color
        self['stroke-width'] = width
        return self

    def opacity(self, opacity):
        self['opacity'] = opacity
        return self

    def dashArray(self, *lengths):
        self['stroke-dasharray'] = ' '.join(map(str, lengths))
        return self

    def lineJoin(self, join):
        self['stroke-linejoin'] = join
        return self

    def lineCap(self, cap):
        self['stroke-linecap'] = cap
        return self


class Fill(FigureStyle):
    def __init__(self, color, opacity=None):
        super().__init__({'fill': color, 'stroke': None})
        
        if opacity is not None:
            self.opacity(opacity)

class Stroke(FigureStyle):
    def __init__(self, color, width, opacity=None):
        super().__init__({'fill': None, 'stroke': color, 'stroke-width': width})
        if opacity is not None:
            self.opacity(opacity)

class FillStroke(FigureStyle):
    def __init__(self, fill, stroke, width, opacity=None):
        super().__init__({'fill': fill, 'stroke': stroke, 'stroke-width': width})

        if opacity is not None:
            self.opacity(opacity)

class Font(FigureStyle):
    def __init__(self, fontFamily, size, fill='black', weight=None):
        properties = {'font-family': fontFamily, 'font-size': size, 'fill': fill, 'stroke': None}
        if weight is not None:
            properties['font-weight'] = weight
        super().__init__(properties)
