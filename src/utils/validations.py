"""
Módulo de utilitários de validação.
Centraliza regras de formato e unicidade para inputs do sistema.
Localização: src/utils/validations.py
"""
import re

# Padrão compilado para placas (Antiga e Mercosul)
# Aceita: AAA1234 ou AAA1B23
REGEX_PLACA = re.compile(r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$')

# --- VALIDAÇÕES GERAIS ---

def validate_names(name):
    """Aceita apenas letras e espaços."""
    cleaned = name.strip().title()
    if cleaned and all(c.isalpha() or c.isspace() for c in cleaned):
        return cleaned, None
    return None, "O nome deve conter apenas letras."

def validate_yes_no(input_value):
    """Aceita s/n ou y/n."""
    cleaned = input_value.strip().lower()
    if cleaned in ('s', 'n', 'y'):
        return cleaned, None
    return None, "Digite apenas 's' (sim) ou 'n' (não)."

def validate_apartamento(apto_input):
    """Valida identificador de apartamento (Max 6 chars)."""
    cleaned = str(apto_input).strip().upper()
    if not cleaned:
        return None, "O apartamento não pode estar vazio."
    if len(cleaned) > 6:
        return None, "Máximo de 6 caracteres (ex: 102, 12-B)."
    return cleaned, None

# --- VALIDAÇÕES DE VEÍCULO (PLACA) ---

def validate_placa(placa_input):
    """Valida formato AAA-1234 ou Mercosul."""
    limpa = placa_input.replace("-", "").strip().upper()
    
    if REGEX_PLACA.match(limpa):
        return limpa, None
    return None, "Formato inválido. Use AAA-1234 ou Mercosul."

def validate_placa_unica(placa_input, placas_existentes):
    """Valida formato e verifica se já existe na lista proibida."""
    placa, erro = validate_placa(placa_input)
    if erro:
        return None, erro

    if placa in placas_existentes:
        return None, f"A placa {placa} JÁ ESTÁ CADASTRADA."
    
    return placa, None

# --- VALIDAÇÕES PESSOAIS (CNH) ---

def validate_cnh(cnh_input):
    """Valida se contém exatamente 11 dígitos numéricos."""
    limpa = str(cnh_input).strip()
    
    if not limpa.isdigit():
        return None, "A CNH deve conter apenas números."
    
    if len(limpa) != 11:
        return None, f"A CNH deve ter 11 dígitos (atual: {len(limpa)})."
    
    return limpa, None

def validate_cnh_unica(cnh_input, cnhs_existentes):
    """Valida formato e verifica duplicidade."""
    cnh, erro = validate_cnh(cnh_input)
    if erro:
        return None, erro

    if cnh in cnhs_existentes:
        return None, f"A CNH {cnh} já pertence a outro cadastro."
    
    return cnh, None