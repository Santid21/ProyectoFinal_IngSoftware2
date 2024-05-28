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
from tkinter import Tk, Entry, Button

from src.Bussines_layer.clientes import Cclientes
from src.Data_interface.Conexion import Cconexion
from src.User_interface.Interfaz import FormularioClientes, GuardarRegistros 





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
