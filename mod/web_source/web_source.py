
import requests, time, os, re
from typing import List
from utils.automacao_navegador.navegacao_web import NavegacaoWeb
from utils.yaml_config import get_configuration_by_path
from utils.funcoes_auxiliares import calcular_ano_vencimento
from entidades.enums import ClasseProcesso, TipoCredor, OrigemDados
from entidades.credito import Advogado, Credor

class WebDataSource():
    """ """
    
    def __init__(self) -> None:
        """ """
        
        self._navegador=NavegacaoWeb()    
        self._url_padrao=get_configuration_by_path('url/padrao')
        self._pasta_download=get_configuration_by_path('folder_path/temp')
        
    # funcoes de apoio
    
    def _verificar_estabilidade_url(self):
        """ """
        
        # verificador
        status=False
        
        # tentar até o site ficar estável
        while status == True:
            
            # verificando se a url de login está ativa
            resposta=requests.get(self._url_padrao)
            
            # se ok finaliza while
            if resposta.status_code == 200:
                status=True
            # aguardar para a próxima checagem
            else:
                time.sleep(15)
    
    def _clicar_acesso_certificado(self):
        
        # obter sessao aberta
        sessao_web=self._navegador.obter_sessao()

        # recarregar pagina
        sessao_web.recarregar_pagina()
        
        # trocar para frame principal       
        frame_principal = sessao_web.encontrar_elemento(localizador_elemento='mainFrame', tipo_elemento='ID')
        sessao_web.trocar_para_frame(elemento_iframe= frame_principal)
    
        # clicar no botão para acesso via certificado
        sessao_web.encontrar_elemento(localizador_elemento='//body[@id="mainPage"]/div[contains(@class, "flex-container-main")]/div[contains(@class, "flex-container")]/div[contains(@class, "signOnMenu")]/div[contains(@class, "areaLogin")]/ul/li[contains(@class, "certificado")]', tipo_elemento='XPATH').click()

    def _pesquisar_processo(self, numero: str):
        """ """
        
        # abrir sessao ativa
        sessao_web=self._navegador.obter_sessao()

        # etapa de preenchimento e pesquisar a existência do processo 
        sessao_web.trocar_frames(frame_value= 'iframe', index= 0)
        
        # localizar caixa de texto
        caixa_text_processo=sessao_web.encontrar_elemento(localizador_elemento="//td/input[@name='numeroProcesso']", tipo_elemento='XPATH')
        
        
        # percorrer e enviar digito por digito
        for i in numero:
            # preecher caixa com o numero
            caixa_text_processo.send_keys(i)
        
        # clicar em pesquisar
        sessao_web.encontrar_elemento(localizador_elemento= "//td/input[@id='pesquisar']", tipo_elemento='XPATH').click()
     
    def _capturar_polo_ativo(self) -> dict:
        """ """
        
        # abrir sessao ativa
        sessao_web=self._navegador.obter_sessao()       
        
        # colunas contendo os dados do polo ativo
        colunas_polo_ativo=sessao_web.encontrar_lista_elementos(localizador_elemento='//*[@id="includeContent"]/table[1]/tbody//td', tipo_elemento='XPATH')
        
        # dados polo_ativo
        polo_ativo={
            'credor': {
                'nome_credor': colunas_polo_ativo[1].text,
                'documento_credor': colunas_polo_ativo[3].text,
                'documento_adicional': colunas_polo_ativo[2].text
            },
            'advogados': []
        }
        
        # extrair lista de advogados
        lista_dados_advogados=colunas_polo_ativo[5].text.split("\n")
        
        for advogado in lista_dados_advogados:
            
            try: 
                dict_advogado={
                    'nome': advogado.split(" - ")[1].strip().upper(),
                    'oab': advogado.split(" - ")[0].strip()
                    }
            
                polo_ativo['advogados'].append(dict_advogado)
            
            except Exception:
                pass
    
        return polo_ativo
        
    def _capturar_polo_passivo(self) -> dict:
        """ """

        # abrir sessao ativa
        sessao_web=self._navegador.obter_sessao() 
        
        # colunas contendo os dados do polo passivo
        colunas_polo_passivo=sessao_web.encontrar_lista_elementos(localizador_elemento='//*[@id="includeContent"]/table[2]/tbody//td', tipo_elemento='XPATH')
        
        # formatar nome
        nome_ente=str(colunas_polo_passivo[1].text)
        nome_ente=nome_ente.replace('(citação online)','').strip()
        
        # dados polo_ativo
        polo_passivo={
            'ente_devedor': nome_ente,
            'documento': colunas_polo_passivo[3]
            
        }
        
        return polo_passivo 
    
    def _formartar_credor_principal(self, dict_credor: dict, valor_face: float) -> Credor:
        """ """
        
        credor=Credor()
        credor.nome_credor=str(dict_credor['nome_credor']).upper().strip()
        credor.documento_credor=dict_credor['documento_credor']
        credor.valor_face=valor_face
        credor.tipo_credor=TipoCredor.Beneficiario
        credor.origem_dados=OrigemDados.Web 
        return credor
    
    def _formartar_lista_advogados(self, lista_advogados: list) -> List[Advogado]:
        """ """
        
        lista_retorno=[]
        for advogado in lista_advogados:
            advogado_obj = Advogado(**advogado)
            lista_retorno.append(advogado_obj)
        return lista_retorno
      
    def _tratar_arquivo_baixado(self, titulo_documento: str) -> str:
        """ """
        
        pasta=self._pasta_download
        
        # Filtra apenas os arquivos (ignora pastas) e verifica se são arquivos PDF
        arquivos_pdf=[os.path.join(pasta, arquivo) for arquivo in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, arquivo)) and arquivo.lower().endswith(('.pdf', '.PDF'))]

        # Ordena os arquivos por data de modificação, do mais recente para o mais antigo
        arquivos_pdf.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        # se houver pelo menos um arquivo na pasta
        if arquivos_pdf:
            
            # arquivo a ser movido, o ultimo baixado    
            arquivo_origem=arquivos_pdf[0]
            
            # arquivo destino, onde sera deixado o documento
            arquivo_destino=os.path.join(pasta, titulo_documento)
            
            if os.path.exists(arquivo_destino):
                
                nome_do_arquivo=str(os.path.basename(arquivo_destino))
                nome_base=nome_do_arquivo.split('.')[0]
                arquivo_destino=os.path.join(pasta, f'{nome_base}-(1).pdf')
                
            # renemar  o ultimo arquivo para a pasta especifica
            os.rename(arquivo_origem, arquivo_destino)
            
            # retorna o caminho do arquivo movido
            return arquivo_destino  
         
    # funcoes chamadas externamente
    
    # funcoes padroes (com especificidades para cada tribunal)
    
    def inicializar_navegador(self):
        """ """

        # aguardar site estável
        self._verificar_estabilidade_url()
        
        # abrir o navegador
        sessao_web=self._navegador.iniciar_sessao(**get_configuration_by_path('navegador_config')) 

        # abrir url padrao
        sessao_web.acessar_url(self._url_padrao)
    
    def realizar_login(self) -> bool:
        """ """    
        
        # abrir sessao ativa
        sessao_web=self._navegador.obter_sessao()

        # acessar url padrao
        sessao_web.acessar_url(self._url_padrao)
        
        # clicar no login via certificado
        self._clicar_acesso_certificado()

        # se algum login acontecer corretamente
        return True
    
    def verificar_sessao_ativa(self):
        """ """

        # abrir sessao ativa
        #sessao_web=self._navegador.obter_sessao()
    
        return True
    
    def terminar_navegador(self):
        """ """
        
        self._navegador.finalizar_todas_sessoes()
    
    def validar_numero_input(self, numero: str) -> bool:
        """ """

        # abrir sessao ativa
        sessao_web=self._navegador.obter_sessao()

        # fluxo de tentativas para o preenchimento dos numeros de processo
        status_preechimento=False
        
        # enquanto o status de preenchimento não for verdadeiro, repetir bloco de pesquisa de numero
        while status_preechimento == False:
            
            # recarregar pagina
            sessao_web.recarregar_pagina()
            
            # reiniciar o procedimento de acesso da pagina padrão
            self._clicar_acesso_certificado()
            
            # direcionar sistema interno para o servico de buscar processo 
            sessao_web.encontrar_elemento(localizador_elemento="//a[@name='projudiMenu'][contains(text(), 'Buscas')]", tipo_elemento='XPATH').click()
            sessao_web.encontrar_elemento(localizador_elemento="//a[@name='projudiMenu'][contains(text(), 'Processos 1º Grau')]", tipo_elemento='XPATH').click()
            
            # preencher numero 
            self._pesquisar_processo(numero=numero)
            
            # localizar elemento da tabela e extrair a primeira linha
            linha_tabela=sessao_web.encontrar_elemento(localizador_elemento= '//table[contains(@class,"resultTable")]/tbody/tr[1]', tipo_elemento='XPATH') 
            
            # verificar se houve o click de pesquisa
            if linha_tabela:
                status_preechimento=True
            else:
                # se nao localizado, aguardar 2 segundos e tentar a pesquisa novamente
                time.sleep(2)
            
        # capturar o texto da linha localizada anteriormente
        texto_linha=linha_tabela.text
            
        # logica para retornar a validade do numero do processo
        return True if 'Nenhum registro encontrado' not in  texto_linha else False
    
    def validar_classe(self) -> ClasseProcesso:
        """ """
         
        # abrir sessao ativa
        sessao_web=self._navegador.obter_sessao()
        
        # localizar elemento da tabela e extrair a primeira linha
        linha_tabela=sessao_web.encontrar_elemento(localizador_elemento= '//table[contains(@class,"resultTable")]/tbody/tr[1]', tipo_elemento='XPATH') 
        texto_linha=linha_tabela.text
        
        # logica para retornar a classe do processo
        return ClasseProcesso.Precatorio if 'Precatório' in texto_linha else ClasseProcesso.OutraClasse
        
    # funcoes especificas
    
    def acessar_detalhes_processo(self):
        """ """
        
        # obter sessao aberta
        sessao_web=self._navegador.obter_sessao()
        
        # localizar o primeiro elemento da tabela e clicar no link da primeira linha
        linha_tabela=sessao_web.encontrar_elemento(localizador_elemento= '//table[contains(@class, "resultTable")]/tbody/tr[1]/td[2]/a[1]',tipo_elemento= 'XPATH')
        
        # link existe
        if 'projudi/processo.do?_tj=' in linha_tabela.get_attribute('href'):
            
            # acessa pagina com os detalhes do processo
            linha_tabela.click()
        
    def declarar_ciente(self):
        """ """
        
        # obter sessao aberta
        sessao_web=self._navegador.obter_sessao()
    
        # abrir janela de aceite de termo de responsabilidade
        botao_janela=sessao_web.encontrar_elemento(localizador_elemento="//td/input[@name='habilitacaoProvisoriaButton']", tipo_elemento='XPATH')
        
        # botao de declarar ciente existe
        if botao_janela:
            
            # clicar no botao
            botao_janela.click()
            
            # marcar caixa de seleção
            sessao_web.encontrar_elemento(localizador_elemento= "//td//input[@id='termoAceito']", tipo_elemento= 'XPATH').click()
            
            # salvar registro
            sessao_web.encontrar_elemento(localizador_elemento= "//td//input[@name='saveButton']", tipo_elemento= 'XPATH').click()
            
    def capturar_numero_processo(self) -> str:
        """ """

        # obter sessao aberta
        sessao_web=self._navegador.obter_sessao()
        
        # localizar cabeçalho
        cabecalho=sessao_web.encontrar_elemento(localizador_elemento='informacoesProcessuais', tipo_elemento='ID')
        linhas=sessao_web.encontrar_lista_elementos(localizador_elemento='a', tipo_elemento='TAG_NAME',navegar_elemento=cabecalho)

        # localizar numero
        for linha in linhas:
            if 'Eletrônico' in linha.text:
                return linha.text.split(" ")[3]
            
    def capturar_dados_gerais(self) -> dict:
        """ """
        
        # dicionario de dados de retorno
        dict_result={
            'data_autuacao': None,
            'ano_vencimento': None,
            'valor_principal': None
        }
        
        # obter sessao aberta
        sessao_web=self._navegador.obter_sessao()
        
        # clicar na aba de informacoes gerais
        aba_info_gerais=sessao_web.encontrar_elemento(localizador_elemento='tabItemprefix0', tipo_elemento='ID')
        aba_info_gerais.click()
        data_autuacao=sessao_web.encontrar_elemento(localizador_elemento='//*[@id="includeContent"]/fieldset/table/tbody/tr[2]/td[2]', tipo_elemento='XPATH').text
        dict_result['data_autuacao'] = data_autuacao.split(" ")[0]
        if dict_result['data_autuacao']:
            ano_vencimento = calcular_ano_vencimento(data_autuacao[:10], "%d/%m/%Y")
            dict_result['ano_vencimento'] = ano_vencimento
        valor_principal=sessao_web.encontrar_elemento(localizador_elemento='//*[@id="includeContent"]/fieldset/table/tbody/tr[10]/td[2]', tipo_elemento='XPATH').text
        valor_principal=valor_principal.replace("R$", "").strip()
        dict_result['valor_principal'] = float(valor_principal.replace('.','').replace(',','.'))
        return dict_result
                 
    def capturar_dados_aba_partes(self, valor_principal: float | None) -> dict:
        """ """
        
        # obter sessao aberta
        sessao_web=self._navegador.obter_sessao()
        
        # clicar na aba de partes
        sessao_web.encontrar_elemento(localizador_elemento= 'tabItemprefix2', tipo_elemento= 'ID').click()
    
        # polo ativo
        dados_polo_ativo=self._capturar_polo_ativo()
        
        # polo passivo
        dados_polo_passivo=self._capturar_polo_passivo()
       
        # formatar credor principal
        credor=self._formartar_credor_principal(dict_credor= dados_polo_ativo['credor'], valor_face=valor_principal) 
       
        # formatar lista de advogados
        advogados=self._formartar_lista_advogados(lista_advogados= dados_polo_ativo['advogados'])
       
        # retorno
        return {
            'credor': credor, 
            'advogados': advogados,
            'ente_devedor': dados_polo_passivo['ente_devedor']
        }
    
    def realizar_download(self, numero_processo: str) -> dict:
        """ """
        
        # lista de arquivos baixados 
        lista_arquivos=[]
        
        # criar pasta para salvar os downloads desse processo
        titulo=f'{numero_processo}.pdf'
   
        # palavras chaves para a identificação de documentos
        palavras_chave=get_configuration_by_path('rules/keys_docs')

        # obter sessao aberta
        sessao_web=self._navegador.obter_sessao()    
                
        # clicar na aba de movimentacoes
        sessao_web.encontrar_elemento(localizador_elemento= 'tabItemprefix3', tipo_elemento= 'ID').click()
        
        # lista resultados com anexos
        linhas_resultado_acesso=sessao_web.encontrar_lista_elementos(localizador_elemento= '//tr/td/a/img[contains(@onclick, "showDetail")]', tipo_elemento= 'XPATH')
        
        # acessar a ultima lista de anexos
        linhas_resultado_acesso[-1].click()
        
        # tempo necessario para processo nao travar
        time.sleep(1)
        
        # capturar a lista de documentos em anexo
        lista_documentos=sessao_web.encontrar_lista_elementos(localizador_elemento= '//a[contains(@onclick, "diech9oh")]', tipo_elemento= 'XPATH')
        
        # funcao temporaria para capturar apenas as palavaras, e deixar em letras minusculas
        format_titulo=lambda x: re.sub(r'[^a-zA-Z]', '', x.split('.')[0]).lower()
        
        # obter a lista de documentos que constem no titulo alguma das palavras chaves
        documentos_para_download=[documento for documento in lista_documentos if format_titulo(str(documento.text)) in palavras_chave]
        
        # percorrer a lista de documentos
        for documento in documentos_para_download:
              
            # abrir o link em uma nova aba e iniciar o download
            sessao_web.abrir_nova_aba(url= documento.get_attribute('href'))
            
            # tempo após o download ter iniciado
            time.sleep(5)

            # mover o arquivo baixado
            arquivo_movido=self._tratar_arquivo_baixado(titulo_documento= titulo)
            
            # salvar o caminho do arquivo movido
            lista_arquivos.append(arquivo_movido)       
        
                                 
        # nao houve arquivos
        if lista_arquivos == []:
            # controle de documentos
            documento_existe=False
        
        # houve 
        else:
            # controle de documentos
            documento_existe=True
        
        return {
            'documento_existe': documento_existe,
            'documentos': lista_arquivos
        }