from abc import ABC, abstractmethod
from datetime import datetime


class Conta():
    def __init__(self,saldo,numero,agencia,cliente):
        
        self._saldo = 0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()
    
    def saldo(self):
        return self._saldo
    
    @classmethod
    def nova_conta(cls, cliente, numero):
     return cls(
        saldo=0.0,
        numero=numero,
        agencia="0001",
        cliente=cliente
    )
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico    
    
    def sacar(self,valor):
        if valor <= self._saldo:
            self._saldo -= valor
            return True
        else:
            print("Saldo insuficiente!")
            return False
        
    def depositar(self,valor):
        self._saldo += valor
        print("Depósito realizado com sucesso!")
    
    def executar_transacao(self, transacao):
        transacao.registrar_transacao(self)
        self._historico.adicionar_transacao(transacao)

class ContaCorrente(Conta):
    def __init__(self, saldo, numero, agencia, cliente, historico,limite,limite_saques):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques


class Transacao(ABC):

    @abstractmethod
    def registrar_transacao(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self,valor):
        self._valor = valor
        
    def registrar_transacao(self,conta):
        conta.depositar(self._valor)
        
class Saque(Transacao):
    def __init__(self,valor):
        self._valor = valor
        
    def registrar_transacao(self,conta):
        conta.sacar(self._valor)
        
class Historico:
    def __init__(self):
        self._transacoes = []
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": getattr(transacao, "_valor", None),
            "data": datetime.now()
        })
    
    def listar(self):
        return self._transacoes

class PessoaFisica:
    def __init__(self,nome,cpf,data_nascimento):
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento        
        
class Cliente(PessoaFisica):
    
    def __init__(self,nome,cpf,data_nascimento,endereco):
        super().__init__(nome,cpf,data_nascimento)
        
        self._endereco = endereco
        self._contas = []
        
    def adicionar_conta(self,conta):
        self._contas.append(conta)
    
    def realizar_transacao(self,conta,transacao):
        conta.executar_transacao(transacao) 
        

def menu():
    cliente = None
    conta = None

    while True:
        print("\n===== SISTEMA BANCÁRIO =====")
        print("1 - Criar cliente")
        print("2 - Criar conta")
        print("3 - Depositar")
        print("4 - Sacar")
        print("5 - Ver saldo")
        print("6 - Ver histórico")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        # 🔹 Criar cliente
        if opcao == "1":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            nascimento = input("Data de nascimento: ")
            endereco = input("Endereço: ")

            cliente = Cliente(nome, cpf, nascimento, endereco)
            print("Cliente criado com sucesso!")

        # 🔹 Criar conta
        elif opcao == "2":
            if cliente is None:
                print("Crie um cliente primeiro!")
                continue

            numero = input("Número da conta: ")
            conta = Conta.nova_conta(cliente, numero)
            cliente.adicionar_conta(conta)

            print("Conta criada com sucesso!")

        # 🔹 Depositar
        elif opcao == "3":
            if conta is None:
                print("Crie uma conta primeiro!")
                continue

            valor = float(input("Valor do depósito: "))
            conta.executar_transacao(Deposito(valor))

        # 🔹 Sacar
        elif opcao == "4":
            if conta is None:
                print("Crie uma conta primeiro!")
                continue

            valor = float(input("Valor do saque: "))
            conta.executar_transacao(Saque(valor))

        # 🔹 Ver saldo
        elif opcao == "5":
            if conta is None:
                print("Crie uma conta primeiro!")
                continue

            print(f"Saldo atual: {conta.saldo}")

        # 🔹 Histórico
        elif opcao == "6":
            if conta is None:
                print("Crie uma conta primeiro!")
                continue

            historico = conta.historico.listar()

            print("\n--- HISTÓRICO ---")
            for t in historico:
                print(t)

        # 🔹 Sair
        elif opcao == "0":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida!")

# 🔥 roda o menu
menu()