#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from flask import Flask, render_template, request
import sane
import numpy
from PIL import Image
import zipfile
import zlib
import time
import datetime
import netifaces 
from datetime import datetime

#---- SCANNER REGLAGES ------------------------------------------------


#
# Change these for 16bit / grayscale scans
#
depth = 8
mode = 'color'

#
# Initialize sane
#
"""
Return a tuple ('Nom de la version': sane_ver, ver_maj, ver_min, ver_patch) 
"""
ver = sane.init()

#
# Get devices
#
"""
Return a list of 4-tuples containing the available scanning devices.
Each tuple is of the format (device_name, vendor, model, type) with
device_name = the device name, suitabe for passing to sane.open()
"""
devices = sane.get_devices()


#
# Open first device
#
"""
Open a device for scanning. Suitable values for devname are returned
in the first item of the tuples returned by san.get_devices(). Returns
a SaneDev object on success. SaneDev is a class representing a SANE device. 
"""
dev = sane.open(devices[0][0])

#
# List of all the available options
#
"""
Returns a list of tuples describing all the available options
"""

opt_avail = dev.get_options()

#
# Gives all the current device settings:
#
""" Returns a 5-tuple holding all the current device settings
(format, last_frame, (pixels_per_line,lines), depth, bytes_per_line)
Format = "grey", "color", "red"
Pixels_per_line = width of the scanned image = longueur
lines = height of the scanner image. = largeur
depth = number of bits per sample.
bytes_per_line = the number of bytes per line. 
"""
params = dev.get_parameters()

#
# Set some options
#
""" Format""" 
try:
    dev.mode = mode
except:
    print('Cannot set mode, defaulting to %s' % params[0])


""" Profondeur""" 
try:
    dev.depth = depth
except:
    print('Cannot set depth, defaulting to %d' % params[3])




#---- ZIP ----------------------------------------------------------
    
#
# Création d'un fichier zip "scanner.zip"
#
zfile = zipfile.ZipFile('scanner.zip','w',zipfile.ZIP_DEFLATED,True)
#zfile = zipfile.ZipFile('scanner.zip','w')
zfile.close()


#
# Enregistre toutes les images dans un fichier zip s'appelant "Scaner.odt" 
#
""" Ici, on inclut dans l'archive "Scanner.zip" le fichier im qui est 'coucou.png'."""
def ajoutZip(name):
    zfile = zipfile.ZipFile('scanner.zip','a',zipfile.ZIP_DEFLATED,True)
    #zfile = zipfile.ZipFile('scanner.zip','a')
    zfile.write(name)
    zfile.close()


#
# Name the file
#
def name_image(x):
    date = datetime.today()
    d = '{:%d-%m %H:%M}'.format(date)
    a = str(d)
    if (x<10):
        name = "n_"+ str(0)+ str(x)
        real_n = name+'.png'
    else:
        name = 'n_'+ str(x)
        real_n = name+'.png'
    return real_n

#----- SCANNER PARAMETRES ----------------------------------------------------

#
# Set area 
#
def set_area(plaq):
    dev.tl_x = 68 #Largeur d'une bande
    dev.tl_y = 0 #Largeur d'une bande
    if plaq == 1:
      dev.br_y = 127
      dev.br_x = 153 #68+85
    if plaq ==2:
       dev.br_y = 254
       dev.br_x = 153

       
#----POST PROCESSING------------------------------------------------------------
#
# Découpage des photos
#
def getNewName(x,y):
    if x==0:
        if y==0:
            name = "A_"+ str(x+1) +".png"  
        if y==1:
            name = "B_"+ str(x+1) +".png"  
        if y==2:
            name = "C_"+ str(x+1) +".png"
        return name 
    if x==1:
        if y==0:
            name = "A_"+ str(x+1) +".png"  
        if y==1:
            name = "B_"+ str(x+1) +".png"  
        if y==2:
            name = "C_"+ str(x+1) +".png"
        return name

    
def get_simple_name(x):
    if (x<10):
        name = "n_"+ str(0)+ str(x)
    else:
        name = 'n_'+ str(x)
    return name

 
def cut_plaq(plaq,image,largeur, hauteur,xsize,ysize,line,column,i):
     if(plaq ==1):
        for x in range(column):
            for y in range(line):
                imgpiece = image.crop((x*xsize, y*ysize, (x+1)*xsize, (y+1)*ysize))
                name = getNewName(x,y)
                newName = get_simple_name(i+1)+"_" +name
                imgpiece.save(newName)
                ajoutZip(newName)
     if(plaq ==2):
        for x in range(column):
            for y in range(line):
                imgpiece = image.crop((xxsize, yysize, (x+1)*xsize, (y+1)*ysize))
                name = getNewName(x,y)
                newName = get_simple_name(i+1)+"_" +name
                ajoutZip(newName)
                
def cut(plaq,puits,acc,i):
    image = Image.open(acc)
    largeur,hauteur = image.size
    if (puits==6):
        xsize = largeur//2
        ysize = hauteur//3
        cut_plaq(plaq,image,largeur, hauteur,xsize,ysize,3,2,i)
    if (puits==12):
        #A FAIRE 
        cut_plaq(plaq,image,largeur, hauteur,12,12,3,2,i)

#---- Création d'un fichier CSV ------------------------------------------------------------
        """
def csv():
    fname = "scanner.csv"
    file = open(fname,"wb")
    writer = csv.writer(file)
    writer.writerow(('Prix','Désignation'))
    writer.writerow( (9.80, 'Tarte aux pommes') )
    writer.writerow( ('13.40', 'Galette des rois') )
    writer.writerow( (2.45, 'Beignet') )
    file.close()
    file = open(fname,"rb")
    reader = csv.reader(file)
    for row in reader:
        print row

file.close()

"""

#---- RUN ------------------------------------------------------------
#
# Création d'une boucle qui enregistre toutes les x minutes une photo
#

def run_scanner(ti,prises, plaq,puits):
    i = 0
    timer = ti//prises
    if prises==1:
       dev.start()
       im = dev.snap() #Read image data and return a PIL.Image object.
       name = name_image(i+1)
       im.save(name)
       ajoutZip(name)
       acc = "/home/pi/Documents/Scanner/"+name
       cut(plaq,puits,acc,i)
       
    else:
         while i < prises:
            dev.start()
            im = dev.snap()
            name = name_image(i+1)
            im.save(name)
            ajoutZip(name)
            acc = "/home/pi/Documents/Scanner/"+name
            cut(plaq,puits,acc,i)
            time.sleep(timer)
            i+=1 



 
#---- INTERFACE -------------------------------------------------------
app = Flask(__name__)

@app.route('/')
def acceuil():
    return render_template('accueil.html')

@app.route('/result', methods= ['POST', 'GET'])
def result():
    if request.method=='POST':
        result = request.form
        time = request.form.get('time')
        t = int(time)
        prises = request.form.get('prises')
        p= int(prises)
        plaq = request.form.get('samples')
        pl = int(plaq)
        set_area(pl)
        puits = request.form.get('puits')
        pu = int(puits)
        run_scanner(t,p,pl,pu)
    return render_template("Bienvenue.html", result = result)
        


#---- RUN PAGE WEB --------------------------------------------------------------------
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

#------------------------------------------------------------------------
    
#
# Close the device
#
dev.close()                                             
