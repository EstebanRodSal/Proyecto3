from agenda import agenda as Agenda, lista as Lista, persona as Persona
from datetime import datetime

class MiAgenda(Agenda):
    def __init__(self,titulo:str,fecha:datetime) -> None:
        super().__init__()
        self.titulo:str=titulo
        self.fecha:datetime=fecha
        self.participantes:MiPersona

    def agregar_participante(self, nombre: str, apellido1: str, apellido2: str):
        if self.participantes==None:
            self.participantes=MiPersona(nombre=nombre,apellido1=apellido1,apellido2=apellido2)
        else:
            self.participantes.agregar(nombre,apellido1,apellido2)
    @property
    def asDict(self):
        return {"Título":self.titulo,"fecha":self.fecha.__str__(),"participantes":self.participantes.asList}


class MiLista(Lista):
    def __init__(self) -> None:
        super().__init__()
    
    def _agregar(self,r,e):
        if self==None:
            return e
        else:
            self.sig=self._agregar(r.sig,e)

class MiPersona(Persona):
    def __init__(self, nombre: str, apellido1: str, apellido2: str) -> None:
        super().__init__(nombre, apellido1, apellido2)

    def agregar (self,nombre: str, apellido1: str, apellido2: str):
        nueva_persona= MiPersona(nombre,apellido1,apellido2)
        self._agregar(self,nueva_persona)

    def _agregar(self,r,p):
        if r==None:
            return p
        else:
            r.sig=self._agregar(r.sig,p)
    @property
    def asList(self):
        if self==None:
            return []
        else:
            return self._asList(self)
        
    def _asList(self,r):
        r:MiPersona=r
        if r.sig==None:
            return [r.__str__()]
        else:
            return [r.__str__()]+self._asList(r.sig)
    
    def __str__(self) -> str:
        return ("{0} {1} {2}".format(self.nombre,self.apellido1,self.apellido2))

miAgenda=MiAgenda(fecha=datetime.today(),titulo='Semana 16')
miAgenda.agregar_participante('Leonardo','Víquez','Acuña')
miAgenda.agregar_participante('Rita','Días','Saenz')

pass