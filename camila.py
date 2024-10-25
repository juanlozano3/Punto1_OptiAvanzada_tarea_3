from gurobipy import *

# Conjuntos
dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
franjas = ['00am-2am', '2am-4am', '4am-6am', '6am-8am', '8am-10am', '10am-12pm', 
           '12pm-2pm', '2pm-4pm', '4pm-6pm', '6pm-8pm', '8pm-10pm', '10pm-12am']
D = [i for i in range(len(dias))]
F = [i for i in range(len(franjas))]


# Parámetro aij (requerimientos mínimos de equipos por franja horaria y día)
aij = [
    [11, 11, 24, 55, 68, 80, 88, 75, 79, 93, 67, 15],
    [12, 12, 25, 50, 70, 85, 90, 80, 75, 93, 65, 15],
    [11, 11, 24, 55, 68, 80, 88, 75, 79, 93, 67, 15],
    [15, 15, 27, 60, 70, 85, 93, 78, 78, 90, 72, 15],
    [15, 20, 35, 64, 77, 86, 92, 86, 75, 91, 76, 15],
    [15, 20, 35, 64, 77, 86, 92, 86, 75, 91, 76, 15],
    [10, 10, 30, 60, 68, 82, 85, 77, 79, 95, 74, 10]
]

# Parámetro cij (costos por equipo asignado por franja horaria y día)
cij = [
    [100, 100, 100, 66, 66, 66, 66, 72, 72, 100, 100, 100],
    [100, 100, 100, 66, 66, 66, 66, 72, 72, 100, 100, 100],
    [100, 100, 100, 66, 66, 66, 66, 72, 72, 100, 100, 100],
    [100, 100, 100, 66, 66, 66, 66, 72, 72, 100, 100, 100],
    [100, 100, 100, 66, 66, 66, 66, 72, 72, 100, 100, 100],
    [100, 100, 100, 66, 66, 66, 66, 72, 72, 100, 100, 100],
    [130, 130, 130, 84, 84, 84, 84, 97, 97, 130, 130, 130]
]

def costosTurnos(Phij, cij):
    costos =[]
    for k in range(len(Phij)):
        costos_k = 0
        for i in range(len(Phij[k])):
            for j in range(len(cij[i])):
                costos_k += Phij[k][i][j] * cij[i][j]
        costos.append(costos_k)
    return costos

def costoTurno(xij, cij):
    costo = 0
    for i in range(len(xij)):
        for j in range(len(cij[i])):
            costo += xij[i][j] * cij[i][j]
    return costo


