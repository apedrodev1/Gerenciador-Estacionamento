"""
Contém todas as constantes de queries SQL usadas pelo Repositório.
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
    vaga_id INTEGER,
    estacionado INTEGER DEFAULT 0
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
    entrada TEXT NOT NULL,
    numero_vaga INTEGER NOT NULL
);
"""

# --- Queries para Moradores ---

INSERT_MORADOR = """
INSERT INTO moradores (nome, placa, cnh, modelo, cor, apartamento, vaga_id)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

SELECT_ALL_MORADORES = "SELECT id, nome, placa, cnh, modelo, cor, apartamento, vaga_id, estacionado FROM moradores;"

UPDATE_MORADOR = """
UPDATE moradores 
SET nome=?, placa=?, cnh=?, modelo=?, cor=?, apartamento=?, vaga_id=?
WHERE id=?;
"""

DELETE_MORADOR = "DELETE FROM moradores WHERE id=?;"
REGISTRAR_ENTRADA_MORADOR = "UPDATE moradores SET estacionado = 1 WHERE id = ?;"
REGISTRAR_SAIDA_MORADOR = "UPDATE moradores SET estacionado = 0 WHERE id = ?;"

# --- Queries para Visitantes ---

INSERT_VISITANTE = """
INSERT INTO visitantes (nome, placa, cnh, modelo, cor, entrada, numero_vaga)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

SELECT_ALL_VISITANTES = "SELECT id, nome, placa, cnh, modelo, cor, entrada, numero_vaga FROM visitantes;"

SELECT_VAGAS_OCUPADAS = "SELECT numero_vaga FROM visitantes;"

DELETE_VISITANTE = "DELETE FROM visitantes WHERE id=?;"
COUNT_VISITANTES = "SELECT COUNT(*) FROM visitantes;"


# Seleciona Visitantes E Moradores (apenas os estacionados)
SELECT_OCUPACAO_TOTAL = """
SELECT numero_vaga as vaga, 'Visitante' as tipo, nome, placa, modelo, cor 
FROM visitantes
UNION ALL
SELECT vaga_id as vaga, 'Morador' as tipo, nome, placa, modelo, cor 
FROM moradores 
WHERE estacionado = 1
ORDER BY vaga ASC;
"""