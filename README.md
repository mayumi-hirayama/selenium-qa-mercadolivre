# Selenium QA — Mercado Livre

Script de automação em Python com Selenium que simula um fluxo de busca e validação de produto no Mercado Livre, como parte do meu portfólio de QA.

## O que o script faz

1. Abre o site do Mercado Livre
2. Busca por um termo (ex.: "celular")
3. Fecha o popup de login que aparece via iframe do Google
4. Localiza um produto específico nos resultados (ex.: "Galaxy A37"), rolando a página automaticamente até encontrá-lo
5. Extrai o título e o preço do produto na página de detalhes
6. Converte o preço extraído (texto) para número (float)

## Funcionalidades técnicas

- **Espera explícita reutilizável** (`esperar_elemento`) usando `WebDriverWait` + `expected_conditions`, evitando `sleep()` fixos onde possível
- **Remoção de popup via JavaScript** (`fechar_popup_login`) — o Mercado Livre injeta um iframe de login do Google que bloqueia a interação; o script remove esse iframe diretamente do DOM
- **Busca com scroll e múltiplas tentativas** (`selecionar_produto`) — como nem todo produto aparece na primeira leva de resultados carregados, a função rola a página e tenta novamente antes de desistir, retornando `True`/`False` conforme o resultado
- **Extração de dados da página de detalhes** (`extrair_dados_produto`) — captura título e preço via seletores CSS
- **Conversão de preço para número** (`conversao_preco_float`) — trata o formato brasileiro (ponto como separador de milhar) antes de converter para `float`

## Tecnologias

- Python
- Selenium WebDriver (Firefox)

## Como rodar

```bash
pip install selenium
python ML.py
```

> É necessário ter o [geckodriver](https://github.com/mozilla/geckodriver/releases) instalado e acessível no PATH para rodar com Firefox.

## Próximos passos

- [ ] Adicionar validações/asserts (ex.: conferir que o título contém o termo buscado, que o preço é maior que zero)
- [ ] Estruturar como testes automatizados (Pytest)
- [ ] Documentar casos de teste e possíveis bugs encontrados durante a exploração

## Sobre

Projeto feito como parte da minha transição de carreira para QA/desenvolvimento, praticando automação de testes web com Selenium.

- LinkedIn/GitHub: [mayumi-hirayama](https://github.com/mayumi-hirayama)
