import muser as ms
import random
import os
import pickle


noteList = [
        'a0', 'a#0', 'b0',
         'c1', 'c#1', 'd1', 'd#1', 'e1', 'f1', 'f#1', 'g1', 'g#1', 'a1', 'a#1', 'b1', 
         'c2', 'c#2', 'd2', 'd#2', 'e2', 'f2', 'f#2', 'g2', 'g#2', 'a2', 'a#2', 'b2', 
         'c3', 'c#3', 'd3', 'd#3', 'e3', 'f3', 'f#3', 'g3', 'g#3', 'a3', 'a#3', 'b3', 
         'c4', 'c#4', 'd4', 'd#4', 'e4', 'f4', 'f#4', 'g4', 'g#4', 'a4', 'a#4', 'b4', 
         'c5', 'c#5', 'd5', 'd#5', 'e5', 'f5', 'f#5', 'g5', 'g#5', 'a5', 'a#5', 'b5', 
         'c6', 'c#6', 'd6', 'd#6', 'e6', 'f6', 'f#6', 'g6', 'g#6', 'a6', 'a#6', 'b6', 
         'c7', 'c#7', 'd7', 'd#7', 'e7', 'f7', 'f#7', 'g7', 'g#7', 'a7', 'a#7', 'b7', 
         'c8'
         ]

noteList4 = [
         'c4', 'c#4', 'd4', 'd#4', 'e4', 'f4', 'f#4', 'g4', 'g#4', 'a4', 'a#4', 'b4'
         ]

noteList3 = [
         'c3', 'c#3', 'd3', 'd#3', 'e3', 'f3', 'f#3', 'g3', 'g#3', 'a3', 'a#3', 'b3'
         ]

noteList2 = [
         'c2', 'c#2', 'd2', 'd#2', 'e2', 'f2', 'f#2', 'g2', 'g#2', 'a2', 'a#2', 'b2' 
         ]


# scales
noteListC = ['c2', 'd2', 'e2', 'f2', 'g2', 'a2', 'b2','c3']
noteListG = [ 'g2', 'a2', 'b2','c2', 'd2', 'e2', 'f#2','g3']



class Music:
    def generateSong():
        output = []
        # noteLength = 2**random.randrange(0,4)
        lastNote = random.randrange(0,len(noteListC))
        def generateLayer(noteList,noteLength):
            layerOut = []
            barLength = 4
            nonlocal lastNote

            # lastNote = random.randrange(0,len(noteList))
            for noteIndex in range(barLength):
                lastNote = ((random.randrange(0,3,2)-1 + lastNote) % len(noteListC))
                # lastNote = random.randrange(0,len(noteListC))
                
                # newNote = random.randrange(-2,2) + lastNote
                # # print("new note: ", newNote)

                # if newNote < 0:
                #     lastNote = 0
                # elif newNote > len(noteList)-1:
                #     lastNote = len(noteList)-1
                # else:
                #     lastNote = newNote

                # print(lastNote)
                note  = noteList[lastNote]

                # Adding notelength
                dot = random.randrange(0,3,2)-1
                # dot = 1
                noteLength = 2**random.randrange(0,5)
                noteTuple = [note, dot*noteLength]

                layerOut.append(noteTuple)
                # layerOut.append((note, 8))
            return layerOut
        
        output.append(generateLayer(noteListC,8))
        output.append(generateLayer(noteListG,16))
        return output
    
    def generateAudio(input,path):
        muser = ms.Muser()
        muser.generate(input,path)
    
    def extend(song1,song2):
        output = [[],[]]
        for outputIndex in range(2):
            output[outputIndex].extend(song1[outputIndex])
            output[outputIndex].extend(song2[outputIndex])
            # output[outputIndex] = tuple(output[outputIndex])
        return output
    
    def mutate(song, notes = (noteListC,noteListG)):
        layerIndex = random.randrange(0,2)
        layerNoteIndex = random.randrange(0,len(song[layerIndex]))
        noteIndex = random.randrange(0,2)
        if noteIndex == 0:
            compare = song[layerIndex][layerNoteIndex][0]
            while song[layerIndex][layerNoteIndex][0] == compare:
                song[layerIndex][layerNoteIndex][0] = notes[layerIndex][random.randrange(0,len(notes[layerIndex]))]
        elif noteIndex == 1:
            compare = song[layerIndex][layerNoteIndex][1]
            while song[layerIndex][layerNoteIndex][1] == compare:
                dot = random.randrange(0,3,2)-1
                song[layerIndex][layerNoteIndex][1] = dot*2**random.randrange(0,4)
        return song

    def singlePointCrossover(song1, song2):
        if len(song1) != len(song2):
            raise ValueError("not same size")
        crossoverPoint = random.randrange(1, len(song1[0]))
        crossedLayer1 = song1[0][0:crossoverPoint] + song2[0][crossoverPoint:]
        crossedLayer2 = song1[1][0:crossoverPoint] + song2[1][crossoverPoint:]
        return [crossedLayer1,crossedLayer2]

            


