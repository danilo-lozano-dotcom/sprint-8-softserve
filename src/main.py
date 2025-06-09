# Módulo central que coordina la ejecución del sistema

import logging # Importación del módulo logging para manejar registros de eventos
from persistencia import guardar_mascotas_csv, guardar_consultas_json, cargar_mascotas_csv, cargar_consultas_json # Importación de funciones para guardar y cargar datos en formatos CSV y JSON
from modulos.modulo_duenos import submenu_dueno # Importación del submenú de dueños
from modulos.modulo_mascotas import submenu_mascota # Importación del submenú de mascotas
from modulos.modulo_consultas import submenu_consulta # Importación del submenú de consultas
import db # Importación del módulo de base de datos para manejar la conexión y creación de tablas


# Configuración del sistema de logging para registrar eventos, errores y excepciones
logging.basicConfig(
    filename='logs/clinica_veterinaria.log',
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s')


# Submenú para gestión de datos (exportar/importar) JSON y CSV. Permite exportar los datos de mascotas y consultas a archivos CSV y JSON, así como importar datos desde estos archivos, con la opción de sobrescribir los datos actuales
def submenu_datos():
    while True:
        print("\n--- Gestión de Datos ---")
        print("1. Exportar datos (CSV/JSON)")
        print("2. Importar datos (CSV/JSON)")
        print("3. Volver")
        opcion = input("Seleccione una opción: ")
        try:
            if opcion == "1":
                guardar_mascotas_csv()
                guardar_consultas_json()
                print("¡Datos exportados exitosamente!")
            elif opcion == "2":
                cargar_mascotas_csv()
                cargar_consultas_json()
                print("\n¡Datos importados exitosamente!")
            elif opcion == "3":
                break
            else:
                print("Opción inválida.")
        except Exception as e:
            print("Error en gestión de datos.")
            logging.exception("Error en gestión de datos")
            
            
# Menú principal de la aplicación
def menu():
    logging.info("Inicio de la aplicación.") # Registro del inicio de la aplicación
    while True:
        print("\n--- Clínica Veterinaria Amigos Peludos ---")
        print("1. Gestionar consultas veterinarias")
        print("2. Gestionar mascotas")
        print("3. Gestionar dueños de mascotas")
        print("4. Gestión de datos")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        # Validación de posibles errores en la entrada del menú
        try:
            if opcion == "1":
                submenu_consulta()
            elif opcion == "2":
                submenu_mascota()
            elif opcion == "3":
                submenu_dueno()
            elif opcion == "4":
                submenu_datos()
            elif opcion == "5":
                print("¡Hasta luego!")
                logging.info("Cierre de la aplicación.") # Registro del cierre de la aplicación
                break
            else:
                print("Opción inválida. Intente de nuevo.\n")
        except Exception as e: # Captura de errores imprevistos en tiempo de ejecución
            print("Error en el menú principal.")
            logging.exception("Error en el menú principal") # Registro de la excepción general
        
            
# Punto de entrada de la aplicación
if __name__ == "__main__":
    
    db.crear_tablas() # Crear las tablas en la base de datos al iniciar la aplicación
    
    menu() # Llamada al menú principal para iniciar la aplicación