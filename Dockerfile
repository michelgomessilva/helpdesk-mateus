# 1. Imagem base: Python 3.12 (leve)
FROM python:3.12-slim

# 2. Diretório de trabalho dentro do container
WORKDIR /app

# 3. Instala o uv (gerenciador de dependências)
RUN pip install uv

# 4. Copia os arquivos de dependências primeiro (para aproveitar cache)
COPY pyproject.toml uv.lock ./

# 5. Instala as dependências (sem as de desenvolvimento, como pytest)
RUN uv sync --no-dev

# 6. Copia todo o resto do código
COPY . .

# 7. Porta que a aplicação vai usar
EXPOSE 8000

# 8. Comando para iniciar a aplicação
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]