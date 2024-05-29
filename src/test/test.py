import sys
import os
import unittest
from unittest.mock import patch
import pytest
from dotenv import load_dotenv
import mysql.connector
from unittest.mock import MagicMock
from test import Formulario
from unittest import TestCase
from tkinter import Tk, Entry, Button, ttk,messagebox
global tree
from src.Bussines_layer.clientes import Cclientes, MostrarDatos, Cconexion,ingresarClientes,ModificarClientes,EliminarClientes
from src.Data_interface.Conexion import Cconexion
from src.User_interface.Interfaz import FormularioClientes, GuardarRegistros, ActualizarTreeView,Cclientes,tree,seleccionarRegistro,combo,textBoxId,textBoxApellidos,textBoxNombres,ActualizarRegistros,ActualizarTreeView, EliminacionRegistros






# ----------------------------------Pruebas Integracion----------------------------------

class TestConexionBaseDeDatos:
    @pytest.fixture(scope='module')
    def db_connection(self):
         # Configurar una conexión a la base de datos MySQL para simular la conexión
        conexion = Cconexion.ConexionBaseDeDatos()
        yield conexion
        conexion.close()
    def test_conexion_exitosa(self, db_connection):
        # Verificar si se devuelve una conexión válida
        assert isinstance(db_connection, mysql.connector.connection.MySQLConnection)

    def test_conexion_fallida(self):
        # Configurar una conexión con credenciales incorrectas para simular una conexión fallida
        with pytest.raises(mysql.connector.Error):
            Cconexion.ConexionBaseDeDatos()

class TestFormularioFuncionalidades:
    @staticmethod
    @pytest.fixture
    def formulario():
        root = Tk()
        form = Formulario(root)
        return form

    def test_crear_interfaz(self, formulario):
        # Verificar que se creen los widgets de la interfaz correctamente
        assert formulario.textBoxId.winfo_exists()
        assert formulario.textBoxNombres.winfo_exists()
        assert formulario.textBoxApellidos.winfo_exists()
        assert formulario.combo.winfo_exists()
        assert formulario.tree.winfo_exists()

    def test_guardar_registros(self, formulario):
        # Llamar al método de guardar registros
        formulario.guardar_registros()

class TestGuardarRegistros:
    @pytest.fixture
    def ventana(self):
        # Configuración común para las pruebas
        root = Tk()
        textBoxNombres = Entry(root)
        textBoxApellidos = Entry(root)
        combo = Entry(root)  # Esto es un Entry porque el combo es un Entry según la función GuardarRegistros
        return root, textBoxNombres, textBoxApellidos, combo

    def test_guardar_registros_exitoso(self, ventana):
        # Configurar el estado previo necesario para la prueba
        root, textBoxNombres, textBoxApellidos, combo = ventana
        textBoxNombres.insert(0, "John")
        textBoxApellidos.insert(0, "Doe")
        combo.insert(0, "Masculino")

        # Ejecutar la función que se está probando
        GuardarRegistros()

        # Verificar el comportamiento esperado
        # Puedes realizar verificaciones sobre el estado de la aplicación después de llamar a GuardarRegistros
        # Por ejemplo, verificar si los datos se guardaron correctamente en la base de datos y si se mostró el mensaje de información correcto

    def test_guardar_registros_campos_vacios(self, ventana):
        # Configurar el estado previo necesario para la prueba
        root, textBoxNombres, textBoxApellidos, combo = ventana
        textBoxNombres.insert(0, "")
        textBoxApellidos.insert(0, "")
        combo.insert(0, "")

        # Ejecutar la función que se está probando
        GuardarRegistros()



class TestActualizarTreeView:
    @pytest.fixture
    def ventana(self):
        # Configuración común para las pruebas
        root = Tk()
        tree = ttk.Treeview(root, columns=("Id", "Nombres", "Apellidos", "Sexo"), show="headings")
        tree.heading("#1", text="Id")
        tree.heading("#2", text="Nombres")
        tree.heading("#3", text="Apellidos")
        tree.heading("#4", text="Sexo")
        tree.pack()
        return root, tree

    def test_actualizar_treeview(self, ventana, monkeypatch):
        # Configurar el estado previo necesario para la prueba
        root, tree_widget = ventana

        # Declarar tree como global antes de asignarle el valor
        global tree
        tree = tree_widget

        # Mockear la función Cclientes.MostrarDatos para devolver datos de prueba
        datos_prueba = [("1", "John", "Doe", "Masculino"), ("2", "Jane", "Doe", "Femenino")]
        monkeypatch.setattr(Cclientes, "MostrarDatos", lambda: datos_prueba)

        # Ejecutar la función que se está probando
        ActualizarTreeView()

        # Verificar que los datos en el treeview se actualizaron correctamente
        children = tree.get_children()
        assert len(children) == 2  # Verificamos que se insertaron 2 filas

        # Verificar el contenido de las filas
        row1 = tree.item(children[0])["values"]
        row2 = tree.item(children[1])["values"]
        assert row1 == ["1", "John", "Doe", "Masculino"]
        assert row2 == ["2", "Jane", "Doe", "Femenino"]

    def test_actualizar_treeview_vacio(self, ventana, monkeypatch):
        # Configurar el estado previo necesario para la prueba
        root, tree_widget = ventana

        # Declarar tree como global antes de asignarle el valor
        global tree
        tree = tree_widget

        # Mockear la función Cclientes.MostrarDatos para devolver una lista vacía
        monkeypatch.setattr(Cclientes, "MostrarDatos", lambda: [])

        # Ejecutar la función que se está probando
        ActualizarTreeView()

        # Verificar que no hay filas en el treeview
        children = tree.get_children()
        assert len(children) == 0  # Verificamos que no se insertaron filas

