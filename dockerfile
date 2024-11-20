# Usando uma imagem base oficial do Python
FROM python:3.10-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos do projeto para o container
COPY . /app

# Instalar dependências do sistema que podem ser necessárias (ex: gcc, libpq-dev)
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Atualizar werkzeug para garantir que a versão correta seja instalada
RUN pip install werkzeug==2.2.3

# Expor a porta 1313 (ou a que você usar) para acesso ao servidor
EXPOSE 1313

# Definir o comando padrão para iniciar a aplicação Flask
CMD ["python", "app.py"]
