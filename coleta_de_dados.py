import pandas as pd
from typing import Generator, Iterable
from functools import lru_cache
from dataclasses import dataclass, field



class Self_Sorting_List():

    __slots__ = "_lista", 

    def __init__(self, vals: Iterable[any] | None = None) -> None:
        
        self._lista: list[any] = list if vals is None else list(vals)
        self._lista.sort()


    def insert(self, val: any, *, final_index:int | None = None, initial_index: int | None = None) -> int:

        # se final_index for None ele recebe o valor len(self._lista) como defaut
        if final_index is None: final_index = len(self._lista)

        # se initial_index for None ele recebe o valor 0 como defaut
        if initial_index is None: initial_index = 0


        # se final_index e initial_index forem iguais só existe uma posição para colocar o val
        if final_index == initial_index:

            self._lista.insert(final_index, val) # inserindo na posição
            return final_index          # retornado a posição


        mid: int = (final_index + initial_index)//2 # ponto medio dos index

        # se o ponto medio tiver o mesmo valor que val, nos colocamos val na posição
        if self._lista[mid] == val:

            self._lista.insert(mid, val) # inserindo na posição
            return mid     # retornando a posição


        # se o ponto medio for maior, como a lista está ordenada, val só pode estar entre initial_index e mid
        elif self._lista[mid] > val:

            return self.insert(val, final_index= mid, initial_index= initial_index) #chamada recursiva com os novos valores e retorno do resultado


        # se o ponto medio for menor, como a lista está ordenada, val só pode estar entre mid e final_index
        elif self._lista[mid] < val:

            return self.insert(val, final_index= final_index, initial_index= mid) #chamada recursiva com os novos valores e retorno do resultado
        
        
    def sort(self) -> None:

        self._lista.sort()


    def pop(self, pos: int | None = None) -> any:

        return self._lista.pop(pos)
    

    def __get__(self, key: int) -> any:
        return self._lista[key]
    

    def __set__(self, key: int, val: any) -> None:
        self._lista[key] = val
    

    def __add__(self, obj: object) -> object:

        # vê se é um iterável
        if isinstance(obj, Iterable):

            i1 = 0 # indice do self
            i2 = 0 # indice do obj
            lista = [] # lista resultante do merge

            obj = sorted(list(obj)) # tranforma o iterável em uma lista ordenada


            # como ambas as listas estão ordenadas podemos usar um merge do merge_sort para junta-lás
            while i1 <= len(self._lista) and i2 <= len(obj):
                if self._lista[i1] <= obj[i2]:
                    lista.append(self._lista[i1])
                    i1 += 1
                else:
                    lista.append(obj[i2])
                    i2 += 1
                
            # coloca o que sobrou na lista
            while i1 <= len(self._lista):
                lista.append(self._lista[i1])
                i1 += 1

            # coloca o que sobrou na lista
            while i2 <= len(obj):
                lista.append(obj[i2])
                i2 += 1

            # transforma em um obj self
            return Self_Sorting_List(lista)
        
        else:
            
            retorno = Self_Sorting_List(self) # cria uma copia do self
            retorno.insert(obj)         # insere o obj
            return retorno          # retorna o obj
            

    def __iter__(self) -> Iterable:
        return iter(self._lista)


    def __next__(self) -> any:
        return next(self._lista)


    @property
    def lista(self) -> list[any]:

        return self._lista
    

    @lista.setter
    def lista(self, vals: Iterable[any] | None = None) -> None:

        self._lista: list[any] = list if vals is None else list(vals)
        self._lista.sort() 


@dataclass(slots=True)
class Participante():

    nome  : str 
    id    : int | None = field(default_factory=str)
    email : str | None = field(default_factory=str)


@dataclass(slots=True)
class Palestrante():

    nome : str
    descricao: str = field(default_factory=str)

    
@dataclass(slots=True)
class Atividade():

    nome: str 
    id: str | None = field(default_factory=str)
    local: str | None = field(default_factory=str)
    data: str | None = field(default_factory=str)
    hora_init: str | None = field(default_factory=str) 
    hora_final: str | None = field(default_factory=str)
    palestrantes: list[str] = field(default_factory=list)
    _participantes: list[Participante] = field(default_factory=list)

    def __post_init__(self) -> None:

        self._participantes.sort()

    @property
    def participantes(self) -> list[Participante]:
        return list(self._participantes)
        
    
    @participantes.setter
    def participantes(self, vals: Iterable[Participante]) -> None:

        self._participantes = list(vals)
        self._participantes.sort()


    

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

    from random import shuffle, choices
    from time import time, sleep

    





    
    

