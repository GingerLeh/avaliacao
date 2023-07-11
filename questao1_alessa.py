import requests
import csv
from flask import Flask, jsonify, request

app = Flask(__name__)

# Função para obter informações do PyPI
def get_package_info(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        package_info = response.json()
        releases = package_info.get("releases", {})
        if releases:
            latest_release = max(releases, default=None, key=lambda r: releases[r][0].get("upload_time", ""))
            if latest_release:
                release_info = releases[latest_release]
                if release_info:
                    upload_time = release_info[0].get("upload_time", "")
                    python_version = release_info[0].get("python_version", "")
                    downloads = sum(r.get("downloads", 0) for r in release_info)
                    return {
                        "Nome": package_name,
                        "Data de Publicação": upload_time,
                        "Versão Python": python_version,
                        "Downloads do Último Mês": downloads
                    }
    return None

# Restante do código...


# Restante do código...

# Função para criar o arquivo CSV com as informações dos pacotes
def create_package_csv():
    packages = [
        "requests",
        "flask",
        "numpy",
        "pandas",
        "matplotlib"
        # Adicione mais pacotes aqui
    ]
    
    with open("package_info.csv", "w", newline="") as csvfile:
        fieldnames = ["Nome", "Data de Publicação", "Versão Python", "Downloads do Último Mês"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for package in packages:
            package_info = get_package_info(package)
            if package_info:
                writer.writerow(package_info)

# Rota para retornar os pacotes ordenados por nome
@app.route("/packages/sort_by_name")
def sort_packages_by_name():
    with open("package_info.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        sorted_packages = sorted(reader, key=lambda row: row["Nome"])
        return jsonify(list(sorted_packages))

# Rota para retornar os pacotes ordenados por data de publicação da versão mais recente
@app.route("/packages/sort_by_upload_date")
def sort_packages_by_upload_date():
    with open("package_info.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        sorted_packages = sorted(reader, key=lambda row: row["Data de Publicação"], reverse=True)
        return jsonify(list(sorted_packages))

# Rota para retornar os pacotes ordenados por versão Python da versão mais recente
@app.route("/packages/sort_by_python_version")
def sort_packages_by_python_version():
    with open("package_info.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        sorted_packages = sorted(reader, key=lambda row: row["Versão Python"], reverse=True)
        return jsonify(list(sorted_packages))

# Rota para retornar os pacotes ordenados por quantidade de downloads do último mês
@app.route("/packages/sort_by_downloads")
def sort_packages_by_downloads():
    with open("package_info.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        sorted_packages = sorted(reader, key=lambda row: int(row["Downloads do Último Mês"]), reverse=True)
        return jsonify(list(sorted_packages))

# Rota para buscar pacotes por nome
@app.route("/packages/search_by_name")
def search_packages_by_name():
    package_name = request.args.get("name")
    with open("package_info.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        filtered_packages = [row for row in reader if row["Nome"].lower().startswith(package_name.lower())]
        return jsonify(list(filtered_packages))

# Rota para buscar pacotes por versão Python
@app.route("/packages/search_by_python_version")
def search_packages_by_python_version():
    python_version = request.args.get("version")
    with open("package_info.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        filtered_packages = [row for row in reader if row["Versão Python"] == python_version]
        return jsonify(list(filtered_packages))

if __name__ == "__main__":
    create_package_csv()
    app.run()
