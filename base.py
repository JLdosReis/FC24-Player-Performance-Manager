import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import json
from tkinter import filedialog
import numpy as np

class Jogador:
    def __init__(self, nome, geral, potencial_min, potencial_max):
        self.nome = nome
        self.geral = geral
        self.potencial_min = [potencial_min]
        self.potencial_max = [potencial_max]
        self.gerais = [geral]  # Histórico de geral
    
    def atualizar_potencial(self, novo_geral, novo_pot_min, novo_pot_max):
        self.geral = novo_geral
        self.gerais.append(novo_geral)
        self.potencial_min.append(novo_pot_min)
        self.potencial_max.append(novo_pot_max)
    
    # Converte o jogador para dicionário
    def to_dict(self):
        return {
            'nome': self.nome,
            'geral': self.geral,
            'gerais': self.gerais,
            'potencial_min': self.potencial_min,
            'potencial_max': self.potencial_max
        }
    
    # Cria um jogador a partir de um dicionário
    @staticmethod
    def from_dict(data):
        jogador = Jogador(data['nome'], data['geral'], data['potencial_min'][0], data['potencial_max'][0])
        jogador.potencial_min = data['potencial_min']
        jogador.potencial_max = data['potencial_max']
        jogador.gerais = data['gerais']
        return jogador

