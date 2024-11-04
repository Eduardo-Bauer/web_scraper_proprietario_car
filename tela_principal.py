from playwright.sync_api import sync_playwright
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

######### INTERFACE #########
tela = Tk()
tela.title('Web Scraping')
tela.config(background='white')

######### STYLES #########
style = ttk.Style()
style.theme_use('default')

botao = ttk.Style()
botao.configure('TButton', font=('Calibri', 12, 'bold'), relief = "solid", background='#00cf5d')
botao.map('TButton', background=[("active", "#00e40a")], foreground=[("pressed", "white")])

botao = ttk.Style()
botao.configure('pesquisa.TButton', font=('Calibri', 10, 'bold'), relief = "solid", background='white')
botao.map('pesquisa.TButton', background=[("active", "#d9d9d9")], foreground=[("pressed", "white")])

entrada = ttk.Style()
entrada.configure('TEntry', relief = "solid")

titulo = ttk.Style()
titulo.configure('TLabel', font=('Calibri', 20, 'bold'), background='white')

texto = ttk.Style()
texto.configure('texto.TLabel', font=('Calibri', 10, 'bold'), background='white')

######### FUNCOES / JANELAS #########
def pesquisar_arquivo():
    entrada_arquivo = filedialog.askopenfilename()
    texto_arquivo.delete(0, 'end')
    texto_arquivo.insert(0, entrada_arquivo)

def pesquisar():
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
    return proprietario

######### COMPONENTES #########
titulo = ttk.Label(tela, text='PROPRIETÁRIO CAR', style='TLabel')
texto_pesquisa = ttk.Label(tela, text='Digite ou Pesquise a Tabela Excel', style='texto.TLabel')

foto1 = PhotoImage(file='imagens/1f60e.png')
foto1 = foto1.subsample(4, 4)
foto2 = PhotoImage(file='imagens/oculos.png')
foto2 = foto2.subsample(4, 4)
figura1 = Label(image=foto1, background='white')
figura2 = Label(image=foto2, background='white')

botao_pesquisar_arquivo = ttk.Button(tela, text='Pesquisar', style='pesquisa.TButton', command=pesquisar_arquivo)
botao_de_inicializacao = ttk.Button(tela, text='teste', style='TButton', command=pesquisar)

texto_arquivo = ttk.Entry(tela, style='TEntry', font=('Calibri', 10, 'bold'))

######### POSICAO DOS COMPONENTES #########
figura1.grid(row=0, column=0)
figura2.grid(row=0, column=2)

titulo.grid(row=0, column=1, pady=(0, 150))

texto_pesquisa.grid(row=0, column=1, pady=(0, 5), padx=(0, 198))

botao_pesquisar_arquivo.grid(row=0, column=1, pady=(49, 0), padx=(310, 0))
texto_arquivo.grid(row=0, column=1, pady=(50, 0), ipadx=80, ipady=4, padx=(0, 70))

botao_de_inicializacao.grid(row=0, column=1, pady=(150, 10))

tela.mainloop()