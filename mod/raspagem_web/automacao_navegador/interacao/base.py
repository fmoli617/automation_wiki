from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import JavascriptException
from selenium.common.exceptions import NoSuchAttributeException
import urllib
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

class InteracaoWeb:
    """ Representa ... """
    
    def __init__(self, motor_navegador: WebDriver):
        self._motor_navegador = motor_navegador
    
    def obter_titulo_janela(self) -> str:
        """ """
        return self._motor_navegador.title
        
    def verificar_existencia_navegacao(self) -> bool:
        try:
            self._motor_navegador.current_url
            return True
        except:
            return False
    
    def execute_script(self, script: str):
        self._motor_navegador.execute_script(script=script)
    
    def acessar_url(self, url: str) -> None:
        self._motor_navegador.get(url)
    
    def trocar_para_frame(self, elemento_iframe: WebElement) -> None:
        self._motor_navegador.switch_to.frame(elemento_iframe)

    def voltar_para_frame_padrao(self) -> None:
        self._motor_navegador.default_content()
        
    def trocar_para_aba(self, indice_aba: int) -> None:
        self._motor_navegador.switch_to.window(self._motor_navegador.window_handles[indice_aba])
    
    def recarregar_pagina(self) -> None:
        self._motor_navegador.refresh()
        
    def abrir_nova_aba(self, url: str = '') -> None:
        self._motor_navegador.execute_script(f"window.open('{url}');")
        
    def fechar_janela(self) -> None:
        self._motor_navegador.close()   
    
    def fechar_nova_janela(self):
        
        driver = self._motor_navegador
        janelas_abertas = driver.window_handles
        janela_a_fechar = janelas_abertas[-1]
        driver.switch_to.window(janela_a_fechar)
        driver.close()
        driver.switch_to.window(janelas_abertas[0])
            
    def pressionar_tecla(self, tecla: str) -> None:
        if tecla == 'enter':
            tecla = Keys.ENTER
        if tecla == 'home':
            tecla = Keys.HOME
        try:
            actions = ActionChains(self._motor_navegador)
            actions = actions.send_keys(tecla)
            actions.perform()
        except (AttributeError, NoSuchElementException):
            self._navegador.send_keys(tecla)
    
    def clicar(self, elemento: WebElement) -> None:
        try:
            elemento.click()
        except (AttributeError, NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException):
            self._motor_navegador.execute_script("arguments[0].click();", elemento)
        except JavascriptException as e:
            raise Exception("Nao foi possivel executar a função 'click'") from e
    
    def digitar_texto(self, elemento: WebElement, texto: str) -> None:
        elemento.send_keys(texto)
    
    def limpar_campo(self, elemento: WebElement) -> None:
        elemento.clear()
    
    def encontrar_elemento(self, localizador_elemento: str, tipo_elemento: str = 'XPATH', navegar_elemento: WebElement = None) -> WebElement:
        
        if navegar_elemento:
            driver = navegar_elemento
        else:
            driver = self._motor_navegador
        
        #
        
        try:
            return driver.find_element(by=By().__getattribute__(tipo_elemento.upper()), value=localizador_elemento)
        except AttributeError:
            raise Exception("Tipo de elemento inválido. Tipos de elementos válidos: ID, XPATH etc")
        except NoSuchElementException:
            return None
    
    def encontrar_lista_elementos(self, localizador_elemento: str, tipo_elemento: str = 'XPATH', navegar_elemento: WebElement = None) -> WebElement:
       
        if navegar_elemento:
            driver = navegar_elemento
        else:
            driver = self._motor_navegador
        
        try:
            return driver.find_elements(by=By().__getattribute__(tipo_elemento.upper()), value=localizador_elemento)
        except AttributeError:
            raise Exception("Tipo de elemento inválido. Tipos de elementos válidos: ID, XPATH etc")
        except NoSuchElementException:
            return None
                
    def obter_atributo_do_elemento(self, elemento: WebElement, atributo: str) -> str | None:
        try:
            return elemento.get_attribute(atributo)
        except NoSuchAttributeException:
            return None
        except (NoSuchElementException, ElementNotInteractableException):
            raise Exception("Não foi possível interagir com elemento para buscar seu atributo.")
    
    def aceitar_alerta(self, tempo_maximo_espera: int = 15) -> None:
        try:
            WebDriverWait(self._motor_navegador, tempo_maximo_espera).until(EC.alert_is_present())
            alerta = self._motor_navegador.switch_to.alert
            alerta.accept()
        except TimeoutException:
            pass
    
    def salvar_img_html(self, elemento_img: WebElement, caminho_arquivo_imagem: str) -> None:
        with open(caminho_arquivo_imagem, 'wb') as arquivo_img:
            arquivo_img.write(elemento_img.screenshot_as_png)
            
    def salvar_img_atributo_src(self, elemento_img: WebElement, caminho_arquivo_imagem: str) -> None:
        src = elemento_img.get_attribute('src')
        urllib.request.urlretrieve(src, caminho_arquivo_imagem)
            
    def aguardar_existir(self, localizador_elemento: str, tipo_elemento: str = 'XPATH', tempo_maximo_espera: int = 60) -> WebElement:
        try:
            return WebDriverWait(self._motor_navegador, tempo_maximo_espera).until(EC.presence_of_element_located((By().__getattribute__(tipo_elemento.upper()), localizador_elemento)))
        except TimeoutException:
            return None
        except AttributeError:
            raise Exception("Tipo de elemento inválido. Tipos de elementos válidos: ID, XPATH etc")    
    
    def aguardar_clicavel(self, localizador_elemento: str, tipo_elemento: str = 'XPATH', tempo_maximo_espera: int = 60) -> WebElement:
        try:
            return WebDriverWait(self._motor_navegador, tempo_maximo_espera).until(EC.element_to_be_clickable((By().__getattribute__(tipo_elemento.upper()), localizador_elemento)))
        except TimeoutException:
            return None
        except AttributeError:
            raise Exception("Tipo de elemento inválido. Tipos de elementos válidos: ID, XPATH etc")
    
    def aguardar_visibilidade(self, localizador_elemento: str, tipo_elemento: str = 'XPATH', tempo_maximo_espera: int = 60) -> WebElement:
        try:
            return WebDriverWait(self._motor_navegador, tempo_maximo_espera).until(EC.visibility_of_element_located((By().__getattribute__(tipo_elemento.upper()), localizador_elemento)))
        except TimeoutException:
            return None
        except AttributeError:
            raise Exception("Tipo de elemento inválido. Tipos de elementos válidos: ID, XPATH etc")
        
    def aguardar_visibilidade_todos_elementos(self, localizador_elemento: str, tipo_elemento: str = 'XPATH', tempo_maximo_espera: int = 60) -> list[WebElement]:
        try:
            return WebDriverWait(self._motor_navegador, tempo_maximo_espera).until(EC.visibility_of_all_elements_located((By().__getattribute__(tipo_elemento.upper()), localizador_elemento)))
        except TimeoutException:
            return None
        except AttributeError:
            raise Exception("Tipo de elemento inválido. Tipos de elementos válidos: ID, XPATH etc")
        
    def aguardar_invisibilidade(self, localizador_elemento: str, tipo_elemento: str = 'XPATH', tempo_maximo_espera: int = 60) -> WebElement:
        try:
            return WebDriverWait(self._motor_navegador, tempo_maximo_espera).until(EC.invisibility_of_element_located((By().__getattribute__(tipo_elemento.upper()), localizador_elemento)))
        except TimeoutException:
            return None
        except AttributeError:
            raise Exception("Tipo de elemento inválido. Tipos de elementos válidos: ID, XPATH etc")
        
    def aguardar_quantidade_janelas_ser(self, quantidade: int, tempo_maximo_espera: int = 30) -> None:
        try:
            return WebDriverWait(self._motor_navegador, tempo_maximo_espera).until(EC.number_of_windows_to_be(quantidade))
        except TimeoutException:
            return None
    
    def aguardar_alerta_existir(self, tempo_maximo_espera: int = 10) -> None:
        try:
            return WebDriverWait(self._motor_navegador, tempo_maximo_espera).until(EC.alert_is_present())
        except TimeoutException:
            return None

    def aguardar_url_ser(self, url_esperada: str, tempo_maximo_espera: int = 10) -> WebElement:
        return WebDriverWait(self._motor_navegador, tempo_maximo_espera).until(EC.url_to_be(url_esperada))
    
    def trocar_frames(self, frame_value, index):
        try:
            frames = self._motor_navegador.find_elements(by=By.TAG_NAME, value=frame_value)
            self._motor_navegador.switch_to.frame(frames[index])
        
        except Exception as e:
            raise e
    
    def selecionar_item_por_valor(self, elemento_selecao: WebElement, valor_item: str):
        select = Select(elemento_selecao)
        select.select_by_value(valor_item)