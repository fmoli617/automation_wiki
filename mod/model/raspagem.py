from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from entidades.enums import ClasseProcesso, MotivoErro, NaturezaCredito
from entidades.credito import Credito, Advogado, Credor


class DadosExtraidos(BaseModel):
    """ """
    
    numero_apoio: Optional[str] = None
    documento_existe: bool = False
    documentos: List[str] = []
    url_arquivo_oficio: Optional[str] = None
    
    natureza_credito: Optional[NaturezaCredito] = None
    numero_processo: Optional[str] = None
    data_autuacao: Optional[str] = None
    ano_vencimento: Optional[str] = None
    ente_devedor: Optional[str] = None
    
    vara: Optional[str] = None
    valor_principal: Optional[str] = None
    data_transito_conhecimento: Optional[str] = None
    data_transito_execucao: Optional[str] = None
    meses_rra: Optional[str] = None
    valor_juros: Optional[str] = None
    
    credores: List[Credor] = []
    advogados: List[Advogado] = []
      
class Item(BaseModel):
    """ """
    numero_input: str
    tribunal: str
    estado: str
    data_captura: datetime
    processo_existe: bool = False
    classe: Optional[ClasseProcesso] = None
    status_input: Optional[bool] = None    
    dados_web: Optional[DadosExtraidos] = None
    dados_doc: Optional[DadosExtraidos] = None
    output: List[Credito] = []
    detalhes_processamento: Optional[str] = None
    motivo_erro: Optional[MotivoErro] = None
    tempo_execucao: Optional[str] = None