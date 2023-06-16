import muser as ms
import random
import os

path = os.getcwd()

# noteList = [
#         'a0', 'a#0', 'b0',
#          'c1', 'c#1', 'd1', 'd#1', 'e1', 'f1', 'f#1', 'g1', 'g#1', 'a1', 'a#1', 'b1', 
#          'c2', 'c#2', 'd2', 'd#2', 'e2', 'f2', 'f#2', 'g2', 'g#2', 'a2', 'a#2', 'b2', 
#          'c3', 'c#3', 'd3', 'd#3', 'e3', 'f3', 'f#3', 'g3', 'g#3', 'a3', 'a#3', 'b3', 
#          'c4', 'c#4', 'd4', 'd#4', 'e4', 'f4', 'f#4', 'g4', 'g#4', 'a4', 'a#4', 'b4', 
#          'c5', 'c#5', 'd5', 'd#5', 'e5', 'f5', 'f#5', 'g5', 'g#5', 'a5', 'a#5', 'b5', 
#          'c6', 'c#6', 'd6', 'd#6', 'e6', 'f6', 'f#6', 'g6', 'g#6', 'a6', 'a#6', 'b6', 
#          'c7', 'c#7', 'd7', 'd#7', 'e7', 'f7', 'f#7', 'g7', 'g#7', 'a7', 'a#7', 'b7', 
#          'c8'
#          ]

noteList4 = [
         'c4', 'c#4', 'd4', 'd#4', 'e4', 'f4', 'f#4', 'g4', 'g#4', 'a4', 'a#4', 'b4'
         ]

noteList2 = [
         'c2', 'c#2', 'd2', 'd#2', 'e2', 'f2', 'f#2', 'g2', 'g#2', 'a2', 'a#2', 'b2' 
         ]

noteLength = 8
MAXOCTAVE = 4
layers = 2
output = []

# lastNote = random.randrange(0,len(noteList)-1)
# lastOctave = random.randrange(1,MAXOCTAVE)
# lastNote = random.randrange(1,88)

# for layerIndex in range(layers):
#     for noteI in range(noteLength):
#         # lastNote = ((random.randrange(-1,1) + lastNote) % len(noteList))
#         newNote = random.randrange(-2,4,2) + lastNote
#         print("new note: ", newNote)
#         if newNote < 0:
#             lastNote = 0
#         elif newNote > len(noteList)-1:
#             lastNote = len(noteList)-1
#         else:
#             lastNote = newNote
#         print(lastNote)
#         note  = noteList[lastNote]
#         # lastOctave = ((random.randrange(-1,1) + lastNote) % MAXOCTAVE)
#         # note = note + str(lastOctave)
#         # print(note)

#         # Adding notelength
#         layerOut.append((note, 2**random.randrange(2,5)))
#         # layerOut = tuple(layerOut)
#     output.append(tuple(layerOut))
# output = tuple(output)
# print(output)


def generateLayer(noteList):
    layerOut = []
    lastNote = random.randrange(0,len(noteList)-1)
    for noteI in range(noteLength):
        # lastNote = ((random.randrange(-2,2,4) + lastNote) % len(noteList))
        newNote = random.randrange(-2,2) + lastNote
        print("new note: ", newNote)

        if newNote < 0:
            lastNote = 0
        elif newNote > len(noteList)-1:
            lastNote = len(noteList)-1
        else:
            lastNote = newNote

        print(lastNote)
        note  = noteList[lastNote]
        # lastOctave = ((random.randrange(-1,1) + lastNote) % MAXOCTAVE)
        # note = note + str(lastOctave)
        # print(note)

        # Adding notelength
        dot = random.randrange(0,3,2)-1
        layerOut.append((note, dot*2**random.randrange(0,4)))
        # layerOut.append((note, 8))
    return tuple(layerOut)

if __name__ == "__main__":

    print("layer 1")
    output.append(generateLayer(noteList4))
    print("layer 2")
    output.append(generateLayer(noteList2))
    print(output)
    file = open(path+"/txt_files/gen1.txt",'w')
    file.write(str(output))
    file.close()
    muser = ms.Muser()

    # output = ((('c4', -16), ('c#4', -16), ('c4', -16), ('c4', -16),('c4', -16), ('c#4', -16), ('c4', -16), ('c4', -16)), (('f#2', -1), ('f2', -1), ('f2', -1), ('e2', -1), ('f#2', -1), ('f2', -1), ('f2', -1), ('e2', -1)))

    muser.generate(output, 'song.wav')
    
    print(path + "/txt_files")


# song3 = (
#   ('bb', 8),
#   ('g5*', 2), ('f5', 8), ('g5', 8), ('f5', -4), ('eb5', 4), ('bb', 8),
#   ('g5*', 4), ('c5', 8), ('c6', 4), ('g5', 8), ('bb5', -4), ('ab5', 4), ('g5', 8),
#   ('f5*', -4), ('g5', 4), ('d5', 8), ('eb5', -4), ('c5', -4),
#   ('bb*', 8), ('d6', 8), ('c6', 8), ('bb5', 16), ('ab5', 16), ('g5', 16), ('ab5', 16), ('c5', 16), ('d5', 16), ('eb5', -4),
# )

# import tomita.legacy.pysynth as ps
# ps.make_wav (
#     song3,
#     bpm = 100,
#     transpose = 0,
#     pause = 0.1,
#     boost = 1.15,
#     repeat = 1,
#     fn = "test.wav"
# )