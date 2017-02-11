import sys
import io
#import numpy as np

def neighborhood(iterable):
    iterator = iter(iterable)
    prev_item = None
    current_item = next(iterator)  # throws StopIteration if empty.
    for next_item in iterator:
        yield (prev_item, current_item, next_item)
        prev_item = current_item
        current_item = next_item
    yield (prev_item, current_item, None)

#This function is python2 only.
def shift_jis2unicode(charcode): # charcode is an integer
    if charcode <= 0xFF:
        string = chr(charcode)
    else:
        string = chr(charcode >> 8) + chr(charcode & 0xFF)

    try:
        val = ord(string.decode('shift-jis'))
    except:
        val = 32
    return val


"""
Example of character line in LR2Font
#R,36,0,126,0,49,130,
1st slot: character, texture, etc. #R is character
2nd slot: ASCII table position (in this case, the character '$')
3rd slot: The image it's being loaded from.
4th slot: starting position on the x axis
5th slot: starting position on the y axis
6th slot: Width
7th slot: Height

Note: LR2 fonts have no concept of line numbers or line height.
"""

class fontChr:
    """Class for managing a LR2 font character"""
        
    lineNumber = None
    characterValue = None
    texturePage = None
    xPosition = None
    yPosition = None
    width = None
    height = None
    '''IIDX fonts actually all use the same height per page,
    so it only needs to be read once. SM fonts only support one
    height per page anyway.'''
    
    def __init__(self, char, tex, xPos, yPos, tWidth, tHeight):
        self.characterValue = int(char)
        self.texturePage = int(tex)
        self.xPosition = int(xPos)
        self.yPosition = int(yPos)
        self.width = int(tWidth)
        self.height = int(tHeight)
        

file = io.open(sys.argv[1], "rt", encoding="shift_jis_2004")
textures = []
characters = []
for line in file:
    lineArray = line.split(",")
    if lineArray[0] == "#T":
        textures.append(lineArray[2].rstrip())
    elif lineArray[0] == "#R":
                    #char, texture page, xPos, yPos, Width, Height
        x = fontChr(lineArray[1], lineArray[2], lineArray[3], lineArray[4], lineArray[5], lineArray[6])
        characters.append(x)
'''for textureFileName in textures:
    print(textureFileName)'''



print("[common]")
print("Baseline=" + str(characters[0].height))
print("Top=0")
print("LineSpacing=" + str(characters[0].height))
print("DrawExtraPixelsLeft=0")
print("DrawExtraPixelsRight=0")
print("AdvanceExtraPixels=0")


linestr = "Line " + str(line) + "="
#lineYPosition = 0
#linestr = None
charactersInPage = 0
for prev,curr,next in neighborhood(characters):
    if prev != None and curr.texturePage == prev.texturePage:
        
        #Ignore ASCII characters below 32
        if curr.characterValue > 32:
            linestr+= unichr(curr.characterValue)
            charactersInPage = charactersInPage+1
        if curr.yPosition != next.yPosition:
            print(linestr)
            line = line+1
            #lineYPosition = character.yPosition
            linestr = "Line " + str(line) + "="
    else:
        print("\n\n[page " + str(curr.texturePage)+"]")
        line=0
        
            
#print(str(charactersInPage))