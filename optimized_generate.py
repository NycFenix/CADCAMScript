FREECADPATH = "C:\\Program Files\\FreeCAD 1.0\\bin"
import sys
sys.path.append(FREECADPATH) # Adiciona o path do FreeCAD ao sys.path
import FreeCAD
import Mesh
import Part
import MeshPart
import os

def type_converter(file_path):
    """
    Imports a 3d model file in some extension and converts it to a FreeCAD object, now with mor eoptimizede convertion and diferent faces numbers.

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
        obj = new_doc.addObject("Mesh::Feature", "ImportedMesh")
        obj.Mesh = Mesh.read(file_path)
        new_doc.recompute()
        print("STL file imported as Mesh Object.")

        mesh = obj.Mesh

        segments = mesh.getPlanarSegments(0.0001)
        faces = []


        for i in segments:
            if len(i) > 0:
                # a segment can have inner holes
                wires = MeshPart.wireFromSegment(mesh, i)
                print(f"Made wire number {i}")
                # we assume that the exterior boundary is that one with the biggest bounding box
                if len(wires) > 0:
                    ext = None
                    max_length=0
                    for i in wires:
                        if i.BoundBox.DiagonalLength > max_length:
                            max_length = i.BoundBox.DiagonalLength
                            ext = i

                    wires.remove(ext)
                    # all interior wires mark a hole and must reverse their orientation, otherwise Part.Face fails
                    for i in wires:
                        i.reverse()

                    # make sure that the exterior wires comes as first in the list
                    wires.insert(0, ext)
                    faces.append(Part.Face(wires))

        new_doc.recompute()
        print("FreeCad solid conversion Finished")
        solid = Part.Solid(Part.Shell(faces))
        Part.show(solid)

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


        
    except Exception as e:
        print(f"An error occurred while importing the file: {e}")
        
        FreeCAD.closeDocument(new_doc.Name)

        
        return None
    
test_file_path = "torch.STL"

if __name__ == "__main__":
    new_FCDoc = type_converter(test_file_path)
