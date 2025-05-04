class Tarefas:
    def _init_(self, descrição, data_vencimento, status):
        self.descrição = descrição
        self.data_vencimento = data_vencimento
        self.status = status

lista_tarefas = []

def adicionar_tarefas(descrição, data_vencimento, status):
    nova_tarefa = Tarefas(descrição, data_vencimento, status)
    lista_tarefas.append(nova_tarefa)

def listar_tarefas(filtro_status=None, filtro_data=None):
    for tarefa in lista_tarefas:
        if filtro_status and tarefa.status.lower() != filtro_status.lower():
            continue

        if filtro_data and tarefa.data_vencimento != filtro_data:
            continue

        print(f"{tarefa.descrição} | Vencimento: {tarefa.data_vencimento} | Status: {tarefa.status}")


adicionar_tarefas("Estudar Python", "30/04/2025", "pendente")
adicionar_tarefas("Enviar travazap para o Lucas", "01/05/2025", "pendente")
adicionar_tarefas("Fazer trabalho do Léo", "04/05/2025", "pendente")

print("Todas as tarefas:")
listar_tarefas()

print("\nTarefas pendentes:")
listar_tarefas(filtro_status="pendente")

print("\nTarefas com vencimento em 04/05/2025:")
listar_tarefas(filtro_data="04/05/2025")