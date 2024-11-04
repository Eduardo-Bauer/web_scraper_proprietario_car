from playwright.sync_api import sync_playwright

def pegar_texto(url, seletor):
    with sync_playwright() as p:
        # Inicializa o navegador e abre uma nova página
        navegador = p.firefox.launch()
        pagina = navegador.new_page()

        # Navega para a URL desejada
        pagina.goto(url)

        # Pega o conteúdo de texto do elemento com o seletor específico
        texto = pagina.locator(seletor).text_content()

        # Fecha o navegador
        navegador.close()

        return texto

# Exemplo de uso
car = 'RS-4313201-B5E3AB7E74694571A04F4FED4A06EB82/'
url = f'https://www.registrorural.com.br/car/item/{car}'
seletor = '//html/body/div[2]/div/div[2]/div[2]/div/div/h3/a'
texto_encontrado = pegar_texto(url, seletor).strip()

proprietario = ''
for i in range(0, len(texto_encontrado)):
    if texto_encontrado[i] != ' ' or texto_encontrado[i + 1] != '-':
        proprietario += texto_encontrado[i]
    else:
        break

print(proprietario)
