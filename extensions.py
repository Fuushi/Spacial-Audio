class fileManager(object):
    import wave
    import array

    def make_stereo(file1, output):
        import wave
        import array
        ifile = wave.open(file1)
        # (1, 2, 44100, 2013900, 'NONE', 'not compressed')
        (nchannels, sampwidth, framerate, nframes, comptype, compname) = ifile.getparams()
        assert comptype == 'NONE'  # Compressed not supported yet
        array_type = {1:'B', 2: 'h', 4: 'l'}[sampwidth]
        left_channel = array.array(array_type, ifile.readframes(nframes))[::nchannels]
        ifile.close()

        stereo = 2 * left_channel
        stereo[0::2] = stereo[1::2] = left_channel

        ofile = wave.open(output, 'w')
        ofile.setparams((2, sampwidth, framerate, nframes, comptype, compname))
        ofile.writeframes(stereo.tostring())
        ofile.close()

class SoundObjects():
    #sound objects handles sound objects, not playback
    def __init__(self):
        import random
        self.id = random.randint(0, 10000)
        self.position = [0, 0, 0]
        self.volume = 1
        self.file = None
        self.packetSize = 1024
        self.fq = 44100
        self.packetIndex = 0 #use for packet iteration
        self.data = [] ## <<stores packetized Data
        self.packetOutputData = []
        self.stream = None #<< use to input a stream if needed, though playback should be iterated in main



    def separatePackets(self): ## threaded in main
        import numpy as np
        PacketsLeft = True
        cache = self.data
        newCache = []
        while PacketsLeft:
            if len(cache) >= 1024:
                data = cache[0:1024] #<< 24?
                #print(len(data))
                cache = cache[1025:len(cache)]
                newCache.append(data)
                if len(cache) == 0:
                    x = 0 / 0
            else:
                PacketsLeft = False

        #ret
        self.data = np.array(newCache, dtype='float64') #dtype check
        return()

    def getPacketData(self):
        try:
            self.packetOutputData = self.data[self.packetIndex] #optimise to use less data shuffling
        except Exception as error:
            return(None)
        return(self.data[self.packetIndex])

    def getFileFromIO(self):
        #import soundfile as sf
        #self.data = sf.open()

        import soundfile as sf
        self.data, self.fq = sf.read(self.file)


    def snooper(self):
        print("ID: " + str(self.id))
        print(self.position)
        print(self.volume)
        print(self.file)
        print(self.packetSize)
        print(self.fq)
        print(self.packetIndex)

class SoundEffects():
    def spacialization(object, data, ear): #ear is boolean
        if ear == True: #True ear is left
            #print(object.position)
            #find moment arm
            #change the 0.5 to change hear difference
            distance = (((-1 - object.position[0]) ** 2) + (object.position[1] ** 2) + (object.position[2] ** 2)) ** 0.5
            sound = (data * ((5 / distance) ** 2)) * object.volume
            return(sound)
            pass
        else:#right ear
            distance = (((1 - object.position[0]) ** 2) + (object.position[1] ** 2) + (object.position[2] ** 2)) ** 0.5
            sound = (data * ((5 / distance) ** 2)) * object.volume
            return(sound)

def pickPath():
    import os
    import sys
    import pathlib
    import random

    path1 = pathlib.Path().absolute()
    path2 = os.path.join(path1, 'sounds')
    files2 = []
    for root, dirs, files in os.walk(path2):
        for file in files:
            files2.append(file)
    pathed_files = []
    for file in files2:
        if '.wav' in str(file):
            file3 = os.path.join(path2, file)
            pathed_files.append(file3)
    intt = random.randint(0, (len(pathed_files) - 1))
    print(pathed_files[intt])
    return(pathed_files[intt])






