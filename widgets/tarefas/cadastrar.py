from tkinter import *
import json
import os


class Cadastro(Frame):
    def __init__(self, master=None, ao_salvar=None):
        super().__init__(master)
        self.master = master
        self.ao_salvar = ao_salvar

        self.fonte = ("Arial", 12)

        # Container com borda e título
        self.container = LabelFrame(
            self, text="Nova Tarefa", font=("Arial", 12, "bold"), padx=15, pady=10
        )
        self.container.pack(fill="both", expand=True, padx=20, pady=10)

        # Adicionar os campos de entrada
        self.criar_campo("Nome da tarefa:", "entry_nome")
        self.criar_campo("Descrição da tarefa:", "entry_descricao")
        self.criar_campo("Vencimento da tarefa:", "entry_vencimento")
        self.criar_campo("Status da tarefa:", "entry_status")

        self.botaoSalvar = Button(
            self,
            text="Salvar",
            command=self.cadastro,
            font=self.fonte,
            bg="#2196F3",
            fg="white",
            padx=10,
            pady=5,
        )
        self.botaoSalvar.pack(pady=10)

    # Função para criar campos dinamicamente
    def criar_campo(self, texto, attr_name):
        frame = Frame(self.container)
        frame.pack(fill="x", pady=4)

        label = Label(frame, text=texto, font=self.fonte, width=18, anchor="w")
        label.pack(side=LEFT)

        entry = Entry(frame, font=self.fonte, width=25)
        entry.pack(side=LEFT, padx=5)

        setattr(self, attr_name, entry)

    def cadastro(self):
        tarefa = {
            "nome": self.entry_nome.get(),
            "descricao": self.entry_descricao.get(),
            "vencimento": self.entry_vencimento.get(),
            "status": self.entry_status.get(),
        }

        # Verificar se o diretório existe, senão criar
        if not os.path.exists("./data"):
            os.makedirs("./data")

        # Gerar o nome do arquivo
        nome_arquivo = tarefa["nome"].strip().replace(" ", "_") + ".json"
        caminho = os.path.join("./data", nome_arquivo)

        # Salvar tarefa no arquivo
        with open(caminho, "w", encoding="utf-8") as file:
            json.dump(tarefa, file)

        # Atualizar a lista de tarefas após salvar
        if self.ao_salvar:
            self.ao_salvar()

        # Fechar a janela após salvar
        self.master.destroy()
