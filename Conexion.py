import mysql.connector

class Cconexion:
    
    
 def ConexionBaseDeDatos():
     try:
         conexion = mysql.connector.connect(user='root',password='santiD2.1',
                                       host='127.0.0.1',
                                       database='clientesdb',
                                       port='3306',)
         print("Conexion correcta")

         return conexion



     except mysql.connector.Error as error:
         print("Error al conectarte a la base de datos{}".format(error))

         return conexion
        
conexion = Cconexion.ConexionBaseDeDatos()

        
