
from librosa import load
from pyparsing import C
import soundfile
import os, glob
from pathlib import Path
import subprocess
from tkinter import filedialog
from pedalboard import Delay, Pedalboard, Chorus, Reverb, Delay, Distortion, HighpassFilter, Phaser, Bitcrush, IIRFilter, Compressor, LadderFilter, Gain, Convolution
from pedalboard.io import AudioFile
import moviepy.editor as mpy
import math
import multiprocessing 
import imageio.v3 as iio
import imageio.v2 as iio2
import numpy as np
import sys
import rawdodendron as raw
#vid = "/vid/test.mkv"
from functools import partial

class glitch():
    def __init__(self):
        self.vidname = ""
        self.dir = ""
        self.current_dir = ""
        self.frames_dir = ""
        self.sound_dir = ""
        self.framesC_dir = ""
        self.mods_dir = ""
        self.counting = 0
        self.fps = 25
        self.width = 0
    def creating_dir(self,vid, fps, width):
        self.vidname = os.path.basename(vid)[:-4]
        self.fps = fps
        self.width = width
        self.dir = os.getcwd().replace('\\', '/')
        self.current_dir = "{}/{}2".format(self.dir, self.vidname)
        d = Path(self.current_dir)
        d.mkdir(exist_ok=True)
        print(self.current_dir)
        self.frames_dir = "{}/frames".format(self.current_dir)
        self.sound_dir = "{}/sound".format(self.current_dir)
        self.framesC_dir = "{}/framesC".format(self.current_dir)
        self.mods_dir = "{}/mods".format(self.current_dir)
        f = Path(self.frames_dir)
        f.mkdir(exist_ok=True)
        c = Path(self.framesC_dir)
        c.mkdir(exist_ok=True)
        s = Path(self.sound_dir)
        s.mkdir(exist_ok=True)
        m = Path(self.mods_dir)
        m.mkdir(exist_ok=True)

        return self.vidname, self.frames_dir, self.sound_dir, self.framesC_dir, self.mods_dir

    def extracting(self):
        #fhand = open(fname)
        count = np.asarray([])
        for idx, frame in enumerate(iio.imiter(vid)):
            print(idx)
            path = "{}/{}_frame".format(self.frames_dir, self.vidname)
            iio.imwrite(f"{path}{idx:d}.jpg", frame)
            count = np.append(count, idx)
            #print(self.count)
        #self.counting = np.array_split(self.count, 4)
        print("idx: {}, count:{}".format(idx,count))
        self.counting = int(idx)
        return count

    def transform(self, count):
        outputs = []
        for i in np.nditer(count):
            #print(len(count))
            print("this is i:{}".format(i))
            x = str(i)
            print("x = {}".format(x))
            x = x[:-2]
            x= int(x)
            print("X=={}".format(x))
            #self.outputs[x] = raw.initialize(input = '{}/{}_frame{}.jpg'.format(self.self.frames_dir, self.vid_name, x), output = '{}/{}_sound{}.wav'.format(self.self.sound_dir, self.vid_name,x), self.vidname = self.vid_name)
            #print("outputs: {}".format(outputs[x]))
            os.system('python rawdodendron.py -i {}/{}_frame{}.jpg  -o {}/{}_sound{}.wav -w {} --ignore-history'.format(self.frames_dir, self.vidname, x, self.sound_dir, self.vidname,x, self.width))
        #return outputs    

