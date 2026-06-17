<div align="center">

# Z-Message

![Status](https://img.shields.io/badge/Status-Concluído-darkgreen)
![Python](https://img.shields.io/badge/Python-3.12.3-yellow?logo=python)

Z-Message, um projeto para envio automatizado de mensagens via Whatsapp utilizando Supabase.

</div>

## Stack Tecnológica

- **Python 3.12.3**
- **Supabase 2.15.2**
- **Z-API**

## Arquitetura de Diretórios

```plain
├── pyproject.toml          -> Configurações do projeto e dependências
├── README.md               -> Documentação simples do projeto
├── requirements-dev.txt    -> Dependências para desenvolvimento
├── requirements.txt        -> Dependências principais para execução
└── src
    ├── config.py           -> Carregamento de variáveis de ambiente
    ├── database.py         -> Conexão e operações com Supabase
    ├── logger_config.py    -> Configuração do logging
    ├── main.py             -> Script principal para execução
    └── whatsapp.py         -> Integração com a Z-API para envio de mensagens
```

## Setup da Tabela

Execute no SQL Editor do Supabase:

```sql
-- Criação da tabela
CREATE TABLE contacts (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name TEXT NOT NULL,
  phone TEXT NOT NULL UNIQUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ
);

-- Função que atualiza o campo updated_at automaticamente
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que chama a função antes de qualquer UPDATE
CREATE TRIGGER trigger_set_updated_at
BEFORE UPDATE ON contacts
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

-- Dados de teste (use o formato 55 + DDD + Número sem espaços ou símbolos)
INSERT INTO contacts (name, phone) VALUES
    ('João Silva',  '5583999998881'),
    ('Maria Souza', '5583999998882'),
    ('Carlos Lima', '5583999998883');

-- Habilitar RLS e permitir leitura para service_role
ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "allow_select_service_role"
ON contacts
FOR SELECT
USING (true);

GRANT SELECT ON public.contacts TO service_role;
```

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:

| Variável                  | Descrição                        |
|---------------------------|----------------------------------|
| `SUPABASE_URL`            | URL do projeto no Supabase       |
| `SUPABASE_SERVICE_ROLE_KEY` | Chave service_role do Supabase |
| `ZAPI_INSTANCE_ID`        | ID da instância na Z-API         |
| `ZAPI_TOKEN`              | Token da instância na Z-API      |
| `ZAPI_CLIENT_TOKEN`         | Client token para autenticação Z-API |

## Instalando e Rodando
```bash
# Criar e ativar ambiente virtual
python -m venv .venv
source .venv/bin/activate # Linux/Mac
# ou Windows: .venv\Scripts\activate

# Para instalação das dependências principais
pip install -r requirements.txt

# Para desenvolvimento (linting, tasks)
pip install -r requirements-dev.txt

# Rodar o script (a partir da raiz do projeto)
python -m src.main # ou: task run (se requirements-dev estiver instalado)
```

## Documentação das Tecnologias

**Python**: [https://docs.python.org/3/](https://docs.python.org/3/)

**Supabase**: [https://supabase.com/docs](https://supabase.com/docs)

**Z-API**: [https://z-api.io/docs](https://z-api.io/docs)
