from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List, Optional
import os
import sys


class Historico:
    def __init__(self):
        self.transacoes = []
    
    def adicionar_transacao(self, transacao):
        """Add a transaction to the history"""
        self.transacoes.append(transacao)


class Transacao(ABC):
    """Abstract base class for transactions"""
    
    @abstractmethod
    def registrar(self, conta):
        """Register the transaction in an account"""
        pass


class Deposito(Transacao):
    def __init__(self, valor: float):
        self.valor = valor
        self.data = datetime.now()
    
    def registrar(self, conta):
        """Register a deposit in the account"""
        return conta.depositar(self.valor)
    
    def __str__(self):
        return f"Depósito: R$ {self.valor:.2f} - {self.data.strftime('%d/%m/%Y %H:%M:%S')}"


class Saque(Transacao):
    def __init__(self, valor: float):
        self.valor = valor
        self.data = datetime.now()
    
    def registrar(self, conta):
        """Register a withdrawal from the account"""
        return conta.sacar(self.valor)
    
    def __str__(self):
        return f"Saque: R$ {self.valor:.2f} - {self.data.strftime('%d/%m/%Y %H:%M:%S')}"


class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        """Perform a transaction in the given account"""
        return transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        """Add an account to the client"""
        self.contas.append(conta)


class PessoaFisica(Cliente):
    contador = 0
    
    def __init__(self, endereco: str, cpf: str, nome: str, data_nascimento: date):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        PessoaFisica.contador += 1

    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf})"


class Conta:
    contador = 0
    
    def __init__(self, cliente: Cliente, agencia: str = "0001"):
        Conta.contador += 1
        self._saldo = 0.0
        self.numero = Conta.contador
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()
        
        # Add this account to the client's accounts
        cliente.adicionar_conta(self)
    
    @property
    def saldo(self) -> float:
        """Return the current balance"""
        return self._saldo
    
    @classmethod
    def nova_conta(cls, cliente: Cliente) -> 'Conta':
        """Factory method to create a new account"""
        return cls(cliente)
    
    def sacar(self, valor: float) -> bool:
        """Withdraw money from the account"""
        if valor > 0 and self._saldo >= valor:
            self._saldo -= valor
            self.historico.adicionar_transacao(Saque(valor))
            return True
        return False
    
    def depositar(self, valor: float) -> bool:
        """Deposit money into the account"""
        if valor > 0:
            self._saldo += valor
            self.historico.adicionar_transacao(Deposito(valor))
            return True
        return False
    
    def __str__(self):
        return f"Agência: {self.agencia} | Conta: {self.numero} | Titular: {self.cliente}"


class ContaCorrente(Conta):
    def __init__(self, cliente: Cliente, limite: float = 500.0, limite_saques: int = 3, agencia: str = "0001"):
        super().__init__(cliente, agencia)
        self.limite = limite
        self.limite_saques = limite_saques
        self._saques_realizados = 0
    
    def sacar(self, valor: float) -> bool:
        """Withdraw money from checking account with special limit"""
        if self._saques_realizados >= self.limite_saques:
            print("Limite de saques excedido!")
            return False
            
        # Can withdraw up to balance + overdraft limit
        if valor > 0 and self._saldo + self.limite >= valor:
            self._saldo -= valor
            self.historico.adicionar_transacao(Saque(valor))
            self._saques_realizados += 1
            return True
        return False
    
    def __str__(self):
        return f"{super().__str__()} | Limite: R$ {self.limite:.2f}"


# Sistema Bancário
class SistemaBancario:
    def __init__(self):
        self.clientes = []
        self.contas = []
    
    def buscar_cliente(self, cpf: str) -> Optional[PessoaFisica]:
        """Search for a client by CPF"""
        for cliente in self.clientes:
            if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
                return cliente
        return None
    
    def buscar_conta(self, numero: int) -> Optional[Conta]:
        """Search for an account by number"""
        for conta in self.contas:
            if conta.numero == numero:
                return conta
        return None

    def registrar_cliente(self, cliente: Cliente):
        """Register a client in the system"""
        self.clientes.append(cliente)
    
    def registrar_conta(self, conta: Conta):
        """Register an account in the system"""
        self.contas.append(conta)

    def listar_clientes(self):
        """List all registered clients"""
        for i, cliente in enumerate(self.clientes, 1):
            print(f"{i}. {cliente}")
    
    def listar_contas(self):
        """List all registered accounts"""
        for i, conta in enumerate(self.contas, 1):
            print(f"{i}. {conta} | Saldo: R$ {conta.saldo:.2f}")


