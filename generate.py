FREECADPATH = "C:\\Program Files\\FreeCAD 1.0\\bin"

import sys

sys.path.append(FREECADPATH) # Adiciona o path do FreeCAD ao sys.path


import FreeCAD
import Part

# Teste: cria uma forma geométrica simples

my_box = Part.makeBox(10, 20, 30)

print(f"The volume of the box is: {my_box.Volume}")
print(f"The area of the box is: {my_box.Area}")