from app.agent import summarize


def test_respeta_el_limite_de_palabras():
    texto = " ".join(["palabra"] * 100)
    assert len(summarize(texto, max_words=10).split()) <= 10


def test_no_devuelve_vacio():
    assert summarize("El Ayuntamiento aprueba el presupuesto. Más detalles.") != ""
