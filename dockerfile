# Arquivo: Dockerfile

# Usando uma imagem base oficial do Python
FROM python:3.10-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos do projeto para o container
COPY . /app

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta 1313 (ou a que você usar) para acesso ao servidor
EXPOSE 1313

# Definir o comando padrão para iniciar a aplicação Flask
CMD ["python", "app.py"]
