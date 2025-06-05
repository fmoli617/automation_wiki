import re
from entidades.raspagem import DadosExtraidos

def re_search(pattern, s):
    """
    Verifica se o padrão se encontra dentro da string.

    :param pattern: padrão regex
    :param s: string a qual se deseja procurar algo
    :returns: True quando o padrão é identificado.
    """
    
    if re.search(pattern, s, flags=re.I | re.M | re.X):
        return True
    else:
        return False

    
class Document:
    """ """
    
    _tipo = 'DESCONHECIDO'
    
    # regex para verificar se o conteúdo pertence a essa classe
    _regex_validate = None
    # regex para verificar se rejeita o conteúdo para essa classe
    _regex_reject = None
    
    def __init__(self, content: str):
        """ """
        self._content = content
    
    def validate(self) -> bool:
        """
        Valida se o conteúdo pertence a este parser.

        :returns: True quando validado
        """
        if self._regex_validate is not None:
            return re_search(self._regex_validate, self._content)

        return True

    def reject(self) -> bool:
        """
        Indica se o conteúdo deve ser rejeitado.

        :returns: True quando deve ser rejeitado
        """
        if self._regex_reject is not None:
            return re_search(self._regex_reject, self._content)

        return False
          
    def _run_extraction_flow(self, dados_doc: DadosExtraidos) -> DadosExtraidos:
        """
        Adiciona informações do corpo da peticao inicial

        :param peticao_incial: peticao_incial atual
        :returns: peticao_incial atualizado
        """
        
        raise NotImplementedError('Extração do corpo de dados não implementada!')
            
    def parse(self) -> DadosExtraidos:
        """ """

        dados_doc = DadosExtraidos()

        assert self.validate(), 'Este conteúdo não é para este parser'
        
        assert not self.reject(), 'Este conteúdo não é para este parser'
        
        dados_doc = self._run_extraction_flow(dados_doc=dados_doc)
        
        return dados_doc