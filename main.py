import customtkinter as ctk
import math
import re

# --- Configuração da Janela ---
janela = ctk.CTk()
janela.title("Calculadora")
janela.geometry("320x450")
janela.minsize(320, 450)
janela.maxsize(600, 700)

# --- Variáveis Globais ---
limpar_tela = False
historico_contas = []

# --- FUNÇÕES DO HISTÓRICO ---
def reativar_botoes():
    btn_historico.configure(state="normal")
    for btn in frame_botoes.winfo_children():
        btn.configure(state="normal")

def fechar_historico():
    frame_historico.place_forget()
    janela.after(150, reativar_botoes)

def verificar_clique_fora(event):
    if frame_historico.winfo_ismapped():
        nome_widget_clicado = str(event.widget)
        nome_gaveta = str(frame_historico)
        
        if nome_gaveta not in nome_widget_clicado:
            fechar_historico()

def usar_historico(resultado):
    visor.delete(0, "end")
    visor.insert(0, resultado)
    global limpar_tela
    limpar_tela = True
    fechar_historico()

def abrir_historico():
    # 1. Limpa os itens antigos
    for widget in scroll_hist.winfo_children():
        widget.destroy()
        
    # 2. Cria os itens
    if len(historico_contas) == 0:
        lbl_vazio = ctk.CTkLabel(scroll_hist, text="Ainda não há histórico.", font=("Arial", 14))
        lbl_vazio.pack(pady=20, anchor="e", padx=20)
    else:
        for item in historico_contas:
            conta_str, resultado_str = item.split(" = ")
            btn_item = ctk.CTkButton(
                scroll_hist,
                text=f"{conta_str} = {resultado_str}",
                font=("Arial", 16),
                fg_color="transparent",
                text_color="white",
                hover_color="#333333",
                anchor="e",
                command=lambda r=resultado_str: usar_historico(r)
            )
            btn_item.pack(fill="x", pady=2, padx=10)

    # 3. Faz o painel do histórico aparecer por cima da metade da tela
    frame_historico.place(relx=0, rely=0.4, relwidth=1, relheight=0.6)
    frame_historico.lift() 
    
    # 4. Desativa os botões físicos atrás da gaveta 
    btn_historico.configure(state="disabled")
    for btn in frame_botoes.winfo_children():
        btn.configure(state="disabled")


# --- FUNÇÕES AUXILIARES DA CALCULADORA ---
def limpar():
    global limpar_tela
    visor.delete(0, "end")
    lbl_conta_atual.configure(text="") 
    limpar_tela = False

def apagar():
    texto_atual = visor.get()
    visor.delete(0, "end")
    visor.insert(0, texto_atual[:-1])

def calcular():
    global limpar_tela
    texto_atual = visor.get()

    if texto_atual and texto_atual[-1] in ['+', '−', '×', '÷']:
        pass

    else:
        try:
            conta_original = texto_atual 
            conta = (texto_atual.replace("×", "*")
                                .replace('÷', '/')
                                .replace('−', '-')
                                .replace(',', '.')
                                .replace('√', 'math.sqrt'))
            if '%' in conta:
                conta = re.sub(r'(\d+(?:\.\d+)?)([\+\-])(\d+(?:\.\d+)?)%', r'\1\2(\1*\3/100)', conta)
            
                conta = conta.replace('%', '/100')
                    
            resultado_math = eval(conta, {"__builtins__": None}, {"math": math})
    
            if resultado_math == int(resultado_math):
                resultado_math = int(resultado_math)
    
            resultado_final = str(resultado_math).replace('.', ',')
            lbl_conta_atual.configure(text=f"{conta_original} =")
    
            visor.delete(0, "end")
            visor.insert(0, resultado_final)
                    
            historico_contas.append(f"{conta_original} = {resultado_final}")
            limpar_tela = True

        except ZeroDivisionError:
            visor.delete(0, "end")
            visor.insert(0, "Impossível dividir por 0")
            limpar_tela = True
            
        except (SyntaxError, NameError, TypeError):
            visor.delete(0, "end")
            visor.insert(0, "Erro")
            limpar_tela = True

def calcular_raiz():
    global limpar_tela
    texto_atual = visor.get()

    try:
        conta_original = texto_atual 
                
        num_str = texto_atual.replace(',', '.')
        numero = float(num_str)
                
        resultado_math = math.sqrt(numero)
    
        if resultado_math == int(resultado_math):
            resultado_math = int(resultado_math)
    
        resultado_final = str(resultado_math).replace('.', ',')
                
        lbl_conta_atual.configure(text=f"√({conta_original}) ")
                
        visor.delete(0, "end")
        visor.insert(0, resultado_final)
                
        historico_contas.append(f"√{conta_original} = {resultado_final}")
        limpar_tela = True

    except ValueError:
        visor.delete(0, "end")
        visor.insert(0, "Erro")
                
        limpar_tela = True

