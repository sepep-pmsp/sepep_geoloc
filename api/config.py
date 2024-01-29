from dotenv import load_dotenv
import os

def load_env(var_name:str)->str:

    load_dotenv()
    try:
        return os.environ[var_name]
    except KeyError:
        raise RuntimeError(f'Variável de ambiente {var_name} não definida!')