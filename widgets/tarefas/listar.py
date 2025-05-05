# widgets/tarefas/listar.py
import os
import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from enums.status_tarefa import StatusTarefa
from widgets.tarefas.cadastrar import Cadastro
from widgets.tarefas.editar import EditarTarefa
from widgets.tarefas.deletar import DeletarTarefa


class ListaTarefas(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(padx=20, pady=10)

        self.fonte = ("Arial", 12)

        Label(self, text="Tarefas cadastradas:", font=self.fonte).pack(anchor="w")

        filtros_frame = Frame(self)
        filtros_frame.pack(fill="x", pady=5)

        Label(filtros_frame, text="Filtrar por vencimento:", font=self.fonte).pack(side=LEFT)
        self.filtro_vencimento = Entry(filtros_frame, font=self.fonte, width=12)
        self.filtro_vencimento.pack(side=LEFT, padx=5)

        Label(filtros_frame, text="Status:", font=self.fonte).pack(side=LEFT)
        self.filtro_status = StringVar()
        self.filtro_status.set("")  # vazio significa "sem filtro"
        status_options = [""] + [status.value for status in StatusTarefa]
        self.status_dropdown = OptionMenu(filtros_frame, self.filtro_status, *status_options)
        self.status_dropdown.config(font=self.fonte)
        self.status_dropdown.pack(side=LEFT, padx=5)

        Button(filtros_frame, text="Aplicar Filtros", font=self.fonte, command=self.carregarTarefas).pack(side=LEFT, padx=10)

        self.tree = ttk.Treeview(
            self,
            columns=("nome", "descricao", "vencimento", "status"),
            show="headings",
            height=10,
        )
        self.tree.pack(fill="both", expand=True, pady=10)

        self.tree.heading("nome", text="Nome")
        self.tree.heading("descricao", text="Descrição")
        self.tree.heading("vencimento", text="Vencimento")
        self.tree.heading("status", text="Status")

        # Botões de editar, deletar e nova tarefa
        self.btnNova = Button(
            self,
            text="Nova Tarefa",
            font=self.fonte,
            bg="#4CAF50",
            fg="white",
            command=self.abrirCadastro,
        )
        self.btnNova.pack(pady=10)

        self.btnEditar = Button(
            self,
            text="Editar Tarefa",
            font=self.fonte,
            bg="#FF9800",
            fg="white",
            command=self.editarTarefa,
        )
        self.btnEditar.pack(pady=5)

        self.btnDeletar = Button(
            self,
            text="Deletar Tarefa",
            font=self.fonte,
            bg="#F44336",
            fg="white",
            command=self.deletarTarefa,
        )
        self.btnDeletar.pack(pady=5)

        self.carregarTarefas()

    def carregarTarefas(self):
        vencimento_filtro = self.filtro_vencimento.get().strip()
        status_filtro = self.filtro_status.get().strip()

        for row in self.tree.get_children():
            self.tree.delete(row)

        if not os.path.exists("./data"):
            os.makedirs("./data")

        for nome_arquivo in os.listdir("./data"):
            if nome_arquivo.endswith(".json"):
                caminho = os.path.join("./data", nome_arquivo)
                try:
                    with open(caminho, "r", encoding="utf-8") as file:
                        tarefa = json.load(file)

                    vencimento = tarefa.get("vencimento", "")
                    status = tarefa.get("status", "")

                    if vencimento_filtro and vencimento_filtro not in vencimento:
                        continue
                    if status_filtro and status != status_filtro:
                        continue

                    self.tree.insert(
                        "",
                        END,
                        values=(
                            tarefa.get("nome", ""),
                            tarefa.get("descricao", ""),
                            vencimento,
                            status,
                        ),
                    )

                except Exception as e:
                    print(f"Erro ao carregar {nome_arquivo}: {e}")

    def editarTarefa(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Seleção", "Selecione uma tarefa para editar.")
            return

        nome_tarefa = self.tree.item(item_selecionado)["values"][0]
        caminho_arquivo = os.path.join("./data", f"{nome_tarefa}.json")

        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, "r", encoding="utf-8") as file:
                tarefa = json.load(file)

            nova_janela = Toplevel(self.master)
            nova_janela.title(f"Editar Tarefa - {nome_tarefa}")
            nova_janela.geometry("450x300")
            EditarTarefa(
                master=nova_janela, tarefa=tarefa, ao_salvar=self.carregarTarefas
            ).pack()
        else:
            messagebox.showerror("Erro", "Tarefa não encontrada.")

    def deletarTarefa(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Seleção", "Selecione uma tarefa para deletar.")
            return

        nome_tarefa = self.tree.item(item_selecionado)["values"][0]

        nova_janela = Toplevel(self.master)
        nova_janela.title(f"Deletar Tarefa - {nome_tarefa}")
        nova_janela.geometry("400x200")
        DeletarTarefa(
            master=nova_janela, nome_tarefa=nome_tarefa, ao_deletar=self.carregarTarefas
        ).pack()

    def abrirCadastro(self):
        nova_janela = Toplevel(self.master)
        nova_janela.title("Nova Tarefa")
        nova_janela.geometry("450x300")
        Cadastro(master=nova_janela, ao_salvar=self.carregarTarefas).pack()


