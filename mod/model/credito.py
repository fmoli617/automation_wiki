from pydantic import BaseModel
from typing import List, Optional

from datetime import datetime, date
from entidades.enums import TipoProcesso, NaturezaCredito, TipoCredor, OrigemDados, MotivoErro

class Credor(BaseModel):
    """ """
    
    nome_credor: Optional[str] = None
    documento_credor: Optional[str] = None
    valor_face: Optional[float] = None
    data_liquidacao: Optional[str] = '01/01/1900'
    tipo_credor: Optional[TipoCredor] = None
    origem_dados: Optional[OrigemDados] = None


class Advogado(BaseModel):
    """ """
    
    nome: Optional[str] = None
    documento: Optional[str] = None
    oab: Optional[str] = None

class Credito(BaseModel):
    """ """
    
    tribunal: str
    data_captura: datetime
    nome_credor: Optional[str] = None
    documento_credor: Optional[str] = None
    numero_processo: Optional[str] = None
    numero_precatorio: str
    estado_processo: str
    valor_face: Optional[str] = None
    valor_principal: Optional[str] = None
    valor_juros: Optional[str] = None
    url_arquivo_oficio: Optional[str] = None
    ano_vencimento: Optional[str] = None
    ente_devedor: Optional[str] = None
    tipo_processo: TipoProcesso = TipoProcesso.Desconhecido
    data_liquidacao: Optional[str] = None
    data_autuacao: Optional[str] = None
    processo_coletivo: Optional[str] = None
    quantidade_credores: Optional[int] = None
    delegado_tj: Optional[str] = None
    honorarios_destacados: Optional[str]  = None
    precatorio_pago: Optional[str] = None
    precatorio_cancelado: Optional[str] = None
    precatorio_cedido: Optional[str] = None
    precatorio_penhorado: Optional[str] = None
    ultima_movimentacao_data: Optional[str]= None
    ultima_movimentacao_descricao:Optional[str] = None
    natureza_credito: Optional[NaturezaCredito] = None
    vara: Optional[str] = None
    data_transito_conhecimento: Optional[str]  = None
    data_transito_execucao: Optional[str] = None
    valor_pss: Optional[str] = None
    beneficio_assistencial_loas: Optional[str] = None
    cnis: Optional[str] = None
    meses_rra: Optional[str] = None
    tipo_credor: Optional[TipoCredor] = None
    tipo_honorario: Optional[str] = None
    status_precatorio: Optional[str] = None
    advogado_nome: Optional[str] = None
    advogado_oab: Optional[str] = None
    advogado_documento: Optional[str] = None
    advogados: List[Advogado] = []
    motivo_erro: Optional[MotivoErro] = None