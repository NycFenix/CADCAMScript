import sys
import os

# --- CONFIGURAÇÃO DE CAMINHOS (CRÍTICO) ---
# Ajuste o caminho abaixo para onde o FreeCAD está instalado no seu PC.
# Windows: Geralmente 'C:\\Program Files\\FreeCAD 0.21\\bin'
# Linux: Geralmente '/usr/lib/freecad/lib' ou '/usr/share/freecad/Mod'
FREECAD_LIB_PATH = r'C:\\Program Files\\FreeCAD 1.0\\bin' 
sys.path.append(FREECAD_LIB_PATH)


try:
    import FreeCAD as App
    import Part
    # Importar bibliotecas específicas do Path (CAM)
    # Nota: Em versões muito novas (1.0+), Path pode ser referenciado como CAM, 
    # mas os scripts internos ainda usam 'PathScripts'.
    import Path
    
    import PathScripts.PathJob as PathJob
    import PathScripts.PathProfile as PathProfile
    import PathScripts.PathPostProcessor as PathPostProcessor
    import PathScripts.PathUtil as PathUtil
except ImportError as e:
    print("Erro ao importar bibliotecas do FreeCAD. Verifique o FREECAD_LIB_PATH.")
    print(f"Detalhe do erro: {e}")
    sys.exit(1)

# --- 1. CRIAÇÃO DO DOCUMENTO E SÓLIDO ---
doc_name = "AutomacaoCNC"
if App.getDocument(doc_name):
    App.closeDocument(doc_name)
doc = App.newDocument(doc_name)

# Criar um cubo (Box)
box = doc.addObject("Part::Box", "MeuCubo")
box.Length = 50.0  # mm
box.Width = 50.0   # mm
box.Height = 20.0  # mm
doc.recompute()

print("Sólido criado: Cubo 50x50x20mm")

# --- 2. CRIAÇÃO DO JOB (CAM) ---
# O Job gerencia o bloco (stock), as ferramentas e as operações.
# PathJob.Create(Nome, [ObjetosBase], ObjetoJobTemplate)
job = PathJob.Create('Job', [box], None)

# Configurar o Bloco (Stock)
# Estendemos o bloco 0mm além da peça (tamanho exato da peça)
stock = job.Stock
stock.Extents = [0, 0, 0, 0, 0, 0] 
job.Stock = stock

# Configurar uma Ferramenta Básica (Endmill 5mm)
# O script PathJob cria um ToolController padrão, vamos usá-lo.
tool_controller = job.Tools.Group[0]
tool_controller.Name = "Ferramenta_5mm"
# É possível detalhar diâmetro e velocidade aqui acessando tool_controller.Tool

doc.recompute()
print("Job e Stock configurados.")

# --- 3. OPERAÇÃO DE PERFIL (CONTORNO) ---
# Vamos criar um perfil ao redor do cubo.
# Precisamos dizer ao FreeCAD qual geometria seguir.
profile = PathProfile.Create('Perfil')

# Definir a base da operação. 
# (box, 'Face6') refere-se geralmente à face superior (TOP) num cubo padrão.
# Para robustez, idealmente se busca a face pelo vetor normal Z.
profile.Base = [(box, 'Face6')]

# Adicionar operação ao Job
job.addTask(profile)

# Ajustes da Operação (Exemplos)
profile.StepDown = 5.0  # Passo vertical de 5mm
profile.Side = "Outside" # Cortar por fora
doc.recompute()

print("Operação de Perfil adicionada.")

# --- 4. PÓS-PROCESSAMENTO (EXPORTAR G-CODE) ---
output_filename = "trajetoria_cubo.ngc"
output_path = os.path.join(os.getcwd(), output_filename)
post_processor = "linuxcnc"  # Nome exato do arquivo .py do pós no FreeCAD

# O objeto PostProcessor
pp = PathPostProcessor.PostProcessor()

try:
    # A função export aceita (Job/Operação, ArquivoSaída, Opções)
    # job faz a exportação de todas as operações contidas nele
    gcode = pp.export(job, output_path, post_processor)
    print("------------------------------------------------")
    print(f"Sucesso! G-Code exportado para: {output_path}")
    print("------------------------------------------------")
    
    # Exibir as primeiras linhas do Gcode gerado para conferência
    with open(output_path, 'r') as f:
        print("Preview do G-Code:")
        print("\n".join(f.readlines()[:10]))
        
except Exception as e:
    print(f"Erro ao exportar G-Code: {e}")

# Salvar o projeto FreeCAD para inspeção visual depois
doc.saveAs(os.path.join(os.getcwd(), "ProjetoAutomacao.FCStd"))
print("Arquivo FCStd salvo.")