class TestIngresarClientes:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        # Configuración común para las pruebas
        self.nombres = "John"
        self.apellidos = "Doe"
        self.sexo = "Masculino"

    def test_ingresar_clientes_exitoso(self):
        try:
            # Conectar a la base de datos real
            conexion = mysql.connector.connect(user='your_username', password='your_password', host='your_host', database='your_database')
            cursor = conexion.cursor()

            # Llamar a la función bajo prueba
            ingresarClientes(self.nombres, self.apellidos, self.sexo)

            # Verificar que se insertó un registro correctamente
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE nombres = %s AND apellidos = %s AND sexo = %s", (self.nombres, self.apellidos, self.sexo))
            count = cursor.fetchone()[0]
            assert count == 1  # Debería haber un registro insertado

        except mysql.connector.Error as error:
            pytest.fail("Error de conexión a la base de datos: {}".format(error))

        finally:
            # Cerrar la conexión
            cursor.close()
            conexion.close()


class TestModificarClientes:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        # Configuración común para las pruebas
        self.idUsuario = 1
        self.nombres = "John"
        self.apellidos = "Doe"
        self.sexo = "Masculino"

    def test_modificar_clientes_exitoso(self):
        try:
            # Conectar a la base de datos real
            conexion = mysql.connector.connect(user='your_username', password='your_password', host='your_host', database='your_database')
            cursor = conexion.cursor()

            # Llamar a la función bajo prueba
            ModificarClientes(self.idUsuario, self.nombres, self.apellidos, self.sexo)

            # Verificar que se actualizó un registro correctamente
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", (self.idUsuario,))
            result = cursor.fetchone()
            assert result is not None  # Debería haber un registro actualizado
            assert result[1] == self.nombres  # Verificar que los datos se actualizaron correctamente

        except mysql.connector.Error as error:
            pytest.fail("Error de conexión a la base de datos: {}".format(error))

        finally:
            # Cerrar la conexión
            cursor.close()
            conexion.close()            

class TestEliminarClientes:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        # Configuración común para las pruebas
        self.idUsuario = 1  # ID del usuario a eliminar

    def test_eliminar_clientes_exitoso(self):
        try:
            # Conectar a la base de datos real
            conexion = mysql.connector.connect(user='your_username', password='your_password', host='your_host', database='your_database')
            cursor = conexion.cursor()

            # Insertar un registro de usuario para luego eliminarlo
            cursor.execute("INSERT INTO usuarios (id, nombres, apellidos, sexo) VALUES (%s, %s, %s, %s)", (self.idUsuario, 'John', 'Doe', 'Masculino'))
            conexion.commit()

            # Llamar a la función bajo prueba
            EliminarClientes(self.idUsuario)

            # Verificar que el registro se eliminó correctamente
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", (self.idUsuario,))
            result = cursor.fetchone()
            assert result is None  # El registro no debería existir después de eliminarlo

        except mysql.connector.Error as error:
            pytest.fail("Error de conexión a la base de datos: {}".format(error))

        finally:
            # Cerrar la conexión
            cursor.close()
            conexion.close()





# ----------------------------------Pruebas Unitarias----------------------------------
class TestFormularioTree:
    @pytest.fixture
    def formulario(self):
        root = Tk()
        form = Formulario(root)
        root.wait_visibility()
        yield form
        root.destroy()
    
    def test_treeview(self, formulario):  # Agrega 'self' como primer parámetro
        # Verificar que se hayan creado las cuatro columnas
        assert formulario.tree["columns"] == ("Id", "Nombres", "Apellidos", "Sexo")

        # Verificar los encabezados de las columnas
        assert formulario.tree.heading("# 1")["text"] == "Id"
        assert formulario.tree.heading("# 2")["text"] == "Nombres"
        assert formulario.tree.heading("# 3")["text"] == "Apellidos"
        assert formulario.tree.heading("# 4")["text"] == "Sexo"

