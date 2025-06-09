# Módulo para gestionar dueños de mascotas

import logging
import db as db

# Submenú para gestionar dueños de mascotas. Permite insertar, listar, actualizar y eliminar dueños de mascotas
def submenu_dueno():
    while True:
        print("\n--- Gestión de Dueños ---")
        print("1. Insertar dueño")
        print("2. Listar dueños")
        print("3. Actualizar dueño")
        print("4. Eliminar dueño")
        print("5. Volver")
        opcion = input("Seleccione una opción: ")
        try:
            if opcion == "1":
                nombre = input("Nombre del dueño: ")
                telefono = input("Teléfono: ")
                direccion = input("Dirección: ")
                db.insertar_dueno(nombre, telefono, direccion)
                print("Dueño registrado exitosamente.")
            elif opcion == "2":
                duenos = db.obtener_duenos()
                print("\n--- Lista de Dueños ---")
                if not duenos:
                    print("No hay dueños registrados.")
                else:
                    for d in duenos:
                        print(f"ID: {d[0]}, Nombre: {d[1]}, Teléfono: {d[2]}, Dirección: {d[3]}")
            elif opcion == "3":
                while True:
                    id_dueno = input("ID del dueño a actualizar: ")
                    if id_dueno.isdigit() and int(id_dueno) >= 1:
                        id_dueno = int(id_dueno)
                        break
                    print("Por favor, ingrese un ID válido (entero mayor o igual a 1).")
                nombre = input("Nuevo nombre: ")
                telefono = input("Nuevo teléfono: ")
                direccion = input("Nueva dirección: ")
                db.actualizar_dueno(id_dueno, nombre, telefono, direccion)
                print("Dueño actualizado exitosamente.")
            elif opcion == "4":
                while True:
                    id_dueno = input("ID del dueño a eliminar: ")
                    if id_dueno.isdigit() and int(id_dueno) >= 1:
                        id_dueno = int(id_dueno)
                        break
                    print("Por favor, ingrese un ID válido (entero mayor o igual a 1).")
                confirm = input("¿Está seguro que desea eliminar este dueño? (S/N): ").strip().lower()
                if confirm == 's':
                    db.eliminar_dueno(id_dueno)
                    print("Dueño eliminado exitosamente.")
                else:
                    print("Eliminación cancelada.")
            elif opcion == "5":
                break
            else:
                print("Opción inválida.")
        except Exception as e:
            print("Error en gestión de dueños.")
            logging.exception("Error en gestión de dueños")