# Lista de Clientes
# C - Create - Insere um objeto na lista
# R - Read   - Listar os objetos da lista
# U - Update - Atualizar um objeto na lista
# D - Delete - Exclui um objeto da lista

import json

# Modelo
class Cliente:
    def __init__(self, id, nome, email, fone, senha):
        self._id = id
        self.nome = nome  # chama o setter para validação
        self.email = email  # chama o setter para validação
        self.fone = fone  # chama o setter para validação
        self.senha = senha  # chama o setter para validação

    
    def id(self):
        return self._id

    
    def id(self, value):
        self._id = value

    
    def nome(self):
        return self._nome

    
    def nome(self, value):
        if not value.strip():
            raise ValueError("O nome não pode estar vazio.")
        self._nome = value

    
    def email(self):
        return self._email

    
    def email(self, value):
        if not value.strip():
            raise ValueError("O e-mail não pode estar vazio.")
        self._email = value

    
    def fone(self):
        return self._fone

    
    def fone(self, value):
        if not value.strip():
            raise ValueError("O telefone não pode estar vazio.")
        self._fone = value

   
    def senha(self):
        return self._senha

    
    def senha(self, value):
        if not value.strip():
            raise ValueError("A senha não pode estar vazia.")
        self._senha = value

    def __str__(self):
        return f"{self.nome} - {self.email} - {self.fone}"

# Persistência
class Clientes:
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
            c.nome = obj.nome
            c.email = obj.email
            c.fone = obj.fone
            c.senha = obj.senha
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
        cls.objetos.sort(key=lambda cliente: cliente.nome)
        return cls.objetos

    @classmethod
    def salvar(cls):
        with open("clientes.json", mode="w") as arquivo:  # w - write
            json.dump(cls.objetos, arquivo, default=vars)

    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("clientes.json", mode="r") as arquivo:  # r - read
                texto = json.load(arquivo)
                for obj in texto:
                    c = Cliente(obj["id"], obj["nome"], obj["email"], obj["fone"], obj["senha"])
                    cls.objetos.append(c)
        except FileNotFoundError:
            pass

