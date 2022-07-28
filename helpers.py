import math
import random

def source(uri, consts={}):
    """
    Read glsl code
    """
    with open(uri, 'r') as fp:
        content = fp.read()

    # feed constant values
    for key, value in consts.items():
        content = content.replace(f"%%{key}%%", str(value))
    return content

def gen_initial_data(COUNT):
        """Generator function creating the initial buffer data"""
        for i in range(COUNT):
            radius = random.random() * 0.01 + 0.01
            _v = random.random() * 0.0001 + 0.01
            if (i%5 == 0): # horizontal line
                yield 2* i/(COUNT-1) -1
                yield 0
                yield 0.
                yield radius 

                yield -_v 
                yield 0.
                yield 0.
                yield 0.

                yield 248 / 255
                yield 108 / 255
                yield 31 / 255
                yield 1.0
            elif (i%5 == 1): # slanted line
                yield .2*(2* i/(COUNT-1) -1)
                yield 2* i/(COUNT-1) -1
                yield 0.
                yield radius 

                yield 0
                yield -_v
                yield 0.
                yield 0.

                yield 248 / 255
                yield 108 / 255
                yield 31 / 255
                yield 1.0
            elif (i%5 == 2): # big circle
                _angle = (i / COUNT) * math.pi * 2.0
                _dist = 0.125
                # position and radius (vec4)
                yield math.cos(_angle) * _dist
                yield math.sin(_angle) * _dist
                yield 0.0
                yield radius
                # velocity (vec4)
                yield math.cos(_angle) * _v
                yield math.sin(_angle) * _v
                yield 0.
                yield 0.
                # color (vec4)
                yield 248 / 255
                yield 108 / 255
                yield 31 / 255
                yield 1.
            elif (i%5 == 3): # small 0
                _angle = (i / COUNT) * math.pi * 2.0
                _dist = 0.001
                # position and radius (vec4)
                yield math.cos(_angle) * _dist - 0.06
                yield math.sin(_angle) * _dist
                yield 0.0
                yield radius
                # velocity (vec4)
                yield 0.
                yield 0.
                yield 0.
                yield 0.
                # color (vec4)
                yield 1.
                yield 1.
                yield 1.
                yield 1.
            else: # little slanted bar
                yield .07*(2* i/(COUNT-1) -1)
                yield   .2*(i/(COUNT-1) -.5)
                yield 0.
                yield radius 

                yield 0
                yield -_v
                yield 0.
                yield 0.

                yield 1.
                yield 1.
                yield 1.
                yield 1.