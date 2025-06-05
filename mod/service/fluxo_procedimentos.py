import time
from datetime import datetime
from typing import List
from entidades.raspagem import Item, MotivoErro
from utils.loggers import AppLogger
from servicos.input import InputList
from servicos.consolidar import ConsolidarOutput
from servicos.output import ExportarOutput
from data_access.web_scraping import WebScrapingDataAccess
from data_access.doc_scraping import DocScrapingDataAccess

class FluxoProcedimentos():
    """ Representa a integração de recursos para a raspagem de dados """
    
    def __init__(self):
        """ Construtor da Classe """
        
        # funcionalidades
        self._logger=AppLogger.instance()
        self._dao_input=InputList()
        self._dao_web=WebScrapingDataAccess()
        self._dao_doc=DocScrapingDataAccess()
        self._dao_consolidar=ConsolidarOutput()
        self._dao_output=ExportarOutput()
    
    def _executar_extracao_tratamento(self, item: Item) -> Item:
        """ """
        
        # inicializadores
        logger=self._logger

        # tentativa de execucao
        try:
                
            # validar número de input
            item=self._dao_web.validar_item(item=item)
            
            # se o numero de input for válido, extrair demais dados
            if item.status_input:
            
                # extracao de dados web
                item.dados_web=self._dao_web.extrair_dados_web(numero_input=item.numero_input)
                logger.info('\n- Dados web extraídos.')

                # extracao de dados de documentos extraidos da web
                retorno=self._dao_doc.extrair_dados_doc(lista_arquivos=item.dados_web.documentos)
                item.dados_doc=retorno['dados_doc']
                if retorno['msg_erro']:
                    item.detalhes_processamento=retorno['msg_erro']
                    item.motivo_erro=MotivoErro.OcrIncompleto
        
        # erro nao mapeado
        except Exception as e:
                
           # procedimentos pós erro
            msg_erro=f'- Erro não mapeado: {e}'
            item.detalhes_processamento=msg_erro
            item.motivo_erro=MotivoErro.ErroNaoMapeado
            logger.error(f'\n{msg_erro}')
        
        return item
        
    def _executar_por_lote(self, list_itens_raspagem: List[Item]):
        """ """
        
        # inicializadores
        logger=self._logger
        dao_output=self._dao_output
        
        # iniciar execucao do lote
        for i, item in  enumerate(list_itens_raspagem):
            
            # indicador de tempo 
            dt_item=datetime.now()
            start_item=time.time()
            logger.info(f'- Inicio: {dt_item.strftime("%Y-%m-%d %H:%M:%S")}.')
            logger.info(f'  Processo: {i+1} de {len(list_itens_raspagem)} - Número do input: {item.numero_input}.\n')
            
            # atualizar data de captura
            item.data_captura = dt_item
            
            # verificar se a sessao esta ativa
            self._dao_web.verificar_sessao()
            logger.info('\n- Sessão ativa.\n')
            
            # executar extração tratamento e persitência de dados
            item=self._executar_extracao_tratamento(item=item)

            # conciliacao de informacoes, e gerar lista de creditos
            item=self._dao_consolidar.executar_consolidacao(item= item)
            logger.info('\n- Dados conciliados.')
            
            # fim do processamento de raspagem de dados
            msg_tempo=f'Tempo total: {time.time() - start_item:.2f}s'
            item.tempo_execucao=msg_tempo
            logger.info('\n- Fluxo de extração e tratamento concluído de dados.')  
    
            # efetuar a persistencia dos dados
            dao_output.persistencia_dados(item=item)
            logger.info('\n- Persitência de dados realizada.')
                
            # efetuar o bloqueio do item
            if dao_output.bloqueio(item=item):
                logger.info('\n- Bloqueio realizado.')
                
            # fim do fluxo principal 
            logger.info(f'\n- Fluxo de processamento do item {item.numero_input} concluído. Tempo total: {time.time() - start_item:.2f}s.')
            logger.info(f'\n{chr(61)*204}')
        
    def gerar_output(self):
        """ """
        self._dao_output.gerar_output()
                
    def executar(self):
        """ """
        
        # funcionalidades, servicos e fonte de dados
        logger=self._logger

        # input
        self._dao_input.preparar_diretorios()
        lista_itens=self._dao_input.gerar_lista_itens_raspagem()
        
        # se houver input válido
        if lista_itens is not None and len(lista_itens) > 0:
            
            logger.info(f'- Quantidade de itens à serem processados: {len(lista_itens)}.\n')
            
            # gerando uma sessao web configurado
            logger.info('- Iniciando sessão.')
            self._dao_web.iniciar_sessao()

            # fluxo de iteracao nos itens da lista de processos
            logger.info('\n- Iniciando análise dos itens encontrados...\n')
            logger.info(f'{chr(61)*204}')
            
            self._executar_por_lote(list_itens_raspagem=lista_itens)
            
            # finalizando qualquer sessao web que possa ter sido aberta durante o processo.
            logger.info('\n- Finalizando qualquer navegador aberto durante o procedimento.')
            self._dao_web.finalizar_sessao()
        
            # gerar ouput_padrao e planilha in_geral ao final do procedimento
            logger.info('- Gerando output.')
            self.gerar_output()
        
        # em caso de não haver input
        else:
            logger.error('- Nenhum processo foi localizado.')
            logger.info('- Nenhum output será gerado. Verificar procedimento de INPUT.')