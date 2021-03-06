########################
import json
import re
from os import system
from pprint import pprint
from html import *
from collections import OrderedDict
PeM = {}
PeMVT = {}
FrameTraps = {} #3F gap
FrameTrapsVT = {}
FrameTraps4 = {} #4f gap
FrameTraps5 = {} #5f gap
AllChars = []
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
        AllChars.append(per)
    AuxList = []

    for Char in AllChars:
        AuxList.clear()
        for move in data[Char]["moves"]["normal"]:
            AuxList.append(move)
        PeM[Char] = list(AuxList) #Char and Normal Moves
    
    for Char in AllChars:
        AuxList.clear()
        for move in data[Char]["moves"]["vtrigger"]:
            AuxList.append(move)
        if len(AuxList) > 0:
            PeMVT[Char] = list(AuxList)

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

    for Char in AllChars:
        AuxList.clear()
        Lights.clear()
        Medium.clear()
        Others.clear()
        List.clear()
        #FT4F.clear()
        #FT5F.clear()
        for move in PeM[Char]:
            if ((isInt(data[Char]["moves"]["normal"][move]["onBlock"]) and isInt(data[Char]["moves"]["normal"][move]["startup"])) and (isInt(data[Char]["moves"]["normal"][move]["recovery"]))):
                if (int(data[Char]["moves"]["normal"][move]["onBlock"] > 0)):
                    onblock = int(data[Char]["moves"]["normal"][move]["onBlock"]) + 3 #3 com o gap de frames
                    #onblock4 = int(data[Char]["moves"]["normal"][move]["onBlock"]) + 4 #4 com o gap de frames
                    #onblock5 = int(data[Char]["moves"]["normal"][move]["onBlock"]) + 5 #5 com o gap de frames
                    for move2 in PeM[Char]:
                        Invalid = False
                        if ((isInt(data[Char]["moves"]["normal"][move2]["startup"]) and isInt(data[Char]["moves"]["normal"][move2]["onBlock"]) and isInt(data[Char]["moves"]["normal"][move2]["recovery"])) and int(data[Char]["moves"]["normal"][move2]["onBlock"]) >= -2):
                            startup = int(data[Char]["moves"]["normal"][move2]["startup"])
                            if ((re.search(MediumRgx, move2) and (onblock >= startup)) or (not re.search(MediumRgx, move2) and (onblock > startup))):
                            #if onblock >= startup:
                                if (Char == "Vega"):
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
                                    AuxList.append((move, move2))
        List.append(list(Lights))
        List.append(list(Medium))
        List.append(list(Others))
        FrameTraps[Char] = list(List)

        AuxList.clear()
        Lights.clear()
        Medium.clear()
        Others.clear()
        List.clear()
        if Char in PeMVT:
            for move in PeMVT[Char]:
                if ((isInt(data[Char]["moves"]["vtrigger"][move]["onBlock"]) and isInt(data[Char]["moves"]["vtrigger"][move]["startup"])) and (isInt(data[Char]["moves"]["vtrigger"][move]["recovery"]))):
                    if (int(data[Char]["moves"]["vtrigger"][move]["onBlock"] > 0)):
                        onblock = int(data[Char]["moves"]["vtrigger"][move]["onBlock"]) + 3 #3 com o gap de frames
                        for move2 in PeMVT[Char]:
                            Invalid = False
                            if ((isInt(data[Char]["moves"]["vtrigger"][move2]["startup"]) and isInt(data[Char]["moves"]["vtrigger"][move2]["onBlock"]) and isInt(data[Char]["moves"]["vtrigger"][move2]["recovery"])) and int(data[Char]["moves"]["vtrigger"][move2]["onBlock"]) >= -2):
                                startup = int(data[Char]["moves"]["vtrigger"][move2]["startup"])
                                if ((re.search(MediumRgx, move2) and (onblock >= startup)) or (not re.search(MediumRgx, move2) and (onblock > startup))):
                                #if onblock >= startup:
                                    if (Char == "Vega"):
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
                                        AuxList.append((move, move2))
            if (len(Lights) > 0):
                List.append(list(Lights))
            if (len(Medium) > 0):
                List.append(list(Medium))
            if (len(Others) > 0):
                List.append(list(Others))
            if len(List) > 0:
                FrameTrapsVT[Char] = list(List)

