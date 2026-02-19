from src.utils.validations import validate_cpf, validate_cnh

class Funcionario:
    def __init__(self, nome, cpf, cargo, cnh=None, id=None, ativo=True, id_usuario=None):
        """
        Representa um colaborador do condomínio.
        :param cnh: Opcional. Só preencher se o funcionário dirigir veículos da empresa/condomínio.
        """
        self.id = id
        self.nome = nome
        self.cpf = cpf      
        self.cargo = cargo
        self.cnh = cnh       
        self.ativo = ativo
        self.id_usuario = id_usuario 

    # --- Getter e Setter do CPF (Obrigatório) ---
    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, valor):
        cpf_limpo, erro = validate_cpf(valor)
        if erro:
            raise ValueError(f"Erro no CPF de '{self.nome}': {erro}")
        self._cpf = cpf_limpo

    # --- Getter e Setter da CNH (Opcional) ---
    @property
    def cnh(self):
        return self._cnh

    @cnh.setter
    def cnh(self, valor):
        if not valor:
            self._cnh = None
            return

        cnh_limpa, erro = validate_cnh(valor)
        if erro:
            raise ValueError(f"Erro na CNH de '{self.nome}': {erro}")
        self._cnh = cnh_limpa

    def __str__(self):
        status = "✅" if self.ativo else "❌"
        cpf_fmt = f"{self._cpf[:3]}.{self._cpf[3:6]}.{self._cpf[6:9]}-{self._cpf[9:]}"
        cnh_fmt = f"CNH: {self._cnh}" if self._cnh else "CNH: N/A"
        
        return f"{status} [ID: {self.id}] {self.nome} | {self.cargo} | {cpf_fmt} | {cnh_fmt}"

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self._cpf,
            "cargo": self.cargo,
            "cnh": self._cnh,
            "ativo": self.ativo,
            "id_usuario": self.id_usuario # <--- CORRIGIDO AQUI
        }