# Menu Interface
def menu():
    sistema = SistemaBancario()
    
    while True:
        limpar_tela()
        print("=" * 30)
        print("===== SISTEMA BANCÁRIO =====")
        print("=" * 30)
        print("1 - Criar Cliente")
        print("2 - Criar Conta")
        print("3 - Listar Clientes")
        print("4 - Listar Contas")
        print("5 - Realizar Depósito")
        print("6 - Realizar Saque")
        print("7 - Exibir Extrato")
        print("0 - Sair")
        print("=" * 30)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            criar_cliente(sistema)
        elif opcao == "2":
            criar_conta(sistema)
        elif opcao == "3":
            listar_clientes(sistema)
        elif opcao == "4":
            listar_contas(sistema)
        elif opcao == "5":
            realizar_deposito(sistema)
        elif opcao == "6":
            realizar_saque(sistema)
        elif opcao == "7":
            exibir_extrato(sistema)
        elif opcao == "0":
            print("Obrigado por utilizar nosso sistema!")
            break
        else:
            print("Opção inválida, tente novamente.")
            input("Pressione Enter para continuar...")


def limpar_tela():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def criar_cliente(sistema):
    """Function to register a new client"""
    limpar_tela()
    print("===== CADASTRO DE CLIENTE =====")
    
    nome = input("Nome: ")
    cpf = input("CPF: ")
    
    # Validate if CPF already exists
    if sistema.buscar_cliente(cpf):
        print(f"Cliente com CPF {cpf} já está cadastrado.")
        input("Pressione Enter para continuar...")
        return
    
    endereco = input("Endereço: ")
    
    try:
        data_input = input("Data de Nascimento (DD/MM/AAAA): ")
        dia, mes, ano = map(int, data_input.split('/'))
        data_nascimento = date(ano, mes, dia)
    except ValueError:
        print("Formato de data inválido. Use DD/MM/AAAA.")
        input("Pressione Enter para continuar...")
        return
    
    cliente = PessoaFisica(endereco, cpf, nome, data_nascimento)
    sistema.registrar_cliente(cliente)
    
    print(f"\nCliente {nome} cadastrado com sucesso!")
    input("Pressione Enter para continuar...")


def criar_conta(sistema):
    """Function to create a new account"""
    limpar_tela()
    print("===== ABERTURA DE CONTA =====")
    
    if not sistema.clientes:
        print("Não há clientes cadastrados. Cadastre um cliente primeiro.")
        input("Pressione Enter para continuar...")
        return
    
    print("Selecione o cliente:")
    sistema.listar_clientes()
    
    try:
        idx = int(input("\nNúmero do cliente: ")) - 1
        if idx < 0 or idx >= len(sistema.clientes):
            print("Cliente inválido!")
            input("Pressione Enter para continuar...")
            return
        
        cliente = sistema.clientes[idx]
        
        print("\nTipo de conta:")
        print("1 - Conta Comum")
        print("2 - Conta Corrente")
        tipo = input("Escolha o tipo de conta: ")
        
        if tipo == "1":
            conta = Conta.nova_conta(cliente)
            print(f"\nConta comum criada com sucesso! Número da conta: {conta.numero}")
        elif tipo == "2":
            limite = float(input("Limite de crédito: R$ "))
            limite_saques = int(input("Limite de saques por dia: "))
            conta = ContaCorrente(cliente, limite, limite_saques)
            print(f"\nConta corrente criada com sucesso! Número da conta: {conta.numero}")
        else:
            print("Opção inválida!")
            input("Pressione Enter para continuar...")
            return
        
        sistema.registrar_conta(conta)
        input("Pressione Enter para continuar...")
        
    except ValueError:
        print("Entrada inválida. Digite um número.")
        input("Pressione Enter para continuar...")


