from PIL import Image

def getNewName(x,y):
    name = ""
    if x==0:
        name = "plaq_A_"+ str(y+1) +".png"
            
        
    if x==1:
        name = "plaq_B_"+str(y+1) +".png"
    return name
        
name = "/home/pi/Documents/Scanner/n_01.png"

image = Image.open(name)
largeur,hauteur = image.size
xsize= largeur//2
ysize = hauteur//3
for x in range(2):
    for y in range(3):
        colonne = 1
        imgpiece = image.crop((x*xsize,y*ysize,(x+1)*xsize,(y+1)*ysize))
        newName = getNewName(x,y)
        imgpiece.save(newName)	   
    colonne +=1

print("coucou")