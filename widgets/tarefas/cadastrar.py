from tkinter import *
import json
import os
from tkinter import messagebox
from enums.status_tarefa import StatusTarefa
from helpers.data_valida import data_valida


class Cadastro(Frame):
    def __init__(self, master=None, ao_salvar=None):
        super().__init__(master)
        self.master = master
        self.ao_salvar = ao_salvar

        self.fonte = ("Arial", 12)

        self.container = LabelFrame(
            self, text="Nova Tarefa", font=("Arial", 12, "bold"), padx=15, pady=10
        )
        self.container.pack(fill="both", expand=True, padx=20, pady=10)

        self.criar_campo("Nome da tarefa:", "entry_nome")
        self.criar_campo("Descrição da tarefa:", "entry_descricao")
        self.criar_campo("Vencimento da tarefa:", "entry_vencimento")
        self.criar_campo("Status da tarefa:", "entry_status", is_status=True)

        self.botaoSalvar = Button(
            self,
            text="Salvar",
            command=self.cadastrar,
            font=self.fonte,
            bg="#2196F3",
            fg="white",
            padx=10,
            pady=5,
        )
        self.botaoSalvar.pack(pady=10)

    # Função que cria os campos da tela
    def criar_campo(self, texto, attr_name, is_status=False):
        frame = Frame(self.container)
        frame.pack(fill="x", pady=4)

        label = Label(frame, text=texto, font=self.fonte, width=18, anchor="w")
        label.pack(side=LEFT)

        if is_status:
            # Cria um menu com os status da tarefa
            var = StringVar()
            var.set(StatusTarefa.PENDENTE.value)
            options = [status.value for status in StatusTarefa]
            dropdown = OptionMenu(frame, var, *options)
            dropdown.config(font=self.fonte)
            dropdown.pack(side=LEFT, padx=5)
            setattr(self, attr_name, var)
        else:
            # Cria um campo de texto normal
            entry = Entry(frame, font=self.fonte, width=25)
            entry.pack(side=LEFT, padx=5)
            setattr(self, attr_name, entry)

    # Função que salva a tarefa
    def cadastrar(self):
        # Pega o que o usuário digitou
        nome = self.entry_nome.get()
        descricao = self.entry_descricao.get()
        vencimento = self.entry_vencimento.get()
        status = self.entry_status.get()

        # Verifica se os campos estão preenchidos
        if not (nome or descricao or vencimento or status):
            messagebox.showerror("Tarefa inválida!", "Preencha todos os campos.")
            return

        # Valida a data
        if not data_valida(vencimento):
            messagebox.showerror(
                "Data inválida", "A data deve estar no formato dd/mm/aaaa e ser válida."
            )
            return

        # Cria um dicionário com as informações
        tarefa = {
            "nome": nome,
            "descricao": descricao,
            "vencimento": vencimento,
            "status": status,
        }

        # Cria a pasta "data" se ela não existir
        if not os.path.exists("./data"):
            os.makedirs("./data")

        # Cria o nome do arquivo com base no nome da tarefa
        nome_arquivo = tarefa["nome"].strip().replace(" ", "_") + ".json"
        caminho = os.path.join("./data", nome_arquivo)

        # Salva os dados no arquivo JSON
        with open(caminho, "w", encoding="utf-8") as file:
            json.dump(tarefa, file)

        # Se tiver uma função ao_salvar, executa ela
        if self.ao_salvar:
            self.ao_salvar()

        # Fecha a janela
        self.master.destroy()