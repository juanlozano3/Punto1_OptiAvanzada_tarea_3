from gurobipy import *
import gurobipy as gp
import math
import os
import numpy as np
import pandas as pd

#Importar datos

#Conjuntos MP
F = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
D = [0, 1, 2, 3, 4, 5, 6]
H = [i for i in range(0, 83)]

    
def costosHor(Phij, cij):
    costos =[]
    for k in range(len(Phij)):
        costos_k = 0
        for i in range(len(Phij[k])):
            for j in range(len(cij[i])):
                costos_k += Phij[k][i][j] * cij[i][j]
        costos.append(costos_k)
    return costos

def costoH(xij, cij):
    costo = 0
    for i in range(len(xij)):
        for j in range(len(cij[i])):
            costo += xij[i][j] * cij[i][j]
    return costo

current_directory = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(current_directory, "Caviana def.xlsx")

df_requerimientos=pd.read_excel(file_name,sheet_name="Caviana TACA",skiprows=3,nrows=12,usecols="B:I")


df_costos=pd.read_excel(file_name,sheet_name="Caviana TACA",skiprows=20,nrows=12,usecols="B:I")



req=df_requerimientos.iloc[:,1:].values.flatten(order="F")
cos=df_costos.iloc[:,1:].values.flatten(order="F")

"""pij = []
cij=[]  

for i in range(0, 8):
    fila = []  
    for j in range(0, 12):
        fila.append(req[j])
    pij.append(fila) 


for i in range(0, 8):
    fila = []  
    for j in range(0, 12):
        fila.append(cos[j])
    cij.append(fila)"""

pij = [
    [11, 11, 24, 55, 68, 80, 88, 75, 79, 93, 67, 15],
    [12, 12, 25, 50, 70, 85, 90, 80, 75, 93, 65, 15],
    [11, 11, 24, 55, 68, 80, 88, 75, 79, 93, 67, 15],
    [15, 15, 27, 60, 70, 85, 93, 78, 78, 90, 72, 15],
    [15, 20, 35, 64, 77, 86, 92, 86, 75, 91, 76, 15],
    [15, 20, 35, 64, 77, 86, 92, 86, 75, 91, 76, 15],
    [10, 10, 30, 60, 68, 82, 85, 77, 79, 95, 74, 10]
]

cij = [
    [100, 100, 100, 66, 66, 66, 66, 72, 72, 100, 100, 100],
    [100, 100, 100, 66, 66, 66, 66, 72, 72, 100, 100, 100],
    [100, 100, 100, 66, 66, 66, 66, 72, 72, 100, 100, 100],
    [100, 100, 100, 66, 66, 66, 66, 72, 72, 100, 100, 100],
    [100, 100, 100, 66, 66, 66, 66, 72, 72, 100, 100, 100],
    [100, 100, 100, 66, 66, 66, 66, 72, 72, 100, 100, 100],
    [130, 130, 130, 84, 84, 84, 84, 97, 97, 130, 130, 130]
]


patrones_iniciales=pd.read_excel(file_name,sheet_name="Inicializacion", header=None, skiprows=1, nrows=84)


#print(pij)
#dict_of_dicts = {col: patrones_iniciales[col].to_dict() for col in patrones_iniciales.columns}
#print(dict_of_dicts)


dict_of_lists = {col: list(patrones_iniciales[col]) for col in patrones_iniciales.columns}
#print(dict_of_lists[0])

"""
solucion_inicial_def={}

for k in range(0, 84):

    solucion_inicial=[]

    contador=0

    for i in range(0,7):
        fila=[]
        for j in range(0,12): 
            fila.append(dict_of_lists[k][contador])
            contador+=1
        solucion_inicial.append(fila)

    solucion_inicial_def[k]=solucion_inicial  

"""

solucion_inicial_def = { 0: [
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
], 1: [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
], 2: [
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
], 3: [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
], 4: [
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
], 5:[
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]}

Ch = costosHor(solucion_inicial_def, cij)

num_columnas = len(solucion_inicial_def)


modelMP=Model("Master Problem")
modelMP.Params.OutputFlag = 0
modelMP.setParam('MIPGap', 0.01)
modelMP.setParam('TimeLimit', 3600)

#---------Funcion encargada de calcular los costos de los horarios generados---------
x=[]
for j in solucion_inicial_def.keys():
    obj_j = costoH(solucion_inicial_def[j], cij)
    x.append(modelMP.addVar(vtype=GRB.CONTINUOUS, obj = obj_j,  name="x"))


demRestricciones=[]
for i in (D):
    for j in (F):
        demRestricciones.append(modelMP.addConstr(quicksum(x[k] * solucion_inicial_def[k][i][j] for k in range((num_columnas))) >= pij[i][j]))


#modelMP.setObjective(quicksum(x[i]*cos[i] for i in range(0, len(H)-1)), GRB.MINIMIZE)

modelMP.ModelSense = GRB.MINIMIZE

modelAP = Model("Problema Auxiliar")
modelAP.Params.OutputFlag = 0

a_auxiliar = modelAP.addVars(len(D), len(F), vtype=GRB.BINARY, name="a_auxiliar")
d_auxiliar = modelAP.addVars(len(D), vtype=GRB.BINARY, name="d_auxiliar")

for i in D:
    modelAP.addConstr(quicksum(a_auxiliar[i,j] for j in F) == 4 * d_auxiliar[i], name=f"exactly_4_franjas_{i}")


