# Sistema de Biblioteca — Iteração 2
Implementação em **Flask** com persistência simples em arquivos JSON.

## Arquivos importantes
- `app.py` — aplicação Flask (endpoints REST)
- `auth.py` — funções de autenticação e tokens simples
- `storage.py` — leitura/escrita em arquivos JSON em `data/`
- `data/` — contém `users.json` e `books.json`
- `requirements.txt` — dependências

## Pré-requisitos
- Python 3.10+ instalado
- Git (opcional)
- (Windows) Recomenda-se usar `python -m venv venv`

## Como rodar localmente (Linux / macOS / Windows PowerShell)
1. Clone o repositório:
   ```bash
   git clone <url-do-repo>
   cd <repo>
