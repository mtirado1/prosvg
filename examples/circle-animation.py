import math
from prosvg import *
from style import *

video = Render(600, 600, fps=30)
video.start('circle-animation.mp4')
video.scene.fill(white)

circle = Circle(video.center, 50, svg.Fill(red))

video.add(circle)

video.play(circle.grow())

video.play(circle.move(X(100)))
video.play(circle.move(X(-200), time=2, ease=linear))
video.pause(2)

video.play(
    circle.rotate(
        2 * math.pi,  # Rotation point
        video.center, # Rotation center
        time=2,       # Animation time
        ease=linear   # Ease function
    ).scale(0.5, time=2)
)

video.pause()

video.end()