class App:
    def __init__(self, root):
        self.jogadores = []
        self.root = root
        self.root.title("Gerenciador de Jogadores")

        # Frame para dados do jogador
        self.frame_dados = ttk.LabelFrame(root, text="Dados do Jogador")
        self.frame_dados.grid(row=0, column=0, padx=10, pady=10)

        self.nome_label = ttk.Label(self.frame_dados, text="Nome:")
        self.nome_label.grid(row=0, column=0)
        self.nome_entry = ttk.Entry(self.frame_dados)
        self.nome_entry.grid(row=0, column=1)

        self.geral_label = ttk.Label(self.frame_dados, text="Geral:")
        self.geral_label.grid(row=1, column=0)
        self.geral_entry = ttk.Entry(self.frame_dados)
        self.geral_entry.grid(row=1, column=1)

        self.pot_min_label = ttk.Label(self.frame_dados, text="Potencial Mínimo:")
        self.pot_min_label.grid(row=2, column=0)
        self.pot_min_entry = ttk.Entry(self.frame_dados)
        self.pot_min_entry.grid(row=2, column=1)

        self.pot_max_label = ttk.Label(self.frame_dados, text="Potencial Máximo:")
        self.pot_max_label.grid(row=3, column=0)
        self.pot_max_entry = ttk.Entry(self.frame_dados)
        self.pot_max_entry.grid(row=3, column=1)

        # Botão para adicionar jogador
        self.add_button = ttk.Button(self.frame_dados, text="Adicionar Jogador", command=self.adicionar_jogador)
        self.add_button.grid(row=4, column=1)

        # Frame para lista de jogadores
        self.frame_lista = ttk.LabelFrame(root, text="Lista de Jogadores")
        self.frame_lista.grid(row=0, column=1, padx=10, pady=10)

        self.jogadores_listbox = tk.Listbox(self.frame_lista)
        self.jogadores_listbox.grid(row=0, column=0, rowspan=6)

        # Botões para atualizar e remover jogador
        self.update_button = ttk.Button(self.frame_lista, text="Atualizar Potencial", command=self.atualizar_jogador)
        self.update_button.grid(row=0, column=1)

        self.remove_button = ttk.Button(self.frame_lista, text="Remover Jogador", command=self.remover_jogador)
        self.remove_button.grid(row=1, column=1)

        # Botão para salvar e carregar dados
        self.save_button = ttk.Button(self.frame_lista, text="Salvar Dados", command=self.salvar_dados)
        self.save_button.grid(row=2, column=1)

        self.load_button = ttk.Button(self.frame_lista, text="Carregar Dados", command=self.carregar_dados)
        self.load_button.grid(row=3, column=1)

        # Botão para mostrar gráfico
        self.grafico_button = ttk.Button(self.frame_lista, text="Mostrar Gráfico", command=self.mostrar_grafico)
        self.grafico_button.grid(row=4, column=1)

        # Botão para mostrar histórico
        self.historico_button = ttk.Button(self.frame_lista, text="Mostrar Histórico", command=self.mostrar_historico)
        self.historico_button.grid(row=5, column=1)

        # Campo de pesquisa
        self.search_label = ttk.Label(root, text="Pesquisar Jogador:")
        self.search_label.grid(row=1, column=0, padx=10, pady=5)

        self.search_entry = ttk.Entry(root)
        self.search_entry.grid(row=1, column=1, padx=10, pady=5)

        self.search_button = ttk.Button(root, text="Pesquisar", command=self.pesquisar_jogador)
        self.search_button.grid(row=1, column=2, padx=10, pady=5)

    def adicionar_jogador(self):
        nome = self.nome_entry.get()
        try:
            geral = int(self.geral_entry.get())
            pot_min = int(self.pot_min_entry.get())
            pot_max = int(self.pot_max_entry.get())

            if nome == "":
                raise ValueError("O nome não pode estar vazio")

            jogador = Jogador(nome, geral, pot_min, pot_max)
            self.jogadores.append(jogador)

            self.jogadores_listbox.insert(tk.END, nome)
            self.limpar_campos()
        except ValueError as e:
            messagebox.showerror("Erro", f"Erro de entrada: {e}")

    def limpar_campos(self):
        self.nome_entry.delete(0, tk.END)
        self.geral_entry.delete(0, tk.END)
        self.pot_min_entry.delete(0, tk.END)
        self.pot_max_entry.delete(0, tk.END)

    def atualizar_jogador(self):
        selecionado = self.jogadores_listbox.curselection()
        if selecionado:
            index = selecionado[0]
            jogador = self.jogadores[index]
            try:
                novo_geral = int(self.geral_entry.get())
                novo_pot_min = int(self.pot_min_entry.get())
                novo_pot_max = int(self.pot_max_entry.get())
                jogador.atualizar_potencial(novo_geral, novo_pot_min, novo_pot_max)
                messagebox.showinfo("Sucesso", f"Dados de {jogador.nome} atualizados.")
                self.limpar_campos()
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira valores numéricos para geral, potencial mínimo e máximo.")
        else:
            messagebox.showerror("Erro", "Selecione um jogador na lista.")

    def remover_jogador(self):
        selecionado = self.jogadores_listbox.curselection()
        if selecionado:
            index = selecionado[0]
            self.jogadores.pop(index)
            self.jogadores_listbox.delete(index)
        else:
            messagebox.showerror("Erro", "Selecione um jogador na lista.")

    def mostrar_grafico(self):
        selecionado = self.jogadores_listbox.curselection()
        if selecionado:
            index = selecionado[0]
            jogador = self.jogadores[index]

            fig = Figure(figsize=(6, 4))
            ax = fig.add_subplot(111)

            x = range(1, len(jogador.potencial_min) + 1)
            ax.plot(x, jogador.potencial_min, label="Potencial Mínimo")
            ax.plot(x, jogador.potencial_max, label="Potencial Máximo")

            # Adicionar linha de tendência
            z = np.polyfit(x, jogador.potencial_min, 1)
            p = np.poly1d(z)
            ax.plot(x, p(x), "r--", label="Tendência Potencial Mínimo")

            ax.set_title(f"Progresso de {jogador.nome}")
            ax.set_xlabel("Número de Atualizações")
            ax.set_ylabel("Potencial")

            ax.legend()

            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.draw()
            canvas.get_tk_widget().grid(row=2, column=0, columnspan=3)

            # Botão para exportar gráfico
            export_button = ttk.Button(self.root, text="Exportar Gráfico", command=lambda: self.exportar_grafico(fig))
            export_button.grid(row=3, column=1)

    def mostrar_historico(self):
        selecionado = self.jogadores_listbox.curselection()
        if selecionado:
            index = selecionado[0]
            jogador = self.jogadores[index]
            historico = f"Histórico de {jogador.nome}:\n\nGeral: {jogador.gerais}\nPotencial Mínimo: {jogador.potencial_min}\nPotencial Máximo: {jogador.potencial_max}"
            messagebox.showinfo("Histórico do Jogador", historico)
        else:
            messagebox.showerror("Erro", "Selecione um jogador na lista.")

    def exportar_grafico(self, fig):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            fig.savefig(file_path)
            messagebox.showinfo("Sucesso", "Gráfico exportado com sucesso!")

    def salvar_dados(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as f:
                json.dump([jogador.to_dict() for jogador in self.jogadores], f)
            messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")

    def carregar_dados(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.jogadores = [Jogador.from_dict(item) for item in data]
                self.jogadores_listbox.delete(0, tk.END)
                for jogador in self.jogadores:
                    self.jogadores_listbox.insert(tk.END, jogador.nome)
            messagebox.showinfo("Sucesso", "Dados carregados com sucesso!")

    def pesquisar_jogador(self):
        query = self.search_entry.get().lower()
        for i, jogador in enumerate(self.jogadores):
            if query in jogador.nome.lower():
                self.jogadores_listbox.selection_clear(0, tk.END)
                self.jogadores_listbox.selection_set(i)
                return
        messagebox.showinfo("Resultado", "Nenhum jogador encontrado.")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
