#Importamos FastAPi
from fastapi import FastAPI, requests, responses, Form
from fastapi.staticfiles import StaticFiles

from typing import Annotated
#Importamos SQLAlchemy
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.model.connection import Connection

#Importamos Jinja2
from jinja2 import Template, Environment, FileSystemLoader

#Llamamos la base de Datos
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/universidad')
Base = declarative_base()

#Creamos las Tablas: Estudiante y Materia
class estudiante(Base):
    __tablename__="estudiante"
    id = Column(Integer, primary_key=True)
    cedula = Column(String(20))
    nombre = Column(String(20))
    apellido = Column(String(20))
    #Relacion con Materia
    materia = relationship("materia", back_populates="estudiante")
    def __str__(self):
         return self.nombre
    
class materia(Base):
    __tablename__="materia"
    id = mapped_column(Integer, primary_key=True)
    nombre = Column(String(20))
    credito = Column(String(20))
    nota = Column(String(20))
    #Relacion con Alumno
    alumno_id = Column(Integer, ForeignKey("estudiante.id"))
    estudiante = relationship("estudiante", back_populates="materia")
    def __str__(self):
         return self.nombre

#Creamos la API
app = FastAPI()
file_loader = FileSystemLoader('src/templates')
env = Environment(loader=file_loader)

# Configura la carpeta "static" para servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

#Llamamos nuestro HTML
@app.get("/")
async def root():
    #Habilitamos una sesión
    Session = sessionmaker(engine)
    session = Session()

    #Creamos las tablas
    Base.metadata.create_all(engine)

    #Consultas
    #Esto equivale a = Select * from [tabla]
    try:
        items = []
        itemsMateria = []
        users = session.query(estudiante).all()
        usersMateria = session.query(materia).all()
        #Guardamos la Materia en una Lista
        for list in users:
            dictionary = {}
            dictionary['id'] = list.id
            dictionary['cedula'] = list.cedula
            dictionary['nombre'] = list.nombre
            dictionary['apellido'] = list.apellido
            items.append(dictionary)
            print(f'Ced.: {list.cedula}, Nombre: {list.nombre} {list.apellido}')
        #Guardamos la Materia en una Lista
        for listMateria in usersMateria:
            dictMateria = {}
            dictMateria['materia_id'] = listMateria.id
            dictMateria['materia_nombre'] = listMateria.nombre
            dictMateria['materia_credito'] = listMateria.credito
            dictMateria['materia_nota'] = listMateria.nota
            print(f'Nombre: {listMateria.nombre}, Credito {listMateria.credito}')
            itemsMateria.append(dictMateria)
    except NoResultFound as Err:
        print("No se ha conseguido nada")
    template = env.get_template('index.html')
    return responses.HTMLResponse(content=template.render(items=items, itemsMateria=itemsMateria))

#Registramos Usuario
@app.post('/estudiante')
async def add_estudiante(cedula: Annotated[str, Form()],nombre: Annotated[str, Form()],apellido: Annotated[str, Form()],
                         name_materia: Annotated[str, Form()],credito: Annotated[str, Form()],nota: Annotated[str, Form()],):
    #Habilitamos una sesión
    Session = sessionmaker(engine)
    session = Session()

    #Vaciamos Datos
    datos = estudiante(
        cedula = cedula,
        nombre = nombre,
        apellido = apellido
    )
    session.add(datos)
    session.commit()

    #Añadimos la Materia
    userCheckID = session.query(estudiante).filter(
        estudiante.cedula == cedula
    ).one()
    datos_materia = materia(
        nombre = name_materia,
        credito = credito,
        nota = nota,
        alumno_id = userCheckID.id
    )
    session.add(datos_materia)
    session.commit()

    #Consultas
    #Esto equivale a = Select * from [tabla]
    try:
        items = []
        itemsMateria = []
        users = session.query(estudiante).all()
        usersMateria = session.query(materia).all()
        #Guardamos la Materia en una Lista
        for list in users:
            dictionary = {}
            dictionary['id'] = list.id
            dictionary['cedula'] = list.cedula
            dictionary['nombre'] = list.nombre
            dictionary['apellido'] = list.apellido
            items.append(dictionary)
            print(f'Ced.: {list.cedula}, Nombre: {list.nombre} {list.apellido}')
        #Guardamos la Materia en una Lista
        for listMateria in usersMateria:
            dictMateria = {}
            dictMateria['materia_id'] = listMateria.id
            dictMateria['materia_nombre'] = listMateria.nombre
            dictMateria['materia_credito'] = listMateria.credito
            dictMateria['materia_nota'] = listMateria.nota
            print(f'Nombre: {listMateria.nombre}, Credito {listMateria.credito}')
            itemsMateria.append(dictMateria)
    except NoResultFound as Err:
        print("No se ha conseguido nada")
    template = env.get_template('index.html')
    return responses.HTMLResponse(content=template.render(items=items, itemsMateria=itemsMateria))