class Algorithm:
    def __init__(self):
        self.path = os.getcwd()
        self.txtPath = self.path+ "/txt_files/"
        self.wavPath = self.path+ "/wav_files/"
        self.picklePath = self.path+ "/pickle_files/"
        self.generationSize = 5
        # pygame.init()

    def generateRoot(self):
        for songIndex in range(self.generationSize):
            generatedSong = Music.generateSong()
            print(generatedSong)
            self.writeFile(generatedSong,songIndex)
            Music.generateAudio(generatedSong,self.wavPath+ "song_" + str(songIndex) + ".wav")
        
    def readFile(self, songIndex):
        with open(self.picklePath +"song_"+ str(songIndex) +".pkl",'rb') as handle:
            song = pickle.load(handle)
        return song
    
    def writeFile(self,song, songIndex):
        with open(self.picklePath +"song_"+ str(songIndex) +".pkl",'wb') as handle:
            pickle.dump(song,handle)
    
    def fitness(self):
        grades = [0 for i in range(self.generationSize)]
        bestSongGrade = secondbestSongGrade = -1
        bestSongIndex = secondbestSongIndex = -1

        for songIndex in range(self.generationSize):
            grade = input("what do you think of song " + str(songIndex) + "? (0-5): ")
            while (0 > int(grade) or int(grade) > 5):
                grade = input("please enter a number within 0 and 5 \n what do you think of song " + str(songIndex) + "? (0-5): ")
            grade = int(grade)
            grades[songIndex] = grade
            if grade > bestSongGrade:
                secondbestSongGrade = bestSongGrade
                secondbestSongIndex = bestSongIndex
                bestSongGrade = grade
                bestSongIndex = songIndex
            elif grade > secondbestSongGrade:
                secondbestSongGrade = grade
                secondbestSongIndex = songIndex
        return (bestSongIndex,secondbestSongIndex)

    def crossover(self):
        bestSongIndexes = self.fitness()
        for songIndex in range(self.generationSize):
            if songIndex not in bestSongIndexes:
                print("parent 1: ",parentSong1 := self.readFile(bestSongIndexes[random.randrange(0,2)]))
                print("parent 2: ",parentSong2 := self.readFile(songIndex))
                print("child: ",childSong := Music.singlePointCrossover(parentSong1,parentSong2))
                self.writeFile(childSong,songIndex)


    def mutate(self):
        for songIndex in range(self.generationSize):
            print("mutating track: ",songIndex)
            print("input: ", song := self.readFile(songIndex))
            print("output: ", mutatedSong := Music.mutate(song))
            self.writeFile(mutatedSong,songIndex)
    
    def generateAudio(self):
        for songIndex in range(self.generationSize):
            song = self.readFile(songIndex)
            print("generating track:", songIndex)
            Music.generateAudio(song,self.wavPath+ "song_" + str(songIndex) + ".wav")




if __name__ == "__main__":
    generations = 3

    genetics = Algorithm()
    genetics.generateRoot()
    for testIteration in range(generations):
        genetics.crossover()
        genetics.mutate()
        genetics.generateAudio()


