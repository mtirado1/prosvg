import subprocess
import cairosvg
from . import svg

FFMPEG_BIN = 'ffmpeg'

class Render():
    def __init__(self, width, height, fps=30, scale=1, title=None):
        self.scene = svg.Drawing(width, height)

        self.width = width
        self.height = height

        # Useful reference points
        self.center = svg.Point(width/2, height/2)
        self.left   = svg.Point(0,       height/2)
        self.right  = svg.Point(width,   height/2)
        self.top    = svg.Point(width/2, 0)
        self.bottom = svg.Point(width/2, height)
        
        self.topLeft     = svg.Point(0,     0)
        self.topRight    = svg.Point(width, 0)
        self.bottomLeft  = svg.Point(0,     height)
        self.bottomRight = svg.Point(width, height)

        self.title = title
        self.frames = 0

        self.processes = {}
        self.fps = fps
        self.scale = scale

    def start(self, filename):
        self.running = True

        command = [ FFMPEG_BIN,
            '-hide_banner',
            '-loglevel', 'error',
            '-y', # Overwrite output file if it exists
            #'-f', 'image2pipe',
            '-r', str(self.fps),
            '-i', '-', # The input comes from a pipe
            '-pix_fmt', 'yuv420p',
            '-vcodec', 'libx264',
            '-b:v', '500k', 
            filename]
        self.processes[filename] = subprocess.Popen(command, stdin=subprocess.PIPE)


    def add(self, *elements): # Add svg elements, don't render them
        self.scene.add(*elements)
        return self

    def remove(self, *elements):
        self.scene.remove(*elements)
        return self

    def writeFrame(self, frames = 1):
        raster = cairosvg.svg2png(bytestring=self.scene.byteString(), scale=self.scale) * frames
        for filename, process in self.processes.items():
            process.stdin.write(raster)
        self.frames += frames

    def save(self, filename = None):
        print('Saving File...')
        if filename == None:
            filename = 'frame-{}.svg'.format(self.frames)
            self.scene.write(filename)
        else:
            extension = ''
            if len(filename.split('.')) > 0:
                extension = filename.split('.')[-1]
            if extension == 'png':
                cairosvg.svg2png(bytestring=self.scene.byteString(), scale=self.scale, write_to=filename)
            else:
                self.scene.write(filename)


    def play(self, *objects, comment=None):
        if not self.running:
            return
        runTime = max([o.animation.runTime for o in objects])
        frames = int(runTime * self.fps)
        if comment is None:
            print('Rendering {} frames ({} s)...'.format(frames, runTime))
        else:
            print('{} - Rendering {} frames ({} s)...'.format(comment, frames, runTime))
        for frame in range(frames):
            for o in objects:
                o.animation.run(1 / self.fps)
            self.writeFrame()
        for o in objects:
            o.animation.reset()
        return self

    def pause(self, time=1): # Pause animation
        if not self.running:
            return
        print('Pausing for {} frames ({} s)...'.format( int(time * self.fps), time))
        self.writeFrame(int(time * self.fps))
        return self

    def stop(self):
        print('Animation stopped')
        self.running = False
    def resume(self):
        print('Animation resumed')
        self.running = True

    def end(self, filename=None):
        if filename is None:
            for filename, process in self.processes.items():
                process.stdin.close()
                process.wait()
        elif filename in self.processes:
            self.processes[filename].stdin.close()
            self.processes[filename].wait()
            self.processes.pop(filename)
        print('Done. {} frames ({:.2f} s @ {} fps) generated.'.format(self.frames, self.frames/self.fps, self.fps))
