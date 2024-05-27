from Conexion import *

class Cclientes:

    def MostrarDatos():
        try:
            cone = Cconexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = "SELECT * FROM usuarios"
            cursor.execute(sql)            
            miresultado = cursor.fetchall()
            cone.commit()
            cone.close()
            return miresultado
        
        except mysql.connector.Error as error:
            print("Error al mostrar de datos {}".format(error))
            return
        cursor.close()
        
        
    def ingresarClientes(nombres,apellidos,sexo):
        
        try:
            cone = Cconexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = "INSERT INTO usuarios (nombres, apellidos, sexo) VALUES (%s, %s, %s)"
            valores = (nombres, apellidos, sexo)
            cursor.execute(sql,valores)
            cone.commit()
            print(cursor.rowcount,"Registro ingresado")
            cone.close()


        except mysql.connector.Error as error:
            print("Error de ingreso de datos {}".format(error))


    def ModificarClientes(idUsuario,nombres,apellidos,sexo):
     try:
            cone = Cconexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = "update usuarios set usuarios.nombres = %s, usuarios.apellidos = %s, usuarios.sexo = %s where usuarios.id = %s;"
            valores = (nombres, apellidos, sexo, idUsuario)
            cursor.execute(sql,valores)
            cone.commit()
            print(cursor.rowcount,"Registro actualizado")
            cone.close()


     except mysql.connector.Error as error:
            print("Error de actualizacion de datos {}".format(error))
     
     
    def EliminarClientes(idUsuario):
     try:
            cone = Cconexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = "Delete from usuarios where usuarios.id = %s;"
            valores = (idUsuario,)
            cursor.execute(sql,valores)
            cone.commit()
            print(cursor.rowcount,"Registro eliminado")
            cone.close()


     except mysql.connector.Error as error:
            print("Error de eliminacion de datos {}".format(error))
        
     cursor.close()  