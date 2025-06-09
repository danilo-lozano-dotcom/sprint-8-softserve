# Módulo para la gestión de la base de datos SQLite de la clínica veterinaria

import sqlite3 # Importación del módulo sqlite3 para manejar la base de datos SQLite
import logging
import os # Importación del módulo os para manejar rutas de archivos

# Calcula la ruta absoluta a la carpeta 'data'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

nombre_db = os.path.join(DATA_DIR, 'clinica_veterinaria.db')

# Función para establecer el nombre de la base de datos
def set_db_name(name):
    global nombre_db
    nombre_db = name

# Función para conectar a la base de datos SQLite
def conectar():
    try:
        conn = sqlite3.connect(nombre_db)
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error al conectar a la base de datos: {e}")
        return None
    

# Creación de las tablas en la base de datos si no existen
def crear_tablas():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS duenos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT,
                direccion TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mascotas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                especie TEXT,
                raza TEXT,
                edad INTEGER,
                id_dueno INTEGER,
                FOREIGN KEY (id_dueno) REFERENCES duenos(id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                motivo TEXT,
                diagnostico TEXT,
                id_mascota INTEGER,
                FOREIGN KEY (id_mascota) REFERENCES mascotas(id)
            )
        ''')
        conn.commit()
        logging.info("Tablas creadas/verificadas correctamente en la base de datos.")
    except sqlite3.Error as e:
        logging.error(f"Error al crear tablas: {e}")
    finally:
        if conn:
            conn.close()

# --- Funciones CRUD para Dueños ---

# Función para insertar un nuevo dueño en la base de datos
def insertar_dueno(nombre, telefono, direccion):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO duenos (nombre, telefono, direccion) VALUES (?, ?, ?)",
            (nombre, telefono, direccion)
        )
        conn.commit()
        logging.info(f"Dueño '{nombre}' insertado correctamente.")
        return cursor.lastrowid
    except sqlite3.Error as e:
        logging.error(f"Error al insertar dueño: {e}")
        return None
    finally:
        if conn:
            conn.close()

# Función para devolver una lista de todos los dueños en la base de datos
def obtener_duenos():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM duenos")
        duenos = cursor.fetchall()
        return duenos
    except sqlite3.Error as e:
        logging.error(f"Error al obtener dueños: {e}")
        return []
    finally:
        if conn:
            conn.close()

# Función para actualizar los datos de un dueño en la base de datos
def actualizar_dueno(id_dueno, nombre, telefono, direccion):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE duenos SET nombre=?, telefono=?, direccion=? WHERE id=?",
            (nombre, telefono, direccion, id_dueno)
        )
        conn.commit()
        logging.info(f"Dueño con ID {id_dueno} actualizado correctamente.")
    except sqlite3.Error as e:
        logging.error(f"Error al actualizar dueño: {e}")
    finally:
        if conn:
            conn.close()

# Función para eliminar un dueño de la base de datos
def eliminar_dueno(id_dueno):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM duenos WHERE id=?", (id_dueno,))
        conn.commit()
        logging.info(f"Dueño con ID {id_dueno} eliminado correctamente.")
    except sqlite3.Error as e:
        logging.error(f"Error al eliminar dueño: {e}")
    finally:
        if conn:
            conn.close()

# --- Funciones CRUD para Mascotas ---

# Función para insertar una nueva mascota en la base de datos
def insertar_mascota(nombre, especie, raza, edad, id_dueno):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO mascotas (nombre, especie, raza, edad, id_dueno) VALUES (?, ?, ?, ?, ?)",
            (nombre, especie, raza, edad, id_dueno)
        )
        conn.commit()
        logging.info(f"Mascota '{nombre}' insertada correctamente.")
        return cursor.lastrowid
    except sqlite3.Error as e:
        logging.error(f"Error al insertar mascota: {e}")
        return None
    finally:
        if conn:
            conn.close()

# Función para devolver una lista de todas las mascotas con su dueño
def obtener_mascotas():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT m.id, m.nombre, m.especie, m.raza, m.edad, d.nombre, d.telefono, d.direccion
            FROM mascotas m
            JOIN duenos d ON m.id_dueno = d.id
        ''')
        mascotas = cursor.fetchall()
        return mascotas
    except sqlite3.Error as e:
        logging.error(f"Error al obtener mascotas: {e}")
        return []
    finally:
        if conn:
            conn.close()

# Función para actualizar los datos de una mascota en la base de datos
def actualizar_mascota(id_mascota, nombre, especie, raza, edad, id_dueno):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE mascotas SET nombre=?, especie=?, raza=?, edad=?, id_dueno=? WHERE id=?",
            (nombre, especie, raza, edad, id_dueno, id_mascota)
        )
        conn.commit()
        logging.info(f"Mascota con ID {id_mascota} actualizada correctamente.")
    except sqlite3.Error as e:
        logging.error(f"Error al actualizar mascota: {e}")
    finally:
        if conn:
            conn.close()

# Función para eliminar una mascota de la base de datos
def eliminar_mascota(id_mascota):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM mascotas WHERE id=?", (id_mascota,))
        conn.commit()
        logging.info(f"Mascota con ID {id_mascota} eliminada correctamente.")
    except sqlite3.Error as e:
        logging.error(f"Error al eliminar mascota: {e}")
    finally:
        if conn:
            conn.close()

# --- Funciones CRUD para Consultas Veterinarias ---

# Función para insertar una nueva consulta en la base de datos
def insertar_consulta(fecha, motivo, diagnostico, id_mascota):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO consultas (fecha, motivo, diagnostico, id_mascota) VALUES (?, ?, ?, ?)",
            (fecha, motivo, diagnostico, id_mascota)
        )
        conn.commit()
        logging.info(f"Consulta para mascota ID {id_mascota} insertada correctamente.")
        return cursor.lastrowid
    except sqlite3.Error as e:
        logging.error(f"Error al insertar consulta: {e}")
        return None
    finally:
        if conn:
            conn.close()

# Función para devolver una lista de consultas para una mascota específica
def obtener_consultas_por_mascota(id_mascota):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, fecha, motivo, diagnostico FROM consultas WHERE id_mascota=?",
            (id_mascota,)
        )
        consultas = cursor.fetchall()
        return consultas
    except sqlite3.Error as e:
        logging.error(f"Error al obtener consultas: {e}")
        return []
    finally:
        if conn:
            conn.close()

# Función para actualizar los datos de una consulta en la base de datos
def actualizar_consulta(id_consulta, fecha, motivo, diagnostico):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE consultas SET fecha=?, motivo=?, diagnostico=? WHERE id=?",
            (fecha, motivo, diagnostico, id_consulta)
        )
        conn.commit()
        logging.info(f"Consulta con ID {id_consulta} actualizada correctamente.")
    except sqlite3.Error as e:
        logging.error(f"Error al actualizar consulta: {e}")
    finally:
        if conn:
            conn.close()

# Función para eliminar una consulta de la base de datos
def eliminar_consulta(id_consulta):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM consultas WHERE id=?", (id_consulta,))
        conn.commit()
        logging.info(f"Consulta con ID {id_consulta} eliminada correctamente.")
    except sqlite3.Error as e:
        logging.error(f"Error al eliminar consulta: {e}")
    finally:
        if conn:
            conn.close()