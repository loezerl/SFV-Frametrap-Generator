########################
import json
import re
from os import system
from pprint import pprint
from html import *

FrameTraps = {} #3F gap
FrameTrapsNova = {} #3F gap
FrameTraps4 = {} #4f gap
FrameTraps5 = {} #5f gap
Personagens = []
#{"Akuma": {"LP": "FT 1", "FT 2", "FT 3"},
#          {"MP": "FT 2", "FT 3", FT}           
# }

def isInt(x):
    if x == None:
        return False
    try:
        int(x)
        return True
    except ValueError:
        return False

def CarregaDadosFramedata():
    with open('characterData.json') as data_file:
            data = json.load(data_file)
    for per in data:
        Personagens.append(per)
    Teste2 = []

    PeM = {}
    for Boneco in Personagens:
        Teste2.clear()
        for move in data[Boneco]["moves"]["normal"]:
            Teste2.append(move)
        PeM[Boneco] = list(Teste2)

    FT4F = []
    FT5F = []
    Lights = []
    Medium = []
    Others = []
    List = []
    LightsRgx = re.compile("LP|LK")
    MediumRgx = re.compile("MP|MK")
    NoClawRgx = re.compile("[\w\s]+(claw)")
    Invalid = False

    for Boneco in Personagens:
        Teste2.clear()
        Lights.clear()
        Medium.clear()
        Others.clear()
        List.clear()
        #FT4F.clear()
        #FT5F.clear()
        for move in PeM[Boneco]:
            if ((isInt(data[Boneco]["moves"]["normal"][move]["onBlock"]) and isInt(data[Boneco]["moves"]["normal"][move]["startup"])) and (isInt(data[Boneco]["moves"]["normal"][move]["recovery"]))):
                if (int(data[Boneco]["moves"]["normal"][move]["onBlock"] > 0)):
                    onblock = int(data[Boneco]["moves"]["normal"][move]["onBlock"]) + 3 #3 é o gap de frames
                    #onblock4 = int(data[Boneco]["moves"]["normal"][move]["onBlock"]) + 4 #4 é o gap de frames
                    #onblock5 = int(data[Boneco]["moves"]["normal"][move]["onBlock"]) + 5 #5 é o gap de frames
                    for move2 in PeM[Boneco]:
                        Invalid = False
                        if ((isInt(data[Boneco]["moves"]["normal"][move2]["startup"]) and isInt(data[Boneco]["moves"]["normal"][move2]["onBlock"]) and isInt(data[Boneco]["moves"]["normal"][move2]["recovery"])) and int(data[Boneco]["moves"]["normal"][move2]["onBlock"]) >= -2):
                            startup = int(data[Boneco]["moves"]["normal"][move2]["startup"])
                            if ((re.search(MediumRgx, move2) and (onblock >= startup)) or (not re.search(MediumRgx, move2) and (onblock > startup))):
                            #if onblock >= startup:
                                if (Boneco == "Vega"):
                                    if(re.search(NoClawRgx, move) and re.search(NoClawRgx, move2)):
                                        Invalid = True
                                    elif(not re.search(NoClawRgx, move) and not re.search(NoClawRgx, move2)):
                                        Invalid = True
                                else:
                                    Invalid = True
                                if (Invalid):
                                    if (re.search(LightsRgx,move)):
                                        Lights.append((move, move2))
                                    elif (re.search(MediumRgx, move)):
                                        Medium.append((move, move2))
                                    else:
                                        Others.append((move, move2))
                                    Teste2.append((move, move2))
        FrameTraps[Boneco] = list(Teste2)
        List.append(list(Lights))
        List.append(list(Medium))
        List.append(list(Others))
        FrameTrapsNova[Boneco] = list(List)

CarregaDadosFramedata()

def GenerateHTMLFiles():
    for Boneco in Personagens:
        message = ""
        file = open("%s.html" % Boneco, 'w')
        message = message + header1 + Boneco1 + Boneco + Boneco2 + header2
        for LM in FrameTrapsNova[Boneco][0]:
            message = message + linha1 + str(LM[0]) + " > " + str(LM[1]) + linha2
        message = message + bottom
        file.write(message)
        file.close()

GenerateHTMLFiles()