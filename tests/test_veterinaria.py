# Pruebas unitarias para el sistema de gestión de veterinaria. Estas pruebas verifican el correcto funcionamiento de las clases y funciones del sistema

import sys # Importación del módulo sys para manejar argumentos de línea de comandos y redirección de salida
import os # Importación del módulo os para manejar operaciones del sistema operativo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))) # Inserción de la ruta del directorio src en el inicio de la lista de rutas del sistema para importar módulos desde allí
import unittest # Importación del módulo unittest para realizar pruebas unitarias
from io import StringIO # Importación de "StringIO" del módulo "io" para simular archivos de texto en memoria (útil en pruebas de entrada/salida)
from unittest.mock import patch # Importación de "patch" para sustituir temporalmente funciones u objetos durante pruebas (mocking)
from datetime import datetime # Importación del módulo datetime para manejar fechas y horas
import db # Importación del módulo db que contiene las funciones para interactuar con la base de datos
import persistencia as persistencia # Importación del módulo persistencia que maneja la exportación e importación de datos en formatos CSV y JSON
from persistencia import (guardar_mascotas_csv, guardar_consultas_json,
                         cargar_mascotas_csv, cargar_consultas_json,
                         archivo_csv, archivo_json) # Importación de funciones para guardar y cargar datos en formatos CSV y JSON

# Cambiar a base de datos de pruebas antes de cualquier operación
db.set_db_name('tests/clinica_veterinaria_test.db')
db.crear_tablas() # Creación de tablas en la base de datos de pruebas si no existen

# Clase de pruebas unitarias para el módulo de base de datos
class TestDB(unittest.TestCase):
    def setUp(self):
        # Limpiar tablas antes de cada prueba
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM consultas")
        cursor.execute("DELETE FROM mascotas")
        cursor.execute("DELETE FROM duenos")
        conn.commit()
        conn.close()

    def test_insertar_y_obtener_dueno(self):
        id_dueno = db.insertar_dueno("Juan", "555-1234", "Calle 1")
        duenos = db.obtener_duenos()
        self.assertEqual(len(duenos), 1)
        self.assertEqual(duenos[0][1], "Juan")
        self.assertEqual(duenos[0][2], "555-1234")
        self.assertEqual(duenos[0][3], "Calle 1")

    def test_insertar_y_obtener_mascota(self):
        id_dueno = db.insertar_dueno("Ana", "555-5678", "Calle 2")
        id_mascota = db.insertar_mascota("Luna", "Gato", "Siamés", 2, id_dueno)
        mascotas = db.obtener_mascotas()
        self.assertEqual(len(mascotas), 1)
        self.assertEqual(mascotas[0][1], "Luna")
        self.assertEqual(mascotas[0][2], "Gato")
        self.assertEqual(mascotas[0][3], "Siamés")
        self.assertEqual(mascotas[0][4], 2)
        self.assertEqual(mascotas[0][5], "Ana")

    def test_insertar_y_obtener_consulta(self):
        id_dueno = db.insertar_dueno("Pedro", "555-9999", "Calle 3")
        id_mascota = db.insertar_mascota("Rex", "Perro", "Labrador", 5, id_dueno)
        id_consulta = db.insertar_consulta("2024-01-01", "Vacuna", "Saludable", id_mascota)
        consultas = db.obtener_consultas_por_mascota(id_mascota)
        self.assertEqual(len(consultas), 1)
        self.assertEqual(consultas[0][1], "2024-01-01")
        self.assertEqual(consultas[0][2], "Vacuna")
        self.assertEqual(consultas[0][3], "Saludable")

    def test_actualizar_y_eliminar(self):
        id_dueno = db.insertar_dueno("Laura", "555-0000", "Calle 4")
        db.actualizar_dueno(id_dueno, "Laura Mod", "555-1111", "Calle 44")
        dueno = db.obtener_duenos()[0]
        self.assertEqual(dueno[1], "Laura Mod")
        db.eliminar_dueno(id_dueno)
        self.assertEqual(len(db.obtener_duenos()), 0)

class TestPersistencia(unittest.TestCase):
    def setUp(self):
        
        # Guardar los nombres originales de los archivos
        self._csv_original = persistencia.archivo_csv
        self._json_original = persistencia.archivo_json
        
        # Usar archivos de prueba
        persistencia.archivo_csv = 'test_mascotas.csv'
        persistencia.archivo_json = 'test_consultas.json'
        
        # Limpiar tablas y archivos antes de cada prueba
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM consultas")
        cursor.execute("DELETE FROM mascotas")
        cursor.execute("DELETE FROM duenos")
        conn.commit()
        conn.close()
        if os.path.exists(persistencia.archivo_csv):
            os.remove(persistencia.archivo_csv)
        if os.path.exists(persistencia.archivo_json):
            os.remove(persistencia.archivo_json)

    def tearDown(self):
        # Limpiar archivos después de cada prueba
        if os.path.exists(persistencia.archivo_csv):
            os.remove(persistencia.archivo_csv)
        if os.path.exists(persistencia.archivo_json):
            os.remove(persistencia.archivo_json)
            
        # Restaurar los nombres originales de los archivos
        persistencia.archivo_csv = self._csv_original
        persistencia.archivo_json = self._json_original

    def test_guardar_y_cargar_csv(self):
        id_dueno = db.insertar_dueno("Mario", "555-2222", "Calle 5")
        db.insertar_mascota("Toby", "Perro", "Beagle", 4, id_dueno)
        guardar_mascotas_csv()
        self.assertTrue(os.path.exists(persistencia.archivo_csv))
        # Limpiar y volver a cargar desde CSV
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM mascotas")
        cursor.execute("DELETE FROM duenos")
        conn.commit()
        conn.close()
        cargar_mascotas_csv()
        mascotas = db.obtener_mascotas()
        self.assertEqual(len(mascotas), 1)
        self.assertEqual(mascotas[0][1], "Toby")

    def test_guardar_y_cargar_json(self):
        id_dueno = db.insertar_dueno("Sofía", "555-3333", "Calle 6")
        id_mascota = db.insertar_mascota("Nina", "Gato", "Persa", 3, id_dueno)
        db.insertar_consulta("2024-02-02", "Chequeo", "Bien", id_mascota)
        guardar_consultas_json()
        self.assertTrue(os.path.exists(persistencia.archivo_json))
        # Limpiar y volver a cargar desde JSON
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM consultas")
        conn.commit()
        conn.close()
        cargar_consultas_json()
        consultas = db.obtener_consultas_por_mascota(id_mascota)
        self.assertEqual(len(consultas), 1)
        self.assertEqual(consultas[0][2], "Chequeo")

    def test_cargar_csv_inexistente(self):
        if os.path.exists(persistencia.archivo_csv):
            os.remove(persistencia.archivo_csv)
        # No debe lanzar excepción
        cargar_mascotas_csv()

    def test_cargar_json_inexistente(self):
        if os.path.exists(persistencia.archivo_json):
            os.remove(persistencia.archivo_json)
        # No debe lanzar excepción
        cargar_consultas_json()

# Ejecución de las pruebas unitarias
if __name__ == '__main__':
    unittest.main(verbosity=2)
    
# Comando para ejecución de pruebas desde la terminal: python -m tests.test_veterinaria