from typing import List
from utils.yaml_config import get_configuration_by_path
from entidades.raspagem import Item, DadosExtraidos
from entidades.credito import Credito, Credor, Advogado
from entidades.enums import TipoProcesso, OrigemDados, TipoCredor, MotivoErro

class ConsolidarOutput():
    """ """
    
    def __init__(self):
        """ """
        self._lista_informacaoes=get_configuration_by_path('app/dados_consolidados')
    
    # funcoes de apoio

    def _comparar_credores(self, credor_validado: Credor, credor_comparado: Credor) -> Credor:
        """ """
        
        # validar nome
        credor_validado.nome_credor=credor_comparado.nome_credor if credor_validado.nome_credor == None else credor_validado.nome_credor
        # validar data
        credor_validado.data_liquidacao=credor_comparado.data_liquidacao if credor_validado.data_liquidacao == '01/01/1900' else credor_validado.data_liquidacao
        # validar valor
        credor_validado.valor_face=credor_comparado.valor_face if credor_validado.valor_face == None else credor_validado.valor_face
        # tipo do credor
        credor_validado.tipo_credor=credor_comparado.tipo_credor if credor_validado.tipo_credor == None else credor_validado.tipo_credor
        # origem dos dados
        credor_validado.origem_dados=OrigemDados.Validado

        return credor_validado
    
    def _extrair_chave_credor(self, credor: Credor) -> str:
        """ """
        return getattr(credor, 'documento_credor')

    def _extrair_lista_chave_validacao(self, credores_obtidos: List[Credor]) -> set:
        """ """
        # lista de documentos a serem verficados
        return set([getattr(credor_obtido,'documento_credor') for credor_obtido in credores_obtidos])
    
    # funcoes de consolidacao
    
    def _consolidar_lista_credores(self, credores_obtidos: List[Credor]) -> List[Credor]:
        """ 
        Tem como aplicar as regras de validação dos dados dos credores que foram obtidos
        
        - para o mesmo documento, o valor_face do documento prevalece (caso identificado), caso contrário considere o valor da web
        
        :param: credores_obtidos: lista de objetos do tipo Credor obtida a partir do serviço de raspagem.
        :returns: lista de objetos do tipo Credor valida
        """

    # lista de retorno
        credores_validados=[]
        
        # obter os documentos que existem dos credores
        chaves=self._extrair_lista_chave_validacao(credores_obtidos=credores_obtidos)
        
        # percorrer cada chave
        for chave in chaves:
            
            # criar um objeto vazio que irá receber os dados
            credor_validado=Credor()
            
            # percorrer a lista de credores obtidos
            for credor in credores_obtidos:
                
                # se o credor possuir a chave de verificacao unica
                if chave == self._extrair_chave_credor(credor=credor):
                    
                    # comparar credores
                    credor_validado=self._comparar_credores(credor_validado=credor_validado, credor_comparado=credor)
            
            credor_validado.documento_credor=chave
            credores_validados.append(credor_validado)    
          
        return credores_validados
        
    def _consolidar_lista_advogados(self, advogados_obtidos: List[Advogado]) -> List[Advogado]:
        """ 
        Tem como aplicar as regras de validação dos dados dos objetos dos advogados recebidos
        
        :param: advogados_obtidos: lista de objetos do tipo Advogado obtida a partir do serviço de raspagem.
        :returns: lista de objetos do tipo Credor valida
        """
        return advogados_obtidos
        
    def _consolidar_credito_padrao(self, item: Item) -> Credito:
        """ """    
            
        # criar um objeto com os dados padroes do item
        credito=Credito(tribunal=item.tribunal,
                        estado_processo=item.estado,
                        data_captura=item.data_captura,
                        numero_precatorio=item.numero_input,
                        tipo_processo=TipoProcesso.Eletronico,
                        motivo_erro=item.motivo_erro)
        return credito   
    
    def _consolidar_lista_creditos(self, credito_padrao: Credito, dicionario_padrao: dict, lista_credores: List[Credor]) -> List[Credito]:
        """ """
        
        # lista de retorno
        creditos=[]
        
        # criar um novo credito com as informações do dicionario padrao
        credito_atualizado=credito_padrao.model_copy(update=dicionario_padrao)
        
        #atualizar dados dos advogados expecificos
        if len(credito_atualizado.advogados) > 0:
            adv_principal=credito_atualizado.advogados[0]
            credito_atualizado.advogado_nome=adv_principal.nome
            credito_atualizado.advogado_documento=adv_principal.documento
            credito_atualizado.advogado_oab=adv_principal.oab
            
        # percorrendo a lista de credores
        for credor in lista_credores:
            creditos.append(credito_atualizado.model_copy(update=credor.model_dump()))
        
        # retornar uma lista de credito
        return creditos
    
    # funcoes principais
    
    def _gerar_creditos(self, credito_padrao: Credito, dados_web: DadosExtraidos, dados_doc: DadosExtraidos) -> List[Credito]:
        """ """

        # dicionario com os dados web
        dict_web=dados_web.model_dump()
        
        # dicionario com os dados doc
        dict_doc=dados_doc.model_dump()
            
        # dicionario de dados consolidado
        dict_consolid=DadosExtraidos().model_dump()
            
        # para cada informacao a ser consolidada
        for informacao in self._lista_informacaoes:
            
            # atualiza o um dicionario novo, dando preferencia para as informações do documento
            dict_consolid[informacao]=dict_doc[informacao] if dict_doc[informacao] != None else dict_web[informacao]

        # lista de advogados validados
        dict_consolid['advogados']=self._consolidar_lista_advogados(advogados_obtidos=dados_web.advogados+dados_doc.advogados)

        # lista de credores validados
        dict_consolid['credores']=self._consolidar_lista_credores(credores_obtidos=dados_web.credores+dados_doc.credores)

        return self._consolidar_lista_creditos(credito_padrao=credito_padrao, dicionario_padrao=dict_consolid, lista_credores=dict_consolid['credores'])
        
    # funcao chamada externamente

    def executar_consolidacao(self, item: Item) -> Item:
        """ """
        
        # gerar credito padrao
        credito=self._consolidar_credito_padrao(item=item)
        
        # nao houve erros durante a extracao de dados
        if item.motivo_erro == MotivoErro.OcrIncompleto or item.motivo_erro == None:
            item.output=self._gerar_creditos(credito_padrao=credito, dados_web=item.dados_web, dados_doc=item.dados_doc)
        
        # houve erros    
        else:
            item.output=[credito]
        
        return item