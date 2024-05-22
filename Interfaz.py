import tkinter as Tk

#import modulos restantes de tkinter

from tkinter import *

from tkinter import ttk,StringVar
from tkinter import  messagebox


class FormularioClientes:

 def Formulario():
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

     Button(groupBox,text="Guardar",width=10).grid(row=4,column=0)
     Button(groupBox,text="Modificar",width=10).grid(row=4,column=1)
     Button(groupBox,text="Eliminar",width=10).grid(row=4,column=2)

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



     tree.pack()






     
     
     
     base.mainloop()

  except ValueError as error:
     print("error al mostrar la interfaz,error:{}".format(error))
        
 Formulario()

