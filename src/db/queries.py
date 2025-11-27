"""
Contém todas as constantes de queries SQL usadas pelo Repositório.
Mantém a lógica do banco separada do código Python.
"""

# --- Criação de Tabelas ---

CREATE_TABLE_MORADORES = """
CREATE TABLE IF NOT EXISTS moradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    placa TEXT NOT NULL,
    cnh TEXT NOT NULL,
    modelo TEXT,
    cor TEXT,
    apartamento TEXT NOT NULL,
    vaga_id INTEGER
    estacionado INTEGER DEFAULT 0  -- 0: Fora, 1: Dentro
);
"""

CREATE_TABLE_VISITANTES = """
CREATE TABLE IF NOT EXISTS visitantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    placa TEXT NOT NULL,
    cnh TEXT NOT NULL,
    modelo TEXT,
    cor TEXT,
    entrada TEXT NOT NULL
);
"""
# A coluna 'entrada' será salva como TEXT no formato ISO (ex: "2023-11-20 14:30:00")

# --- Queries para Moradores (CRUD) ---

INSERT_MORADOR = """
INSERT INTO moradores (nome, placa, cnh, modelo, cor, apartamento, vaga_id)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

SELECT_ALL_MORADORES = "SELECT id, nome, placa, cnh, modelo, cor, apartamento, vaga_id FROM moradores;"

UPDATE_MORADOR = """
UPDATE moradores 
SET nome=?, placa=?, cnh=?, modelo=?, cor=?, apartamento=?, vaga_id=?
WHERE id=?;
"""

DELETE_MORADOR = "DELETE FROM moradores WHERE id=?;"

# --- Queries para Moradores (Entrada/Saída) ---

REGISTRAR_ENTRADA_MORADOR = "UPDATE moradores SET estacionado = 1 WHERE id = ?;"
REGISTRAR_SAIDA_MORADOR = "UPDATE moradores SET estacionado = 0 WHERE id = ?;"


# --- Queries para Visitantes (Entrada/Saída) ---

INSERT_VISITANTE = """
INSERT INTO visitantes (nome, placa, cnh, modelo, cor, entrada)
VALUES (?, ?, ?, ?, ?, ?);
"""

# Seleciona apenas quem está ativo (neste modelo simples, se está na tabela, está no estacionamento)
SELECT_ALL_VISITANTES = "SELECT id, nome, placa, cnh, modelo, cor, entrada FROM visitantes;"

# Quando o visitante sai, removemos o registro (ou poderíamos mover para uma tabela de histórico)
DELETE_VISITANTE = "DELETE FROM visitantes WHERE id=?;"

# Query auxiliar para a "Catraca" (saber quantos visitantes estão dentro)
COUNT_VISITANTES = "SELECT COUNT(*) FROM visitantes;"