from enum import Enum, auto

class TipoDocumento(Enum):
    """ """
    
    Desconhecido = auto()
    PeticaoInicial = auto()


class StatusRaspagem(Enum):
    """ """
    
    SemProcessamento = auto()
    Sucesso = auto()
    Erro = auto()
 
class MotivoErro(Enum):from enum import Enum

class OrigemDados(Enum):
    """ """
    
    Desconhecido = 'Desconhecido'
    Web = 'Web'
    Doc = 'Doc'
    Validado = 'Validado'

class TipoDocumento(Enum):
    """ """
    
    Desconhecido = 'Desconhecido'
    PeticaoInicial = 'PeticaoInicial'


class StatusRaspagem(Enum):
    """ """
    
    SemProcessamento = 'SemProcessamento'
    Sucesso = 'Sucesso'
    Erro = 'Erro'
 
class MotivoErro(Enum):
    """ """
    
    ErroNaoMapeado = 'ErroNaoMapeado'
    ErroSessaoTJ = 'ErroSessaoTj'
    NaoEncontrado = 'NaoEncontrado'
    OutraClasseProcessual = 'OutraClasseProcessual'
    RaspagemIncompleta = 'RaspagemIncompleta'
    OcrIncompleto = 'OcrIncompleto'
    SegredoJustica = 'SegredoJustica'
    
class ClasseProcesso(Enum):
    """ """
    
    Precatorio = 'Precatorio'
    OutraClasse = 'OutraClasse'

class TipoProcesso(Enum):
    """ """
    
    Desconhecido = 'Desconhecido'
    Eletronico = 'Eletronico'
    Fisico = 'Fisico'


class NaturezaCredito(Enum):
    """  """
    Desconhecido = 'Desconhecido'
    Alimentar = 'Alimentar'
    Comum = 'Comum'
    
class TipoCredor(Enum):
    """ """
    Desconhecido = 'Desconhecido' 
    Beneficiario = 'Beneficiario' # credor principal
    Advogado = 'Advogado' # outros credores