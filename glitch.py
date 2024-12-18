
from librosa import load
from pyparsing import C
import os, glob
from pathlib import Path
from tkinter import filedialog
import pedalboard
from pedalboard import Pedalboard, Bitcrush, Chain,  Clipping, Compressor, Chorus, Convolution, Delay, Distortion, Gain, GSMFullRateCompressor, HighShelfFilter, HighpassFilter,  IIRFilter, Invert, LadderFilter, Limiter, LowShelfFilter, LowpassFilter, MP3Compressor, NoiseGate, PeakFilter, PitchShift, Resample, Phaser, Reverb, time_stretch
from pedalboard.io import AudioFile
import moviepy.editor as mpy
import multiprocessing 
import imageio.v3 as iio
import imageio.v2 as iio2
import numpy as np
import numpy.random
import tkinter as tk
import rawdodendron as raw
import threading
from typing import TypedDict
#vid = "/vid/test.mkv"
from functools import partial
from pydub import AudioSegment
from pydub.playback import play
import json
import inspect
jsonfile =  open("config.json", "r", encoding='utf-8')
config = json.load(jsonfile)


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
        self.slc_effects = []
        self.effects = {
            "Bitcrush" : pedalboard.Bitcrush,
            "Chain" : pedalboard.Chain,
            "Clipping" : pedalboard.Clipping,
            "Compressor": pedalboard.Compressor,
            "Chorus": pedalboard.Chorus,
            "Delay":pedalboard.Delay,
            "Distortion":pedalboard.Distortion,
            "Gain":pedalboard.Gain,
            "GSMFullRateCompressor":GSMFullRateCompressor,
            "HighShelfFilter":HighShelfFilter,
            "HighpassFilter":HighpassFilter,
            "IIRFilter":HighpassFilter,
            "Invert":Invert,
            "LadderFilter":LadderFilter,
            "Limiter":Limiter,
            "LowShelfFilter":LowShelfFilter,
            "LowpassFilter":LowpassFilter,
            "MP3Compressor":MP3Compressor,
            "NoiseGate":NoiseGate,
            "PeakFilter":PeakFilter,
            "PitchShift":PitchShift,
            "Resample":Resample,
            "Phaser":Phaser,
            "Reverb":Reverb,
        }




    def creating_dir(self,vid, fps, width, slct_e):
        self.vidname = os.path.basename(vid)[:-4]
        self.fps = fps
        self.width = width
        self.dir = os.getcwd().replace('\\', '/')
        self.current_dir = "{}/VIDEOS/{}1".format(self.dir, self.vidname)
        self.slc_effects = slct_e
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

    def extracting(self, vidx):
        #fhand = open(fname)
        count = np.asarray([])
        for idx, frame in enumerate(iio.imiter(vidx)):
            print(idx)
            fpath = "{}/{}_frame".format(self.frames_dir, self.vidname)
            dpath = f"{fpath}{idx:d}.jpg"
            print(os.path.isfile(dpath))
            if os.path.isfile(dpath)!= True:
                iio.imwrite(f"{fpath}{idx:d}.jpg", frame)
            count = np.append(count, idx)
            #print(self.count)
        #self.counting = np.array_split(self.count, 4)
        print("idx: {}, count:{}".format(idx,count))
        self.counting = int(idx)
        return count

    def transform(self, x):
        fpath = "{}/{}_sound{}.wav".format(self.frames_dir, self.vidname, x)
        if os.path.isfile(fpath) != True:
            os.system('python rawdodendron.py -i {}/{}_frame{}.jpg  -o {}/{}_sound{}.wav -w {} --ignore-history'.format(self.frames_dir, self.vidname, x, self.sound_dir, self.vidname,x, self.width))

    def add_effects(self, x):
        self.entries = os.listdir(self.sound_dir)
        path = "{}/{}_sound{}.wav".format(self.sound_dir, self.vidname, x)
        ffcts = []
        #sine = self.map_range(math.sin(int(x)+ math.sin(int(x))), -1, 1, 0,  32)
        for y in self.slc_effects:
            ffcts.append(self.effects[y]())
        print(ffcts)
        
        check_file = os.path.isfile(path)
        infile = "{}/{}_sound{}.wav".format(self.sound_dir, self.vidname, x)
        outfile = "{}/{}_mod{}.wav".format(self.mods_dir,self.vidname,x)
        #outfile_temp = "{}/{}_temp{}.wav".format(self.mods_dir,self.vid_name,x)
        
        samplerate = 44100.0
        with AudioFile(infile).resampled_to(samplerate) as f:
            audio = f.read(f.frames)   
        board = Pedalboard(ffcts)
        effected = board(audio, samplerate)
        with AudioFile(outfile, 'w', samplerate, effected.shape[0]) as f:
                f.write(effected)
                    
    def converts(self, function,count):
        for i in np.nditer(count):
            x = str(i)
            x = x[:-2]
            x= int(x)
            function(x)

    def convertBack(self, x):
        path = "{}/{}_frameC{}.jpg".format(self.framesC_dir, self.vidname,x)
        check_file = os.path.isfile(path)
        os.system('python rawdodendron.py -i {}/{}_mod{}.wav  -o {}/{}_frameC{}.png -w {} --ignore-history'.format(self.mods_dir,self.vidname,x, self.framesC_dir, self.vidname, x, self.width))

    def save(self):
        with iio2.get_writer('{}/{}.mp4'.format(self.current_dir, config["out_name"]), fps = self.fps) as writer:
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



