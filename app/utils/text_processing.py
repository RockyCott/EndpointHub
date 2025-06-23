import re
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words('spanish') + stopwords.words('english'))

def clean_text(text: str) -> str:
    """
    Cleans input text for semantic search by:
    - Separating camelCase
    - Lowercasing
    - Removing special characters and digits
    - Removing stopwords and short tokens
    - Normalizing spaces

    Args:
        text (str): Raw input text

    Returns:
        str: Cleaned and normalized text
    """
    if not text:
        return ""

    # Separar palabras en camelCase o PascalCase
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)

    # Reemplazar guiones y guiones bajos por espacio
    text = re.sub(r"[_-]", " ", text)

    # Remover caracteres no alfanuméricos (mantener espacios y letras)
    text = re.sub(r"[^\w\s]", " ", text)

    # Convertir a minúsculas
    text = text.lower()

    # Tokenizar
    tokens = text.split()

    # Filtrar stopwords y tokens muy cortos (<= 2 caracteres)
    cleaned_tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]

    # Normalizar espacios
    return " ".join(cleaned_tokens)
