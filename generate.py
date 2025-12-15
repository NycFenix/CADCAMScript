FREECADPATH = "C:\\Program Files\\FreeCAD 1.0\\bin"

import sys
import os
sys.path.append(FREECADPATH) # Adiciona o path do FreeCAD ao sys.path

import FreeCAD
import Part 
import Mesh

# Conversor de .stl/.step/.SLDPRT para g-code

def type_wrapper (file_path: str):
    """
    Imports a 3d model file in some extension and converts it to a FreeCAD project

    :param file_path: str - path to the 3d model file
    :return: FreeCAD document object
    """
    

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at {file_path} does not exist.")
    
    if not file_path.lower().endswith(('.stl', '.step', '.sldprt')):
        raise ValueError("Unsupported file format. Supported formats are: .stl, .step, .sldprt")    
    
    # freecad_name = os.path.splitext(file_path)[0] + ".FCStd"
    # if os.path.exists(freecad_name):
    #     print(f"FreeCAD document {freecad_name} already exists!")
    #     return None

    new_doc = FreeCAD.newDocument("ImportedModel")

    try:

        # Cria Mesh a partir do arquivo STL
        obj_mesh = new_doc.addObject("Mesh::Feature", "ImportedMesh")
        obj_mesh.Mesh = Mesh.read(file_path)
        new_doc.recompute()
        print("STL file imported as Mesh Object.")
        
        # Converter mesh para shape 
        shape = Part.Shape()
        shape.makeShapeFromMesh(obj_mesh.Mesh.Topology, 0.01)
        
        # Criar sólido a partir do shape
        solid = Part.makeSolid(shape)
        obj_solid = new_doc.addObject("Part::Feature", "SolidFromMesh")
        obj_solid.Shape = solid
        new_doc.recompute()
        print("FreeCad solid conversion Finished")


        freecad_name = os.path.splitext(file_path)[0] + ".FCStd"
        
        if os.path.exists(freecad_name): # Se já existe o arquivo, adiciona um sufixo numérico
            i = 1
            while True:
                new_name = f"{os.path.splitext(freecad_name)[0]}_{i}.FCStd"
                if not os.path.exists(new_name):
                    freecad_name = new_name
                    break
                i += 1
        new_doc.saveAs(freecad_name)
        print(f"FreeCAD document saved as {freecad_name}")

        return new_doc
    
    except Exception as e:
        print(f"An error occurred while importing the file: {e}")
        
        FreeCAD.closeDocument(new_doc.Name)

        return None
    
test_file_path = "torch.STL"

new_FCDoc = type_wrapper(test_file_path)
# path_parte = r"PartDesignExample.FCStd"
# parte = FreeCAD.open(path_parte) # Freecad.open só aceita arquivos .FCStd. Passar os arquivos da peça por algum conversor?



# my_box = Part.makeBox(10, 20, 30)

# if __name__ == '__main__':

#     print(f"The volume of the box is: {my_box.Volume}")
#     print(f"The area of the box is: {my_box.Area}")

