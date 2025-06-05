import os
import pandas as pd
from typing import List
import ast
from utils.yaml_config import get_configuration_by_path
from utils.funcoes_auxiliares import dataframe_para_csv, csv_para_dataframe
from entidades.enums import MotivoErro
from entidades.raspagem import Item

class ExportarOutput:
    """ """
    
    def __init__(self):
        """ """
        
        caminho_recursos=get_configuration_by_path('folder_path/recursos')
        self._caminho_temp=get_configuration_by_path('folder_path/temp')
        self._caminho_resultado=os.path.join(caminho_recursos, 'output', 'resultado.csv')
        self._caminho_controle=os.path.join(caminho_recursos, 'output', 'controle.csv')
        self._caminho_pasta_output=os.path.join(caminho_recursos, 'output')
        self._caminho_pasta_bloqueio=os.path.join(caminho_recursos, 'bloqueio')
     
    def _gerar_lista_dict_item(self, item: Item) -> List[dict]:
        """ """
        nao_capturado='NÃO CAPTURADO'

        dict_item = item.model_dump()
        dict_item['processo_existe']='SIM' if dict_item['processo_existe'] else 'NÃO'
        dict_item['classe']=dict_item['classe'].name if dict_item['classe'] else ''
        dict_item['dados_web']='CAPTURADO' if dict_item['dados_web'] != None else nao_capturado
        dict_item['dados_doc']='CAPTURADO' if dict_item['dados_doc'] != None else nao_capturado
        dict_item['output']=len(dict_item['output'])
        dict_item['motivo_erro']=dict_item['motivo_erro'].name if dict_item['motivo_erro'] != None else 'SEM ERRO'
        return [dict_item]
         
    def _gerar_lista_dict_creditos(self, item: Item) -> List[dict]:
        """ """
        
        list_result=[]
        for credito in item.output:
            dict_credito=credito.model_dump()
            dict_credito['natureza_credito']=dict_credito['natureza_credito'].name if dict_credito['natureza_credito'] != None else ''
            dict_credito['tipo_credor']=dict_credito['tipo_credor'].name if dict_credito['tipo_credor'] != None else ''
            dict_credito['tipo_processo']=dict_credito['tipo_processo'].name if dict_credito['tipo_processo'] != None else ''
            dict_credito['motivo_erro']=dict_credito['motivo_erro'].name if dict_credito['motivo_erro'] != None else ''
            list_result.append(dict_credito)
        return list_result
    
    def _gerar_csv_resultado(self, item: Item):
        """ """
        
        caminho_arquivo=self._caminho_resultado
        lista_creditos=self._gerar_lista_dict_creditos(item=item)
        if lista_creditos != []:
            df=pd.DataFrame(lista_creditos)
            if os.path.exists(caminho_arquivo):
                df_old=csv_para_dataframe(caminho_arquivo=caminho_arquivo)
                df=pd.concat([df, df_old])
            dataframe_para_csv(data_frame=df, caminho_arquivo=caminho_arquivo)
           
    def _gerar_csv_controle(self, item: Item):
        """ """
    
        caminho_arquivo=self._caminho_controle
        df=pd.DataFrame(self._gerar_lista_dict_item(item=item))
        if os.path.exists(caminho_arquivo):
            df_old=csv_para_dataframe(caminho_arquivo=caminho_arquivo)
            df = pd.concat([df, df_old])
        dataframe_para_csv(data_frame=df, caminho_arquivo=caminho_arquivo)
        
    def _gerar_planilha_geral(self):
        """ """
        
        # caminho do arquivo de resultados
        caminho_arquivo_resultado=self._caminho_resultado
        
        # de para
        de_para={
            'Precatorio': 'numero_precatorio',
            'Processo': 'numero_processo',
            'Valor': 'valor_face',
            'CPF': 'documento_credor',     
            'Nome': 'nome_credor',
            'UF': 'estado_processo',
            'Orgao': 'ente_devedor',
            'Data_Liquidacao': 'data_liquidacao',
            'UF_Proc': 'estado_processo',
            'Advogado': 'advogados',
            'OAB': 'advogados',
            'DataTransitoConhecimento': 'data_transito_conhecimento',
            'DataTransitoExecucao': 'data_transito_execucao',
            'Valor_PSS': 'valor_pss',
            'TipoProcesso': 'tipo_processo',
            'ProcessoDelegado': 'delegado_tj',
            'NaturezaPrecatorio': 'natureza_credito',
            'DataAutuacao': 'data_autuacao',
            'AnoVencimento': 'ano_vencimento',
            'ValorPrincipal': 'valor_principal',
            'ValorJuros': 'valor_juros'
        }
        
        # colunas padroes do df in geral
        df_in_geral=pd.DataFrame(columns=list(de_para.keys()))
        
        # verificando se existe um arquivo de resultado
        if os.path.exists(caminho_arquivo_resultado):
            
            # capturando os dados salvos
            df=csv_para_dataframe(caminho_arquivo=caminho_arquivo_resultado)
        
            # atualizar a coluna de advogados
            df['advogados']=df['advogados'].apply(ast.literal_eval)
        
            # percorrer cada linha do data_frame 
            for indice, linha in df.iterrows():
                nova_linha=pd.DataFrame(columns=list(de_para.keys()))

                if not pd.isna(linha['motivo_erro']): 
                    if linha['motivo_erro'] != 'OcrIncompleto':
                        continue
                
                # percorrendo o de para e atualizando a linha com os demais valores
                for chave, valor in de_para.items():
                    nova_linha[chave]=[linha[valor]]
                
                # atualizando os valores para advogados
                advogados=linha['advogados']
                
                # algum advogado foi encontrado    
                if advogados != []:
                    advogado_nome=advogados[0]['nome']
                    advogado_oab=advogados[0]['oab']
                      
                # se nao foi
                else:
                    advogado_nome=''
                    advogado_oab=''

                # salvando os valores para advogados
                nova_linha['Advogado']=advogado_nome
                nova_linha['OAB']=advogado_oab    
                              
                # concatenando os dados da linha atualizada no data frame final    
                df_in_geral=pd.concat([df_in_geral, nova_linha], ignore_index= True)
            
            # se houver linhas
            if df_in_geral.shape[0] != 0:
                # controle de tentativas de salva
                tentativa=0
                status_salva=False
                
                # tentativa de salva do arquivo
                while status_salva==False:
                    nome_arquivo='00_In_Geral.xlsx' if tentativa == 0 else f'00_In_Geral({tentativa}).xlsx'
                    caminho_arquivo=os.path.join(self._caminho_pasta_output, nome_arquivo)
                    try:
                        # salvar:
                        df_in_geral.to_excel(caminho_arquivo, index=False)
                        status_salva = True
                    except Exception:
                        tentativa=+1
    
    def _gerar_output_padrao(self):
        """ """

        # caminho do arquivo de resultados
        caminho_arquivo_resultado=self._caminho_resultado
        
        # verificando se existe um arquivo de resultado
        if os.path.exists(caminho_arquivo_resultado):
            
            # capturando os dados salvos
            df=csv_para_dataframe(caminho_arquivo=caminho_arquivo_resultado)
        
            # controle de tentativas
            tentativa=0
            status_salva=False
            
            # tentativa de salva do arquivo
            while status_salva == False:
                
                nome_arquivo='output_padrao.xlsx' if tentativa == 0 else f'output_padrao({tentativa}).xlsx'

                caminho_arquivo=os.path.join(self._caminho_pasta_output, nome_arquivo)
                    
                try:
                    # salvar:
                    df.to_excel(caminho_arquivo, index=False)
                    status_salva=True
                    
                except Exception:
                    tentativa=+1
                    
    def persistencia_dados(self, item: Item):
        """ """

        # salvar os dados dele em um csv de acompanhamento
        self._gerar_csv_controle(item=item)
        
        # salvar os creditos em um csv para gerar o output padrao
        self._gerar_csv_resultado(item=item)
               
    def bloqueio(self, item: Item) -> bool:
        """ """
        arquivo_bloqueio=os.path.join(self._caminho_pasta_bloqueio, 'bloqueio.csv')
        
        verificador_bloqueio = False
            
        # o item apresentou algum desses status:    
        if item.motivo_erro == None or item.motivo_erro == MotivoErro.OutraClasseProcessual or item.motivo_erro == MotivoErro.NaoEncontrado:
            
            # salvar o lancamento no arquivo de bloqueio, caso for None, RaspagemIncompleta, ProcessoNaoLocalizado, OutraClasse
            if item.motivo_erro == None:
                motivo_erro='SUCESSO'
            
            else:
                motivo_erro=item.motivo_erro.name    
                
            dados=[[item.numero_input, motivo_erro]]
            df=pd.DataFrame(dados, columns=['numero_input', 'motivo_erro'])
        
            # verificar a existencia do arquivo
            if os.path.exists(arquivo_bloqueio):
            
                # capturar possiveis itens no arquivo
                df_old=csv_para_dataframe(caminho_arquivo=arquivo_bloqueio) 
                df=pd.concat([df_old, df])
                
            # atualizar arquivo de bloqueio
            dataframe_para_csv(data_frame=df, caminho_arquivo=arquivo_bloqueio)
            verificador_bloqueio = True
            
        return verificador_bloqueio    
                      
    def gerar_output(self):
        """ """
        
        # gerar output padrao
        self._gerar_output_padrao()
        
        # gerar in geral
        self._gerar_planilha_geral()