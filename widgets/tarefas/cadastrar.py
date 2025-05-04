from tkinter import *
import json
import os
from enums.status_tarefa import StatusTarefa


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
            command=self.cadastro,
            font=self.fonte,
            bg="#2196F3",
            fg="white",
            padx=10,
            pady=5,
        )
        self.botaoSalvar.pack(pady=10)

    def criar_campo(self, texto, attr_name, is_status=False):
        frame = Frame(self.container)
        frame.pack(fill="x", pady=4)

        label = Label(frame, text=texto, font=self.fonte, width=18, anchor="w")
        label.pack(side=LEFT)

        if is_status:
            var = StringVar()
            var.set(StatusTarefa.PENDENTE.value)
            options = [status.value for status in StatusTarefa]
            dropdown = OptionMenu(frame, var, *options)
            dropdown.config(font=self.fonte)
            dropdown.pack(side=LEFT, padx=5)
            setattr(self, attr_name, var)
        else:
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

        if not os.path.exists("./data"):
            os.makedirs("./data")

        nome_arquivo = tarefa["nome"].strip().replace(" ", "_") + ".json"
        caminho = os.path.join("./data", nome_arquivo)

        with open(caminho, "w", encoding="utf-8") as file:
            json.dump(tarefa, file)

        if self.ao_salvar:
            self.ao_salvar()

        self.master.destroy()
