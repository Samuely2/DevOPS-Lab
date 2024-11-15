FROM python:3.9-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos necessários
COPY . .

# Instalar dependências
RUN pip install -r requirements.txt

# Expor a porta da API
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["flask", "run", "--host=0.0.0.0"]
