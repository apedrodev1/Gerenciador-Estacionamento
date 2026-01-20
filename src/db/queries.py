"""
Módulo de Queries SQL.
Contém todas as instruções SQL organizadas por contexto.
"""

# ==============================================================================
# 1. CRIAÇÃO DE TABELAS (DDL)
# ==============================================================================

CREATE_TABLE_MORADORES = """
CREATE TABLE IF NOT EXISTS moradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    placa TEXT NOT NULL,
    cnh TEXT NOT NULL,
    modelo TEXT,
    cor TEXT,
    apartamento TEXT NOT NULL,
    vaga_id TEXT,  -- Vaga pode ser alfanumérica (Ex: '10-A', 'V01')
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
    entrada TEXT NOT NULL, -- Formato ISO: YYYY-MM-DD HH:MM:SS
    numero_vaga TEXT NOT NULL
);
"""

# Alterado de 'visitantes_frequentes' para 'visitantes_cadastrados'
CREATE_TABLE_VISITANTES_CADASTRO = """
CREATE TABLE IF NOT EXISTS visitantes_cadastrados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    placa TEXT UNIQUE NOT NULL,
    cnh TEXT,
    modelo TEXT,
    cor TEXT,
    data_cadastro TEXT
);
"""


# ==============================================================================
# 2. MORADORES (CRUD + CATRACA)
# ==============================================================================

# --- CRUD Básico ---
INSERT_MORADOR = """
INSERT INTO moradores (nome, placa, cnh, modelo, cor, apartamento, vaga_id)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

SELECT_ALL_MORADORES = """
SELECT id, nome, placa, cnh, modelo, cor, apartamento, vaga_id, estacionado 
FROM moradores;
"""

SELECT_MORADOR_BY_PLACA = """
SELECT id, nome, placa, cnh, modelo, cor, apartamento, vaga_id, estacionado 
FROM moradores WHERE placa = ?;
"""

UPDATE_MORADOR = """
UPDATE moradores 
SET nome=?, placa=?, cnh=?, modelo=?, cor=?, apartamento=?, vaga_id=?
WHERE id=?;
"""

DELETE_MORADOR = "DELETE FROM moradores WHERE id=?;"

# --- Controle de Acesso (Catraca) ---
# Usamos a placa como chave para operação rápida na catraca
REGISTRAR_ENTRADA_MORADOR = "UPDATE moradores SET estacionado = 1 WHERE placa = ?;"
REGISTRAR_SAIDA_MORADOR = "UPDATE moradores SET estacionado = 0 WHERE placa = ?;"


# ==============================================================================
# 3. VISITANTES ROTATIVOS (OPERAÇÃO DIÁRIA)
# ==============================================================================
# Gerencia quem está PARADO no estacionamento AGORA.

INSERT_VISITANTE = """
INSERT INTO visitantes (nome, placa, cnh, modelo, cor, entrada, numero_vaga)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

SELECT_ALL_VISITANTES = """
SELECT id, nome, placa, cnh, modelo, cor, entrada, numero_vaga 
FROM visitantes;
"""

SELECT_VISITANTE_BY_PLACA = """
SELECT id, nome, placa, cnh, modelo, cor, entrada, numero_vaga 
FROM visitantes WHERE placa = ?;
"""

SELECT_VAGAS_OCUPADAS = "SELECT numero_vaga FROM visitantes;"

DELETE_VISITANTE = "DELETE FROM visitantes WHERE id=?;"

COUNT_VISITANTES = "SELECT COUNT(*) FROM visitantes;"


# ==============================================================================
# 4. VISITANTES CADASTRO (FREQUENTES / PRESTADORES)
# ==============================================================================
# Banco de dados de visitantes conhecidos para agilizar a entrada.

INSERT_VISITANTE_CADASTRO = """
INSERT INTO visitantes_cadastrados (nome, placa, cnh, modelo, cor, data_cadastro)
VALUES (?, ?, ?, ?, ?, ?);
"""

SELECT_ALL_VISITANTES_CADASTRO = "SELECT * FROM visitantes_cadastrados;"

SELECT_VISITANTE_CADASTRO_BY_PLACA = "SELECT * FROM visitantes_cadastrados WHERE placa = ?;"

UPDATE_VISITANTE_CADASTRO = """
UPDATE visitantes_cadastrados 
SET nome=?, cnh=?, modelo=?, cor=?
WHERE id=?;
"""

DELETE_VISITANTE_CADASTRO = "DELETE FROM visitantes_cadastrados WHERE id=?;"


# ==============================================================================
# 5. RELATÓRIOS E MAPAS
# ==============================================================================
# Une as duas tabelas para mostrar o mapa completo do pátio

SELECT_OCUPACAO_TOTAL = """
SELECT 
    vaga_id as vaga, 
    'MORADOR' as tipo, 
    nome, 
    placa, 
    modelo, 
    cor,
    apartamento
FROM moradores 
WHERE estacionado = 1

UNION ALL

SELECT 
    numero_vaga as vaga, 
    'VISITANTE' as tipo, 
    nome, 
    placa, 
    modelo, 
    cor,
    NULL as apartamento
FROM visitantes
ORDER BY tipo, vaga;
"""

# ==============================================================================
# 6. AUDITORIA / HISTÓRICO 
# ==============================================================================
# Cria a tabela de registro de entradas e saidas 

CREATE_TABLE_HISTORICO = """
CREATE TABLE IF NOT EXISTS historico_movimentacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_hora TEXT NOT NULL,
    placa TEXT NOT NULL,
    tipo_veiculo TEXT NOT NULL,  -- 'MORADOR' ou 'VISITANTE'
    tipo_evento TEXT NOT NULL    -- 'ENTRADA' ou 'SAIDA'
);
"""

INSERT_HISTORICO = """
INSERT INTO historico_movimentacao (data_hora, placa, tipo_veiculo, tipo_evento)
VALUES (?, ?, ?, ?)
"""

# --- LEITURA DE HISTÓRICO ---
SELECT_HISTORICO_GERAL = """
SELECT data_hora, placa, tipo_veiculo, tipo_evento 
FROM historico_movimentacao 
ORDER BY id DESC 
LIMIT 50;
"""

SELECT_HISTORICO_POR_PLACA = """
SELECT data_hora, placa, tipo_veiculo, tipo_evento 
FROM historico_movimentacao 
WHERE placa = ? 
ORDER BY id DESC;
"""