import uuid
import random
import string

# Génération d'un UUID aléatoire
def generate_random_uuid() -> str:
    return str(uuid.uuid4())

# Génération d'un code aléatoire
def generate_random_code() -> str:
    return str(uuid.uuid4().int)[:6]

# Génération d'une chaîne de caractères aléatoire
def generate_random_string(length: int) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))

# Génération d'un nombre aléatoire
def generate_random_number(length: int) -> str:
    return "".join(random.choices(string.digits, k=length))

# Génération d'un hexadécimal aléatoire
def generate_random_hex(length: int) -> str:
    return "".join(random.choices(string.hexdigits, k=length))