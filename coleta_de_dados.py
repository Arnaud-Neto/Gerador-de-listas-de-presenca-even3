import pandas as pd
from os import path, getcwd
from typing import Generator
import abc





class Participante():

    id    : int | None = None
    nome  : str = None
    email : str | None = None
    evento: str | None = None

    def __init__(self, nome: str, email: str | None = None, evento: str | None = None, id: int | None = None) -> None:
        
        self.id     = id
        self.nome   = nome
        self.email  = email
        self.evento = evento
        

    
    def __str__(self) -> str:

        r = "{Nome = " + self.nome

        r += ",\nEmail = " + self.email if self.email is not None else ""

        r += ",\nEvento = " + self.evento if self.evento is not None else ""

        r += ",\nId = " + self.id if self.id is not None else ""

        r += "}\ntype = " + str(type(self))

        return r

        

    def __repr__(self) -> str:

        r = "{Nome = " + self.nome

        r += ", Email = " + self.email if self.email is not None else ""

        r += ", Evento = " + self.evento if self.evento is not None else ""

        r += ", Id = " + self.id if self.id is not None else ""

        r += "}"

        return r
    


    def __lt__(self,val:object)-> bool:
        if type(val) == type(self):
            return self.nome < val.nome
        raise TypeError(f"Error: type '{type(self)}' can't be conpared to type '{type(val)}'")
    
    def __gt__(self,val:object)-> bool:
        return not (self.__lt__(val) or self.__eq__(val))
    
    def __eq__(self, value: object) -> bool:
        
        if isinstance(value, Participante) and self.nome == value.nome:
            return True
        return False
        


class Atividade_Participantes():
    
    _participantes: list[Participante] = None

    def __init__(self, *participantes: Participante) -> None:

        if len(participantes) == 1 and hasattr(participantes,"__iter__"):
            self._participantes = list(participantes[0])
        else:
            self._participantes = participantes



    def __add__(self, val: object | list[Participante] | Participante) -> object:

        if isinstance(val, Atividade_Participantes):
            return Atividade_Participantes(self._participantes + val._participantes)

        elif isinstance(val, Participante):
            return Atividade_Participantes(self._participantes + [val])

        elif isinstance(val, list) and all(isinstance(n,Participante) for n in val):
            return Atividade_Participantes(self._participantes + val)

        else:
            raise TypeError(f"Error: cant add a '{type(self)}' to a '{type(val)}'")
        
    def __sub__(self, val: object | list[Participante] | Participante) -> object:

        if isinstance(val, Atividade_Participantes):
            return Atividade_Participantes(i for i in self._participantes if i not in val._participantes)

        elif isinstance(val, Participante):
            return Atividade_Participantes(i for i in self._participantes if i != Participante)

        elif isinstance(val, list) and all(isinstance(n,Participante) for n in val):
            return Atividade_Participantes(i for i in self._participantes if i not in val)

        else:
            raise TypeError(f"Error: cant subtract a '{type(self)}' to a '{type(val)}'")
        


    def __get__(self, key: str | int | slice) -> Participante | list[Participante]:

        if isinstance(key, int):
            return self._participantes[key]

        elif isinstance(key, slice):
            return self._participantes[key]

        elif isinstance(key, str):
            return [i for i in self._participantes if i.nome == str]

        else:
            raise TypeError(f"Error: invalid key type '{type(key)}'")

    def __set__(self,key: str | int ,value: Participante) -> None:
        
        if not isinstance(value, Participante):
            raise TypeError(f"invalid value type '{type(value)}'")

        if isinstance(key, int):
            self._participantes[key] = value

        elif isinstance(key, str):
            for i in range(len(self._participantes)):
                if self._participantes[i].nome == key:
                    self._participantes[i] = value

        else:
            raise TypeError(f"Error: invalid key type '{type(key)}'")



    def __iter__(self) -> object:

        self.i = 0
        return self
    
    def __next__(self) -> Participante:

        if self.i < len(self._participantes):
            retorno = self._participantes[self.i]
            self.i += 1
            return retorno



    def sort(self, *, key: None = None, reverse:bool=False) -> None:
        self._participantes.sort(key=key,reverse=reverse)


class Atividade():

    id: int | None = None
    nome: str = None
    hora_init: str | None = None
    hora_final: str | None = None
    local: str | None = None
    data: str | None = None
    _participantes: Atividade_Participantes = None

    def __init__(self,nome: str,
                 hora_init: str | None = None,
                 hora_final: str | None = None,
                 local: str | None = None,
                 data: str | None = None,
                 id: int | None = None,
                 *participantes: Participante
                 ) -> None:
        
        self.id = id
        self.nome = nome
        self.hora_final = hora_final
        self.hora_init = hora_init
        self.data = data
        self.local = local
        self._participantes: Atividade_Participantes = Atividade_Participantes(participantes)



    @property
    def participantes(self) -> Atividade_Participantes:
        return self._participantes
    
    @participantes.setter
    def participantes(self,val: list[Participante] | Atividade_Participantes) -> None:
        
        if isinstance(val, Atividade_Participantes):
            self._participantes: Atividade_Participantes = val

        elif isinstance(val, list) and all(isinstance(n, Participante) for n in val):
            self._participantes: Atividade_Participantes = Atividade_Participantes(val)

        else:
            raise TypeError(f"Error: invalid type '{type(val)}' for propety participantes")



    def __str__(self) -> str:
        raise NotImplemented



    def __repr__(self) -> str:
        raise NotImplemented



    def sort(self, *, key:None = None, reverse:bool = False) -> None:
        self._participantes.sort(key=key,reverse=reverse)



def criar_evento (caminho_participantesXLSX: str = "participantes.xlsx",
                   caminho_atividadesXLSX: str = "atividades.xlsx", /,
                   idParticipante_id: str = "1",
                   idParticipante_nome: str = "3",
                   idParticipante_email: str = "2",
                   idParticipante_evento: str = "4",
                   idAtividade_nome: str = "4",
                   idAtividade_id: str = "1",
                   idAtividade_hora_init: str = "6",
                   idAtividade_hora_final: str = "7",
                   idAtividade_local: str = "8",
                   idAtividade_data: str = "5"
                   ):

    if caminho_participantesXLSX is None: caminho_participantesXLSX = "participantes.xlsx"
    if caminho_atividadesXLSX is None: caminho_atividadesXLSX = "atividades.xlsx"

    #tabela_p = pd.read_excel(caminho_participantesXLSX)
    #tabela_a = pd.read_excel(caminho_atividadesXLSX)

    with pd.read_excel(caminho_participantesXLSX) as tabela_p:
        
        ...



    




if __name__ == "__main__":

    from random import shuffle

    lrand = list(range(100))
    shuffle(lrand)
    lp : list[Participante] = [Participante(f"{i}") for i in lrand]
    print(*lp,sep="\n\n",end="\n\n"+"-"*150)

    input()

    lpr : list[str] = [repr(i) for i in lp]
    print(*lpr,sep="\n\n",end="\n\n"+"-"*150)

    input()

    lpr.sort()
    print(*lpr,sep="\n\n",end="\n\n"+"-"*150)

    input()

    lp.sort()
    print(*lp,sep="\n\n",end="\n\n"+"-"*150)


