from .base import NavegadorBase, TipoNavegador
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service


class NavegadorEdge(NavegadorBase):
    """ Representa a estrutura da abstração do navegador Edge """
    
    _tipo = TipoNavegador.Edge
    
    def _baixar_motor_navegacao(self) -> str or None:
        """ 
        Executa o download do motor de navegação referente ao navegador instalado localmente na máquina 
        
        :returns: caminho onde o motor foi baixado 
        """
        try:
            return EdgeChromiumDriverManager().install()
        
        except:
            return None       
              
    def _configurar_caracteristicas(self) -> Options:
        """
        Executa a configuração do motor de navegacao
        
        :returns: objeto do tipo Options da biblioteca Selenium
        """
        
        options = Options()
        
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
        
        # Tela Maximizada
        options.add_argument('--start-maximized')

        #  Define o tamanho da janela do navegador para 1920x1080 pixels.
        options.add_argument('--window-size=1920x1080')   
  
        
        return options

    def _configurar_service(self) -> Service:
        """
        Executa a configuração do servico de execucao do motor de navegacao
        
        :returns: objeto do tipo Service da biblioteca Selenium
        """
            
        return Service(service= Service(executable_path= self.obter_caminho_motor_navegacao()))