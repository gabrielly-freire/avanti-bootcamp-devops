# Sistema simples de gerenciamento de Farmácia (Python + Flask)

Aplicação full stack mínima para gerenciar medicamentos e registrar vendas, usando Flask, SQLite e uma página HTML com Bootstrap.

## Objetivo (Bootcamp Avanti)
- Utilizar práticas de DevOps em um projeto didático:
  - Provisionar infraestrutura com Terraform.
  - Dockerizar a aplicação para execução consistente.
  - Construir pipelines de CI/CD (GitHub Actions) para build, testes e entrega.

## Requisitos
- Docker e Docker Compose instalados

## Como rodar
Use Docker ou Docker Compose para executar rapidamente, sem configurar ambiente Python local.

### Como rodar o projeto usando Docker

Você não precisa ter o Python instalado na sua máquina, apenas o Docker. Siga os passos abaixo:

1. Construa a imagem da aplicação:

   Abra o terminal na pasta raiz do projeto e execute:
   ```
   docker build -t farmacia-app .
   ```

2. Inicie o container:
   ```
   docker run -p 5000:5000 farmacia-app
   ```
   Para iniciar e destruir automaticamente após parar:
   ```
   docker run --rm -p 5000:5000 farmacia-app
   ```

3. Acesse no navegador:
Abra o link `http://127.0.0.1:5000`.

Para parar a aplicação, basta apertar `Ctrl + C` no terminal. O container será removido automaticamente para economizar espaço.

### Como rodar com Docker Compose (Recomendado)
Esta é a forma mais fácil e automatizada de subir toda a infraestrutura do projeto de uma só vez.

1. Abra o terminal na pasta raiz do projeto.
2. Inicie o sistema com um único comando:
   ```
   docker compose up
   ```

## CI/CD (GitHub Actions)

- Disparos: push em qualquer branch, pull request para main e manual.
- Jobs:
  - Lint: ruff (Python 3.11) e verificação de sintaxe (py_compile).
  - Test: instala dependências, executa smoke de inicialização e testes com pytest, gera report.xml.
  - Build & Push: constrói imagem multi-arquitetura (Buildx) e publica no Docker Hub.

## Equipe

- Euclides Ferreira de Lira Neto [(euclidesanalistati)](https://github.com/euclidesanalistati)
- Francisca Gabrielly Lopes Freire [(gabrielly-freire)](https://github.com/gabrielly-freire)
- Igor Ezequiel Duarte Barreto [(Igor-Ezequiel)](https://github.com/Igor-Ezequiel)
