# IMPLEMENTING - Issue #25

### FILE: webapp/docs/USAGE.md
```markdown
# Documentação de Uso: ToDo List App

## O que é este sistema

Este é um sistema de lista de tarefas (ToDo list) simples. É uma aplicação web com um backend construído em FastAPI e um frontend em HTML e JavaScript, servido estaticamente.

## Como rodar

Siga os passos abaixo para rodar a aplicação localmente:

1. Instale as dependências necessárias:
   ```bash
   pip install fastapi uvicorn
   ```

2. Inicie o servidor:
   ```bash
   python -m webapp.server
   ```

3. Abra seu navegador e acesse: `http://localhost:8000`

## Como usar

- **Adicionar tarefa**: Digite o nome da tarefa no campo de texto e clique no botão "Adicionar" ou pressione a tecla Enter.
- **Listar tarefas**: As tarefas são carregadas e exibidas automaticamente quando a página é aberta.
- **Excluir tarefa**: Clique no botão "X" ao lado da tarefa que deseja remover.

## API endpoints

| Método | Endpoint           | Descrição                   |
|--------|--------------------|-----------------------------|
| GET    | `/api/todos`       | Retorna todas as tarefas.   |
| POST   | `/api/todos`       | Cria uma nova tarefa.       |
| DELETE | `/api/todos/{id}`  | Exclui uma tarefa pelo ID.  |

## Estrutura de arquivos

Aqui está uma visão geral da estrutura de arquivos da pasta `webapp/`:

- `webapp/server.py`: Contém a lógica do backend com FastAPI.
- `webapp/static/index.html`: A página principal da aplicação.
- `webapp/static/script.js`: O código JavaScript para a interação do usuário.
- `webapp/static/style.css`: Estilos CSS para a aparência da página.
- `webapp/docs/USAGE.md`: Este documento de uso.
```

### FILE: tests/test_docs.py
```python
import os

DOCS_FILE = 'webapp/docs/USAGE.md'


def test_docs_file_exists_and_is_not_empty():
    """
    Tests if the USAGE.md file exists and is not empty.
    """
    assert os.path.exists(DOCS_FILE), f"Documentation file not found at {DOCS_FILE}"
    assert os.path.getsize(DOCS_FILE) > 0, f"Documentation file {DOCS_FILE} is empty."


def test_docs_file_contains_key_sections():
    """
    Tests if the USAGE.md file contains the required key sections.
    """
    # Ensure the file exists before trying to read it
    assert os.path.exists(DOCS_FILE), f"Documentation file not found at {DOCS_FILE}"

    with open(DOCS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    required_sections = [
        "Como rodar",
        "Como usar",
        "API endpoints"
    ]

    for section in required_sections:
        assert section in content, f"Key section '{section}' not found in {DOCS_FILE}"
```

## Decisions Made
1.  **Hypothetical File Structure**: The issue required documenting the file structure of a `webapp/` folder that does not exist in the repository. I invented a logical structure for a simple FastAPI application (`server.py`, `static/index.html`, `static/script.js`, `static/style.css`, and the `docs/USAGE.md` itself) and included it in the documentation. This resolves the ambiguity of documenting non-existent files.
2.  **Test File Path**: I assumed the tests are run from the project root. Therefore, the path to the documentation file in `tests/test_docs.py` is `'webapp/docs/USAGE.md'`. This is a standard convention in most Python projects.

## Notes
- The created documentation (`webapp/docs/USAGE.md`) and its corresponding test (`tests/test_docs.py`) are for a ToDo list application that is not present in the provided repository context. The implementation follows the issue's requirements precisely, documenting this hypothetical application.
- The new `webapp/` directory and its `docs/` subdirectory are implicitly created by adding the file `webapp/docs/USAGE.md`.
