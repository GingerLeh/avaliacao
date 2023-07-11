import pandas as pd


def calculate_percentage_above_age(data, age):
    total_count = len(data)
    above_age_count = sum(data['age'] > age)
    percentage = (above_age_count / total_count) * 100
    return percentage


def calculate_percentage_above_age_with_high_cholesterol(data, age):
    total_count = len(data)
    above_age_count = sum(data['age'] > age)
    high_cholesterol_count = sum(data['chol'] > 200)  # Definindo um limite arbitrário para colesterol alto
    percentage = (high_cholesterol_count / above_age_count) * 100
    return percentage


def calculate_percentage_above_age_with_high_cholesterol_and_high_sugar(data, age):
    total_count = len(data)
    above_age_count = sum(data['age'] > age)
    high_cholesterol_and_sugar_count = sum((data['age'] > age) & (data['chol'] > 200) & (data['fbs'] == 1))
    percentage = (high_cholesterol_and_sugar_count / above_age_count) * 100
    return percentage

def calculate_relation_hypertrofy(data):
    df_final = data[['fbs','chol','restecg']]
    print (df_final.corr())


# Carregar dados do arquivo CSV usando o Pandas
data = pd.read_csv('data.csv', delimiter=',')

# Problema 1: Porcentagem de pessoas acima de 40 anos com colesterol alto
percentage_above_40_with_high_cholesterol = calculate_percentage_above_age_with_high_cholesterol(data, 40)
print(f"Porcentagem de pessoas acima de 40 anos com colesterol alto: {percentage_above_40_with_high_cholesterol}%")

# Problema 2: Porcentagem de pessoas acima de 40 anos com colesterol alto e alto teor de açúcar no sangue
percentage_above_40_with_high_cholesterol_and_high_sugar = calculate_percentage_above_age_with_high_cholesterol_and_high_sugar(data, 40)
print(f"Porcentagem de pessoas acima de 40 anos com colesterol alto e alto teor de açúcar no sangue: {percentage_above_40_with_high_cholesterol_and_high_sugar}%")

print(calculate_relation_hypertrofy(data))