CarregaDadosFramedata()

def GenerateHTMLFiles():
    with open('characterData.json') as data_file:
            data = json.load(data_file, object_pairs_hook = OrderedDict)
    for Char in AllChars:
        message = ""
        file = open("%s.html" % Char.upper(), 'w')
        #Colocar a framedata aqui tambem.
        message = message + header1 + Boneco1 + Char.upper() + Boneco2 + "<br>Health\t- " + data[Char]["stats"]["health"] + "<br>Stun\t- "+ data[Char]["stats"]["stun"] + "<br>" + header2
        message = message + tabelaFD
        for move in data[Char]["moves"]["normal"]:
            message = message + linhafd0 + linhafd + move + linhafd2
            message = message + linhafd + str(data[Char]["moves"]["normal"][move]["plainCommand"]) + linhafd2 
            message = message + linhafd + str(data[Char]["moves"]["normal"][move]["startup"]) + linhafd2
            message = message + linhafd + str(data[Char]["moves"]["normal"][move]["active"]) + linhafd2
            message = message + linhafd + str(data[Char]["moves"]["normal"][move]["recovery"])+ linhafd2
            message = message + linhafd + str(data[Char]["moves"]["normal"][move]["onHit"]) + linhafd2
            message = message + linhafd + str(data[Char]["moves"]["normal"][move]["onBlock"]) + linhafd2
            if "extraInfo" in data[Char]["moves"]["normal"][move]:
                message = message + linhafd + str(data[Char]["moves"]["normal"][move]["extraInfo"]) + linhafd2
            else:
                message = message + linhafd + " " + linhafd2
            message = message + linhafd3
        if "vtrigger" in data[Char]["moves"]:
            message = message + linhavt
            for move in data[Char]["moves"]["vtrigger"]:
                message = message + linhafd0 + linhafd + move + linhafd2
                message = message + linhafd + str(data[Char]["moves"]["vtrigger"][move]["plainCommand"]) + linhafd2 
                message = message + linhafd + str(data[Char]["moves"]["vtrigger"][move]["startup"]) + linhafd2
                message = message + linhafd + str(data[Char]["moves"]["vtrigger"][move]["active"]) + linhafd2
                message = message + linhafd + str(data[Char]["moves"]["vtrigger"][move]["recovery"])+ linhafd2
                message = message + linhafd + str(data[Char]["moves"]["vtrigger"][move]["onHit"]) + linhafd2
                message = message + linhafd + str(data[Char]["moves"]["vtrigger"][move]["onBlock"]) + linhafd2
                if "extraInfo" in data[Char]["moves"]["vtrigger"][move]:
                    message = message + linhafd + str(data[Char]["moves"]["vtrigger"][move]["extraInfo"]) + linhafd2
                else:
                    message = message + linhafd + " " + linhafd2
                message = message + linhafd3
        message = message + endtable
        message = message + Titulo2 + tabelaFT
        for i in range(len(FrameTraps[Char])):
            for LM in FrameTraps[Char][i]:
                message = message + linha1 + str(LM[0]) + " > " + str(LM[1]) + linha2
        if (Char in FrameTrapsVT) and len(FrameTrapsVT[Char]) > 0:
            message = message + linhavt
            for i in range(len(FrameTrapsVT[Char])):
                for LM in FrameTrapsVT[Char][i]:
                    message = message + linha1 + str(LM[0]) + " > " + str(LM[1]) + linha2
  
        message = message + endtable + bottom
        file.write(message)
        file.close()

GenerateHTMLFiles()