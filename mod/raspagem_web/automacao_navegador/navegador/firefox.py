import os
from .base import NavegadorBase, TipoNavegador
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile as Profile

class NavegadorFirefox(NavegadorBase):
    """ Representa a estrutura da abstração do navegador Firefox """
    
    _tipo = TipoNavegador.Firefox
    
    def _baixar_motor_navegacao(self) -> str or None:
        """ 
        Executa o download do motor de navegação referente ao navegador instalado localmente na máquina 
        
        :returns: caminho onde o motor foi baixado 
        """
        try:
            return GeckoDriverManager().install()
        
        except:
            return None       
    
    def _configurar_perfil(self) -> Profile:
        """
        Executa a configuração do perfil do motor de navegacao
        
        :returns: objeto do tipo Profile da biblioteca Selenium
        """    

        profile = Profile()
        
        # preferencias relacionadas com a pasta de download
        if self._caminho_pasta_downloads:
        
            # Define preferência especifica o diretório onde esses downloads devem ser armazenados.
            profile.set_preference('navegador.download.dir', 
                                    self._caminho_pasta_downloads)
            
            # Define se o navegador deve utilizar o diretório de downloads especificado 
            profile.set_preference('navegador.download.useDownloadDir', 
                                   True)
            
            # Define a preferência de impressão para o formato PDF no perfil do navegador.
            profile.set_preference('print.printer_Microsoft_Print_to_PDF.print_to_filename', 
                                   os.path.join(self._caminho_pasta_downloads, 'arquivo_baixado.pdf'))
        
            # Preferência configura o comportamento de downloads do navegador. O valor 2 indica que os downloads serão salvos no diretório especificado.
            profile.set_preference('navegador.download.folderList', 
                                   2)        
        
        # Essa preferência desativa a exibição da janela de gerenciamento de downloads do navegador ao iniciar o download de um arquivo.
        profile.set_preference('navegador.download.manager.showWhenStarting', False)

        # Desativa a extensão de automação no perfil do navegador.
        profile.set_preference('useAutomationExtension', False)
        
        # Desativa o uso do WebDriver DOM (Document Object Model) no perfil do navegador.
        profile.set_preference('dom.webdriver.enabled', False)

        # Desativa as configurações recomendadas remotas no perfil do navegador.
        profile.set_preference('remote.prefs.recommended', False)

        # Desativa a opção "Sempre perguntar onde salvar arquivos" no navegador.
        profile.set_preference('navegador.helperApps.alwaysAsk.force', False)

        # Configura os tipos de arquivos para os quais o navegador nunca deve perguntar onde salvá-los.
        profile.set_preference('navegador.helperApps.neverAsk.saveToDisk', 'application/pdf;text/plain;application/text;text/xml;application/xml;application/octet-stream')

        # Desativa o PDF Viewer integrado (PDF.js) no navegador. O PDF.js é um visualizador de PDF embutido em navegadores modernos.
        profile.set_preference('pdfjs.disabled', True)

        # Define que o navegador sempre imprima silenciosamente (sem exibir diálogos de impressão ou confirmação) quando o código solicita a impressão de uma página da web.
        profile.set_preference('print.always_print_silent', True)

        # Oculta a exibição do progresso da impressão do navegador. 
        profile.set_preference('print.show_print_progress', False)

        # Habilita a impressão de links como parte do processo de salvar uma página da web como PDF.
        profile.set_preference('print.save_as_pdf.links.enabled', True)
            
        # Define com que a impressão seja direcionada para um arquivo em vez de uma impressora física.
        profile.set_preference('print.printer_Microsoft_Print_to_PDF.print_to_file', True)
            
        # Especifica o nome da impressora virtual que será usada para a impressão do navegador.
        profile.set_preference('print_printer', 'Microsoft Print to PDF')
            
        # Substitui o user-agent padrão do navegador pelo user-agent especificado.
        profile.set_preference('general.useragent.override', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0')    
                   
        return profile
              
    def _configurar_caracteristicas(self) -> Options:
        """
        Executa a configuração do motor de navegacao
        
        :returns: objeto do tipo Options da biblioteca Selenium
        """
        
        options = Options()
        
        # Configurar perfil do navegador    
        options.profile = self._configurar_perfil() 
        
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
       
        
        # Desabilita a exibição de barras de informações no navegador.
        options.add_argument('--disable-infobars')

        # Desabilita as extensões instaladas no navegador. As extensões são plugins ou complementos que podem adicionar funcionalidades extras ao navegador.
        options.add_argument('--disable-extensions')

        # Desabilita o bloqueio de pop-ups no navegador. Pop-ups são janelas adicionais.
        options.add_argument('--disable-popup-blocking')
        
        # Esta opção maximiza a janela
        options.add_argument("--start-maximized")
        
        return options
    
    def _configurar_service(self) -> Service:
        """
        Executa a configuração do servico de execucao do motor de navegacao
        
        :returns: objeto do tipo Service da biblioteca Selenium
        """
            
        return Service(service= Service(executable_path= self.obter_caminho_motor_navegacao()))