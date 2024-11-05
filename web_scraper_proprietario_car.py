import pandas as pd
from playwright.sync_api import sync_playwright
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

######### INTERFACE #########
tela = Tk()
tela.title('Web Scraping')
tela.config(background='white')
tela.geometry('650x280')

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

texto = ttk.Style()
texto.configure('texto_aviso.TLabel', font=('Calibri', 9, 'bold'), background='white', foreground='red')

texto = ttk.Style()
texto.configure('texto_sucesso.TLabel', font=('Calibri', 15, 'bold'), background='white', foreground='green')

######### FUNCOES / JANELAS #########
def pesquisar_arquivo():
    entrada_arquivo = filedialog.askopenfilename()
    texto_arquivo.delete(0, 'end')
    texto_arquivo.insert(0, entrada_arquivo)

def pesquisar():

    def pegar_proprietario(url, seletor):
        with sync_playwright() as p:
            navegador = p.firefox.launch()
            pagina = navegador.new_page()

            pagina.goto(url)

            texto = pagina.locator(seletor).text_content()

            navegador.close()

            return texto

    try:
        df = pd.read_excel(texto_arquivo.get())

        cars = df.iloc[:, 0]

        proprietarios = [''] * len(cars)
        cont = 0
        
        for i in cars:
            url = f'https://www.registrorural.com.br/car/item/{i}'
            seletor = '//html/body/div[2]/div/div[2]/div[2]/div/div/h3/a'
            texto_retirado_site = pegar_proprietario(url, seletor).strip()

            proprietario = ''
            for i in range(0, len(texto_retirado_site)):
                if texto_retirado_site[i] != ' ' or texto_retirado_site[i + 1] != '-':
                    proprietario += texto_retirado_site[i]
                else:
                    break
                
            proprietarios[cont] = proprietario
            cont += 1

        df['Proprietarios'] = proprietarios

        df.to_excel(texto_arquivo.get(), index = False)

        texto_de_sucesso.config(text='Programa Realizado Com Sucesso', foreground='green')

    except FileNotFoundError:
        texto_de_sucesso.config(text='*Escolha ou digite o arquivo*', foreground='red')

######### COMPONENTES #########
titulo = ttk.Label(tela, text='PROPRIETÁRIO CAR', style='TLabel')
texto_pesquisa = ttk.Label(tela, text='Digite ou Pesquise a Tabela Excel', style='texto.TLabel')
texto_arquivo = ttk.Entry(tela, style='TEntry', font=('Calibri', 10, 'bold'))
texto_de_aviso = ttk.Label(tela, text='Este programa foi realizado quando não era ilegal web scraping', style='texto_aviso.TLabel')
texto_de_aviso_2 = ttk.Label(tela, text='se web scraping se tornou ilegal, não foi o Eduardo quem fez o programa <3', style='texto_aviso.TLabel')
texto_de_sucesso = ttk.Label(tela, text='', style='texto_sucesso.TLabel')

foto1 = PhotoImage(file='imagens/oculos_escuros.png')
foto1 = foto1.subsample(4, 4)
foto2 = PhotoImage(file='imagens/oculos.png')
foto2 = foto2.subsample(4, 4)
figura1 = Label(image=foto1, background='white')
figura2 = Label(image=foto2, background='white')

botao_pesquisar_arquivo = ttk.Button(tela, text='Pesquisar', style='pesquisa.TButton', command=pesquisar_arquivo)
botao_de_inicializacao = ttk.Button(tela, text='teste', style='TButton', command=pesquisar)

######### POSICAO DOS COMPONENTES #########
figura1.grid(row=0, column=0, pady=(0, 80))
figura2.grid(row=0, column=2, pady=(0, 80))

titulo.grid(row=0, column=1, pady=(0, 260))

texto_pesquisa.grid(row=0, column=1, pady=(0, 125), padx=(0, 198))

botao_pesquisar_arquivo.grid(row=0, column=1, pady=(49, 130), padx=(310, 0))
texto_arquivo.grid(row=0, column=1, pady=(50, 130), ipadx=80, ipady=4, padx=(0, 70))

botao_de_inicializacao.grid(row=0, column=1, pady=(150, 140))

texto_de_sucesso.grid(row=0, column=1, pady=(80, 0))

texto_de_aviso.grid(row=0, column=1, pady=(150, 0))
texto_de_aviso_2.grid(row=0, column=1, pady=(200, 10))
tela.mainloop()