import pandas as pd
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

#abrindo o banco de dados
df = pd.read_csv('leads_cidadania.csv')

# --- Análise básica ---
print("Quantidade de leads captados:", df.shape)
print("\nTipos de dados:")
print(df.dtypes)

# --- Dados nulos ---
print("\n--- Dados Nulos ---")
print(df.isnull().sum())

# --- Dados duplicados ---
print("\n--- Duplicados ---")
duplicados = df.duplicated(subset=['nome', 'email']).sum()
print(f"Quantidade de nomes/emails duplicados: {duplicados}")

#remove nomes/e-mails duplicados
df = df.drop_duplicates(subset=['nome', 'email'])
print(f"Dataset após remover duplicados: {df.shape}")

#principais 'KPI's
print("\n--- KPI's ---")
total_leads = len(df)
em_negociacao = (df['em_negociacao'] == 'Sim').sum()
perdidos = df['data_perda'].notnull().sum()
convertidos = df['data_conversao'].notnull().sum()

#garante que as datas estejam no formato datetime
df['data_contato'] = pd.to_datetime(df['data_contato'])
df['data_perda'] = pd.to_datetime(df['data_perda'])
df['data_conversao'] = pd.to_datetime(df['data_conversao'])

#calcula diferença de dias
df['dias_ate_perda'] = (df['data_perda'] - df['data_contato']).dt.days
df['dias_ate_conversao'] = (df['data_conversao'] - df['data_contato']).dt.days

print("\n--- Tempo Médio ---")
#apenas para quem foi perdido
tempo_medio_perda = df.loc[df['dias_ate_perda'].notnull(), 'dias_ate_perda'].mean()
#apenas para quem foi convertido
tempo_medio_conversao = df.loc[df['dias_ate_conversao'].notnull(), 'dias_ate_conversao'].mean()

print(f"Tempo médio até perda: {tempo_medio_perda:.2f} dias")
print(f"Tempo médio até conversão: {tempo_medio_conversao:.2f} dias")

print(f"Total de leads: {total_leads}")
print(f"Em negociação: {em_negociacao} ({em_negociacao/total_leads:.2%})")
print(f"Convertidos: {convertidos} ({convertidos/total_leads:.2%})")
print(f"Perdidos: {perdidos} ({perdidos/total_leads:.2%})")

#documentos preenchidos
print("\n--- Documentos Preenchidos ---")
doc_portugues_vazios = df['documento_portugues'].isnull().sum() + (df['documento_portugues'] == '').sum()
doc_italiano_vazios = df['documento_italiano'].isnull().sum() + (df['documento_italiano'] == '').sum()

print(f"Documentos portugueses vazios: {doc_portugues_vazios} ({doc_portugues_vazios/total_leads:.2%})")
print(f"Documentos italianos vazios: {doc_italiano_vazios} ({doc_italiano_vazios/total_leads:.2%})")


