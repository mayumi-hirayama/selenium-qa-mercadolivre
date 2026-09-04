from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def abrir_site(navegador):
    navegador.get("https://www.mercadolivre.com.br/")


def buscar_produto(navegador, termo):
    campo_busca = navegador.find_element(By.ID, "cb1-edit")
    campo_busca.send_keys(termo)
    campo_busca.send_keys(Keys.RETURN)


def fechar_popup_login(navegador):
    sleep(10) # tempo pro popup aparecer

    antes = len(navegador.find_elements(By.CSS_SELECTOR, "iframe[src*='accounts.google.com']"))
    print(f"Iframes do Google antes de remover: {antes}")

    #tenta remover repetidamente por 5s, caso o popup volte
    for _ in range(10): #procura na página todos os iframes cujo endereço (src) contenha 'accounts.google.com', e guarda essa lista em popups
        navegador.execute_script("""
            var popups = document.querySelectorAll("iframe[src*='accounts.google.com']");
            popups.forEach(function(popup) {
                popup.remove();
            }); 
        """)
        sleep(0.5)

    depois = len(navegador.find_elements(By.CSS_SELECTOR, "iframe[src*='accounts.google.com']"))
    print(f"Iframes do Google depois de remover: {depois}")


def selecionar_produto(navegador, texto_produto, tentativas=5):
    for _ in range(tentativas):
        produtos = navegador.find_elements(By.CSS_SELECTOR, "a.poly-component__title") # combinação de tag + classe, que é mais específica e menos propensa a erros do que só a classe

        for produto in produtos:
            if texto_produto.lower() in produto.text.lower():
                produto_encontrado = produto
                navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", produto_encontrado)
                sleep(1)  # Pequena pausa para garantir que o elemento esteja visível
                produto_encontrado.click()
                return True

        navegador.execute_script("window.scrollBy(0, 1000);")  # rola a página para baixo para carregar mais produtos
        sleep(1)  # espera um pouco para os produtos carregarem

    return False  # retorna False se não encontrou o produto após todas as tentativas

def esperar_elemento(navegador, seletor_css, tempo=10): # checa se o elemento está presente na página, e espera até 10s por ele
    elemento = WebDriverWait(navegador, tempo).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, seletor_css))
    )
    return elemento

def extrair_dados_produto(navegador):
    #antes eu uso o esperar para garantir que o elemento esteja presente na página antes de tentar acessá-lo
    titulo = esperar_elemento(navegador, "h1.ui-pdp-title").text
    preco = esperar_elemento(navegador, "span.andes-money-amount__fraction").text
    return {"titulo": titulo, "preco": preco}


def conversao_preco_float(preco_str):
    preco_real = preco_str.replace(".", "")
    return float(preco_real) # remove o ponto de milhar pro python não interpretar como separador decimar e converte pra float


def main(): # função principal do programa
    navegador = webdriver.Firefox()
    navegador.maximize_window()
    abrir_site(navegador)
    buscar_produto(navegador, "celular")
    fechar_popup_login(navegador)

    sucesso = selecionar_produto(navegador, "Galaxy A37")
    if sucesso:
        dados = extrair_dados_produto(navegador)
        preco_float = conversao_preco_float(dados["preco"])
        print(dados["titulo"])
        print(preco_float)
    else:
        print("Não foi possível extrair dados: produto não encontrado.")



if __name__ == "__main__":
    main()