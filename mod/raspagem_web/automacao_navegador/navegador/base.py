from ..model.enums import TipoNavegador
from selenium import webdriver
import undetected_chromedriver as uc
import os


class NavegadorBase:
    """ Representa a estrutura básica para a abstração de um objeto navegador """
        
    _tipo = TipoNavegador.Desconhecido
    
    def __init__(self,
                 caminho_motor: str = None,
                 caminho_executavel: str = None,
                 caminho_pasta_downloads: str = None,
                 modo_anonimo: bool = True,
                 modo_sem_janelas: bool = False
                 ):
        """
        Classe que instancia um navegador utilizavel para navegação
        
        :param caminho_motor: local do executavel do motor do navegador
        :param caminho_executavel: local do executavel da instalação do navegador
        :param caminho_pasta_downloads: local a ser salvo os arquivos baixados
        :param modo_anonimo: define se o navegador será aberto no modo anonimo ou não
        :param modo_sem_janelas: define se o navegador será aberto visivel ou não
        """
        
        self._caminho_motor = os.path.abspath(caminho_motor) if caminho_motor != None else None
        self._caminho_executavel = os.path.abspath(caminho_executavel) if caminho_executavel != None else None
        self._caminho_pasta_downloads = os.path.abspath(caminho_pasta_downloads) if caminho_pasta_downloads != None else None
        self._modo_anonimo = modo_anonimo
        self._modo_sem_janelas = modo_sem_janelas
                
    def _baixar_motor_navegacao(self) -> str or None:
        """ 
        Executa o download do motor de navegação referente ao navegador instalado localmente na máquina 
        
        :returns: caminho onde o motor foi baixado 
        """
               
        raise NotImplementedError('Navegador não implementado')
        
    def _configurar_caracteristicas(self):
        """
        Executa a configuração do motor de navegacao
        
        :returns: objeto do tipo Options da biblioteca Selenium
        """
            
        raise NotImplementedError('Navegador não implementado')
   
    def _configurar_service(self):
        """
        Executa a configuração do servico de execucao do motor de navegacao
        
        :returns: objeto do tipo Service da biblioteca Selenium
        """
            
        raise NotImplementedError('Navegador não implementado')
       
    def selecionar_motor(self, tipo_navegador: TipoNavegador) -> webdriver:
        """ 
        Seleciona qual motor irá executar as configuracões de cada navegador 

        :param tipo_navegador: tipo do navegador
        :return: motor para incialização do motor
        """
        
        matches = {
            TipoNavegador.Edge: webdriver.Edge,
            TipoNavegador.Chrome: webdriver.Chrome,
            TipoNavegador.Firefox: webdriver.Firefox,
            TipoNavegador.UndetectedChrome: uc.Chrome
        }
    
        return matches[tipo_navegador]
 
    def obter_caminho_motor_navegacao(self) -> str or None:
        """
        Obtem o caminho do motor de navegacao
         
        :returns: String com o locado do caminho do motor de navegacao
        """    
        caminho_motor = self._caminho_motor
            
        # VERIFICAR SE FOI INDICADO O CAMINHO DO DRIVER
        if caminho_motor == None:
                
            # SE NAO, EFETUAR A TENTATIVA DE DOWNLOAD DO DRIVER
            caminho_motor = self._baixar_motor_navegacao()
                   
        return caminho_motor
         
    def inicializar_navegador(self) -> webdriver:
        """ 
        Executa a inicialização do navegador
        
        :returns: objeto do tipo webdriver da biblioteca Selenium
        """
        
        motor = self.selecionar_motor(self._tipo)
        
        options = self._configurar_caracteristicas()
        
        service = self._configurar_service()
        
        # Caso a função de definição de um servico de configuracao do motor retornar como None,
        #ira ignorar a sua utilização
        if service:
            motor = motor(service= service, options= options)
        else:
            motor = motor(options= options)
        
        return motor