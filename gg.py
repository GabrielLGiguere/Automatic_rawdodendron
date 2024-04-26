import numpy as np
import random
import imageio.v3 as iio
import imageio.v2 as iio2
import os 
import glob
dir = "C:/Users/Gabriel/Automatic_rawdodendron/TV12/frames"
input = os.listdir(dir)
random.shuffle(input)
print(input)



with iio2.get_writer('C:/Users/Gabriel/Automatic_rawdodendron/TV12/testgggg.mp4', fps = 30) as writer:
    for x in input:
        complete = "C:/Users/Gabriel/Automatic_rawdodendron/TV12/frames/{}".format(x)
        image = iio.imread(complete)
        writer.append_data(image)