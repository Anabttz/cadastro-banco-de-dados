
import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database=''
)

cursor= conexao.cursor()

def cadastrar():
    Nome= input('Nome: ').strip()
    if not Nome:
        print('Nome é obrigatório.')
        return

    try:
        Idade= int(input('Idade: '))
    except ValueError:
        print('A idade deve ser um número')
        return
    
    if Idade <= 0:
           print('A idade deve ser maior que 0.')
           return

    Cpf= input('CPF: ').strip()
    if not Cpf:
        print('CPF é obrigatório.')
        return

    Email= input('E-mail: ').strip()
    if not Email:
        print('E-mail é obrigatório. ')
        return

    cursor.execute('INSERT INTO cadastro (Nome, Idade, Cpf, Email) VALUES(%s, %s, %s, %s)',(Nome, Idade, Cpf, Email))
    conexao.commit()
    print('Cadastro realizado com sucesso!')


def listar():
    cursor.execute('SELECT * FROM cadastro')
    cadastro= cursor.fetchall()


    if not cadastro:
        print('Nenhum cadastro encontrado.')

    else:
        print('\\------ CADASTROS ------')

        for linha in cadastro:
            print(f'ID: {linha[0]} Nome: {linha[1]} Idade:{linha[2]} Cpf: {linha[3]} E-mail: {linha[4]}')

        print('--------------------------------')


def atualizar():
    listar()
    try:
        Cpf= int(input('Digite o CPF do usuário que deseja atualizar: '))
    except ValueError:
        print('CPF inválido')
        return
    
    novo_nome= input('Nome atualizado: (Deixe vazio para não alterar.)').strip()
    nova_idade= input('Idade: Deixe vazio para não alterar').strip()
    novo_email= input('E-mail: (Deixe vazio para não alterar)').strip()

    if nova_idade:
        try:
            nova_idade= int(nova_idade)
        except ValueError:
            print('Idade inválida!')
            return

    cursor.execute('SELECT Nome, Idade, Email FROM cadastro WHERE CPF = %s', (Cpf,))
    usuario= cursor.fetchone()


    if not usuario:
        print('Usuário não encontrado!')
        return

    nome_final = novo_nome if novo_nome else usuario [0]
    idade_final = nova_idade if nova_idade else usuario[1]
    email_final = novo_email if novo_email else usuario[2]

    cursor.execute('UPDATE cadastro SET Nome=%s, Idade=%s, Email=%s WHERE CPF=%s',(nome_final, idade_final, email_final, Cpf))

    conexao.commit()
    print('Cadastro atualizado com sucesso')

def deletar():
    listar()
    try:
        id_cadastro= input('Digite o ID do cadastro que deseja excluir')
    except ValueError:
        print('ID inválido!')
        return
    
    cursor.execute('DELETE FROM cadastro WHERE ID= %s', (id_cadastro,))

    conexao.commit()
    print('Cadastro deletado com sucesso!')

while True:
    print('\n=== MENU PRINCIPAL ===')
    print('1 - Cadastrar usuário')
    print('2 - Listar cadastros')
    print('3 - Atualizar cadastro')
    print('4 - Deletar usuário')
    print('5 - Sair')

    opcao= input('Escolha uma opção: ')

    if opcao == '1':
        cadastrar()
    elif opcao == '2':
        listar()
    elif opcao == '3':
        atualizar()
    elif opcao == '4':
        deletar()
    elif opcao == '5':
        print('Encerrando o sistema...')
        break

cursor.close()
conexao.close()
















