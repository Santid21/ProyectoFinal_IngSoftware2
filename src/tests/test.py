import unittest
from unittest.mock import patch, MagicMock
import mysql.connector
from tkinter import Tk, Entry, ttk
from io import StringIO
import sys
from src.Data_interface.Conexion import Cconexion
from src.User_interface.Interfaz import InterfazFormulario, ActualizarRegistros, GuardarRegistros
from src.Bussines_layer.clientes import Cclientes

# ----------------------------------Pruebas Integracion----------------------------------
class TestInterfazFormulario(unittest.TestCase):
    def test_interfaz(self):
        # Redirigir la salida estándar
        captured_output = StringIO()
        sys.stdout = captured_output

        # Llamar a la función InterfazFormulario
        InterfazFormulario()

        # Esperar un tiempo para que la interfaz se abra completamente
        import time
        time.sleep(1)  # Ajusta este valor según sea necesario

        # Restaurar la salida estándar
        sys.stdout = sys.__stdout__

        # Verificar que la salida contiene "Conexion correcta"
        self.assertIn("Conexion correcta", captured_output.getvalue())

        # Cerrar la ventana después de 5 segundos
        root = Tk()
        root.after(5000, root.destroy)

class TestGuardarRegistros(unittest.TestCase):
    def setUp(self):
        # Configurar el entorno de la prueba
        self.root = Tk()
        global textBoxNombres, textBoxApellidos, combo
        textBoxNombres = Entry(self.root)
        textBoxNombres.insert(0, "John")
        textBoxApellidos = Entry(self.root)
        textBoxApellidos.insert(0, "Doe")
        combo = ttk.Combobox(self.root, values=["Masculino", "Femenino"], state="readonly")
        combo.set("Masculino")

    def tearDown(self):
        # Limpiar el entorno de la prueba
        self.root.destroy()

    def test_guardar_registros(self):
        # Llamar a la función GuardarRegistros con los argumentos necesarios
        GuardarRegistros()

        # Verificar que las cajas de entrada estén vacías después de guardar
        textBoxNombres.destroy()  # Destruir el cuadro de entrada
        textBoxApellidos.destroy()  # Destruir el cuadro de entrada
        self.assertEqual(textBoxNombres.get(), "")
        self.assertEqual(textBoxApellidos.get(), "")

        # Cerrar la ventana después de 5 segundos
        self.root.after(5000, self.root.destroy)

class TestActualizarRegistros(unittest.TestCase):
    def setUp(self):
        # Configurar el entorno de la prueba
        self.root = Tk()
        global textBoxId, textBoxNombres, textBoxApellidos, combo
        textBoxId = Entry(self.root)
        textBoxId.insert(0, "1")
        textBoxNombres = Entry(self.root)
        textBoxNombres.insert(0, "John")
        textBoxApellidos = Entry(self.root)
        textBoxApellidos.insert(0, "Doe")
        combo = ttk.Combobox(self.root, values=["Masculino", "Femenino"], state="readonly")
        combo.set("Masculino")

    def tearDown(self):
        # Limpiar el entorno de la prueba
        self.root.destroy()

    def test_actualizar_registros(self):
        # Llamar a la función ActualizarRegistros
        ActualizarRegistros()

        # Verificar que los campos de entrada estén vacíos después de actualizar
        textBoxId.destroy()  # Destruir el cuadro de entrada
        textBoxNombres.destroy()  # Destruir el cuadro de entrada
        textBoxApellidos.destroy()  # Destruir el cuadro de entrada
        self.assertEqual(textBoxId.get(), "")
        self.assertEqual(textBoxNombres.get(), "")
        self.assertEqual(textBoxApellidos.get(), "")

        # Cerrar la ventana después de 5 segundos
        self.root.after(5000, self.root.destroy)
        
# ----------------------------------Pruebas Unitarias----------------------------------
class TestCconexion(unittest.TestCase):

    @patch('mysql.connector.connect')
    def test_conexion_exitosa(self, mock_connect):
        # Configurar el mock para que simule una conexión exitosa
        mock_conexion = MagicMock()
        mock_connect.return_value = mock_conexion

        conexion = Cconexion.ConexionBaseDeDatos()

        # Verificar que la conexión se realizó correctamente
        mock_connect.assert_called_once_with(user='root', password='santiD2.1', host='127.0.0.1', database='clientesdb', port='3306')
        self.assertEqual(conexion, mock_conexion)

    @patch('mysql.connector.connect')
    def test_conexion_fallida(self, mock_connect):
        # Configurar el mock para que simule una conexión fallida
        mock_connect.side_effect = mysql.connector.Error("Error de conexión")

        conexion = Cconexion.ConexionBaseDeDatos()

        # Verificar que la conexión falló y devolvió None
        mock_connect.assert_called_once_with(user='root', password='santiD2.1', host='127.0.0.1', database='clientesdb', port='3306')
        self.assertIsNone(conexion)


class TestModificarClientes(unittest.TestCase):
    @patch('src.Data_interface.Conexion.Cconexion.ConexionBaseDeDatos')
    def test_modificar_clientes(self, mock_conexion):
        # Configurar el mock
        mock_cone = MagicMock()
        mock_cursor = mock_cone.cursor.return_value
        mock_conexion.return_value = mock_cone

        # Llamar a la función
        Cclientes.ModificarClientes(1, "John", "Doe", "Masculino")

        # Verificar que se ejecutó la consulta con los valores correctos
        sql = "update usuarios set usuarios.nombres = %s, usuarios.apellidos = %s, usuarios.sexo = %s where usuarios.id = %s;"
        valores = ("John", "Doe", "Masculino", 1)
        mock_cursor.execute.assert_called_once_with(sql, valores)
        mock_cone.commit.assert_called_once()
        mock_cone.close.assert_called_once()


class TestEliminarClientes(unittest.TestCase):

    @patch('src.Data_interface.Conexion.Cconexion.ConexionBaseDeDatos')
    def test_eliminar_clientes(self, mock_conexion):
        # Configurar el mock
        mock_cone = MagicMock()
        mock_cursor = mock_cone.cursor.return_value
        mock_conexion.return_value = mock_cone

        # Llamar a la función
        Cclientes.EliminarClientes(1)

        # Verificar que se ejecutó la consulta con los valores correctos
        sql = "Delete from usuarios where usuarios.id = %s;"
        valores = (1,)
        mock_cursor.execute.assert_called_once_with(sql, valores)
        mock_cone.commit.assert_called_once()
        mock_cone.close.assert_called_once()

        # Verificar que el cursor fue cerrado
        mock_cursor.close.assert_called_once()


if __name__ == '__main__':
    unittest.main(exit=False)