Columnas = { 0: [
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
Ch = costosTurnos(Columnas, cij)
num_horarios = len(Columnas)
 

# Crear el modelo

ModelMP = Model("Master Problem")
ModelMP.setParam('OutputFlag', 0)

# Crear la variable h
h = []
for j in Columnas.keys():
    obj_j = costoTurno(Columnas[j], cij)
    h.append(ModelMP.addVar(vtype=GRB.CONTINUOUS, obj = obj_j,  name="h"))

# Añadir restricciones para asegurar que se cubran los requerimientos mínimos de equipos por día y franja
demCtr = []
for i in D:
    for j in F:
        demCtr.append(ModelMP.addConstr(quicksum(h[k] * Columnas[k][i][j] for k in range(num_horarios)) >= aij[i][j], 
                        name=f"req_min_equipos_{i}_{j}"))

# Crear la función objetivo
ModelMP.ModelSense = GRB.MINIMIZE

#Parametros
Entre_semana = [0, 1, 2, 3, 4]
Fin_de_semana = [5, 6]

ModelAUX = Model("Auxiliar Problem")
ModelAUX.Params.OutputFlag = 0

# Crear la variable x que indica si se asigna la franja f del dia d al horario
x = ModelAUX.addVars(len(D), len(F), vtype=GRB.BINARY, name="x")

# Crear la variable y que tiene la cantidad de variables de los días y que sea binaria
y = ModelAUX.addVars(len(D), vtype=GRB.BINARY, name="y")

# Restricción para asegurar que el equipo trabaje exactamente 4 franjas por día
for i in D:
    ModelAUX.addConstr(quicksum(x[i,j] for j in F) == 4 * y[i], name=f"exactly_4_franjas_{i}")

# Restricción Asegurar que el equipo trabaje al menos 24 horas entre semana:
ModelAUX.addConstr(quicksum(y[i] for i in Entre_semana) >= 3, name="sum_y_equals_4")

# Restricción Asegurar que el equipo trabaje un maximo de 32  horas entre semana:
ModelAUX.addConstr(quicksum(y[i] for i in Entre_semana) <= 4, name="sum_y_equals_4")

# Restricción para asegurar que el equipo trabaje un máximo de un día por fin de semana
ModelAUX.addConstr(quicksum(y[i] for i in Fin_de_semana) == 1, name="max_1_dia_fin_de_semana")

# Restricción Asegurar que el equipo no trabaje más de dos días consecutivos
for i in range(len(D) - 2):  # Asegúrate de no salir de los límites
    ModelAUX.addConstr(
        quicksum(x[i,j] + x[i+1,j] + x[i+2,j] for j in F) <= 8,
        name=f"max_8_consecutive_days_{i}"
    )
while True:
    
    ModelMP.optimize()
    print(f"FO Master: {ModelMP.objVal} --> #Cols: {num_horarios}")
    # Obtener las duales
    Duals = ModelMP.getAttr("Pi", ModelMP.getConstrs())
    diccionario = {}

    indice_duals = 0
    for i in D:
        for j in F:
            diccionario[(i, j)] = Duals[indice_duals]
            indice_duals += 1

    ModelAUX.setObjective(quicksum((cij[i][j] - diccionario[i,j])*x[i,j] for i in D for j in F), GRB.MINIMIZE)

    ModelAUX.optimize()
    ModelAUX.setParam('OutputFlag', 0)
    
    minReduceCost = ModelAUX.getObjective().getValue()

    # Break or continue
    tolerancia = 1e-9
    if minReduceCost >= -tolerancia:
        print(minReduceCost)
        print(f"FO Aux (Costo Reducido): {ModelAUX.objVal} ")
        print("\nColumn generation stops !\n")
        break
    else:
        num_horarios += 1
        print(ModelAUX.getAttr("X"))
        col_vals = ModelAUX.getAttr("x", x)
        # Crear listas para cada día y reemplazar -0.0 por 0.0
        lunes = [0.0 if val == -0 else val for j in F for val in [col_vals[0, j]]]  # Día 0 (Lunes)
        martes = [0.0 if val == -0 else val for j in F for val in [col_vals[1, j]]]  # Día 1 (Martes)
        miercoles = [0.0 if val == -0 else val for j in F for val in [col_vals[2, j]]]  # Día 2 (Miércoles)
        jueves = [0.0 if val == -0 else val for j in F for val in [col_vals[3, j]]]  # Día 3 (Jueves)
        viernes = [0.0 if val == -0 else val for j in F for val in [col_vals[4, j]]]  # Día 4 (Viernes)
        sabado = [0.0 if val == -0 else val for j in F for val in [col_vals[5, j]]]  # Día 5 (Sábado)
        domingo = [0.0 if val == -0 else val for j in F for val in [col_vals[6, j]]]  # Día 6 (Domingo)
        # Imprimir el nuevo horario
        # print("Nuevo horario:")
        # print("Lunes:", lunes)
        # print("Martes:", martes)
        # print("Miércoles:", miercoles)
        # print("Jueves:", jueves)
        # print("Viernes:", viernes)
        # print("Sábado:", sabado)
        # print("Domingo:", domingo)
        # Crear la nueva columna
        nuevo_horario = [lunes, martes, miercoles, jueves, viernes, sabado, domingo]
        Columnas[num_horarios - 1]= nuevo_horario
        nueva_columna = lunes + martes + miercoles + jueves + viernes + sabado + domingo
        obj_j = costoTurno(nuevo_horario, cij)
        newCol = Column(nueva_columna, demCtr)
        ModelMP.addVar(vtype = GRB.CONTINUOUS, obj = obj_j, column = newCol,  name="h")
        ModelMP.update()
        # Agregar el nuevo costo a la lista de costos
        print(f"Costo del turno: {costoTurno(nuevo_horario, cij)}")
        Ch.append(costoTurno(nuevo_horario, cij))
        print(f"Iteración {num_horarios - 6}")
        print(f"FO Aux (Costo Reducido): {ModelAUX.objVal} ")


if ModelMP.status == GRB.OPTIMAL:
    for v in ModelMP.getVars():
        print(f'{v.varName}: {v.x}')
else:
    print("No se encontró una solución óptima.")
    
num_horarios = len(Columnas)

#Con Variables Enteras
for v in ModelMP.getVars():
    v.setAttr("vtype", GRB.INTEGER)
    
ModelMP.update()
ModelMP.optimize()

print(f"Cantidad de Auxiliares~ Entero y Costo Total {ModelMP.objVal}")
for v in ModelMP.getVars():
    if v.x > 0:
        print(f"TURNO: {v.varName} --> Auxiliares: {v.x}")

print()