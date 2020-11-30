import imageio
import os

def stitch(filename, duration=.1):
    frames = [imageio.imread(os.path.join('frames/', file))
              for file in sorted(os.listdir('frames/'))]
    frames[-1:] += frames[-1:] * int(2 // duration) # Show last frame for longer duration
    imageio.mimsave(f'frames/{filename}.gif', frames, duration=duration)