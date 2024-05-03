import soundfile as sf
import matplotlib.pyplot as plt
from statistics import mean 
import numpy as np
import math

class SigfoxFrame:

    def __init__(self, ul_pr=None, ft=None, ul_phy_content=None, ul_container=None,
                 ul_crc=None, ul_auth=None, ul_payload=None, id=None, mc=None, rep=None,
                 bf=None, li=None, ul_message_content=None):

        self.ul_pr = ul_pr # 19 bits
        self.ft = ft # 13 bits
        self.ul_phy_content = ul_phy_content # 22 octets
        self.ul_container = ul_container # 20 octets
        self.ul_crc = ul_crc # 16 bits
        self.ul_auth = ul_auth # 2 octets
        self.ul_payload = ul_payload # 12 octets = message
        self.id = id # 32 bits
        self.mc = mc # 12 bits
        self.rep = rep # 1 bit
        self.bf = bf # 1 bit
        self.li = li # 2 bits
        self.ul_message_content = ul_message_content # 12 octets


if __name__ == "__main__":
    data, samplerate = sf.read("signal_sigfox.wav")
    print(f"Sample rate: {samplerate} Hz")
    print(f"Data shape: {data.shape}")
    print(f"Length data: {len(data)}")
    print(f"Sample data[0]: {data[0]}")

    # Déclaration de variables
    signal = []
    TrameUn = []
    activ = 0
    dataInter = []
    bits = []
    tabZeroQuatre = []
    print("Déclaration des variables passée")

    # Copie du contenu de data dans dataInter
    for i in range(len(data)): dataInter.append(data[i,0])
    print("Copie de data passée")
    
    # Simplification des trames (3 valeurs possibles : [1,0,-1])
    maxDataP2 = max(dataInter)/5
    minDataP2 = min(dataInter)/5
    nvData = []
    for e in dataInter:
        if (e > maxDataP2):
            nvData.append(int(1))
        elif (e < minDataP2):
            nvData.append(int(-1))
        else:
            nvData.append(int(0))
    print("Simplification des trames passée")

    # Récupération des 3 trames
    Trames = [[],[],[]]
    activ = 0
    debutIndex = 0
    debut = [0,0,0]
    fin = [0,0,0]
    for k in range(3):
        activ = 0
        for i in range(debutIndex,len(nvData)):
            if (activ):
                Trames[k].append(nvData[i])
            elif (nvData[i] != 0):
                activ = 1
                Trames[k].append(nvData[i])
                debutIndex = i
                debut[k] = i
        for i in range(0,len(Trames[k]),10000):
            if (max(Trames[k][i:i+10000]) == 0):
                Trames[k] = Trames[k][:i-10000]
                fin[k] = i-10000 + debutIndex
                debutIndex += i + 10000
                break
    print("Récupération des trames respectives passée")

    # Repérage des zones de zéros dans les trames
    for i in range(10000,len(Trames[0])):
        if (i%10000 == 0):
            tabZeroQuatre.append(Trames[0][i-1000:i+1000].count(0.0))
    print("Repérage des zones de zéros passé")

    # Traduction en bits
    maxZeroMid = max(tabZeroQuatre)/2
    for i in range(len(tabZeroQuatre)):
        if (tabZeroQuatre[i] > maxZeroMid):
            bits.append("1")
        else:
            bits.append("0")
    print("Traduction en bits passée")

    # Rétrécissement
    while (len(bits) > 208): bits.pop() 

    #cptq = 3
    #tabHex = []
    #somme = 0
    #for i in range(0,len(tabZeroQuatre),4):
    #    if (len(tabZeroQuatre)-i < 4): break
    #    somme = int(tabZeroQuatre[i])*pow(2,3) + int(tabZeroQuatre[i+1])*pow(2,2) + int(tabZeroQuatre[i+2])*pow(2,1) + int(tabZeroQuatre[i+3])*pow(2,0)
    #    tabHex.append(somme)

    # Affichage
    print(bits)
    print(hex(int(''.join(bits), 2)))
    print(''.join(bits))
    print(len(bits))
