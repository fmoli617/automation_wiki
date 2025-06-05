import os, shutil
from utils.loggers import AppLogger
from utils.yaml_config import get_configuration_by_path
from entidades.raspagem import DadosExtraidos
from data_source.documentos.pdf import PdfDataSource
from data_source.documentos.modelos.model1 import Model1

class DocScrapingDataAccess():
    """ """
    
    def __init__(self):
        """ """
        self._logger=AppLogger.instance()
        self._caminho_output_arquivo=os.path.join(get_configuration_by_path('folder_path/recursos'),'output','arquivos')
    
    def _deletar_arquivo_nao_processado(self, caminho_arquivo: str):
        """ """
        # o arquivo existe
        if os.path.exists(caminho_arquivo):
            
            # deletar
            shutil.os.remove(caminho_arquivo)
    
    def _mover_arquivo_processado(self, caminho_arquivo_origem: str) -> str:
        """ """

        # pasta nao existe
        if not os.path.exists(self._caminho_output_arquivo):
            
            # criar pasta
            os.makedirs(self._caminho_output_arquivo)   
        
        # o arquivo existe
        if os.path.exists(caminho_arquivo_origem):
            
            # mover arquivo
            shutil.move(src= caminho_arquivo_origem, dst= self._caminho_output_arquivo)

        # retorna o nome base do arquivo
        return os.path.basename(caminho_arquivo_origem)
        
    def extrair_dados_doc(self, lista_arquivos: list) -> dict:
        """ """
        
        # funcionalidades
        logger = self._logger
        
        # extrair texto do arquivo pdf
        arquivo = lista_arquivos[0]
        conteudo_txt = PdfDataSource().extract_text_pdf(file_pdf= arquivo, limit_pages= 16)
        
        # analisadores disponiveis
        parsers = [
            Model1 # Tabela com maior recorrencia
        ]
        
        # teste
        dados_doc=DadosExtraidos()
        
        # percorrer cada analisador:
        logger.debug('\n- Extraindo dados dos documentos extraídos.')
        for parser in parsers:
            try:
                dados_doc = parser(conteudo_txt).parse()     
                msg_erro=None
                logger.debug(f'\n- Documento do tipo {parser._tipo}.')
                dados_doc.url_arquivo_oficio=self._mover_arquivo_processado(caminho_arquivo_origem=arquivo)
                logger.debug('\n- Arquivo processado, movido para a pasta dedicada no output.')
                logger.info('\n- Dados doc extraídos.')
                
                
            except Exception as e:
                try:
                    logger.warning('- Removendo arquivo não processado') 
                    self._deletar_arquivo_nao_processado(caminho_arquivo=arquivo)
                except Exception:
                    logger.warning('- Falha ao deletar arquivo não processado')    
                
                # mensagem padrão a´pos falha da leitura
                msg_erro=f'- Falha na leitura do documento: {e}'
                logger.warning(msg_erro)
        
        return {'dados_doc': dados_doc, 'msg_erro': msg_erro}