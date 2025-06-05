__description__ = f'\nProjeto de Raspagem de Dados Web: Automação Web - Com possíveis alteracãoes para o projeto TJPR'
__version__ = '1.6.0'
__author__ = 'Squad RPA PJUS - 2023'

from .navegador.base import NavegadorBase, TipoNavegador
from .navegador.chrome import NavegadorChrome
from .navegador.firefox import NavegadorFirefox
from .navegador.edge import NavegadorEdge
from .navegador.undetected_chrome import NavegadorUndetectedChrome
from .interacao.base import InteracaoWeb

def selecionar_inicializador(nome_navegador: str):
    """ """
    # DEFINIR QUAL NAVEGADOR WEB FOI SOLICITADO
    matches = {
        'firefox': NavegadorFirefox, 
        'chrome': NavegadorChrome,
        'edge': NavegadorEdge,
        'uc-chrome': NavegadorUndetectedChrome
    }
    
    return matches[nome_navegador] if nome_navegador in matches else NavegadorBase

class NavegacaoWeb:
    """ Representa a abstração dos comandos para a navegacao web """
    
    _list_dict_inicializacao = []
    _list_inicializador_motor = []
    _list_motor = []
    _list_navegacao = []
    
    @classmethod        
    def iniciar_sessao(cls,
                       nome_navegador: str,
                       caminho_motor: str = None,
                       caminho_executavel: str = None,
                       caminho_pasta_downloads: str = None,
                       modo_anonimo: bool = False,
                       modo_sem_janelas: bool = False
                       
                       ) -> InteracaoWeb:
        """
        Instancia um navegador e prepara para ser utilizavel para navegação
        
        Navegadores Implementados
            - firefox
            - chrome
            - edge
            - uc-chrome
        
        :param nome_navegador: local do executavel do motor do navegador    
        :param caminho_motor: local do executavel do motor do navegador
        :param caminho_executavel: local do executavel da instalação do navegador
        :param caminho_pasta_downloads: local a ser salvo os arquivos baixados
        :param modo_anonimo: define se o navegador será aberto no modo anonimo ou não
        :param modo_sem_janelas: define se o navegador será aberto visivel ou não
        
        """
        inicializador_motor = selecionar_inicializador(nome_navegador= nome_navegador)
        
        if inicializador_motor != TipoNavegador.Desconhecido:
            
            dict_inicializacao = {
                'caminho_motor': caminho_motor,
                'caminho_executavel': caminho_executavel,
                'caminho_pasta_downloads': caminho_pasta_downloads,
                'modo_anonimo': modo_anonimo,
                'modo_sem_janelas': modo_sem_janelas
            }
            
            # adicionar o inicializador e o dicionario de inicializacao do motor
            cls._list_inicializador_motor.append(inicializador_motor)
            cls._list_dict_inicializacao.append(dict_inicializacao)
            
            # driver e lista de driver instanciados
            motor_navegacao = inicializador_motor(**dict_inicializacao).inicializar_navegador()
            cls._list_motor.append(motor_navegacao)
            
            # navegacao e lista de navegacoes instanciados
            navegacao = InteracaoWeb(motor_navegacao)
            cls._list_navegacao.append(navegacao)
            
            return navegacao
  
    @classmethod
    def obter_sessao(cls, id: int= 0) -> InteracaoWeb:
        """
        Retorna instância do navegador aberta

        :param id: id especifica de uma sessao aberta 
        """
        # verifica se existe algum objeto de navegacao
        if cls._list_navegacao is not []:
            navegacao = cls._list_navegacao[id]
                
            # navegacao esta ativa
            if navegacao.verificar_existencia_navegacao():
                return navegacao    
        
            # navegacao nao esta ativa
            else:
                # finalizar o objeto que nao existe
                try:
                    navegacao._motor_navegador.quit()
                except:
                    pass
                
                # recuperar inicializador e dicionario de inicializacao
                dict_inicializacao = cls._list_dict_inicializacao[id]
                inicializador = cls._list_inicializador_motor[id]
            
                # informacoes recuperadas, deletar o que foi recuperado
                del cls._list_dict_inicializacao[id]
                del cls._list_inicializador_motor[id]
                del cls._list_motor[id]
                del cls._list_navegacao[id]
                
                # executar a inicializacao do navegador de acordo com o que foi recuperado
                navegador = inicializador(**dict_inicializacao).inicializar_navegador()
                navegacao = InteracaoWeb(navegador)
                
                # salvar as informacoes que foram recuperadas e executadas
                cls._list_dict_inicializacao.append(dict_inicializacao)
                cls._list_inicializador_motor.append(inicializador)
                cls._list_motor.append(navegador)
                cls._list_navegacao.append(navegacao)

                return navegacao
                  
    @classmethod
    def finalizar_sessao(cls, id: int = 0):
        """
        Retorna instância do navegador aberta

        :param method: nome do método que se deseja retornar do logger
        """
        if cls._list_motor is not []:

            cls._list_motor[id].quit()

            # deletar informacao referente a sessao
            del cls._list_dict_inicializacao[id]
            del cls._list_inicializador_motor[id]
            del cls._list_motor[id]
            del cls._list_navegacao[id]
            
        else:
            return None
    
    @classmethod
    def finalizar_todas_sessoes(cls):
        
        if cls._list_motor is not []:
            for id, navegador in enumerate(cls._list_motor):
                del cls._list_dict_inicializacao[id]
                del cls._list_inicializador_motor[id]
                del cls._list_motor[id]
                del cls._list_navegacao[id]
                navegador.quit() 
        
        else:
            return None