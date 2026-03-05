# Sistema simples de gerenciamento de Farmácia (Python + Flask)

Aplicação full stack mínima para gerenciar medicamentos e registrar vendas, usando Flask, SQLite e uma página HTML com Bootstrap.

## Objetivo (Bootcamp Avanti)
- Utilizar práticas de DevOps em um projeto didático:
  - Provisionar infraestrutura com Terraform.
  - Dockerizar a aplicação para execução consistente.
  - Construir pipelines de CI/CD (GitHub Actions) para build, testes e entrega.

## Requisitos
- Python 3.11 ou superior
- Pip (geralmente vem com o Python)

Verifique se o Python está instalado executando:
- Windows: `python --version` ou `py --version`
- Linux/macOS: `python3 --version`

Se o comando não existir, instale o Python a partir de https://www.python.org/downloads/

## Como rodar
1. Abra um terminal na pasta raiz do projeto.
2. Crie um ambiente virtual e ative:
   - Windows (PowerShell)
     ```
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
     Caso `python` não esteja disponível, tente:
     ```
     py -3 -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - Linux/macOS (bash/zsh)
     ```
     python3 -m venv .venv
     source .venv/bin/activate
     ```
3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
4. Inicie o servidor (modo desenvolvimento):
   - Recomendado (evita erros de import):
     ```
     python -m app.app
     ```
   - Alternativa:
     ```
     python app/app.py
     ```
   A aplicação ficará disponível em: http://127.0.0.1:5000

## 🚀 Como rodar o projeto usando Docker

Você não precisa ter o Python instalado na sua máquina, apenas o Docker. Siga os passos abaixo:

**1. Construa a imagem da aplicação:**
1. Abra o terminal na pasta raiz do projeto use:
`docker build -t farmacia-app .`

**2. Inicie o container:**
`docker run -p 5000:5000 farmacia-app`, caso queira iniciar e logo destruí-lo use: `docker run --rm -p 5000:5000 farmacia-app`

**3. Acesse no navegador:**
Abra o link `http://127.0.0.1:5000`.

Para parar a aplicação, basta apertar `Ctrl + C` no terminal. O container será removido automaticamente para economizar espaço.

## Como rodar com Docker Compose (Recomendado)
Esta é a forma mais fácil e automatizada de subir toda a infraestrutura do projeto de uma só vez.

1. Abra o terminal na pasta raiz do projeto.
2. Inicie o sistema com um único comando:
   `docker compose up`