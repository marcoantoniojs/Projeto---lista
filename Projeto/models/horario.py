import json
from datetime import datetime

# Modelo
class Horario:
    def __init__(self, id, data):
        self._id = id
        self.data = data  # chama o setter para validação
        self.confirmado = False  # chama o setter
        self.id_cliente = 0  # chama o setter
        self.id_servico = 0  # chama o setter

    
    def id(self):
        return self._id

    
    def id(self, value):
        self._id = value

    
    def data(self):
        return self._data

    
    def data(self, value):
        if not isinstance(value, datetime):
            raise ValueError("O atributo 'data' deve ser do tipo datetime.")
        self._data = value

    
    def confirmado(self):
        return self._confirmado

    
    def confirmado(self, value):
        if not isinstance(value, bool):
            raise ValueError("O atributo 'confirmado' deve ser um booleano.")
        self._confirmado = value

    
    def id_cliente(self):
        return self._id_cliente

    
    def id_cliente(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("O atributo 'id_cliente' deve ser um número inteiro não negativo.")
        self._id_cliente = value

    
    def id_servico(self):
        return self._id_servico

    
    def id_servico(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("O atributo 'id_servico' deve ser um número inteiro não negativo.")
        self._id_servico = value

    def __str__(self):
        return f"{self.id} - {self.data.strftime('%d/%m/%Y %H:%M')}"

    def to_json(self):
        return {
            "id": self.id,
            "data": self.data.strftime("%d/%m/%Y %H:%M"),
            "confirmado": self.confirmado,
            "id_cliente": self.id_cliente,
            "id_servico": self.id_servico,
        }

# Persistência
class Horarios:
    objetos = []  # atributo estático

    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        m = 0
        for c in cls.objetos:
            if c.id > m:
                m = c.id
        obj.id = m + 1
        cls.objetos.append(obj)
        cls.salvar()

    @classmethod
    def listar_id(cls, id):
        cls.abrir()
        for c in cls.objetos:
            if c.id == id:
                return c
        return None

    @classmethod
    def atualizar(cls, obj):
        c = cls.listar_id(obj.id)
        if c is not None:
            c.data = obj.data
            c.confirmado = obj.confirmado
            c.id_cliente = obj.id_cliente
            c.id_servico = obj.id_servico
            cls.salvar()

    @classmethod
    def excluir(cls, obj):
        c = cls.listar_id(obj.id)
        if c is not None:
            cls.objetos.remove(c)
            cls.salvar()

    @classmethod
    def listar(cls):
        cls.abrir()
        return cls.objetos

    @classmethod
    def salvar(cls):
        with open("horarios.json", mode="w") as arquivo:  # w - write
            json.dump(cls.objetos, arquivo, default=Horario.to_json)

    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("horarios.json", mode="r") as arquivo:  # r - read
                texto = json.load(arquivo)
                for obj in texto:
                    c = Horario(obj["id"], datetime.strptime(obj["data"], "%d/%m/%Y %H:%M"))
                    c.confirmado = obj["confirmado"]
                    c.id_cliente = obj["id_cliente"]
                    c.id_servico = obj["id_servico"]
                    cls.objetos.append(c)
        except FileNotFoundError:
            pass