#modelAP.addConstr(quicksum(a_auxiliar[i, j] for i in range(len(F)) for j in range(len(D)))>=16)
#modelAP.addConstr(quicksum(a_auxiliar[i, j] for i in range(len(F)) for j in range(len(D)))<=20)
for i in range(len(D) - 2):  # Asegúrate de no salir de los límites
    modelAP.addConstr(
        quicksum(a_auxiliar[i,j] + a_auxiliar[i+1,j] + a_auxiliar[i+2,j] for j in F) <= 8,
        name=f"max_8_consecutive_days_{i}"
    )

modelAP.addConstr(quicksum(d_auxiliar[i] for i in [0,1,2,3,4]) >= 3, name="sum_y_equals_4")

# Restricción Asegurar que el equipo trabaje un maximo de 32  horas entre semana:
modelAP.addConstr(quicksum(d_auxiliar[i] for i in [0,1,2,3,4]) <= 4, name="sum_y_equals_4")

# Restricción para asegurar que el equipo trabaje un máximo de un día por fin de semana
modelAP.addConstr(quicksum(d_auxiliar[i] for i in [5, 6]) == 1, name="max_1_dia_fin_de_semana")

"""modelAP.addConstr(sum(d_auxiliar[i] for i in [0,1,2,3,4])>=3)
modelAP.addConstr(sum(d_auxiliar[i] for i in [0,1,2,3,4])<=4)
modelAP.addConstr(d_auxiliar[5] + d_auxiliar[6] == 1, name="FinDeSemanaLibre")
"""

horarios_totales = []  # Guardará los nuevos horarios generados
costos_totales = []    # Guardará los costos de cada horario
# Optimización y generación de horarios
while True:
    modelMP.optimize()
    print(f"FO Master: {modelMP.objVal} --> #Cols: {len(horarios_totales)}")

    # Obtener los duales
    duals = modelMP.getAttr("Pi", modelMP.getConstrs())
    diccionario_duales = {(i, j): duals[indice] for indice, (i, j) in enumerate([(i, j) for i in D for j in F])}

    # Definir la función objetivo del problema auxiliar
    modelAP.setObjective(
        quicksum((cij[i][j] - diccionario_duales[i, j]) * a_auxiliar[i, j] for i in D for j in F),
        GRB.MINIMIZE
    )
    modelAP.optimize()

    min_reduce_cost = modelAP.getObjective().getValue()
    tolerancia = -1e-6

    if min_reduce_cost >= tolerancia:
        print(f"FO Aux (Costo Reducido): {modelAP.objVal} \n¡Deteniendo generación de columnas!")
        break

    # Obtener los valores de las variables auxiliares
    col_vals = modelAP.getAttr("x", a_auxiliar)

    # Crear el nuevo horario en un solo paso
    nuevo_horario = [
        [0.0 if col_vals[d, f] == -0.0 else col_vals[d, f] for f in F] for d in D
    ]

    # Agregar el nuevo horario y su costo
    obj_j = costoH(nuevo_horario, cij)
    horarios_totales.append(nuevo_horario)
    costos_totales.append(obj_j)

    # Añadir la nueva columna al modelo maestro
    nueva_columna = [val for fila in nuevo_horario for val in fila]
    newCol = Column(nueva_columna, modelMP.getConstrs())
    modelMP.addVar(vtype=GRB.CONTINUOUS, obj=obj_j, column=newCol, name=f"h_{len(horarios_totales)}")
    modelMP.update()

    print(f"Costo del turno: {obj_j}")
    print(f"FO Aux (Costo Reducido): {modelAP.objVal} \n¡Deteniendo generación de columnas!")

    Ch.append(obj_j)
    print(f"Iteración: {len(horarios_totales)}")
# Convertir el problema maestro a entero
for v in modelMP.getVars():
    v.setAttr("VType", GRB.INTEGER)

print("Heuristic integer master problem")
modelMP.optimize()

# Verificar si se encontró una solución óptima
if modelMP.status != GRB.OPTIMAL:
    print("No se encontró una solución óptima para el problema entero.")
else:
    print(f"Valor óptimo: {modelMP.objVal}")

# Obtener los valores de las variables x después de la optimización
x_values = [var.X for var in modelMP.getVars()]

# Filtrar los horarios utilizados (aquellos con x_j > 0)
horarios_utilizados = [
    horario for i, horario in enumerate(horarios_totales) if x_values[i] > 0
]

# Mostrar cuántos horarios se usaron en la solución entera
num_horarios_usados = len(horarios_utilizados)
print(f"Total de horarios utilizados: {num_horarios_usados}")

# Guardar los resultados en un archivo Excel
excel_path = os.path.join(current_directory, "HorariosGenerados.xlsx")

with pd.ExcelWriter(excel_path) as writer:
    # Guardar solo los horarios utilizados
    for i, horario in enumerate(horarios_utilizados):
        df_horario = pd.DataFrame(horario, columns=[f"Franja {j}" for j in F])
        df_horario.to_excel(writer, sheet_name=f"Horario_{i + 1}", index=False)

    # Guardar los costos correspondientes
    costos_utilizados = costos_totales[:len(horarios_utilizados)]  # Ajustar a los horarios guardados
    df_costos = pd.DataFrame({"Costo": costos_utilizados})
    df_costos.to_excel(writer, sheet_name="Costos", index=False)

print(f"Archivo Excel generado en: {excel_path}")
