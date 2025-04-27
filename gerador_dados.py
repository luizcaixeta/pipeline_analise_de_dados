import random 
import pandas as pd 
from faker import Faker
from datetime import timedelta

fake = Faker('pt_BR')

n = 1000000

#possíveis documentos do processo português
documentos_portugueses = [
    "Certidão de nascimento de avô português",
    "Certidão de casamento",
    "Documento de identidade",
    "Comprovante de residência",
    ""
]

#possíveis documentos do processo italiano
documentos_italianos = [
    "Certidão de nascimento de antepassado italiano",
    "Certidão de batismo",
    "Registro de imigração",
    "Árvore genealógica",
    ""
]

def gerar_documentos(documentos_possiveis):
    qtd = random.randint(1, len(documentos_possiveis))
    return ", ".join(random.sample(documentos_possiveis, qtd))

def gerar_datas():
    data_contato = fake.date_between(start_date = '-1y', end_date = 'today')
    em_negociacao = random.choice(['Sim', 'Não'])
    data_perda = None
    data_conversao = None

    if em_negociacao == 'Não':
        if random.random() < 0.5:
            data_perda = data_contato + timedelta(days = random.randint(5, 60))
        else:
            data_conversao = data_contato + timedelta(days = random.randint(5, 60))
    
    return data_contato, em_negociacao, data_perda, data_conversao

dados = []

for _ in range(n):
    nome = fake.name()
    email = fake.email()
    processo = random.choice(['Cidadania italiana', 'Cidadania portuguesa'])
    data_contato, em_negociacao, data_perda, data_conversao = gerar_datas()
    
    documento_portugues = gerar_documentos(documentos_portugueses) if processo == 'Cidadania portuguesa' else ''
    documento_italiano = gerar_documentos(documentos_italianos) if processo == 'Cidadania italiana' else ''
    
    dados.append({
        'nome': nome,
        'email': email,
        'processo': processo,
        'data_contato': data_contato,
        'em_negociacao': em_negociacao,
        'data_perda': data_perda,
        'data_conversao': data_conversao,
        'documento_portugues': documento_portugues,
        'documento_italiano': documento_italiano
    })

# Cria o DataFrame
df = pd.DataFrame(dados)

df.to_csv('leads_cidadania.csv', index=False)