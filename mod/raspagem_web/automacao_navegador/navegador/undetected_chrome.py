from .base import NavegadorBase, TipoNavegador
import undetected_chromedriver as uc

class NavegadorUndetectedChrome(NavegadorBase):
    """ Representa a estrutura da abstração do navegador Chrome """
    
    _tipo = TipoNavegador.Chrome
    
    def _baixar_motor_navegacao(self) -> str or None:
        """ 
        Executa o download do motor de navegação referente ao navegador instalado localmente na máquina 
        
        :returns: caminho onde o motor foi baixado 
        """
               
        raise None  
       
    def _configurar_caracteristicas(self) -> uc.ChromeOptions:
        """
        Executa a configuração do motor de navegacao
        
        :returns: objeto do tipo Options da biblioteca Selenium
        """
        options = uc.ChromeOptions()
        
        # DEFINICIOES BASEADAS NOS ARGUMENTOS DA CLASSE:
        # É usada para definir o local do executável do navegador que será utilizado.
        if self._caminho_executavel:
            options.binary_location = self._caminho_executavel
        
        # Configurar o modo de navegação privada (também conhecido como modo anônimo).
        if self._modo_anonimo:
            options.add_argument('--incognito')
        
        # Executa o navegador em modo "headless" ou "sem interface gráfica", e em um único processo em vez de em um modo de várias instâncias. 
        if self._modo_sem_janelas:
            options.add_argument('--headless')
            options.add_argument('--single-process')  

        # DEFINICIOES ESPECIFICAS:
        options.add_experimental_option('prefs',
                                        {'plugins.always_open_pdf_externally': True,
                                         'download.prompt_for_download': False,
                                         'download.default_directory': self._caminho_pasta_downloads,
                                         'savefile.default_directory': self._caminho_pasta_downloads
                                         })
        
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
    
    def _configurar_service(self) -> None:
        """
        Executa a configuração do servico de execucao do motor de navegacao
        
        :returns: objeto do tipo Service da biblioteca Selenium
        """
            
        return None