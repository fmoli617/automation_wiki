import json
from .base import NavegadorBase, TipoNavegador
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class NavegadorChrome(NavegadorBase):
    """ Representa a estrutura da abstração do navegador Chrome """
    
    _tipo = TipoNavegador.Chrome
    
    def _baixar_motor_navegacao(self) -> str or None:
        """ 
        Executa o download do motor de navegação referente ao navegador instalado localmente na máquina 
        
        :returns: caminho onde o motor foi baixado 
        """
        try:
            return ChromeDriverManager().install()
        
        except:
            return None       
             
    def _configurar_caracteristicas(self) -> Options:
        """
        Executa a configuração do motor de navegacao
        
        :returns: objeto do tipo Options da biblioteca Selenium
        """
            
        options = Options()
        
        # Configurar o local do executável do navegador que será utilizado.
        if self._caminho_executavel:
            options.binary_location = self._caminho_executavel
        
        # Configurar o modo de navegação privada (também conhecido como modo anônimo).
        if self._modo_anonimo:
            options.add_argument('--incognito')
        
        # Configurar em modo "headless" ou "sem interface gráfica", e em um único processo em vez de em um modo de várias instâncias. 
        if self._modo_sem_janelas:
            options.add_argument('--headless')
            options.add_argument('--single-process')  
        
        # DEFINICIOES ESPECIFICAS:
        #  Dicionário que define o estado de uma aplicação para impressão de PDFs.
        app_state = {'recentDestinations': [{'id': 'Save as PDF',
                                             'origin': 'local',
                                             'account': ''}],
                     'selectedDestinationId': 'Save as PDF',
                     'version': 2}
                
        dict_experimental_option = {
            # Essa opção define que os arquivos PDF sempre serão abertos externamente ao navegador em vez de serem exibidos internamente.
            'plugins.always_open_pdf_externally': True,
            # Essa opção exclui o switch 'enable-automation', que pode ser usado para detectar a automação do navegador e desabilitar recursos para evitar detecção automatizada.
            'excludeSwitches': ['enable-automation'],
            # Essa opção desativa a extensão de automação do Chrome, que é usada para fins de teste automatizado.
            'useAutomationExtension': False,
            # Essa opção define o estado da aplicação para impressão de PDFs, usando o dicionário app_state convertido para uma string JSON.
            'printing.print_preview_sticky_settings.appState': json.dumps(app_state),
            # Essa opção desativa o recurso de navegação segura para fontes confiáveis.
            'safebrowsing_for_trusted_sources_enabled': False,
            # Essa opção desativa o recurso de navegação segura geral.
            'safebrowsing.enabled': False
        }
        
        if self._caminho_pasta_downloads:
            
            dict_experimental_option.update({
                # Essa opção define que o navegador não deve solicitar a confirmação para iniciar um download e fazê-lo automaticamente.
                'download.prompt_for_download': False,
                # Essa opção define o diretório padrão para salvar os downloads.
                'download.default_directory': self._caminho_pasta_downloads,
                # Essa opção permite que o navegador utilize o diretório padrão configurado anteriormente para downloads.
                'download.directory_upgrade': True,        
                # Essa opção define o diretório padrão para salvar os arquivos.
                'savefile.default_directory': self._caminho_pasta_downloads
            })
        
        # adiciona todas as opções experimentais configuradas
        options.add_experimental_option('prefs',
                                        dict_experimental_option)
        
        # Desativa o uso do sandbox do navegador Chrome. O sandbox é uma camada de segurança para isolar o navegador do sistema operacional.
        options.add_argument('--no-sandbox')
        
        # Impede a exibição da página de boas-vindas na primeira execução.
        options.add_argument('--no-first-run')
        
        # Essa opção permite o modo "kiosk" de impressão, que simplifica o diálogo de impressão e não exibe a pré-visualização de impressão antes de enviar para a impressora.
        options.add_argument('--kiosk-printing')
        
        # Desativa o uso da GPU pelo navegador. Isso pode ser útil em ambientes de teste sem suporte para aceleração por hardware.
        options.add_argument('--disable-gpu')

        # Desativa a exibição de infobars no Chrome, que são as barras de informações, como a sugestão para ativar a sincronização do Chrome.
        options.add_argument('--disable-infobars')

        # Desativa a execução de extensões do Chrome durante a sessão do Selenium. Isso pode evitar conflitos ou interferências com as extensões instaladas no navegador.
        options.add_argument('--disable-extensions')

        #  Desativa as políticas de segurança do mesmo origin (mesma origem) no Chrome. Isso permite que páginas web de diferentes origens interajam umas com as outras.
        options.add_argument('--disable-web-security')

        # Desativa as notificações do Chrome durante a execução controlada pelo Selenium.
        options.add_argument('--disable-notifications')

        # Tela Maximizada
        options.add_argument('--start-maximized')

        #  Define o tamanho da janela do navegador para 1920x1080 pixels.
        options.add_argument('--window-size=1920x1080')

        # Desativa o uso de memória compartilhada /dev/shm.
        options.add_argument('--disable-dev-shm-usage')

        # Desativa o cache de aplicativos do Chrome.
        options.add_argument('--disable-application-cache')

        # Ignora erros de certificado SSL ao carregar páginas HTTPS.
        options.add_argument('--ignore-certificate-errors')
        
        #  Permite que o Chrome carregue conteúdo inseguro em uma página HTTPS.
        options.add_argument('--allow-running-insecure-content')

        #  Desativa a detecção de phishing no lado do cliente pelo Chrome.
        options.add_argument('--disable-client-side-phishing-detection')

        # Desativa recursos do Blink controlados por automação.
        options.add_argument('--disable-blink-features=AutomationControlled')
        

        return options
       
    def _configurar_service(self) -> Service:
        """
        Executa a configuração do servico de execucao do motor de navegacao
        
        :returns: objeto do tipo Service da biblioteca Selenium
        """
            
        return Service(service= Service(executable_path= self.obter_caminho_motor_navegacao()))  