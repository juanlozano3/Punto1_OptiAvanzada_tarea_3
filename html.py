import pandas as pd
import json
import os

# Directorio actual
current_directory = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(current_directory, "HorariosGenerados.xlsx")

# Nombres de los días de la semana
dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

# Leer todas las hojas del archivo Excel
horarios = pd.ExcelFile(excel_path)

# Estructura para acumular toda la información
data = {"horarios": {}, "costos": []}

# Recorrer cada hoja y agregar los datos correspondientes a la estructura 'data'
for sheet_name in horarios.sheet_names:
    df = horarios.parse(sheet_name)  # Leer la hoja en DataFrame
    
    if sheet_name.lower() == "costos":  # Procesar la hoja de costos
        # Guardar los costos en la estructura
        data["costos"] = df.to_dict(orient="records")
        print(f"Costos procesados desde la hoja '{sheet_name}'")
        continue  # Saltar al siguiente ciclo

    # Verificar que el número de filas coincida con los días de la semana
    if len(df) != 7:
        print(f"Advertencia: La hoja '{sheet_name}' no tiene 7 filas (una por cada día). Será omitida.")
        continue  # Omitir hojas que no tienen 7 filas

    # Crear la estructura del horario para esta hoja
    horario = []
    for i, row in df.iterrows():
        dia = dias_semana[i]  # Día correspondiente a la fila
        franjas = row.to_dict()  # Convertir la fila en un diccionario de franjas

        horario.append({
            "día": dia,
            "franjas": franjas
        })

    # Agregar el horario procesado a la estructura principal
    data["horarios"][sheet_name] = horario

# Guardar toda la información en un único archivo JSON
json_path = os.path.join(current_directory, "HorariosCompleto.json")
with open(json_path, "w") as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print(f"Archivo JSON completo generado en: {json_path}")
