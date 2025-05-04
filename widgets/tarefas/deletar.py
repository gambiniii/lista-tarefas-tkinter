import os
from tkinter import *
from tkinter import messagebox


class DeletarTarefa(Frame):
    def __init__(self, master=None, nome_tarefa=None, ao_deletar=None):
        super().__init__(master)
        self.master = master
        self.nome_tarefa = nome_tarefa
        self.ao_deletar = ao_deletar

        self.fonte = ("Arial", 12)

        Label(self, text=f"Você tem certeza que deseja deletar a tarefa {nome_tarefa}?", font=self.fonte).pack(pady=10)

        Button(
            self,
            text="Deletar",
            command=self.deletar,
            font=self.fonte,
            bg="#F44336",
            fg="white",
        ).pack(pady=10)

        Button(
            self,
            text="Cancelar",
            command=self.master.destroy,
            font=self.fonte,
            bg="#8C8C8C",
            fg="white",
        ).pack(pady=5)

    def deletar(self):
        caminho_arquivo = os.path.join("./data", f"{self.nome_tarefa}.json")

        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)
            messagebox.showinfo("Sucesso", "Tarefa deletada com sucesso.")
            if self.ao_deletar:
                self.ao_deletar()
            self.master.destroy()
        else:
            messagebox.showerror("Erro", "Tarefa não encontrada.")
