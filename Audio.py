import sys
import sounddevice as sd
import math
import pyautogui
import random
import asyncio
import soundfile as sf
import random
import wave
import array
import threading
import numpy as np

from extensions import fileManager as FM

from extensions import SoundObjects

from extensions import SoundEffects as se

import extensions

#performance is bad and there are alot of audio bugs, rewrite needed

def main():


    #create soundstream

    stream = sd.Stream(44100, 1024, None, 2, dtype='float32')
    stream.start()




    OBJECTS = []
    #OBJECTS.append(SoundObjects())
    #OBJECTS.append(SoundObjects())


    def packetize(object):
        object.getFileFromIO()
        object.separatePackets()
        return()


    threads = []
  

    threads = []
    while True:
        unProcessedPackets = []
        for object in OBJECTS:
            DD = object.getPacketData()
            if str(DD) != "None":
                unProcessedPackets.append(DD)
            else:
                OBJECTS.remove(object)
        ##merge data
        newPacket = []

        
        for i in range(1024): #<< be carefull for off by one errors
            x = 0
            ind = 0 
            l = 0
            r = 0 #<< optimise
            for upp in unProcessedPackets:


                #
                leftEar = se.spacialization(OBJECTS[ind], upp[i][0], True)
                rightEar = se.spacialization(OBJECTS[ind], upp[i][0], False)


                #
                #for now just store angle in the x component of position
                ind += 1


                
                l = l + leftEar
                r = r + rightEar



            newPacket.append([l, r])
        newPacket = np.array(newPacket, dtype='float32')

            
        

        ## spacialization

        #creates new object
        if len(OBJECTS) <= 3: #<< probly gonna cause issues
            checksum = 8
            if checksum == 8:
                OBJECTS.append(SoundObjects())
                for object in OBJECTS:
                    object.position = [random.randint(-15, 15), random.randint(-15, 15), random.randint(-4, 4)]
                    object.volume = 1
                    object.file = extensions.pickPath()
                    packetize(object)


            





        #threads
        #create sound object event
            #i only need to thread packetization
        


        #pull data


        #merge data
        

        #play sound
        
        stream.write(newPacket) ## not sure

        sd.wait()
        #sd.wait() ## might have to wait handle manually

        



        for object in OBJECTS:
            object.packetIndex += 1
        #print('packet', str(newPacket[1]))


if __name__ == "__main__":
    main()



