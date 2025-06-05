import os
import datetime
from typing import List

from utils.funcoes_auxiliares import csv_para_dataframe
from utils.yaml_config import get_configuration_by_path
from entidades.raspagem import Item

class InputList():
    """ """
    
    def __init__(self):
        """ Construtor da Classe """

        self._tribunal=get_configuration_by_path('app/tribunal')
        self._estado=get_configuration_by_path('app/estado')
        self._caminho_recursos=get_configuration_by_path('folder_path/recursos')
        self._caminho_temp=get_configuration_by_path('folder_path/temp')
                       
    def _obter_input(self) -> list:
        """ """   
        
        # pasta de input
        pasta=os.path.join(self._caminho_recursos, 'input')
        
        # arquivo de input ainda não denominado
        arquivo_input=None
        
        # arquivo de input considerado como padrão
        arquivo_padrao=os.path.join(pasta, 'input.csv')
        
        # arquivo padrao não existe:
        if not os.path.exists(arquivo_padrao): 
            
            # filtra apenas os arquivos (ignora pastas)
            arquivos=[os.path.join(pasta, arquivo) for arquivo in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, arquivo))]
            
            # ordena os arquivos por data de modificação, do mais recente para o mais antigo
            arquivos.sort(key=lambda x: os.path.getmtime(x), reverse=True)

            # se houver pelo menos um arquivo na pasta
            if arquivos:
                
                # capturando o arquivo mais recente
                arquivo_input=arquivos[0]
                
        # arquivo padrão existe:
        else:
            arquivo_input=arquivo_padrao
        
        
        # arquivo de input definido    
        if arquivo_input:    
            
            # arquivo é do tipo csv
            if '.csv' in arquivo_input or '.CSV' in arquivo_input:
            
                # captura a primeira linha do arquivo
                with open(arquivo_input, mode='r') as file:
                    primeira_linha = file.readline().strip()
                    
                # verifica o cabeçalho do arquivo
                if 'INPUT' in primeira_linha:
                    input_list = csv_para_dataframe(caminho_arquivo=arquivo_input)['INPUT']

                    # se haver pelo menos 1 item, retorna a lista
                    if len(input_list) > 0:
                        return input_list              
    
    def _obter_bloqueio(self) -> list:
        """ """   
        
        arquivo_bloqueio = os.path.join(self._caminho_recursos, 'bloqueio', 'bloqueio.csv')
        
        bloq_list = []
        
        # verificar se existe a existencia do arquivo se sim:
        if os.path.exists(arquivo_bloqueio): 
            
            # captura a primeira linha do arquivo
            with open(arquivo_bloqueio, mode='r') as file:
                primeira_linha = file.readline().strip()
                
            # verifica o cabeçalho do arquivo
            if 'numero_input;motivo_erro' in primeira_linha:
                bloq_df = csv_para_dataframe(caminho_arquivo=arquivo_bloqueio)

                # se haver pelo menos 1 item, retorna a lista
                if len(bloq_df) > 0:
                    bloq_list = bloq_df['numero_input']     
                
        else:
            with open(arquivo_bloqueio, mode='w', newline='') as file:
                file.write('numero_input;motivo_erro\n')
    
        return bloq_list
    
    def preparar_diretorios(self):
        
        # diretorios
        diretorios = [
            self._caminho_temp,
            os.path.join(self._caminho_recursos, 'output'),
            os.path.join(self._caminho_recursos, 'bloqueio'),
            os.path.join(self._caminho_recursos, 'input')
        ]
        
        # percorrer cada diretorio
        for pasta in diretorios:

            #  se não existe
            if not os.path.exists(pasta):
                
                #criar
                os.makedirs(pasta)
                         
    def gerar_lista_itens_raspagem(self) -> List[Item]:
        """ """
        
        # obter lista de inputs e de bloqueio
        input_list=self._obter_input()
        bloq_list=self._obter_bloqueio()

        # se haver itens no arquivo de input
        lista_conciliada=[]
        if input_list is not None:
            lista_conciliada = list(set(input_list) - set(bloq_list))
        
        # preparar lista de objetos de raspagem
        lista_item_raspagem = []    
        for item in lista_conciliada:
        
            item_raspagem = Item(numero_input=str(item), 
                                 tribunal=self._tribunal, 
                                 estado=self._estado, 
                                 data_captura=datetime.datetime.now())
            
            lista_item_raspagem.append(item_raspagem)
        
        # ordenar lista
        lista_item_raspagem = sorted(lista_item_raspagem, key=lambda item: item.numero_input)
        
        return lista_item_raspagem