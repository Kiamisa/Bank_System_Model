```markdown
# Sistema Bancário - Gerenciamento de Contas e Transações

Este é um sistema bancário simples que permite o cadastro de clientes, criação de contas, realização de depósitos, saques, e consulta de extratos.

## Funcionalidades

- **Cadastro de Clientes:** Permite o cadastro de clientes (pessoas físicas) com nome, CPF, endereço e data de nascimento.
- **Criação de Contas:** Permite a criação de contas bancárias para os clientes, tanto contas comuns quanto contas correntes com limite de crédito e limite de saques.
- **Transações:** Permite realizar depósitos e saques nas contas bancárias.
- **Histórico de Transações:** Registra o histórico de todas as transações realizadas em uma conta.
- **Extrato de Conta:** Exibe o saldo e o histórico de transações de uma conta bancária.

## Estrutura do Sistema

O sistema é composto pelas seguintes classes:

### 1. **Historico**
Responsável por armazenar as transações realizadas nas contas.

### 2. **Transacao (classe abstrata)**
Base para as transações, com um método abstrato `registrar` que é implementado nas classes `Deposito` e `Saque`.

### 3. **Deposito**
Representa uma transação de depósito em uma conta. Possui um valor e a data em que foi realizado o depósito.

### 4. **Saque**
Representa uma transação de saque em uma conta. Possui um valor e a data em que foi realizado o saque.

### 5. **Cliente**
Classe base para clientes, que mantém o endereço e as contas associadas ao cliente.

### 6. **PessoaFisica (herda Cliente)**
Representa um cliente do tipo pessoa física, com CPF, nome e data de nascimento.

### 7. **Conta**
Representa uma conta bancária de um cliente. Gerencia o saldo, as transações realizadas e possui um número de conta único.

### 8. **ContaCorrente (herda Conta)**
Representa uma conta corrente, que possui limite de crédito e limite de saques diários.

### 9. **SistemaBancario**
Classe principal do sistema, que gerencia os clientes e contas bancárias. Permite a criação de clientes, contas, e a realização de transações.

### 10. **Menu**
Uma interface de menu no terminal, que permite ao usuário interagir com o sistema bancário.

## Como Executar

### Pré-requisitos
Certifique-se de ter o Python 3.x instalado em sua máquina.

### Passos

1. Clone este repositório ou copie o código fonte para sua máquina.
2. Abra o terminal e navegue até o diretório onde o código está salvo.
3. Execute o código com o seguinte comando:
   ```bash
   python sistema_bancario.py
  
4. O menu será exibido e você poderá interagir com o sistema bancário.

## Funções do Menu

1. **Criar Cliente:** Permite cadastrar um novo cliente no sistema.
2. **Criar Conta:** Permite criar uma nova conta bancária para um cliente.
3. **Listar Clientes:** Exibe uma lista de todos os clientes cadastrados.
4. **Listar Contas:** Exibe uma lista de todas as contas bancárias cadastradas.
5. **Realizar Depósito:** Permite realizar um depósito em uma conta bancária.
6. **Realizar Saque:** Permite realizar um saque em uma conta bancária.
7. **Exibir Extrato:** Exibe o extrato da conta, mostrando o saldo e o histórico de transações realizadas.

## Exemplo de Uso

1. **Cadastrar um Cliente:**
   - Nome: João Silva
   - CPF: 123.456.789-00
   - Endereço: Rua das Flores, 123
   - Data de Nascimento: 01/01/1990

2. **Criar uma Conta para o Cliente:**
   - Tipo de Conta: Conta Comum

3. **Realizar um Depósito de R$ 100,00 na Conta:**
   - Conta: [Número da Conta]
   - Valor: R$ 100,00

4. **Realizar um Saque de R$ 50,00 da Conta:**
   - Conta: [Número da Conta]
   - Valor: R$ 50,00

5. **Exibir Extrato da Conta:**
   - Saldo Atual: R$ 50,00
   - Histórico de Transações:
     - Depósito: R$ 100,00
     - Saque: R$ 50,00

## Contribuindo

Se você deseja contribuir para este projeto, fique à vontade para abrir uma *issue* ou enviar um *pull request*. Agradecemos qualquer contribuição!
```