class UI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Automatic Rawdodendron")
        self.master.geometry(config['geometry'])
        self.master.grid()
        self.vid = ""
        self.count_done = False
        self.count = 0
        self.Glitch = None
        self.cpu_count = multiprocessing.cpu_count()
        self.slct_cpu = tk.IntVar()
        self.start = False
        self.effects = tk.StringVar()
        self.out_name = tk.StringVar()
        self.effects.set(config["effects"])
        self.slct_effects = ""

        self.ffects = {
            "Bitcrush" : pedalboard.Bitcrush,
            "Chain" : pedalboard.Chain,
            "Clipping" : pedalboard.Clipping,
            "Compressor": pedalboard.Compressor,
            "Chorus": pedalboard.Chorus,
            "Delay":pedalboard.Delay,
            "Distortion":pedalboard.Distortion,
            "Gain":pedalboard.Gain,
            "GSMFullRateCompressor":pedalboard.GSMFullRateCompressor,
            "HighShelfFilter":pedalboard.HighShelfFilter,
            "HighpassFilter":pedalboard.HighpassFilter,
            "IIRFilter":pedalboard.HighpassFilter,
            "Invert":pedalboard.Invert,
            "LadderFilter":pedalboard.LadderFilter,
            "Limiter":pedalboard.Limiter,
            "LowShelfFilter":pedalboard.LowShelfFilter,
            "LowpassFilter":pedalboard.LowpassFilter,
            "MP3Compressor":pedalboard.MP3Compressor,
            "NoiseGate":pedalboard.NoiseGate,
            "PeakFilter":pedalboard.PeakFilter,
            "PitchShift":pedalboard.PitchShift,
            "Resample":pedalboard.Resample,
            "Phaser":pedalboard.Phaser,
            "Reverb":pedalboard.Reverb,
        }
        self.create_widgets()
        self.gridding()
        self.binding()

    def create_widgets(self):
        self.bttn_vid = tk.Button(self.master, 
                                text = "Fichier" , 
                                )

        self.lbl_vid = tk.Label(self.master, 
                                text = config["vidname"])

        self.scl_cpu = tk.Scale(self.master, 
                                label = "Nombre de CPU utilisés", 
                                from_ = 1, 
                                to = config["cpu_count"], 
                                tickinterval = 1 , 
                                variable = self.slct_cpu, 
                                command = self.updating("slct_cpu", self.slct_cpu.get()),
                                orient=tk.HORIZONTAL )

        self.lbl_effects = tk.Label(self.master,
                                text = "Effects")

        self.lstbx_effects = tk.Listbox(self.master,
                                listvariable = self.effects, 
                                selectmode = tk.MULTIPLE)

        self.lbl_slctd = tk.Label(self.master,
                                text = str(self.slct_effects))

        self.bttn_start = tk.Button(self.master,
                               
                                text = "Start")
        
        self.bttn_test = tk.Button(self.master,
                                
                                text = "test")

        self.ntry_name = tk.Entry(self.master,textvariable=self.out_name)

        self.lbl_out = tk.Label(self.master, text = "Nom du fichier de sauvegarde")

    def gridding(self):
        #row0
        self.bttn_vid.grid(row = 0, column= 0,sticky = 'w',padx = config["padx"], pady = config["pady"])
        self.lbl_vid.grid(row = 0, column=1,sticky = 'w',columnspan= 2,padx = config["padx"], pady = config["pady"])

        #row1
        self.lbl_out.grid(row=1, column = 0, sticky = 'w',padx = config["padx"], pady = config["pady"])

        #row2
        self.ntry_name.grid(row = 2, column = 0, sticky = 'w',padx = config["padx"], pady = config["pady"])
        
        #row3
        self.scl_cpu.grid(row = 3, column=0, columnspan=3 ,sticky = 'w',padx = config["padx"], pady = config["pady"])

        #row4
        self.lbl_effects.grid(row = 4, column=0 ,sticky = 'w',padx = config["padx"], pady = config["pady"])

        #row5
        self.lstbx_effects.grid(row =5, column = 0, columnspan= 2,padx = config["padx"], pady = config["pady"])
        self.lbl_slctd.grid(row = 5 , column=2,padx = config["padx"], pady = config["pady"])

        #row6
        self.bttn_start.grid(row = 6, column=0 ,sticky = 'n', columnspan=2,padx = config["padx"], pady = config["pady"])
        self.bttn_test.grid(row = 7, column=0 ,sticky = 'n', columnspan=2,padx = config["padx"], pady = config["pady"])
    
    def binding(self):
        self.bttn_vid.bind('<Button-1>', lambda evt: self.open_vid())
        self.scl_cpu.bind('<ButtonRelease-1>', lambda evt: self.updating("slct_cpu", self.slct_cpu.get()))
        self.lstbx_effects.bind('<<ListboxSelect>>', lambda evt: self.effect_slctd())
        self.bttn_start.bind('<Button-1>', lambda evt: self.starting())
        self.bttn_test.bind('<Button-1>', lambda evt: self.test())
    def params_change(self, param, value, index):
        name = "lbl_{}".format(param)
        self.name = tk.Label(self,text = param)
        name2 = "ntry_{}".format(param)
        self.name2 = tk.Entry(self, )
    def open_vid(self):
        config["vidname"] = filedialog.askopenfilename()
        self.lbl_vid.configure(text = config["vidname"])
        self.master.update_idletasks()
        print(self.lbl_vid.cget("text"))
    def vdir(self, obj):
        return [x for x in dir(obj) if not x.startswith('__')]
    def effect_slctd(self):
        config["slct_effects"].clear()
        for x in self.lstbx_effects.curselection():
            print(config["effects"][x])
            config["slct_effects"].append(config["effects"][x])
            reverb = pedalboard.Reverb()
            #print(reverb)
            y = self.ffects[config["effects"][x]]()
            for att in dir(y):
               if inspect.ismethod(att) == False:
                j= getattr(y,att)
                for v in config[config["effects"][x]]:
                    if v == att:
                        pb = y.__setattr__(att,1.5)
                        print(pb)     
                        print(y)          
               
        #print(config["slct_effects"])
        self.slct_effects = str(config["slct_effects"])
        self.slct_effects = self.slct_effects.replace(", ", "\n")
        self.slct_effects = self.slct_effects.strip("[]")
        self.lbl_slctd.configure(text = self.slct_effects)
        #print(self.slct_effects)

    def updating(self, name, value):
        config[name] = value
        print(config[name])
        self.master.update_idletasks()

    def get_extract(self):
        if self.out_name.get() != None:
            config["out_name"] = self.out_name.get()

        else:
            config["out_name"] = "untitled"
        print("inside")
        if self.lbl_vid.cget("text") != "":
            print("starting")
            totalframes=iio.improps(self.lbl_vid.cget("text"), plugin="pyav").shape[0]
            metadate = iio.immeta(self.lbl_vid.cget("text"))
            fps = metadate["fps"]
            width = metadate["size"]
            width = width[0]
            print("width{}".format(width))
            print(metadate)
            print(totalframes)
            frames = np.asarray(totalframes)
            print(self.lbl_vid.cget("text"))
            self.Glitch = glitch()
            #multiprocessing.set_start_method('spawn')

            self.Glitch.creating_dir(self.lbl_vid.cget("text"),fps, width, config["slct_effects"])
            count = self.Glitch.extracting(self.lbl_vid.cget("text"))
            return count
    def test(self):
        if self.count_done != True:
            count = self.get_extract()
            self.count_done = True
            self.count = count
        else:
            count = self.count
            #result_args = partial(Glitch.transform, count, frames_dir, sound_dir,vidname)
        result = self.Glitch.transform(10)
        effcts = self.Glitch.add_effects(10)
        revert = self.Glitch.convertBack(10)

    def starting(self):
        if self.count_done != True:
            count = self.get_extract()
            self.count_done = True
            self.count = count
        else:
            count = self.count


        with multiprocessing.Pool(config["slct_cpu"]) as pool:
            #count  = Glitch.chunking(count)
            #frames_dir = chunking(count)
            #sound_dir = chunking(sound_dir)
            #vidname = chunking(vidname)
            
            print("multiprocessing on")
            #result_args = partial(Glitch.transform, count, frames_dir, sound_dir,vidname)
            pool.map(self.Glitch.converts, self.Glitch.transform, count)
            pool.map(self.Glitch.converts, self.Glitch.add_effects, count)
            pool.map(self.Glitch.converts, self.Glitch.convertBack, count)
            pool.close()
        self.Glitch.save()
            #print(result)



if __name__ == "__main__":
    print(config)
    root = tk.Tk()
    config["cpu_count"] = multiprocessing.cpu_count()

    app = UI(root)
    app.mainloop()
    #print("Number of cpu : ", multiprocessing.cpu_count())
    #vid = filedialog.askopenfilename()

        
   

