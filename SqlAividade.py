import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

db_config = {
'host': 'localhost', # Geralmente 'localhost' se o banco está na sua máquina
'user': 'root', # Seu usuário do MySQL (padrão é 'root')
'password': 'senaisp', # A senha que você definiu para o usuário 'root'
'database': 'plataforma_cursos_db' # O nome do banco que criamos no Passo 1
}
query="""
SELECT
    a.nome_aluno,
    a.estado_aluno,
    m.categoria_curso,
    m.nome_curso,
    m.valor_pago,
    m.status_progresso,
    m.data_matricula,
    m.id_aluno
FROM
    alunos a
INNER JOIN
    matriculas m ON a.id_aluno = m.id_aluno
ORDER BY
m.categoria_curso;
"""

try:
# 4.1. Conectar ao banco
# 'mysql.connector.connect()' cria o objeto de conexão.
# O '**db_config' é um atalho do Python para "descompactar"
# nosso dicionário de config, o que é o mesmo que escrever:
# host=db_config['host'], user=db_config['user'], etc.
    conexao = mysql.connector.connect(**db_config)
    print("Conexão bem-sucedida!")
# 4.2. Executar a query e carregar no Pandas
# 'pd.read_sql_query()' é a função do Pandas que faz tudo:
# 1. Envia a 'query' (nossa consulta SQL com JOIN)
# 2. Através da 'conexao' que abrimos
# 3. Pega o resultado
# 4. E o carrega DIRETAMENTE em um DataFrame do Pandas.
# A variável 'df' agora contém nossos dados prontos para análise.
    df = pd.read_sql_query(query, conexao)
    print(f"Passo 2: Dados extraídos com sucesso. {len(df)} linhas recebidas.")
finally:
# 4.3. Fechar a conexão
# Verificamos se a variável 'conexao' existe E se ela está conectada
    if 'conexao' in locals() and conexao.is_connected():
# .close() encerra a conexão com o MySQL.
# É MUITO importante fechar conexões para liberar recursos do servidor.
        conexao.close()
print("Conexão com o MySQL foi fechada.")

#Analise de Receita (Group By + sum)
receita_total = df.groupby('valor_pago')['categoria_curso'].sum()
print(receita_total)

media_curso = df.groupby('nome_curso')['valor_pago'].mean()
print("Media do curso é: ")
print(media_curso)

#2 ANALISE DE ALUNOS (JOIN + GROUP BY)
estados_alunos = df.groupby('valor_pago')['estado_aluno'].sum()
print(estados_alunos)

alunos_sp = df['estado_aluno'] == 'SP' 
em_andamento = df['status_progresso'] =='Em Andamento'

condicao_e = df[em_andamento & alunos_sp]
print(condicao_e)

#Analise de Tempo(datetime)
print("\n")
qtd_matricula = df['data_matricula'] = pd.to_datetime(df['data_matricula'])
print("Quanidade de meses: ")
print(qtd_matricula)

print("\n")
print("Quantidade Mes: ")
qtd_mes =df['data_matricula'] = df['data_matricula'].dt.month
print(qtd_mes)

#Dia de vendas

valor_venda = df.groupby('data_matricula')['valor_pago'].sum()
melhor_dia_valor = valor_venda.max()
melhor_dia_data = valor_venda.idxmax()

print("Melhor valor de venda: ")
print(melhor_dia_data)

#4  ANALISE DE PROGRESSO
print("Analise de progresso")
concluido = df['status_progresso'] =='Concluído'
curso_python = df['nome_curso'] == 'Python para Iniciantes'

qtd_concluido = df[concluido & curso_python ]['id_aluno'].count()
print("Quantidade de aluno com ")
print(qtd_concluido)

#Taxa evasão
iniciantes = df['status_progresso'] =='Iniciante'
qtd_iniciante = df[iniciantes]['id_aluno'].count()
print("Iniciane")
print(qtd_iniciante)