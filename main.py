import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
from PIL import Image, ImageTk
import sqlite3
import os








def tela_de_diario(data_selecionada, obra_id, conteudo_diario=None):

    Tela_de_diario = tk.Toplevel()
    Tela_de_diario.geometry("1025x650")

    label_data = ttk.Label(Tela_de_diario, text = data_selecionada ,font = ('Arial', 10))
    label_data.grid(row=0, column=0)

    label_diario = ttk.Label(Tela_de_diario, text = 'Escreva suas tarefas:',font = ('Arial', 10))
    label_diario.grid(row=1, column=0)

    text_diario = Text(Tela_de_diario, bd=3, relief='sunken')
    text_diario.grid(row=1, column=1)

    if conteudo_diario:
        text_diario.insert("1.0", conteudo_diario)

    def salvar_diario():
        conteudo = text_diario.get('1.0', 'end')
        # Salve o conteúdo do diário no banco de dados de diários
        cursor_diarios.execute("INSERT INTO diarios (obra_id, data, conteudo) VALUES (?, ?, ?)",
                               (obra_id, data_selecionada, conteudo))
        conn_diarios.commit()

        

    botao_salvar = ttk.Button(
            Tela_de_diario,
            text='Salvar!',
            command = salvar_diario
        )
    botao_salvar.grid(row=2, column=1)


# tela de calendario
def tela_de_calendario(obra_id):

    Tela_de_calendario = tk.Toplevel()
    Tela_de_calendario.geometry("1025x650")

    # Use o ID da obra para consultar o banco de dados e obter as informações da obra
    cursor.execute("SELECT nome, data_inicio FROM obras WHERE id=?", (obra_id,))
    obra_info = cursor.fetchone()

    if obra_info:
        nome_obra, data_inicio = obra_info

        # Use as informações da obra para exibir na tela de calendário
        label_nome_obra = ttk.Label(Tela_de_calendario, text=f'Nome da Obra: {nome_obra}', font=('Arial', 10))
        label_nome_obra.pack()

        label_data_inicio = ttk.Label(Tela_de_calendario, text=f'Data de Início: {data_inicio}', font=('Arial', 10))
        label_data_inicio.pack()

        ano = ['2023','2024','2025','2026','2027','2028','2029','2030','2031']
        # Variável para armazenar o ano selecionado 
        ano_selecionado = tk.StringVar(root)
        ano_selecionado.set(ano[0]) 


        # Função para obter a data selecionada no calendário

        def obter_conteudo_do_banco_de_dados(obra_id, data):
            cursor_diarios.execute("SELECT conteudo FROM diarios WHERE obra_id=? AND data=?", (obra_id, data))
            resultado = cursor_diarios.fetchone()
            if resultado:
                return resultado[0]
            return None
        
        def get_selected_date():
            selected_date = cal.get_date()
            conteudo_diario = obter_conteudo_do_banco_de_dados(obra_id, selected_date)
            tela_de_diario(selected_date, obra_id, conteudo_diario)



        # Crie um frame para usar pack dentro dele
        frame = tk.Frame(Tela_de_calendario)
        frame.pack(fill='x', padx=5, pady=5)
        
        # Crie um widget de calendário
        cal = Calendar(frame, selectmode="day", year=int(ano_selecionado.get()), month=1, day=1, width = 800, height = 300)
        cal.pack(fill ='x', padx=5, pady=5)

        # Botão para obter a data selecionada
        btn = tk.Button(frame, text="Obter Data Selecionada", command=get_selected_date)
        btn.pack(padx=5, pady=5)


# tela adicionar obra
def tela_add_obra():
    tela_add_obra = tk.Toplevel()
    tela_add_obra.geometry("1025x650")


    label_nome_obra = ttk.Label(tela_add_obra, text = 'Digite o nome da obra:' ,font = ('Arial', 10))
    label_nome_obra.grid(row=0, column=0)

    text_nome_obra = Text(tela_add_obra, bd=3, relief='sunken', width=50, height=1)
    text_nome_obra.grid(row=0, column=1)

    label_nome_engenheiro = ttk.Label(tela_add_obra, text = 'Digite o nome do Engenheiro:' ,font = ('Arial', 10))
    label_nome_engenheiro.grid(row=1, column=0)

    text_nome_engenheiro = Text(tela_add_obra, bd=3, relief='sunken', width=50, height=1)
    text_nome_engenheiro.grid(row=1, column=1)

    label_data_inicio = ttk.Label(tela_add_obra, text = 'Digite a data de inicio:' ,font = ('Arial', 10))
    label_data_inicio.grid(row=2, column=0)

    text_data_inicio = Text(tela_add_obra, bd=3, relief='sunken', width=50, height=1)
    text_data_inicio.grid(row=2, column=1)

    def salvar_obra():
        # Obtém os valores dos campos de entrada
        nome_obra = text_nome_obra.get("1.0", "end-1c")
        nome_engenheiro = text_nome_engenheiro.get("1.0", "end-1c")
        data_inicio = text_data_inicio.get("1.0", "end-1c")

        # Insere os valores no banco de dados
        cursor.execute("INSERT INTO obras (nome, engenheiro, data_inicio) VALUES (?, ?, ?)",
                       (nome_obra, nome_engenheiro, data_inicio))
        conn.commit()

        # Fecha a tela de adicionar obra após salvar
        tela_add_obra.destroy()

        # Atualiza o Treeview
        atualizar_treeview()

    def atualizar_treeview():
        # Limpa o Treeview
        for item in treeview.get_children():
            treeview.delete(item)

        # Consulta o banco de dados e exibe as informações no Treeview
        cursor.execute("SELECT * FROM obras")
        for row in cursor.fetchall():
            treeview.insert("", "end", values=row)
    
    botao_salvar_obra = ttk.Button(
            tela_add_obra,
            text='Salvar!',
            command = salvar_obra
        )
    botao_salvar_obra.grid(row=3, column=1)

