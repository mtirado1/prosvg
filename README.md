# ProSVG - Programmatic SVG with Python

![functions.png](functions.png)

The purpose behind this framework was toeasily draw mathematical functions using vector graphics.

## Vector Images

## Animations

![Demo](demo/demo.gif)

## How it Works

Similar to [3blue1brown's manim](https://github.com/3b1b/manim), the animation module renders the svg file as an image and pipes it to ffmpeg.

1. Increase animation time by $\text{dt}$
2. Update svg objects (transformations, movement, etc.)
3. If an animation has exceeded its runtime, it will be removed from the object
4. Convert svg to png using [CairoSVG](https://cairosvg.org)
5. Pipe png image to ffmpeg
6. Repeat until the animation ends

