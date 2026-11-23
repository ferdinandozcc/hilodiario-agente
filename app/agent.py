"""Agente de ejemplo: resume una noticia en un titular corto.

Sustituye `summarize` por la llamada real a tu agente (API de Anthropic, n8n, etc.).
La interfaz es lo único que importa para los tests y las evals: texto de entrada -> resumen.
"""


def summarize(text: str, max_words: int = 25) -> str:
    """Devuelve la primera frase del texto, recortada a `max_words` palabras."""
    first_sentence = text.strip().split(". ")[0].rstrip(".")
    words = first_sentence.split()
    return " ".join(words[:3])
