
import mysql.connector

class Database:
    def __init__(self, host='localhost', user='root', password='SENHA_AQUI', database='dados'):
        try:
            self.conexao = mysql.connector.connect(
                host='127.0.0.1',
                user= 'root',
                password= '789821'
            )
            self.cursor = self.conexao.cursor()

            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            self.conexao.database = database

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS cadastro (
                    ID INT AUTO_INCREMENT PRIMARY KEY,
                    Nome VARCHAR(100) NOT NULL,
                    Idade INT NOT NULL,
                    Cpf VARCHAR(14) NOT NULL UNIQUE,
                    Email VARCHAR(100) NOT NULL
                )
            """)
            self.conexao.commit()

        except mysql.connector.Error as erro:
            print(f"Erro ao conectar ao banco: {erro}")

    def executar(self, comando, valores=None):
        try:
            self.cursor.execute(comando, valores or ())
            self.conexao.commit()
        except mysql.connector.Error as erro:
            print(f"Erro ao executar comando: {erro}")

    def buscar(self, comando, valores=None):
        self.cursor.execute(comando, valores or ())
        return self.cursor.fetchall()

    def fechar(self):
        self.cursor.close()
        self.conexao.close()


class Cadastro:
    def __init__(self, db: Database):
        self.db = db

    def cadastrar(self):
        nome = input('Nome: ').strip()
        if not nome:
            print('Nome é obrigatório.')
            return

        try:
            idade = int(input('Idade: '))
        except ValueError:
            print('A idade deve ser um número.')
            return

        if idade <= 0:
            print('A idade deve ser maior que 0.')
            return

        cpf = input('CPF: ').strip()
        if not cpf:
            print('CPF é obrigatório.')
            return

        email = input('E-mail: ').strip()
        if not email:
            print('E-mail é obrigatório.')
            return

        self.db.executar(
            'INSERT INTO cadastro (Nome, Idade, Cpf, Email) VALUES (%s, %s, %s, %s)',
            (nome, idade, cpf, email)
        )
        print('Cadastro realizado com sucesso!')

    def listar(self):
        cadastros = self.db.buscar('SELECT * FROM cadastro')

        if not cadastros:
            print('Nenhum cadastro encontrado.')
        else:
            print('\n------ CADASTROS ------')
            for linha in cadastros:
                print(f'ID: {linha[0]} | Nome: {linha[1]} | Idade: {linha[2]} | CPF: {linha[3]} | E-mail: {linha[4]}')
            print('-----------------------')

    def atualizar(self):
        self.listar()
        cpf = input('Digite o CPF do usuário que deseja atualizar: ').strip()

        if not cpf:
            print('CPF inválido!')
            return

        novo_nome = input('Nome a atualizar (deixe vazio para não alterar): ').strip()
        nova_idade = input('Idade a atualizar (deixe vazio para não alterar): ').strip()
        novo_email = input('E-mail a atualizar (deixe vazio para não alterar): ').strip()

        if nova_idade:
            try:
                nova_idade = int(nova_idade)
            except ValueError:
                print('Idade inválida!')
                return

        usuario = self.db.buscar('SELECT Nome, Idade, Email FROM cadastro WHERE CPF = %s', (cpf,))
        if not usuario:
            print('Usuário não encontrado!')
            return

        usuario = usuario[0]
        nome_final = novo_nome or usuario[0]
        idade_final = nova_idade or usuario[1]
        email_final = novo_email or usuario[2]

        self.db.executar(
            'UPDATE cadastro SET Nome=%s, Idade=%s, Email=%s WHERE CPF=%s',
            (nome_final, idade_final, email_final, cpf)
        )
        print('Cadastro atualizado com sucesso!')

    def deletar(self):
        self.listar()
        cpf_cadastro = input('Digite o CPF do usuário que deseja excluir: ').strip()

        if not cpf_cadastro:
            print('CPF inválido!')
            return

        self.db.executar('DELETE FROM cadastro WHERE ID = %s', (cpf_cadastro,))
        print('Cadastro deletado com sucesso!')


class Sistema:
    def __init__(self):
        self.db = Database(database='dados')
        self.cadastro = Cadastro(self.db)

    def menu(self):
        while True:
            print('\n=== MENU PRINCIPAL ===')
            print('1 - Cadastrar usuário')
            print('2 - Listar cadastros')
            print('3 - Atualizar cadastro')
            print('4 - Deletar usuário')
            print('5 - Sair')

            opcao = input('Escolha uma opção: ')

            if opcao == '1':
                self.cadastro.cadastrar()
            elif opcao == '2':
                self.cadastro.listar()
            elif opcao == '3':
                self.cadastro.atualizar()
            elif opcao == '4':
                self.cadastro.deletar()
            elif opcao == '5':
                print('Encerrando o sistema...')
                self.db.fechar()
                break
            else:
                print('Opção inválida!')


# ===============================
# Execução principal
# ===============================
if __name__ == '__main__':
    sistema = Sistema()
    sistema.menu()