@app.get('/edit/{id}')
async def edit(id):
    #Habilitamos una sesión
    Session = sessionmaker(engine)
    session = Session()

    #Buscamos al Estudiante
    userCheckID = session.query(estudiante).filter(
        estudiante.id == id
    ).one()

    #Consultas
    #Esto equivale a = Select * from [tabla]
    try:
        edit = []
        #Guardamos los Datos del Estudiante
        dictionary = {}
        dictionary['id'] = userCheckID.id
        dictionary['nombre'] = userCheckID.nombre
        dictionary['apellido'] = userCheckID.apellido
        edit.append(dictionary)
        print(f'Editar a: {userCheckID.nombre} {userCheckID.apellido}')
    except NoResultFound as Err:
        print("No se ha conseguido nada")
    template = env.get_template('edit.html')
    return responses.HTMLResponse(content=template.render(edit=edit))

@app.post('/estudiante/edit')
async def user_edit(id: Annotated[int, Form()], cedula: Annotated[str, Form()],nombre: Annotated[str, Form()],apellido: Annotated[str, Form()],
                    name_materia: Annotated[str, Form()],credito: Annotated[str, Form()],nota: Annotated[str, Form()],):
    #Habilitamos una sesión
    Session = sessionmaker(engine)
    session = Session()

    #Buscamos al Estudiante
    userCheckID = session.query(estudiante).filter(
        estudiante.id == id
    ).first()
    materiaCheckID = session.query(materia).filter(
        materia.alumno_id == userCheckID.id
    ).first()
    userCheckID.cedula = cedula
    userCheckID.nombre = nombre
    userCheckID.apellido = apellido
    materiaCheckID.nombre = name_materia
    materiaCheckID.credito = credito
    materiaCheckID.nota = credito
    session.commit()
    #Consultas
    #Esto equivale a = Select * from [tabla]
    try:
        items = []
        itemsMateria = []
        users = session.query(estudiante).all()
        usersMateria = session.query(materia).all()
        #Guardamos la Materia en una Lista
        for list in users:
            dictionary = {}
            dictionary['id'] = list.id
            dictionary['cedula'] = list.cedula
            dictionary['nombre'] = list.nombre
            dictionary['apellido'] = list.apellido
            items.append(dictionary)
            print(f'Ced.: {list.cedula}, Nombre: {list.nombre} {list.apellido}')
        #Guardamos la Materia en una Lista
        for listMateria in usersMateria:
            dictMateria = {}
            dictMateria['materia_id'] = listMateria.id
            dictMateria['materia_nombre'] = listMateria.nombre
            dictMateria['materia_credito'] = listMateria.credito
            dictMateria['materia_nota'] = listMateria.nota
            print(f'Nombre: {listMateria.nombre}, Credito {listMateria.credito}')
            itemsMateria.append(dictMateria)
    except NoResultFound as Err:
        print("No se ha conseguido nada")
    template = env.get_template('index.html')
    return responses.HTMLResponse(content=template.render(items=items, itemsMateria=itemsMateria))

@app.get('/estudiante/delete/{id}')
async def user_delete(id: int):
    #Habilitamos una sesión
    Session = sessionmaker(engine)
    session = Session()
    
    #Borramos Materia
    try:
        #Buscamos la Materia por el ID del Estudiante
        materiaCheckID = session.query(materia).filter(
            materia.alumno_id == id
        ).one()
        session.delete(materiaCheckID)
        session.commit()
        print(f'One Result (Materia): {materiaCheckID.nombre}, {materiaCheckID.credito}')

    except MultipleResultsFound as e:
        print(f'Multiple (Materia): {e}')

    except NoResultFound as e:
        print(f'No Result (Materia): {e}')

    #Borramos Estudiante
    try:
        #Buscamos al Estudiante por su ID
        userCheckID = session.query(estudiante).filter(
            estudiante.id == id
        ).one()
        session.delete(userCheckID)
        session.commit()
        print(f'One Result (Estudiante): {userCheckID.nombre} {userCheckID.apellido}')

    except MultipleResultsFound as e:
        print(f'Multiple (Estudiante): {e}')
        
    except NoResultFound as e:
        print(f'No Result (Estudiante): {e}')
    
    #Consultas
    #Esto equivale a = Select * from [tabla]
    try:
        items = []
        itemsMateria = []
        users = session.query(estudiante).all()
        usersMateria = session.query(materia).all()
        #Guardamos la Materia en una Lista
        for list in users:
            dictionary = {}
            dictionary['id'] = list.id
            dictionary['cedula'] = list.cedula
            dictionary['nombre'] = list.nombre
            dictionary['apellido'] = list.apellido
            items.append(dictionary)
            print(f'Ced.: {list.cedula}, Nombre: {list.nombre} {list.apellido}')
        #Guardamos la Materia en una Lista
        for listMateria in usersMateria:
            dictMateria = {}
            dictMateria['materia_id'] = listMateria.id
            dictMateria['materia_nombre'] = listMateria.nombre
            dictMateria['materia_credito'] = listMateria.credito
            dictMateria['materia_nota'] = listMateria.nota
            print(f'Nombre: {listMateria.nombre}, Credito {listMateria.credito}')
            itemsMateria.append(dictMateria)
    except NoResultFound as Err:
        print("No se ha conseguido nada")
    template = env.get_template('index.html')
    return responses.HTMLResponse(content=template.render(items=items, itemsMateria=itemsMateria))
    template = env.get_template('index.html')
    return responses.HTMLResponse(content=template.render(items=items, itemsMateria=itemsMateria))