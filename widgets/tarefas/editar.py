import os
import json
from tkinter import *
from tkinter import messagebox
from enums.status_tarefa import StatusTarefa
from helpers.data_valida import data_valida


class EditarTarefa(Frame):
    def __init__(self, master=None, tarefa=None, ao_salvar=None):
        super().__init__(master)
        self.master = master
        self.tarefa = tarefa
        self.ao_salvar = ao_salvar

        self.fonte = ("Arial", 12)

        Label(self, text="Nome:", font=self.fonte).pack(anchor="w")
        self.entry_nome = Entry(self, font=self.fonte)
        self.entry_nome.insert(0, self.tarefa.get("nome", ""))
        self.entry_nome.pack(fill="x", pady=5)

        Label(self, text="Descrição:", font=self.fonte).pack(anchor="w")
        self.entry_descricao = Entry(self, font=self.fonte)
        self.entry_descricao.insert(0, self.tarefa.get("descricao", ""))
        self.entry_descricao.pack(fill="x", pady=5)

        Label(self, text="Vencimento:", font=self.fonte).pack(anchor="w")
        self.entry_vencimento = Entry(self, font=self.fonte)
        self.entry_vencimento.insert(0, self.tarefa.get("vencimento", ""))
        self.entry_vencimento.pack(fill="x", pady=5)

        Label(self, text="Status:", font=self.fonte).pack(anchor="w")
        self.status_var = StringVar()
        self.status_var.set(self.tarefa.get("status", StatusTarefa.PENDENTE.value))
        options = [status.value for status in StatusTarefa]
        OptionMenu(self, self.status_var, *options).pack(fill="x", pady=5)

        Button(
            self,
            text="Salvar",
            command=self.salvar,
            font=self.fonte,
            bg="#2196F3",
            fg="white",
        ).pack(pady=10)

    def salvar(self):
        nome = self.entry_nome.get()
        descricao = self.entry_descricao.get()
        vencimento = self.entry_vencimento.get()
        status = self.status_var.get()

        if not (nome and descricao and vencimento and status):
            messagebox.showerror("Tarefa inválida!", "Preencha todos os campos.")
            return

        if not data_valida(vencimento):
            messagebox.showerror(
                "Data inválida", "A data deve estar no formato dd/mm/aaaa e ser válida."
            )
            return

        tarefa = {
            "nome": nome,
            "descricao": descricao,
            "vencimento": vencimento,
            "status": status,
        }

        if not os.path.exists("./data"):
            os.makedirs("./data")

        nome_arquivo = tarefa["nome"].strip().replace(" ", "_") + ".json"
        caminho = os.path.join("./data", nome_arquivo)

        with open(caminho, "w", encoding="utf-8") as file:
            json.dump(tarefa, file, ensure_ascii=False, indent=4)

        if self.ao_salvar:
            self.ao_salvar()

        self.master.destroy()