def add_operador(valor):
    texto_atual = visor.get()
    visor.delete(0, "end")

    if valor == '%':
        if texto_atual != "" and texto_atual[-1] in '0123456789)':
            visor.insert(0, texto_atual + '%')
        else:
            visor.insert(0, texto_atual)
    
    elif valor in ['+', '-', '×', '−', '÷']:
    
        if texto_atual == "":
            visor.insert(0, "0" + valor)
        elif texto_atual[-1] in ['+', '−', '×', '÷']:
            visor.insert(0, texto_atual[:-1] + valor)
        else:
            visor.insert(0, texto_atual + valor)

    elif valor == ',':

        if texto_atual == "" or texto_atual[-1] in ['+', '−', '×', '÷']:
            visor.insert(0, texto_atual + "0,")
        elif texto_atual[-1] == ',':
            visor.insert(0, texto_atual)
        else:
            visor.insert(0, texto_atual + valor)

def add_num(valor):
    texto_atual = visor.get()
    visor.delete(0, "end")
    visor.insert(0, texto_atual + str(valor))


# --- FUNÇÃO PRINCIPAL DA CALCULADORA ---
def clique_botao(valor):
    if frame_historico.winfo_ismapped():
        fechar_historico()
        return
    
    global limpar_tela
    texto_atual = visor.get()
    
    if limpar_tela:
        if valor in ['+', '−', '×', '÷', '%']:
            limpar_tela = False

        elif valor in '0123456789':
            visor.delete(0, "end")
            texto_atual = ""
            limpar_tela = False
        elif valor == ',':
            visor.delete(0, "end")
            texto_atual = "0" # Se clicar em vírgula logo após o resultado, começa com "0,"
            limpar_tela = False
        elif valor in ['C', '⌫']:
            limpar_tela = False
        
    if valor == 'C':
        limpar()
        
    elif valor == '⌫':
        apagar()
            
    elif valor == '=':
        calcular()
        
    elif valor == '√':
        calcular_raiz()

    elif valor in ['%', '+', '-', '×', '−', '÷', ',']:
        add_operador(valor)
            
    else:
        add_num(valor)

# --- INTERFACE (UI) ---

## Histórico rápido da conta em andamento
lbl_conta_atual = ctk.CTkLabel(janela, text="", font=("Arial", 14), text_color="gray", anchor="e")
lbl_conta_atual.pack(padx=10, fill="x")

# 1. Visor
visor = ctk.CTkEntry(janela, font=("Arial", 30), justify="right", height=50)
visor.pack(padx=10, pady=10, fill="x")

# 2. Botão de abrir o histórico
btn_historico = ctk.CTkButton(janela, text="Ver Histórico", fg_color="transparent", border_width=1, command=abrir_historico)
btn_historico.pack(pady=5)

# 3. Botões Numéricos
frame_botoes = ctk.CTkFrame(janela, fg_color="transparent")
frame_botoes.pack(padx=10, pady=10, fill="both", expand=True)

for i in range(4):
    frame_botoes.grid_columnconfigure(i, weight=1)
for i in range(5):
    frame_botoes.grid_rowconfigure(i, weight=1)

teclas = [
    'C', '√', '%', '÷',
    '7', '8', '9', '×',
    '4', '5', '6', '−',
    '1', '2', '3', '+',
    '⌫', '0', ',', '='
]

linha = 0
coluna = 0
for texto in teclas:
    # --- PERSONALIZAÇÃO DE CORES ---
    if texto == '=':
        cor_bg = "#2ecc71"
        cor_hover = "#27ae60"
    else:
        cor_bg = "#3e3e3e"
        cor_hover = "#4e4e4e"
    btn = ctk.CTkButton(
        frame_botoes,
        text=texto,
        font=("Arial", 20),
        fg_color=cor_bg,
        hover_color=cor_hover,
        command=lambda t=texto: clique_botao(t)
    )
    btn.grid(row=linha, column=coluna, padx=5, pady=5, sticky="nsew")
    coluna += 1
    if coluna == 4:
        coluna = 0
        linha += 1

# 4. PAINEL DE HISTÓRICO SOBREPOSTO 
frame_historico = ctk.CTkFrame(janela, fg_color="#2b2b2b", corner_radius=0)

btn_fechar_hist = ctk.CTkButton(frame_historico, text="X", width=30, height=30, 
                                fg_color="transparent", hover_color="#c42b1c", command=fechar_historico)
btn_fechar_hist.pack(anchor="ne", padx=5, pady=5)

scroll_hist = ctk.CTkScrollableFrame(frame_historico, fg_color="transparent")
scroll_hist.pack(fill="both", expand=True)

janela.bind_all("<Button-1>", verificar_clique_fora)

# --- EXECUÇÃO ---
janela.mainloop()