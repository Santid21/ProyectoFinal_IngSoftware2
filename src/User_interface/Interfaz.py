import tkinter as Tk

#import modulos restantes de tkinter

from tkinter import *

from tkinter import ttk,StringVar
from tkinter import  messagebox

from src.Bussines_layer.clientes import Cclientes
from src.Data_interface.Conexion import Cconexion
class FormularioClientes:
 
 global base
 base = None 

 global textBoxId
 textBoxId = None
 
 global textBoxNombres
 textBoxNombres = None

 global textBoxApellidos
 textBoxApellidos = None 
 
 global combo
 combo = None 

 global groupbox
 groupbox = None 
 
 global tree
 tree = None 

def InterfazFormulario():
   global textBoxId
   global textBoxNombres
   global textBoxApellidos
   global combo
   global base 
   global groupbox
   global tree

   try:
     base = Tk()
     base.geometry("1200x300")
     base.title ("formulario python")
     
     groupBox = LabelFrame(base,text="Datos Del Personal",padx=5,pady=5)
     groupBox.grid(row=0,column=0,padx=10,pady=10)

     labelID = Label(groupBox,text="Id:",width=13,font=("arial",12)).grid(row=0,column=0)
     textBoxId = Entry(groupBox)
     textBoxId.grid(row=0,column=1)

     labelNombres = Label(groupBox,text="Nombres:",width=13,font=("arial",12)).grid(row=1,column=0)
     textBoxNombres = Entry(groupBox)
     textBoxNombres.grid(row=1,column=1)

     labelApellidos = Label(groupBox,text="Apellidos:",width=13,font=("arial",12)).grid(row=2,column=0)
     textBoxApellidos = Entry(groupBox)
     textBoxApellidos.grid(row=2,column=1)

     labelSexo = Label(groupBox,text="Sexo:",width=13,font=("arial",12)).grid(row=3,column=0)
     selectSexo = StringVar()
     combo = ttk.Combobox(groupBox,values=["Masculino","Femenino"],textvariable = selectSexo)
     combo.grid(row=3,column=1)
     selectSexo.set("Masculino")

     Button(groupBox,text="Guardar",width=10, command=GuardarRegistros).grid(row=4,column=0)
     Button(groupBox,text="Modificar",width=10, command=ActualizarRegistros).grid(row=4,column=1)
     Button(groupBox,text="Eliminar",width=10,command=EliminacionRegistros).grid(row=4,column=2)

     groupBox = LabelFrame(base,text="Lista del Personal",padx=5,pady=5)
     groupBox.grid(row=0,column=1,padx=5,pady=5)

     #Crear un treeview

     #Configurar columnas

     tree = ttk.Treeview(groupBox,columns=("Id","Nombres","Apellidos","Sexo"),show = "headings",height=5)
     tree.column("# 1",anchor=CENTER)
     tree.heading("# 1",text="Id")
     tree.column("# 2",anchor=CENTER)
     tree.heading("# 2",text="Nombres")
     tree.column("# 3",anchor=CENTER)
     tree.heading("# 3",text="Apellidos")
     tree.column("# 4",anchor=CENTER)
     tree.heading("# 4",text="Sexo")

     #Agregar los datos a la tabla y mostrar la tabla
     for row in Cclientes.MostrarDatos():
        tree.insert("","end",values=row)
     
     tree.bind("<<TreeviewSelect>>", seleccionarRegistro)
     
     tree.pack()

     base.mainloop()

   except ValueError as error:
     print("error al mostrar la interfaz,error:{}".format(error))

def GuardarRegistros():
        
        global textBoxNombres,textBoxApellidos,combo,groupbox

        try:
           if textBoxNombres is None or textBoxApellidos is None or combo is None:
              print("Los widgets no estan initializados")
              return
           nombres = textBoxNombres.get()
           apellidos = textBoxApellidos.get()
           sexo = combo.get() 
           
           Cclientes.ingresarClientes(nombres,apellidos,sexo)
           messagebox.showinfo("informacion","Los datos fueron guardados")

           ActualizarTreeView()

           textBoxNombres.delete(0,END)
           textBoxApellidos.delete(0,END)
         
        except ValueError as error:
           print("Error al ingresar los datos {}".format(error))

def ActualizarTreeView():
   global tree
   try:
   #borrar elementos actuales del treeview
      tree.delete(*tree.get_children())   
   #obtener nuevos datos
      datos = Cclientes.MostrarDatos()
   #insertar los nuevos datos
      for row in datos:
   #Cclientes.MostrarDatos():
         tree.insert("","end",values=row)
   except ValueError as error :
      print("Error al actualizar la tabla {}",format(error))

def seleccionarRegistro(event):
    try:
        itemSeleccionado = tree.focus()

        if itemSeleccionado:
            values = tree.item(itemSeleccionado)["values"]

            # Corregir el nombre de la variable a textBoxId
            textBoxId.delete(0, END)
            textBoxId.insert(0, values[0]) 

            textBoxNombres.delete(0, END)
            textBoxNombres.insert(0, values[1]) 

            textBoxApellidos.delete(0, END)
            textBoxApellidos.insert(0, values[2])
            
            combo.set(values[3])
    except Exception as error:
        print("Error al seleccionar registro:", error)

def ActualizarRegistros():
        
        global textBoxId,textBoxNombres,textBoxApellidos,combo,groupbox

        try:
           if textBoxId is None or textBoxNombres is None or textBoxApellidos is None or combo is None:
              print("Los widgets no estan initializados")
              return
           idUsuario = textBoxId.get()
           nombres = textBoxNombres.get()
           apellidos = textBoxApellidos.get()
           sexo = combo.get() 
           
           Cclientes.ModificarClientes(idUsuario,nombres,apellidos,sexo)
           messagebox.showinfo("informacion","Los datos fueron actualizados")

           ActualizarTreeView()

           textBoxId.delete(0,END)
           textBoxNombres.delete(0,END)
           textBoxApellidos.delete(0,END)
         
        except ValueError as error:
           print("Error al modificar los datos {}".format(error))


def EliminacionRegistros():
        
        global textBoxId, textBoxNombres, textBoxApellidos

        try:
           if textBoxId is None:
              print("Los widgets no estan initializados")
              return
           idUsuario = textBoxId.get()
                      
           Cclientes.EliminarClientes(idUsuario)
           messagebox.showinfo("informacion","Los datos fueron Eliminados")

           ActualizarTreeView()

           textBoxId.delete(0,END)
           textBoxNombres.delete(0,END)
           textBoxApellidos.delete(0,END)

         
        except ValueError as error:
           print("Error al Eliminar los datos {}".format(error))










InterfazFormulario()
