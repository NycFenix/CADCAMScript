FREECADPATH = "C:\\Program Files\\FreeCAD 1.0\\bin"

import sys

sys.path.append(FREECADPATH) # Adiciona o path do FreeCAD ao sys.path

import FreeCAD
import Part 


# Conversor de .stl/.step/.SLDPRT para g-code



#path_parte = r"C:\Users\nycsf\Documents\Peças Teste\PL90-40S - PLACA 90° 40X40 SEM RECORTE"
parte = FreeCAD.open("C:\\Users\\nycsf\\Documents\\Peças Teste\\Ronaldo 40 40.FCStd") # Freecad.open só aceita arquivos .FCStd. Passar os arquivos da peça por algum conversor?



my_box = Part.makeBox(10, 20, 30)


print(f"The volume of the box is: {my_box.Volume}")
print(f"The area of the box is: {my_box.Area}")