#            x = str(i)
           # x = x[:-1]
    def add_effects(self, count):
        self.entries = os.listdir(self.sound_dir)
        for i in np.nditer(count):
            x = str(i)
            print("x = {}".format(x))
            x = x[:-2]
            x= int(x)
            #sine = self.map_range(math.sin(int(x)+ math.sin(int(x))), -1, 1, 0,  32)
            board = Pedalboard([
                                Compressor(threshold_db=-50, ratio=25),
                                Gain(gain_db=30),
                                Chorus(),
                                LadderFilter(mode=LadderFilter.Mode.HPF12, cutoff_hz=900),
                                Phaser(),
                                Reverb(room_size=0.25)])
            path = "{}/{}_mod{}.wav".format(self.mods_dir,self.vidname,x)
            check_file = os.path.isfile(path)
            infile = "{}/{}_sound{}.wav".format(self.sound_dir, self.vidname, x)
            outfile = "{}/{}_mod{}.wav".format(self.mods_dir,self.vidname,x)
            #outfile_temp = "{}/{}_temp{}.wav".format(self.mods_dir,self.vid_name,x)
            if check_file != True:
                with AudioFile(infile) as f:
                    # Open an audio file to write to:
                    sample_rate = 44100
                    with AudioFile(outfile, 'w', sample_rate, f.num_channels) as o:
                        # Read one second of audio at a time, until the file is empty:
                        while f.tell() < f.frames:
                            chunk = f.read(f.samplerate)
                            

                            # Run the audio through our pedalboard:
                            effected = board(chunk, sample_rate, reset=False)
                            #print(effected)
                            # Write the output to our output file:
                            o.write(effected)
        

    def convertBack(self, count):
        for i in np.nditer(count):
            x = str(i)
            x = x[:-2]
            x= int(x)
            path = "{}/{}_frameC{}.jpg".format(self.framesC_dir, self.vidname,x)
            check_file = os.path.isfile(path)
            os.system('python rawdodendron.py -i {}/{}_mod{}.wav  -o {}/{}_frameC{}.png -w {} --ignore-history'.format(self.mods_dir,self.vidname,x, self.framesC_dir, self.vidname, x, self.width))

    def save(self):

        with iio2.get_writer('test_{}.mp4'.format(self.vidname), fps = self.fps) as writer:
            for x in range(self.counting):
                complete_path = '{}/{}_frameC{}.png'.format(self.framesC_dir,self.vidname,x)
                image = iio.imread(complete_path)
                writer.append_data(image)

    


    def map_range(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


    def chunking(self, element):
        element = np.asarray(element)
        num_processes = 4
        chunk_size = int(element.shape[0] / num_processes) 
        chunks = [element[i:i + chunk_size] for i in range(0, element.shape[0], chunk_size)] 
        return chunks

if __name__ == "__main__":
    print("Number of cpu : ", multiprocessing.cpu_count())
    vid = filedialog.askopenfilename()
    totalframes=iio.improps(vid, plugin="pyav").shape[0]
    metadate = iio.immeta(vid)
    fps = metadate["fps"]
    width = metadate["size"]
    width = width[0]
    print("width{}".format(width))
    print(metadate)
    print(totalframes)
    frames = np.asarray(totalframes)
    print(vid)
    Glitch = glitch()
    #multiprocessing.set_start_method('spawn')

    Glitch.creating_dir(vid,fps, width)
    count = Glitch.extracting()

    with multiprocessing.Pool(2) as pool:
        #count  = Glitch.chunking(count)
        #frames_dir = chunking(count)
        #sound_dir = chunking(sound_dir)
        #vidname = chunking(vidname)
        
        print("multiprocessing on")
        #result_args = partial(Glitch.transform, count, frames_dir, sound_dir,vidname)
        result = pool.map(Glitch.transform, count)
        pool.close()

    with multiprocessing.Pool(2) as pool:
        #count  = Glitch.chunking(count)
        #frames_dir = chunking(count)
        #sound_dir = chunking(sound_dir)
        #vidname = chunking(vidname)
        
        print("multiprocessing on")
        #result_args = partial(Glitch.transform, count, frames_dir, sound_dir,vidname)
        effects = pool.map(Glitch.add_effects, count)
        pool.close()
    with multiprocessing.Pool(2) as pool:
        #count  = Glitch.chunking(count)
        #frames_dir = chunking(count)
        #sound_dir = chunking(sound_dir)
        #vidname = chunking(vidname)
        
        print("multiprocessing on")
        #result_args = partial(Glitch.transform, count, frames_dir, sound_dir,vidname)
        revert = pool.map(Glitch.convertBack, count)
        pool.close()



        print(result)

    #glitch.Tpool_handler()
    #glitch.Epool_handler()
    #glitch.Cpool_handler()
    Glitch.save()
