from models.cliente import Cliente, Clientes
from models.horario import Horario, Horarios
from models.servico import Servico, Servicos
from datetime import datetime, timedelta

class View:
    def cliente_admin():
        for c in View.cliente_listar():
            if c.email == "admin": return
        View.cliente_inserir("admin", "admin", "1234", "1234")

   def cliente_inserir(nome, email, fone, senha):
        if any(cliente.email == email for cliente in Clientes.listar_todos()):
            raise ValueError(f"O e-mail '{email}' já está cadastrado.")
        c = Cliente(0, nome, email, fone, senha)
        Clientes.inserir(c)

    def cliente_listar():
        return Clientes.listar()    

    def cliente_listar_id(id):
        return Clientes.listar_id(id)    

    def cliente_atualizar(id, nome, email, fone, senha):
        for cliente in Clientes.listar_todos():
            if cliente.email == email and cliente.id != id:
                raise ValueError(f"O e-mail '{email}' já está associado a outro cliente.")
        c = Cliente(id, nome, email, fone, senha)
        Clientes.atualizar(c)

    def cliente_excluir(id):
        if any(servico.cliente_id == id for servico in Servico.listar_todos()):
            raise ValueError(f"O cliente com ID {id} possui horários na agenda e não pode ser excluído.")
        c = Cliente(id, "", "", "", "")
        Clientes.excluir(c)

    def cliente_autenticar(email, senha):
        for c in View.cliente_listar():
            if c.email == email and c.senha == senha:
                return {"id" : c.id, "nome" : c.nome }
        return None

    def horario_inserir(data, confirmado, id_cliente, id_servico):
        if not any(cliente.id == id_cliente for cliente in Clientes.listar_todos()):
            raise ValueError(f"O ID do cliente {id_cliente} é inválido ou não existe.")
        if not any(servico.id == id_servico for servico in Servicos.listar_todos()):
            raise ValueError(f"O ID do serviço {id_servico} é inválido ou não existe.")
        
        c = Horario(0, data)
        c.confirmado = confirmado
        c.id_cliente = id_cliente
        c.id_servico = id_servico
        Horarios.inserir(c)
        
    def horario_listar():
        return Horarios.listar()    

    def horario_listar_disponiveis():
        horarios = View.horario_listar()
        disponiveis = []
        for h in horarios:
            if h.data >= datetime.now() and h.id_cliente == None: disponiveis.append(h)
        return disponiveis   

    def horario_atualizar(id, data, confirmado, id_cliente, id_servico):
        if not any(cliente.id == id_cliente for cliente in Clientes.listar_todos()):
            raise ValueError(f"O ID do cliente {id_cliente} é inválido ou não existe.")
        if not any(servico.id == id_servico for servico in Servicos.listar_todos()):
            raise ValueError(f"O ID do serviço {id_servico} é inválido ou não existe.")
        
        c = Horario(id, data)
        c.confirmado = confirmado
        c.id_cliente = id_cliente
        c.id_servico = id_servico
        Horarios.atualizar(c)

    def horario_excluir(id):
        horario = next((h for h in Horarios.listar_todos() if h.id == id), None)
        if horario is None:
            raise ValueError(f"Horário com ID {id} não encontrado.")
        if horario.confirmado:
            raise ValueError(f"O horário com ID {id} está agendado para um cliente e não pode ser excluído.")
        
        c = Horario(id, None)
        Horarios.excluir(c)

  def horario_abrir_agenda(data, hora_inicio, hora_fim, intervalo):
        try:
            i = data + " " + hora_inicio
            f = data + " " + hora_fim
            di = datetime.strptime(i, "%d/%m/%Y %H:%M")
            df = datetime.strptime(f, "%d/%m/%Y %H:%M")
        except ValueError:
            raise ValueError("Data ou horário fornecidos estão em um formato inválido. Use DD/MM/AAAA HH:MM.")
    
        if di >= df:
            raise ValueError("O horário inicial deve ser anterior ao horário final.")
        
        if intervalo <= 0:
            raise ValueError("O intervalo deve ser um valor positivo.")
        if (df - di).total_seconds() < intervalo * 60:
            raise ValueError("O intervalo é maior que o período total entre os horários inicial e final.")
        
        d = timedelta(minutes=intervalo)
        x = di
        while x <= df:
            View.horario_inserir(x, False, None, None)
            x = x + ddef horario_abrir_agenda(data, hora_inicio, hora_fim, intervalo):
        try:
            i = data + " " + hora_inicio
            f = data + " " + hora_fim
            di = datetime.strptime(i, "%d/%m/%Y %H:%M")
            df = datetime.strptime(f, "%d/%m/%Y %H:%M")
        except ValueError:
            raise ValueError("Data ou horário fornecidos estão em um formato inválido. Use DD/MM/AAAA HH:MM.")
        
        if di >= df:
            raise ValueError("O horário inicial deve ser anterior ao horário final.")
        
        if intervalo <= 0:
            raise ValueError("O intervalo deve ser um valor positivo.")
        if (df - di).total_seconds() < intervalo * 60:
            raise ValueError("O intervalo é maior que o período total entre os horários inicial e final.")
        
        d = timedelta(minutes=intervalo)
        x = di
        while x <= df:
            View.horario_inserir(x, False, None, None)
            x = x + d

    def servico_inserir(descricao, valor, duracao):
        c = Servico(0, descricao, valor, duracao)
        Servicos.inserir(c)

    def servico_listar():
        return Servicos.listar()    

    def servico_listar_id(id):
        return Servicos.listar_id(id)    

    def servico_atualizar(id, descricao, valor, duracao):
        c = Servico(id, descricao, valor, duracao)
        Servicos.atualizar(c)

    def servico_excluir(id):
        if any(agenda.servico_id == id for agenda in Agenda.listar_todos()):
            raise ValueError(f"O serviço com ID {id} está vinculado a registros na agenda e não pode ser excluído.")
        c = Servico(id, "", 0, 0)
        Servicos.excluir(c)
