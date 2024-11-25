import json

# Modelo
class Servico:
    def __init__(self, id, descricao, valor, duracao):
        self._id = id
        self.descricao = descricao  # chama o setter para validação
        self.valor = valor  # chama o setter para validação
        self.duracao = duracao  # chama o setter para validação

    
    def id(self):
        return self._id

    
    def id(self, value):
        self._id = value

    
    def descricao(self):
        return self._descricao

    
    def descricao(self, value):
        if not value.strip():
            raise ValueError("A descrição do serviço não pode estar vazia.")
        self._descricao = value

    
    def valor(self):
        return self._valor

    
    def valor(self, value):
        if value < 0:
            raise ValueError("O valor do serviço não pode ser negativo.")
        self._valor = value

    
    def duracao(self):
        return self._duracao

    
    def duracao(self, value):
        if value <= 0:
            raise ValueError("A duração do serviço deve ser positiva.")
        self._duracao = value

    def __str__(self):
        return f"{self.id} - {self.descricao} - R$ {self.valor:.2f} - {self.duracao} min"

# Persistência
class Servicos:
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
            c.descricao = obj.descricao
            c.valor = obj.valor
            c.duracao = obj.duracao
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
        with open("servicos.json", mode="w") as arquivo:  # w - write
            json.dump(cls.objetos, arquivo, default=lambda o: vars(o))

    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("servicos.json", mode="r") as arquivo:  # r - read
                texto = json.load(arquivo)
                for obj in texto:
                    c = Servico(obj["_id"], obj["_descricao"], obj["_valor"], obj["_duracao"])
                    cls.objetos.append(c)
        except FileNotFoundError:
            pass