def listar_clientes(sistema):
    """List all registered clients"""
    limpar_tela()
    print("===== LISTA DE CLIENTES =====")
    
    if not sistema.clientes:
        print("Não há clientes cadastrados.")
    else:
        sistema.listar_clientes()
    
    input("\nPressione Enter para continuar...")


def listar_contas(sistema):
    """List all registered accounts"""
    limpar_tela()
    print("===== LISTA DE CONTAS =====")
    
    if not sistema.contas:
        print("Não há contas cadastradas.")
    else:
        sistema.listar_contas()
    
    input("\nPressione Enter para continuar...")


def realizar_deposito(sistema):
    """Function to make a deposit"""
    limpar_tela()
    print("===== DEPÓSITO =====")
    
    if not sistema.contas:
        print("Não há contas cadastradas.")
        input("Pressione Enter para continuar...")
        return
    
    try:
        numero_conta = int(input("Número da conta: "))
        conta = sistema.buscar_conta(numero_conta)
        
        if not conta:
            print(f"Conta {numero_conta} não encontrada!")
            input("Pressione Enter para continuar...")
            return
        
        valor = float(input("Valor do depósito: R$ "))
        
        if valor <= 0:
            print("Valor de depósito inválido!")
            input("Pressione Enter para continuar...")
            return
        
        transacao = Deposito(valor)
        cliente = conta.cliente
        sucesso = cliente.realizar_transacao(conta, transacao)
        
        if sucesso:
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("Erro ao realizar depósito!")
        
        input("Pressione Enter para continuar...")
        
    except ValueError:
        print("Entrada inválida. Digite um número.")
        input("Pressione Enter para continuar...")


def realizar_saque(sistema):
    """Function to make a withdrawal"""
    limpar_tela()
    print("===== SAQUE =====")
    
    if not sistema.contas:
        print("Não há contas cadastradas.")
        input("Pressione Enter para continuar...")
        return
    
    try:
        numero_conta = int(input("Número da conta: "))
        conta = sistema.buscar_conta(numero_conta)
        
        if not conta:
            print(f"Conta {numero_conta} não encontrada!")
            input("Pressione Enter para continuar...")
            return
        
        valor = float(input("Valor do saque: R$ "))
        
        if valor <= 0:
            print("Valor de saque inválido!")
            input("Pressione Enter para continuar...")
            return
        
        transacao = Saque(valor)
        cliente = conta.cliente
        sucesso = cliente.realizar_transacao(conta, transacao)
        
        if sucesso:
            print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
        else:
            if isinstance(conta, ContaCorrente) and conta._saques_realizados >= conta.limite_saques:
                print("Limite de saques excedido!")
            else:
                print("Saldo insuficiente!")
        
        input("Pressione Enter para continuar...")
        
    except ValueError:
        print("Entrada inválida. Digite um número.")
        input("Pressione Enter para continuar...")


def exibir_extrato(sistema):
    """Function to display account statement"""
    limpar_tela()
    print("===== EXTRATO =====")
    
    if not sistema.contas:
        print("Não há contas cadastradas.")
        input("Pressione Enter para continuar...")
        return
    
    try:
        numero_conta = int(input("Número da conta: "))
        conta = sistema.buscar_conta(numero_conta)
        
        if not conta:
            print(f"Conta {numero_conta} não encontrada!")
            input("Pressione Enter para continuar...")
            return
        
        print(f"\nExtrato da Conta {conta.numero}")
        print(f"Cliente: {conta.cliente}")
        print(f"Saldo atual: R$ {conta.saldo:.2f}")
        print("\nHistórico de transações:")
        
        if not conta.historico.transacoes:
            print("Não há transações registradas.")
        else:
            for transacao in conta.historico.transacoes:
                print(f"- {transacao}")
        
        input("\nPressione Enter para continuar...")
        
    except ValueError:
        print("Entrada inválida. Digite um número.")
        input("Pressione Enter para continuar...")


if __name__ == "__main__":
    menu()