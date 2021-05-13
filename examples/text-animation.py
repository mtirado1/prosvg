from prosvg import *
from style import *

video = Render(800, 600, fps=30)
video.start('text-animation.mp4')
video.scene.fill(white)

video.pause()

title = Text(
    video.center, # Position
    'Text Example', # Text
    svg.Font('sans-serif', 40, green) # Attributes
)
title.align('center')

video.add(title)
video.play(title.fadeIn())
video.pause()

video.play(title.move(X(200)))
video.play(title.move(X(-400)))
video.play(title.move(X(200)))

video.play(title.fadeText('Count: 0'))

video.play(title.integerCount('Count: {}', 0, 100, time=5))
video.pause()

video.play(title.deleteText())
video.pause()

video.play(
    title.typeText(
        'Typing some text\nanother line of text\n1 2 3 4 5 6 7 8 9',
        time=4, ease=linear
    )
)
video.pause()

video.end()
