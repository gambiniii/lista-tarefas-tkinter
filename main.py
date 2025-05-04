from tkinter import Tk
from widgets.tarefas.listar import ListaTarefas


def main():
    root = Tk()
    root.title("App de Tarefas ✅")
    root.geometry("600x500")
    app = ListaTarefas(master=root)
    app.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
