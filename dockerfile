# Use uma imagem base do Python
FROM python:3.8-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar todos os arquivos do diretório local para o diretório de trabalho do container
COPY . /app

# Instalar as dependências do projeto
RUN pip install -r requirements.txt

# Expor a porta 1313 no container
EXPOSE 1313

# Executar o aplicativo Flask
CMD ["python", "app.py"]
