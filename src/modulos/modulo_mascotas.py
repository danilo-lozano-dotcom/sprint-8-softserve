# Módulo para gestionar mascotas

import logging
import db as db

# Submenú para gestionar mascotas. Permite insertar, listar, actualizar y eliminar mascotas. Además, permite seleccionar un dueño existente para asociar a la mascota
def submenu_mascota():
    while True:
        print("\n--- Gestión de Mascotas ---")
        print("1. Insertar mascota")
        print("2. Listar mascotas")
        print("3. Actualizar mascota")
        print("4. Eliminar mascota")
        print("5. Volver")
        opcion = input("Seleccione una opción: ")
        try:
            if opcion == "1":
                nombre = input("Nombre de la mascota: ")
                especie = input("Especie: ")
                raza = input("Raza: ")
                while True:
                    edad = input("Edad: ")
                    if edad.isdigit() and int(edad) >= 0:
                        edad = int(edad)
                        break
                    print("Por favor, ingrese una edad válida (entero mayor o igual a 0).")
                duenos = db.obtener_duenos()
                if not duenos:
                    print("No hay dueños registrados. Debe registrar un dueño antes de agregar una mascota.")
                    continue
                while True:
                    id_dueno = input("ID del dueño: ")
                    if id_dueno.isdigit() and int(id_dueno) >= 1:
                        id_dueno = int(id_dueno)
                        if any(d[0] == id_dueno for d in duenos):
                            break
                        else:
                            print("El ID del dueño no existe. Intente nuevamente.")
                    else:
                        print("Por favor, ingrese un ID válido (entero mayor o igual a 1).")
                db.insertar_mascota(nombre, especie, raza, edad, id_dueno)
                print("Mascota registrada exitosamente.")
            elif opcion == "2":
                mascotas_db = db.obtener_mascotas()
                print("\n--- Lista de Mascotas ---")
                if not mascotas_db:
                    print("No hay mascotas registradas.")
                else:
                    for m in mascotas_db:
                        print(f"ID: {m[0]}, Nombre: {m[1]}, Especie: {m[2]}, Raza: {m[3]}, Edad: {m[4]}, Dueño: {m[5]}")
            elif opcion == "3":
                mascotas_db = db.obtener_mascotas()
                if not mascotas_db:
                    print("No hay mascotas registradas para actualizar.")
                    continue
                while True:
                    id_mascota = input("ID de la mascota a actualizar: ")
                    if id_mascota.isdigit() and int(id_mascota) >= 1:
                        id_mascota = int(id_mascota)
                        if any(m[0] == id_mascota for m in mascotas_db):
                            break
                        else:
                            print("El ID de la mascota no existe. Intente nuevamente.")
                    else:
                        print("Por favor, ingrese un ID válido (entero mayor o igual a 1).")
                nombre = input("Nuevo nombre: ")
                especie = input("Nueva especie: ")
                raza = input("Nueva raza: ")
                while True:
                    edad = input("Nueva edad: ")
                    if edad.isdigit() and int(edad) >= 0:
                        edad = int(edad)
                        break
                    print("Por favor, ingrese una edad válida (entero mayor o igual a 0).")
                duenos = db.obtener_duenos()
                if not duenos:
                    print("No hay dueños registrados. Debe registrar un dueño antes de actualizar la mascota.")
                    continue
                while True:
                    id_dueno = input("Nuevo ID de dueño: ")
                    if id_dueno.isdigit() and int(id_dueno) >= 1:
                        id_dueno = int(id_dueno)
                        if any(d[0] == id_dueno for d in duenos):
                            break
                        else:
                            print("El ID del dueño no existe. Intente nuevamente.")
                    else:
                        print("Por favor, ingrese un ID válido (entero mayor o igual a 1).")
                db.actualizar_mascota(id_mascota, nombre, especie, raza, edad, id_dueno)
                print("Mascota actualizada exitosamente.")
            elif opcion == "4":
                mascotas_db = db.obtener_mascotas()
                if not mascotas_db:
                    print("No hay mascotas registradas para eliminar.")
                    continue
                while True:
                    id_mascota = input("ID de la mascota a eliminar: ")
                    if id_mascota.isdigit() and int(id_mascota) >= 1:
                        id_mascota = int(id_mascota)
                        if any(m[0] == id_mascota for m in mascotas_db):
                            break
                        else:
                            print("El ID de la mascota no existe. Intente nuevamente.")
                    else:
                        print("Por favor, ingrese un ID válido (entero mayor o igual a 1).")
                confirm = input("¿Está seguro que desea eliminar esta mascota? (S/N): ").strip().lower()
                if confirm == 's':
                    db.eliminar_mascota(id_mascota)
                    print("Mascota eliminada exitosamente.")
                else:
                    print("Eliminación cancelada.")
            elif opcion == "5":
                break
            else:
                print("Opción inválida.")
        except Exception as e:
            print("Error en gestión de mascotas.")
            logging.exception("Error en gestión de mascotas")