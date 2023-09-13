from passlib.context import CryptContext

# Configuração da segurança
CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_pass(password: str, hash: str) -> bool:
    """
    Função para verificar se a senha está correta, comparando a senha em texto puro, informado pelo usuário,
    e o hash da senha que estará salvo no banco de dados
    """
    return CRIPTO.verify(password, hash)


def generate_hash_pass(password: str) -> str:
    """
    Função que gera e retorna o hash da senha

    Args:
        password (str): senha em texto

    Returns:
        str: hash da senha
    """
    return CRIPTO.hash(password)    