# tela de diario

root = tk.Tk()
root.geometry("1025x650")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)


def atualizar_treeview():
    # Limpa o Treeview
    for item in treeview.get_children():
        treeview.delete(item)

    # Consulta o banco de dados e exibe as informações no Treeview
    cursor.execute("SELECT * FROM obras")
    for row in cursor.fetchall():
        treeview.insert("", "end", values=row)


def excluir_obra():
        # Obtém o ID da obra selecionada no Treeview
        selected_item = treeview.selection()
        if selected_item:
            obra_id = treeview.item(selected_item)["values"][0]

            # Exclui a obra do banco de dados
            cursor.execute("DELETE FROM obras WHERE id=?", (obra_id,))
            conn.commit()

            # Atualiza o Treeview após excluir a obra
            atualizar_treeview()


def selecionar_obra():
        # Obtém o ID da obra selecionada no Treeview
        selected_item = treeview.selection()
        if selected_item:
            obra_id = treeview.item(selected_item)["values"][0]
            tela_de_calendario(obra_id)

            


# Cria ou conecta-se ao banco de dados SQLite

# Determine o caminho completo para a pasta 'data' no seu projeto
pasta_data = os.path.join(os.getcwd(), 'data')

# Se a pasta 'data' não existir, crie-a
if not os.path.exists(pasta_data):
    os.makedirs(pasta_data)

# Especifique o caminho completo para o arquivo do banco de dados
caminho_banco_de_dados_obras = os.path.join(pasta_data, 'obras.db')

conn = sqlite3.connect(caminho_banco_de_dados_obras)
cursor = conn.cursor()

# Cria uma tabela para armazenar informações das obras
cursor.execute('''CREATE TABLE IF NOT EXISTS obras
                  (id INTEGER PRIMARY KEY,
                   nome TEXT,
                   engenheiro TEXT,
                   data_inicio TEXT)''')
conn.commit()

# Crie ou conecte-se ao banco de dados SQLite para os diários

# Especifique o caminho completo para o arquivo do banco de dados
caminho_banco_de_dados_diarios = os.path.join(pasta_data, 'diarios.db')

conn_diarios = sqlite3.connect(caminho_banco_de_dados_diarios)
cursor_diarios = conn_diarios.cursor()

# Crie uma tabela para armazenar os diários relacionados às datas
cursor_diarios.execute('''CREATE TABLE IF NOT EXISTS diarios
                         (id INTEGER PRIMARY KEY,
                          obra_id INTEGER,
                          data DATE,
                          conteudo TEXT)''')
conn_diarios.commit()


plus_icon = Image.open("C:/Users/Victor/OneDrive/Documents/ProjetoAgenda/images/plus_icon.png") 
plus_icon = plus_icon.resize((32, 32)) 
plus_icon = ImageTk.PhotoImage(plus_icon)

botao_add_diario_obra = ttk.Button(
            root, 
            image=plus_icon,
            compound=tk.LEFT,
            command = tela_add_obra
        )
botao_add_diario_obra.grid(row=0, column=1, padx=10, pady=20, sticky='n')
botao_add_diario_obra.image = plus_icon

check_icon = Image.open("C:/Users/Victor/OneDrive/Documents/ProjetoAgenda/images/check_icon.png") 
check_icon = check_icon.resize((32, 32)) 
check_icon = ImageTk.PhotoImage(check_icon)

botao_check_diario_obra = ttk.Button(
            root, 
            image=check_icon,
            compound=tk.LEFT,
            command = selecionar_obra
        )
botao_check_diario_obra.place(x = 967, y = 80, width= 48)
botao_check_diario_obra.image = check_icon

cross_icon = Image.open("C:/Users/Victor/OneDrive/Documents/ProjetoAgenda/images/red_cross_icon.png") 
cross_icon = cross_icon.resize((32, 32)) 
cross_icon = ImageTk.PhotoImage(cross_icon)

botao_cross_diario_obra = ttk.Button(
            root, 
            image=cross_icon,
            compound=tk.LEFT,
            command = excluir_obra
        )
botao_cross_diario_obra.place(x = 967, y = 140, width= 48)
botao_cross_diario_obra.image = cross_icon



# Crie um Treeview (ListView)
treeview = ttk.Treeview(root, columns=("ID", "Nome", "Engenheiro", "Data de Início"))


# Defina os cabeçalhos das colunas
treeview.heading("#0", text="ID")
treeview.heading("#1", text="Nome")
treeview.heading("#2", text="Engenheiro")
treeview.heading("#3", text="Data de Início")

# Consulta o banco de dados e exibe as informações no Treeview
cursor.execute("SELECT * FROM obras")
for row in cursor.fetchall():
    treeview.insert("", "end", values=row)

# Coloque o Treeview na segunda coluna
treeview.grid(row=0, column=0, padx=10, pady=20, sticky='nsew')

# Configuração do peso das linhas e colunas para redimensionamento
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)



root.mainloop()
# Fecha a conexão com o banco de dados após a execução do programa
conn.close()

