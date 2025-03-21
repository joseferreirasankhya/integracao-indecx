# Integração Indecx

Este é um projeto Django para integração do serviço Indecx com o SenseData, para levar os dados de pesquisa de NPS em tempo real e, consequentemente, gerar planos de ação para tratamento dos clientes detratores e neutros.

## Estrutura do Projeto

```
.github/
  workflows/
    django.yml
.gitignore
manage.py
README.md
requirements.txt
sensedata/
  __init__.py
  __pycache__/
  admin.py
  apps.py
  authentication.py
  migrations/
  models.py
  services/
    nps_service.py
  tests/
    __init__.py
    tests.py
  urls.py
  views.py
src/
  __init__.py
  __pycache__/
  asgi.py
  settings.py
  urls.py
  wsgi.py
utils/
  __pycache__/
  utils.py
vercel.json
```

## Requisitos

- Python 3.12
- Django
- Django REST Framework
- python-dotenv

## Instalação

1. Clone o repositório:
    ```sh
    git clone <URL_DO_REPOSITORIO>
    cd integracao-indecx
    ```

2. Crie e ative um ambiente virtual:
    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

4. Configure as variáveis de ambiente:
    Crie um arquivo `.env` na raiz do projeto e adicione as variáveis necessárias.

5. Execute as migrações:
    ```sh
    python manage.py migrate
    ```

6. Inicie o servidor de desenvolvimento:
    ```sh
    python manage.py runserver
    ```

## Testes

Para rodar os testes, execute:
```sh
python manage.py test
```

## CI/CD

Este projeto utiliza GitHub Actions para integração contínua. O workflow está definido em `.github/workflows/django.yml`.

## Estrutura dos Diretórios

- `sensedata/`: Contém os aplicativos Django, incluindo modelos, views, urls e testes.
- `src/`: Contém configurações do projeto Django.
- `utils/`: Contém utilitários usados no projeto.
- `venv/`: Ambiente virtual para dependências do Python.

## Contribuição

1. Faça um fork do projeto.
2. Crie uma branch para sua feature:
   ```sh
   git checkout -b feature/nova-feature
   ```
3. Commit suas mudanças:
   ```sh
   git commit -am 'Adiciona nova feature'
   ```
4. Faça um push para a branch:
   ```sh
   git push origin feature/nova-feature
   ```
5. Abra um Pull Request.
