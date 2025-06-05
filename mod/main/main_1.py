__description__ = 'Projeto de Raspagem de Dados Web: TJPR - Tribunal de Justiça do Paraná'
__version__ = '3.1.2'
__author__ = 'Squad RPA PJUS - 2023'

import os 
import sys
import time
import argparse
import traceback
import warnings
from utils.loggers import AppLogger
from utils.yaml_config import AppConfig
from servicos.fluxo_procedimentos import FluxoProcedimentos
from test.preparar_proxima import teste_buscar_precatorios
from test.extracao_dados_doc import testar_extracao

def main(acao: str):
    """ """
    
    logger = AppLogger.instance()
    procedimentos = FluxoProcedimentos()
    
    # executar com caracteristicas de teste
    if acao == 'teste':
        logger.debug('>>> Em testes...\n')
        teste_buscar_precatorios()
        procedimentos.executar()

    # executar procedimento completo
    elif acao == 'buscar_precatorio':
        logger.info('>>> Buscar precatórios...\n')
        procedimentos.executar()
    
    # executa apenas o procedimento de gerar output
    elif acao == 'gerar_output':
        logger.info('>>> Gerar output...\n')
        procedimentos.gerar_output()
    
    # solicitação não mapeada
    else:
        logger.error(f'{chr(35)*204}')
        logger.error('>>> Execute informando qual ação você deseja: [buscar_precatorio] ou [gerar_output]')
        logger.error(f'{chr(35)*204}')
    
if __name__ == '__main__':
    
    # forçando a configuração de codificação para utf-8
    if sys.stdout.encoding != 'utf-8-sig':
        sys.stdout.reconfigure(encoding='utf-8-sig')

    # desativar alertas no promt
    warnings.filterwarnings('ignore')
    
    # altera diretório atual para o diretório de execução
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # inicializa logger
    log_filename = os.path.basename(__file__).lower().replace('.py', '.log')
    logger = AppLogger.setup(log_filename=log_filename)

    # inicializa arquivo de configuração
    AppConfig.setup(config_filename='./app_config.yaml')

    # criando argument parser
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('function', type=str, help='Passe a função desejada: [buscar_precatorio], [gerar_output]')
    args = parser.parse_args()

    # informações sobre o projeto
    logger.info(f'\n{chr(35)*204}\n')
    logger.info(f'> Descrição: {__description__}')
    logger.info(f'> Autor:     {__author__}')
    logger.info(f'> Versão:    {__version__}')
    logger.info(f'\n{chr(35)*204}')
    
    # execução     
    try:
        start = time.time()
        logger.info('> Inicio...')
        logger.info(f'{chr(35)*204}\n')
        
        main(args.function)
        
        logger.info(f'\n{chr(35)*204}')
        logger.info('> Fim.')
        logger.debug(f'> Tempo total: {time.time() - start:.2f}s')
        logger.info(f'{chr(35)*204}')
        
    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)