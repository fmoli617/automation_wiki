import fitz

class PdfDataSource:
    
    def __init__(self) -> None:
        """ """ 
        pass
    
    def extract_text_pdf(self, file_pdf: str, limit_pages: int = None) -> str:
        """ """

        # efetuando a leitura do documento
        document = fitz.open(file_pdf)
        
        # capturando o total de páginas
        qtd_pages = document.page_count
        
        # gerando um arquivo para salva do conteudo trabalhado
        document_ouptut = fitz.open()
         
        # variavel de texto com os dados lidos
        text_pdf = ''
        
        # se a quantidade de paginas limites não houver sido definida
        if limit_pages == None:
            
            # definir com o total das paginas
            limit_pages = qtd_pages
        
        # se houver sido definida
        else:
            
            # verificar se o documento nao possui menos paginas que o definido como limite
            limit_pages = qtd_pages if qtd_pages < limit_pages else limit_pages
        
        # percorrer o limite de paginas
        for page_num in range(limit_pages):
            
            # carregando a pagina do documento
            page = document.load_page(page_num)
        
            # capturando o conteudo da pagina
            text_pdf += page.get_text()
             
            # adicionando a pagina 
            document_ouptut.insert_pdf(document, from_page=page_num, to_page=page_num)
    
        # fechado documento original    
        document.close()
        
        # sobre-escrevendo o arquivo original pelas paginas capturadas
        document_ouptut.save(file_pdf)
        
        # fechando o novo documento
        document_ouptut.close()
        
        return text_pdf