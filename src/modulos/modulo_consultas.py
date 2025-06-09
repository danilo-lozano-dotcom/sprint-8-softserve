# Módulo para gestionar consultas veterinarias de mascotas

import logging
import db as db
from datetime import datetime

# Submenú para gestionar consultas de mascotas. Permite insertar, listar, actualizar y eliminar consultas veterinarias asociadas a una mascota específica
def submenu_consulta():
    while True:
        print("\n--- Gestión de Consultas ---")
        print("1. Insertar consulta")
        print("2. Listar consultas de una mascota")
        print("3. Actualizar consulta")
        print("4. Eliminar consulta")
        print("5. Listar todas las consultas")
        print("6. Volver")
        opcion = input("Seleccione una opción: ")
        try:
            if opcion == "1":
                mascotas_db = db.obtener_mascotas()
                if not mascotas_db:
                    print("No hay mascotas registradas. Debe registrar una mascota antes de agendar una consulta.")
                    continue
                while True:
                    id_mascota = input("ID de la mascota: ")
                    if id_mascota.isdigit() and int(id_mascota) >= 1:
                        id_mascota = int(id_mascota)
                        if any(m[0] == id_mascota for m in mascotas_db):
                            break
                        else:
                            print("El ID de la mascota no existe. Intente nuevamente.")
                    else:
                        print("Por favor, ingrese un ID válido (entero mayor o igual a 1).")
                while True:
                    fecha = input("Fecha (YYYY-MM-DD): ")
                    try:
                        datetime.strptime(fecha, "%Y-%m-%d")
                        break
                    except ValueError:
                        print("Formato de fecha inválido. Use YYYY-MM-DD.")
                motivo = input("Motivo: ")
                diagnostico = input("Diagnóstico: ")
                db.insertar_consulta(fecha, motivo, diagnostico, id_mascota)
                print("Consulta agendada exitosamente.")
            elif opcion == "2":
                mascotas_db = db.obtener_mascotas()
                if not mascotas_db:
                    print("No hay mascotas registradas.")
                    continue
                while True:
                    id_mascota = input("ID de la mascota: ")
                    if id_mascota.isdigit() and int(id_mascota) >= 1:
                        id_mascota = int(id_mascota)
                        if any(m[0] == id_mascota for m in mascotas_db):
                            break
                        else:
                            print("El ID de la mascota no existe. Intente nuevamente.")
                    else:
                        print("Por favor, ingrese un ID válido (entero mayor o igual a 1).")
                print(f"\n--- Consultas para la mascota ID {id_mascota} ---")
                consultas = db.obtener_consultas_por_mascota(id_mascota)
                if not consultas:
                    print("No hay consultas registradas para esta mascota.")
                else:
                    for c in consultas:
                        print(f"ID: {c[0]}, Fecha: {c[1]}, Motivo: {c[2]}, Diagnóstico: {c[3]}")
            elif opcion == "3":
                consultas_db = []
                mascotas_db = db.obtener_mascotas()
                for m in mascotas_db:
                    consultas_db.extend(db.obtener_consultas_por_mascota(m[0]))
                if not consultas_db:
                    print("No hay consultas registradas para actualizar.")
                    continue
                while True:
                    id_consulta = input("ID de la consulta a actualizar: ")
                    if id_consulta.isdigit() and int(id_consulta) >= 1:
                        id_consulta = int(id_consulta)
                        if any(c[0] == id_consulta for c in consultas_db):
                            break
                        else:
                            print("El ID de la consulta no existe. Intente nuevamente.")
                    else:
                        print("Por favor, ingrese un ID válido (entero mayor o igual a 1).")
                while True:
                    fecha = input("Nueva fecha: ")
                    try:
                        datetime.strptime(fecha, "%Y-%m-%d")
                        break
                    except ValueError:
                        print("Formato de fecha inválido. Use YYYY-MM-DD.")
                motivo = input("Nuevo motivo: ")
                diagnostico = input("Nuevo diagnóstico: ")
                db.actualizar_consulta(id_consulta, fecha, motivo, diagnostico)
                print("Consulta actualizada exitosamente.")
            elif opcion == "4":
                consultas_db = []
                mascotas_db = db.obtener_mascotas()
                for m in mascotas_db:
                    consultas_db.extend(db.obtener_consultas_por_mascota(m[0]))
                if not consultas_db:
                    print("No hay consultas registradas para eliminar.")
                    continue
                while True:
                    id_consulta = input("ID de la consulta a eliminar: ")
                    if id_consulta.isdigit() and int(id_consulta) >= 1:
                        id_consulta = int(id_consulta)
                        if any(c[0] == id_consulta for c in consultas_db):
                            break
                        else:
                            print("El ID de la consulta no existe. Intente nuevamente.")
                    else:
                        print("Por favor, ingrese un ID válido (entero mayor o igual a 1).")
                confirm = input("¿Está seguro que desea eliminar esta consulta? (S/N): ").strip().lower()
                if confirm == 's':
                    db.eliminar_consulta(id_consulta)
                    print("Consulta eliminada exitosamente.")
                else:
                    print("Eliminación cancelada.")
            elif opcion == "5":
                print("\n--- Listado General de Consultas ---")
                try:
                    mascotas = db.obtener_mascotas()
                    mascotas_dict = {m[0]: (m[1], m[5]) for m in mascotas}  # id_mascota: (nombre_mascota, nombre_dueño)
                    conn = db.conectar()
                    cursor = conn.cursor()
                    cursor.execute("SELECT id, fecha, motivo, diagnostico, id_mascota FROM consultas")
                    consultas = cursor.fetchall()
                    if not consultas:
                        print("No hay consultas registradas.")
                    else:
                        for c in consultas:
                            nombre_mascota, nombre_dueno = mascotas_dict.get(c[4], ("Desconocido", "Desconocido"))
                            print(f"ID: {c[0]}, Fecha: {c[1]}, Motivo: {c[2]}, Diagnóstico: {c[3]}, Mascota: {nombre_mascota}, Dueño: {nombre_dueno}")
                    conn.close()
                except Exception as e:
                    print("Error al listar todas las consultas.")
                    logging.exception("Error al listar todas las consultas")
            elif opcion == "6":
                break
            else:
                print("Opción inválida.")
        except Exception as e:
            print("Error en gestión de consultas.")
            logging.exception("Error en gestión de consultas")