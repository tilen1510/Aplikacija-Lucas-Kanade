import numpy as np
from scipy.interpolate import RectBivariateSpline
import os
import time



def izberiDatoteko(datoteka):
    root_ext = os.path.splitext(datoteka)   #razdeli ime datoteke na koren in končnico
    koren = root_ext[0]
    koncnica = root_ext[1]
    shape, FPS = videoPodatki(datoteka)  #pri pretvorbi videa potrebujemo podati obliko videa, ki jo lahko preberemo iz .cih datoteke
    mraw = koren + '.mraw'  #pripravimo si .mraw datoteko za pretvorbo

    if koncnica != ".cih":
        print("datoteka mora imeti končnico '.cih'!")
    else:
        video = np.memmap(mraw, dtype=np.uint16, mode='r', shape=(shape)) #z numpy.memmap pretvorimo zapis slike v matrični zapis (array-like), posebnost funkcije memmap je ta, da omogoča obdelavo datoteke na disku in ne v pomnilniku.
        print(video.shape)
        return video, FPS, shape


def izracunPomikov(video, tocka, ROI=(15, 15), stopnjaInterp=3, maxiter=25, tol=10e-8, pad = 2, piksli=1., dolzina=1., progressBar=None, messageBox=None):
    f = video[0].copy().astype(float)   #za začetek potrebujemo le prvo (referenčno) sliko
    x, y = np.array(tocka).astype(int)  #določimo koordinati točke
    w, h = np.array(ROI).astype(int)    #določimo širino in višino območja, ki nas zanima
    xslice = slice(x - w // 2 - pad, x + w // 2 + 1 + pad)  #pripravimo si izrez slike okoli točke
    yslice = slice(y - h // 2 - pad, y + h // 2 + 1 + pad)
    ROI = ROI_lihost(ROI)   #v funkciji RectBivariateSpline morata biti x in y vrednost taki, da bosta po velikosti ustrezali tudi paramteru z, zato morata biti obe vrednosti ROI lihi števili.
    N = video.shape[0]      #vrne število sličic

    spline = RectBivariateSpline(   #interpoliramo referenčno sliko, da dobimo tudi vrednosti med piksli
        x=np.arange(-pad, ROI[1] + pad),
        y=np.arange(-pad, ROI[0] + pad),
        z=f[yslice, xslice],
        kx=stopnjaInterp,           #izberemo stopnjo interpolacije
        ky=stopnjaInterp,
        s=0)                        #"Positive smoothing factor" - za interpolacijo je s = 0

    pomiki = np.zeros((N,2)) #pripravimo matriko, v katero bomo zapisovali vrednosti pomikov

    start_time = time.time()
    napake = False

    for i in range(1, N):
        cas = ((time.time() - start_time) / (i + 0.0001)) * (N - (i))
        time_m = cas // 60
        time_s = cas % 60
        print(f'{i}/{N}, {time_m:.0f} min, {time_s:.1f} s')
        # print(f'{int(i/N*100)} %')

        if messageBox != None:
            messageBox.setText(f'Izračunano bo v {time_m:.0f} min, {time_s:.1f} s')
        else:
            pass

        if progressBar != None:
            progressBar.setValue(int((i+1)/N*100))
        else:
            pass

        zac_pomik = np.round(pomiki[i - 1, :]).astype(int)     #prepiše zadnjo celo vrednost
        x_i = x + zac_pomik[0]
        y_i = y + zac_pomik[1]

        xslice = slice(x_i - w // 2, x_i + w // 2 + 1)  #izreže ROI
        yslice = slice(y_i - h // 2, y_i + h // 2 + 1)
        G_0 = video[i].copy().astype(float) #izbere i-to sliko
        G = G_0[yslice,xslice] #iz i-te slike izreže ROI

        pomik, napaka = LukasKanade(   #izračun pomika za i-to sliko
            G=G,
            F_spline=spline,
            maxiter=maxiter,
            tol=tol,
            ROI=ROI)

        pomiki[i, :] = pomik + zac_pomik #izračunanemu pomiku pripiše začetno celo vrednost in se zapiše v skupni matriki pomikov
        if napaka == True:
            napake = True
        else:
            pass

    merilo = kalibracija(piksli, dolzina)   #enačba za upoštevanje merila
    pomiki = pomiki * merilo
    cas = time.time() - start_time
    time_m = cas // 60
    time_s = cas % 60
    print(f'Izračunano v {time_m:.0f} min in {time_s:.1f} s')

    if napaka == True:
        print(f'Izračun ni bil možen. Spremeni parametre!')

    if messageBox != None:
        cas = time.time() - start_time
        time_m = cas // 60
        time_s = cas % 60
        messageBox.setText(f'Izračunano v {time_m:.0f} min in {time_s:.1f} s')
    else:
        pass

    return pomiki, napake

def LukasKanade(G, F_spline, maxiter, tol, ROI):
    napaka = False
    Gy, Gx = np.gradient(G.astype(np.float64), edge_order=2)
    Gx2 = np.sum(Gx ** 2)
    Gy2 = np.sum(Gy ** 2)
    GxGy = np.sum(Gx * Gy)

    A_inv = np.linalg.inv(              
        np.array([[Gx2, GxGy],
                  [GxGy, Gy2]]))

    pomik = np.zeros((2), dtype=np.float64)
    for i in range(maxiter):            #optimizacijska zanka po Sutton, Orteu, Schrier: Image Correlation for Shape, Motion and Deformation Measurments
        x_f = np.arange(ROI[0], dtype=np.float64) - pomik[0] #v vsaki iteraciji poravna na podlagi prejšnega izračuna
        y_f = np.arange(ROI[1], dtype=np.float64) - pomik[1]
        F = F_spline(y_f, x_f)

        F_G = F-G

        b = np.array([np.sum(Gx * F_G), 
                      np.sum(Gy * F_G)])

        delta = np.dot(A_inv, b)

        error = np.linalg.norm(delta)
        pomik += delta
        if error < tol:
            return pomik, napaka
        if error > tol and i == maxiter-1:
            pomik = np.zeros((2), dtype=np.float64)
            print("NAPAKA!!!")
            napaka = True
            return pomik, napaka

def videoPodatki(datoteka):
    cih = dict()
    with open(datoteka, 'r') as f:
        for line in f:
            if line == '\n':
                break
            line_sp = line.replace('\n', '').split(' : ')
            if len(line_sp) == 2:
                key, value = line_sp
                try:
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                    cih[key] = value
                except:
                    cih[key] = value

    N = cih['Total Frame']
    w = cih['Image Width']
    h = cih['Image Height']
    FPS = cih['Record Rate(fps)']
    return (N, h, w), FPS


def ROI_lihost(ROI):
    roi = []
    for i in ROI:
        if (i % 2) != 0:
            roi.append(i)
        else:
            roi.append(i + 1)
    return roi



def kalibracija(piklsi=1, dolzina=1):
    merilo = dolzina / piklsi
    return merilo

