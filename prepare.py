import sys, os

from glob import glob
from PIL import Image


height = 1600
process = True

# glob image sequence folders e.g. images-nytimes.com/
items = glob('*.com')


for path in items:
    maxw = 0

    for file in glob(path+'/*.png'):
        maxw = max(maxw, Image.open(file).size[0])

    for file in glob(path+'/*-full.png'):
        if process:
            im = Image.open(file)
            _w = im.size[0]
            im = im.crop((0,0,_w,height))
            src = Image.new("RGB",(maxw,height))
            src.paste(im,(maxw/2-_w/2,0))
            src = src.resize((maxw/3,height/3))
            src.save(file.replace('.png','-processed.png'),'PNG')

    os.system('convert -delay 10 -dither none -matte -depth 8 -deconstruct -layers optimizePlus -colors 64 -loop 0 {0}/*-processed.png {0}.gif'.format(path))