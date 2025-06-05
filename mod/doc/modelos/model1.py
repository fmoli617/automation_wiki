import re
from data_source.documentos.base import Document
from entidades.raspagem import DadosExtraidos, NaturezaCredito, Credor
from entidades.enums import TipoCredor, OrigemDados
from utils.funcoes_auxiliares import extrair_valor_monetario
from utils.data_hora import formatar_string_data, FORMATO_DATA_BRASIL

class Model1(Document):
    """ """
    
    _tipo = 'OFICIO REQUISITÓRIO'
    
    # regex para verificar se o conteúdo pertence a essa classe

    _regex_validate = r"""
    \nNatureza\sdo\sCrédito:\s
    """

    def _extract_natureza_credito(self) -> NaturezaCredito | None:
        """ """
        # capturando texto original
        texto=self._content
        
        # padrao de captura atual
        padrao=r"(Natureza\sdo\sCrédito:\s(?P<natureza>.*))"
        
        # localizar
        match=re.search(padrao, texto)
    
        # localizado
        if match:
            return NaturezaCredito.Comum if 'Comum' in match.group('natureza') else NaturezaCredito.Alimentar
    
    def _extract_numero_processo(self) -> str | None:
        """ """

        # capturando texto original
        texto=self._content

        # padroes de captura do numero do processo
        padroes=[
            r'(Número\sda\sAção:\n(?P<numero>.*))',
            r'(Número\sdos\sAutos\sde\sExecução:\s(?P<numero>.*))'
        ]
        
        # percorrendo cada padrao de captura
        for padrao in padroes:
            
            # localizando ocorrencia
            match=re.search(padrao, texto)

            # padrao localizado
            if match:
                return match.group('numero')

    def _extract_credor_principal(self) -> Credor:
        """ """

        padrao=r""" 
        (Beneficiário:\s(?P<nome_credor>.*)\n)
        ((?P<documento>.*)\n)
        [\s\S]*?\s
        (Total:\n(?P<valor_face>.*)\sem\s)
        ((?P<data_liquidacao>.*)\n)"""
        
        match=re.search(padrao, self._content, flags= re.X)
        
        if match:
            credor=Credor()    
            
            credor.nome_credor=match.group('nome_credor').strip().upper()
            credor.data_liquidacao=formatar_string_data(match.group('data_liquidacao'),formato_saida=FORMATO_DATA_BRASIL)
            credor.documento_credor=match.group('documento')
            credor.valor_face=extrair_valor_monetario(match.group('valor_face'))
            credor.tipo_credor=TipoCredor.Beneficiario
            credor.origem_dados=OrigemDados.Doc

            return credor
    
    def _extract_ente_devedor(self) -> str:
        """ """
        
        # separar o bloco que contem as informacoes da data de liquidacao
        texto_format=self._content.split('Devedor: ')[1]
        texto_format=texto_format.split('\nNúmero da Ação:')[0]
        texto_format=texto_format.replace('\n','').strip().upper()

        return texto_format

    def _run_extraction_flow(self, dados_doc: DadosExtraidos) -> DadosExtraidos:
        """ """
        
        # MANTIVE NESSE OBJETO OFICIO 1 O FLUXO DE EXTRACAO DE DADOS ORIGINAL E SO TENTEI ACOMPLAR ELE NO OBJETO DE DOCUMENTO
        
        # etapa de refatoracao em etapas 3.1.0
        
        # capturar natureza do crédito    
        dados_doc.natureza_credito=self._extract_natureza_credito()
            
        # capturar numero do processo
        dados_doc.numero_processo=self._extract_numero_processo()    

        # adicionar credor principal na lista de credore
        dados_doc.credores.append(self._extract_credor_principal())
        
        # extrair ente devedor
        dados_doc.ente_devedor=self._extract_ente_devedor()
             
        return dados_doc 