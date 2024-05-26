from Conexion import *

class Cclientes:
    

    def ingresarClientes(nombres,apellidos,sexo):
        
        try:
            cone = Cconexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = "insert into usuarios values (null,%s,%s,%s);"
            valores = (nombres,apellidos,sexo)
            cursor.execute(sql.valores)
            cone.commit()
            print(cursor.rowcount,"Registro ingresado")
            cone.close()
            



        except mysql.connector.Error as error:
            print("Error de ingreso de datos {}".format(error))