class TestActualizarRegistros:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        # Configuración común para las pruebas
        self.root = Tk()
        self.textBoxId = Entry(self.root)
        self.textBoxNombres = Entry(self.root)
        self.textBoxApellidos = Entry(self.root)
        self.combo = ttk.Combobox(self.root, values=["Masculino", "Femenino"])

        # Simulación de datos en los campos
        self.textBoxId.insert(0, "1")
        self.textBoxNombres.insert(0, "John")
        self.textBoxApellidos.insert(0, "Doe")
        self.combo.set("Masculino")

        # Simulación de la variable global tree
        global tree
        tree = ttk.Treeview(self.root)

    def test_actualizar_registros_exitoso(self):
        # Simulación de la función ModificarClientes y ActualizarTreeView
        def modificar_clientes_mock(idUsuario, nombres, apellidos, sexo):
            assert idUsuario == "1"
            assert nombres == "John"
            assert apellidos == "Doe"
            assert sexo == "Masculino"

        def actualizar_treeview_mock():
            pass

        # Sustitución de las funciones reales por los mocks
        original_modificar_clientes = Cclientes.ModificarClientes
        original_actualizar_treeview = ActualizarTreeView

        Cclientes.ModificarClientes = modificar_clientes_mock
        ActualizarTreeView = actualizar_treeview_mock

        try:
            ActualizarRegistros()

            # Verificar que los campos de entrada se limpian
            assert self.textBoxId.get() == ""
            assert self.textBoxNombres.get() == ""
            assert self.textBoxApellidos.get() == ""

        finally:
            # Restaurar las funciones originales
            Cclientes.ModificarClientes = original_modificar_clientes
            ActualizarTreeView = original_actualizar_treeview

    def test_widgets_no_inicializados(self):
        # Simulación de widgets no inicializados
        global textBoxId, textBoxNombres, textBoxApellidos, combo
        textBoxId = None
        textBoxNombres = None
        textBoxApellidos = None
        combo = None

        # Llamada a la función bajo prueba
        ActualizarRegistros()
        
class TestEliminarRegistros:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        # Configuración común para las pruebas
        self.root = Tk()
        self.textBoxId = Entry(self.root)

        # Simulación de datos en el campo de entrada
        self.textBoxId.insert(0, "1")

        # Simulación de la variable global tree
        global tree
        tree = None

    def test_eliminar_registros_exitoso(self):
        # Simulación de la función EliminarClientes y ActualizarTreeView
        def eliminar_clientes_mock(idUsuario):
            assert idUsuario == "1"

        def actualizar_treeview_mock():
            pass

        # Sustitución de las funciones reales por los mocks
        original_eliminar_clientes = Cclientes.EliminarClientes
        original_actualizar_treeview = ActualizarTreeView

        Cclientes.EliminarClientes = eliminar_clientes_mock
        ActualizarTreeView = actualizar_treeview_mock

        try:
            EliminacionRegistros()

            # Verificar que los campos de entrada se limpian
            assert self.textBoxId.get() == ""

        finally:
            # Restaurar las funciones originales
            Cclientes.EliminarClientes = original_eliminar_clientes
            ActualizarTreeView = original_actualizar_treeview

    def test_widgets_no_inicializados(self, capsys):
        # Simulación de widgets no inicializados
        global textBoxId, textBoxNombres, textBoxApellidos
        textBoxId = None
        textBoxNombres = None
        textBoxApellidos = None

        # Llamada a la función bajo prueba
        EliminacionRegistros()

        # Capturar la salida de la función print
        captured = capsys.readouterr()

        # Verificar que el mensaje de error se imprime correctamente
        assert "Los widgets no están inicializados" in captured.out

class TestMostrarDatos:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        # Configuración común para las pruebas
        self.mock_resultado = [("1", "John", "Doe", "Masculino"), ("2", "Jane", "Smith", "Femenino")]

    def test_mostrar_datos_exitoso(self, mocker):
        # Mockear la conexión a la base de datos y el cursor
        mock_conexion = mocker.MagicMock()
        mock_cursor = mocker.MagicMock()
        mocker.patch.object(Cconexion, "ConexionBaseDeDatos", return_value=mock_conexion)
        mock_conexion.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = self.mock_resultado

        # Llamar a la función bajo prueba
        resultado = MostrarDatos()

        # Verificar que se llamó a la función de conexión a la base de datos
        Cconexion.ConexionBaseDeDatos.assert_called_once()

        # Verificar que se llamó al método execute con la consulta SQL correcta
        mock_cursor.execute.assert_called_once_with("SELECT * FROM usuarios")

        # Verificar que se llamó al método fetchall
        mock_cursor.fetchall.assert_called_once()

        # Verificar que el resultado es el esperado
        assert resultado == self.mock_resultado

    def test_mostrar_datos_con_error(self, mocker, capsys):
        # Mockear la conexión a la base de datos para simular un error
        mocker.patch.object(Cconexion, "ConexionBaseDeDatos", side_effect=Exception("Error de conexión"))

        # Llamar a la función bajo prueba
        resultado = MostrarDatos()

        # Capturar la salida de la función print
        captured = capsys.readouterr()

        # Verificar que se imprime el mensaje de error adecuado
        assert "Error al mostrar de datos Error de conexión" in captured.out

        # Verificar que se devuelve None
        assert resultado is None


