# Funciones para guardar y cargar datos en archivos CSV y JSON

import os # Importación del módulo os para manejar operaciones del sistema operativo y verificar la existencia de archivos
import csv # Importación del módulo csv para manejar archivos CSV
import json # Importación del módulo json para manejar archivos JSON
import logging # Importación del módulo logging para manejar registros de eventos
import db # Importación del módulo db que contiene las funciones para interactuar con la base de datos


# Archivos donde se alamcenrán los datos de las mascotas y sus consultas
archivo_csv = 'data/mascotas_dueños.csv'
archivo_json = 'data/consultas.json'


# Función para exportar mascotas y dueños a CSV desde la base de datos
def guardar_mascotas_csv():
    try:
        mascotas = db.obtener_mascotas()  # Mascotas con datos de dueño
        if not mascotas:
            logging.warning("No hay mascotas registradas para guardar en el archivo CSV.")
            return
        with open(archivo_csv, mode='w', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(['ID', 'Nombre', 'Especie', 'Raza', 'Edad', 'Dueño', 'Teléfono', 'Dirección'])
            for m in mascotas:
                writer.writerow(m)
        logging.info("Mascotas exportadas a CSV correctamente.")
    except Exception as e:
        logging.error(f"Error al guardar mascotas en CSV: {e}")


# Función para importar mascotas y dueños desde CSV a la base de datos
def cargar_mascotas_csv():
    try:
        with open(archivo_csv, mode='r', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)
            for row in reader:
                # Insertar dueño si no existe (puedes mejorar esto con una consulta previa)
                duenos = db.obtener_duenos()
                dueno_existente = next((d for d in duenos if d[1] == row['Dueño'] and d[2] == row['Teléfono'] and d[3] == row['Dirección']), None)
                if dueno_existente:
                    id_dueno = dueno_existente[0]
                else:
                    id_dueno = db.insertar_dueno(row['Dueño'], row['Teléfono'], row['Dirección'])
                # Insertar mascota
                db.insertar_mascota(row['Nombre'], row['Especie'], row['Raza'], int(row['Edad']), id_dueno)
        logging.info("Mascotas importadas desde CSV correctamente.")
    except Exception as e:
        logging.error(f"Error al cargar mascotas desde CSV: {e}")


# Función para exportar consultas a JSON desde la base de datos
def guardar_consultas_json():
    try:
        mascotas = db.obtener_mascotas()
        data = []
        for m in mascotas:
            consultas = db.obtener_consultas_por_mascota(m[0])
            for c in consultas:
                data.append({
                    "id": c[0],
                    "fecha": c[1],
                    "motivo": c[2],
                    "diagnostico": c[3],
                    "id_mascota": m[0],
                    "nombre_mascota": m[1]
                })
        with open(archivo_json, mode='w', encoding='utf-8') as archivo:
            json.dump(data, archivo, ensure_ascii=False, indent=4)
        logging.info("Consultas exportadas a JSON correctamente.")
    except Exception as e:
        logging.error(f"Error al guardar consultas en JSON: {e}")


# Función para importar consultas desde JSON a la base de datos
def cargar_consultas_json():
    try:
        with open(archivo_json, mode='r', encoding='utf-8') as archivo:
            data = json.load(archivo)
            for c in data:
                # Verifica que la mascota exista
                mascotas = db.obtener_mascotas()
                mascota_existente = next((m for m in mascotas if m[0] == c['id_mascota']), None)
                if mascota_existente:
                    db.insertar_consulta(c['fecha'], c['motivo'], c['diagnostico'], c['id_mascota'])
        logging.info("Consultas importadas desde JSON correctamente.")
    except Exception as e:
        logging.error(f"Error al cargar consultas desde JSON: {e}")
