import soundfile as sf
import matplotlib.pyplot as plt
from statistics import mean 
import numpy as np
import math

if __name__ == "__main__":
    data, samplerate = sf.read("sigfox1.wav")
    print(f"Sample rate: {samplerate} Hz")
    print(f"Data shape: {data.shape}")
    print(f"Length data: {len(data)}")
    print(f"Sample data[0]: {data[0]}")
    # Déclaration de variables
    activ = 0
    dataInter = []
    bits = []
    tabZeroQuatre = []
    norm = int(samplerate/1000000)
    print("Déclaration des variables passée")

    # Copie du contenu de data dans dataInter
    for i in range(len(data)):
        dataInter.append(data[i, 0])
    print("Copie de data passée")

    # Simplification des trames (3 valeurs possibles : [1,0,-1])
    maxDataP2 = max(dataInter)/7
    minDataP2 = min(dataInter)/7
    nvData = []
    for e in dataInter:
        if e > maxDataP2:
            nvData.append(int(1))
        elif e < minDataP2:
            nvData.append(int(-1))
        else:
            nvData.append(int(0))
    print("Simplification des trames passée")
    # plt.plot(nvData)
    # plt.show()

    # Récupération des 3 trames
    Trames = [[], [], []]
    activ = 0
    # debutIndex = 2500000 # sigfox3.wav
    debutIndex = 0 # si pas de bruit en début de trame
    debut = [0, 0, 0]
    fin = [0, 0, 0]
    for k in range(3):
        activ = 0
        for i in range(debutIndex, len(nvData)):
            if activ:
                Trames[k].append(nvData[i])
            elif nvData[i] != 0:
                activ = 1
                Trames[k].append(nvData[i])
                debutIndex = i
                debut[k] = i
        for i in range(0, len(Trames[k]), (norm * 10000)):
            if max(Trames[k][i:i + norm * 10000]) == 0:
                Trames[k] = Trames[k][:i - (norm * 10000)]
                fin[k] = i-(norm * 10000) + debutIndex
                debutIndex += i + norm * 10000
                break
    # plt.plot(Trames[0])
    # plt.show()

    # Repérage des zones de zéros dans les trames
    for i in range(norm * 11000, len(Trames[0])):
        # verifier tous les 20000 points si on passe par 0
        if i % (norm * 10000) == 0:
            tabZeroQuatre.append(Trames[0][i-(norm * 3000):i+(norm * 3000)].count(0.0))
    print("Repérage des zones de zéros passé : ")

    # Traduction en bits
    maxZeroMid = max(tabZeroQuatre)/2
    print("maxZeroMid: ", maxZeroMid)
    for i in range(len(tabZeroQuatre)):
        if tabZeroQuatre[i] > maxZeroMid:
            bits.append("0")
        else:
            bits.append("1")
    print("Traduction en bits passée")

    # Rétrécissement
    while len(bits) > 208:
        bits.pop()

    # Affichage
    print("Trame 1        : ", ''.join(bits))
    print("Trame 1 (hexa) : ", hex(int(''.join(bits), 2)))
    print("Taille Trame 1 : ", len(bits), "bits, soit", len(bits)/8, "octets")
    # delimitation du message
    message = bits[80: 176]
    print("Message        : ", hex(int(''.join(message), 2)))
    # sigfox1 : AABBCCDDEEFF112233445501
    # sigfox2 : AABBCCDDEEFF11223344????
    # sigfox3 : AABBCCDDEEFF112233446964
