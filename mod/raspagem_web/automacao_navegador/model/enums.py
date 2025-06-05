from enum import Enum, auto

class TipoNavegador(Enum):
    """ Enumera os tipos de navegadores implementados """
    
    Desconhecido = auto()
    Chrome = auto()
    UndetectedChrome = auto()
    Firefox = auto()
    Edge = auto()