from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def abrir_site(navegador):
    navegador.get("https://www.mercadolivre.com.br/")
    pass


def buscar_produto(navegador, termo):
    campo_busca = navegador.find_element(By.ID, "cb1-edit")
    campo_busca.send_keys(termo)
    campo_busca.send_keys(Keys.RETURN)
    pass


def fechar_popup_login(navegador):
    sleep(10) # tempo pro popup aparecer

    antes = len(navegador.find_elements(By.CSS_SELECTOR, "iframe[src*='accounts.google.com']"))
    print(f"Iframes do Google antes de remover: {antes}")

    #tenta remover repetidamente por 5s, caso o popup volte
    for _ in range(10):
        navegador.execute_script("""
            var popups = document.querySelectorAll("iframe[src*='accounts.google.com']");
            popups.forEach(function(popup) {
                popup.remove();
            });
        """)
        sleep(0.5)

    depois = len(navegador.find_elements(By.CSS_SELECTOR, "iframe[src*='accounts.google.com']"))
    print(f"Iframes do Google depois de remover: {depois}")

def selecionar_produto(navegador, texto_produto):
    produtos = navegador.find_elements(By.CSS_SELECTOR, "a.poly-component__title") # combinação de tag + classe, que é mais específica e menos propensa a erros do que só a classe

    for produto in produtos:
        if texto_produto.lower() in produto.text.lower():
            produto_encontrado = produto
            navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", produto_encontrado)
            sleep(1)  # Pequena pausa para garantir que o elemento esteja visível
            produto_encontrado.click()
            break
    else: # else fora do if, junto com o for, significa que o for terminou sem encontrar o produto
        print(f"Produto '{texto_produto}' não encontrado.")
        return
    pass


def main(): # função principal do programa
    navegador = webdriver.Firefox()
    navegador.maximize_window()
    abrir_site(navegador)
    buscar_produto(navegador, "celular")
    fechar_popup_login(navegador)
    selecionar_produto(navegador, "Galaxy A36")

    pass


if __name__ == "__main__":
    main()