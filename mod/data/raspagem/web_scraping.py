from data_source.web_source import WebDataSource
from utils.loggers import AppLogger
from entidades.enums import ClasseProcesso, MotivoErro
from entidades.raspagem import Item, DadosExtraidos

class WebScrapingDataAccess():
    """ """
    
    def __init__(self):
        """ """
        self._logger=AppLogger.instance()
        self._web_source=WebDataSource()
        
    # funcoes padrão
        
    def iniciar_sessao(self):
        """ """

        # funcionalidades
        web_source=self._web_source
        
        # verificador
        status=False

        # fluxo de tentativas até que o status seja verdadeiro
        while status == False:
            
            try:
                # inicializar navegador
                web_source.inicializar_navegador()
                
                # realizar login
                assert web_source.realizar_login(), 'Erro ao relizar login'
                
                # verificar sessao
                status=web_source.verificar_sessao_ativa()

            except Exception as e:
                self._logger.warning(f'- Falha ao tentar iniciar a sessao: {e}')
                web_source.terminar_navegador()
    
    def verificar_sessao(self):
        """ """
        
        logger=self._logger
        logger.debug('- Verificando sessão.')
        
        # sessao nao verificada
        if not self._web_source.verificar_sessao_ativa():
            logger.warning('- Sessao nao verificada. Reiniciando sessão...')
            self.iniciar_sessao()
    
    def finalizar_sessao(self):
        """ """
        
        self._web_source.terminar_navegador()
    
    def validar_item(self, item: Item) -> Item:
        """ """

        # funcionalidades
        logger=self._logger
        web_source=self._web_source
        
        # verificar existência do processo
        item.processo_existe=web_source.validar_numero_input(numero=item.numero_input)

        # processo localizado
        if item.processo_existe:
            logger.info('- O processo existe.\n')
            
            # verifica se é precatorio
            item.classe=web_source.validar_classe()
            
            # se é precatório
            if item.classe == ClasseProcesso.Precatorio:
                logger.info('- O processo é da classe precatório.\n')
                
                # numero de input válido
                item.status_input = True

            # não é precatório
            else:
                item.status_input = False
                item.motivo_erro = MotivoErro.OutraClasseProcessual
                logger.warning('- Processo é referente a outra classe.')
        
        # nao localizado
        else:
            item.status_input = False
            item.motivo_erro = MotivoErro.NaoEncontrado
            logger.warning('- O número não é um processo.') 
        
        return item
    
    # funcao que estabelece uma ordem na extracao de dados
    
    def extrair_dados_web(self, numero_input: str) -> DadosExtraidos:
        """ """
        
        # funcionalidades
        logger=self._logger
        web_source=self._web_source
    
        # gerando um objeto dos dados web novo
        dados_web=DadosExtraidos()
    
        logger.debug('- Inicio do fluxo de captura de dados web.')
        
        # acessar dados do processo verificado
        web_source.acessar_detalhes_processo()
        web_source.declarar_ciente()
        
        # capturar numero do processo
        dados_web.numero_apoio=web_source.capturar_numero_processo()
            
        # captura data de autuacao, ano de vencimento e valor da causa
        retorno=web_source.capturar_dados_gerais()
        dados_web.data_autuacao=retorno['data_autuacao']
        dados_web.ano_vencimento=retorno['ano_vencimento']
   
        # capturar dados da aba de partes
        retorno=web_source.capturar_dados_aba_partes(valor_principal=retorno['valor_principal'])
        
        # credor principal
        dados_web.credores.append(retorno['credor']) 
        
        # advogador
        dados_web.advogados=retorno['advogados'] 
        
        # capturar ente-devedor
        dados_web.ente_devedor=retorno['ente_devedor']
        
        # realizar download
        logger.debug('\n- Inicio do download de documentos.')
        retorno=web_source.realizar_download(numero_processo=numero_input)
        dados_web.documento_existe=retorno['documento_existe']
        dados_web.documentos=retorno['documentos']
        logger.debug('\n- Término do download.')
        
        return dados_web