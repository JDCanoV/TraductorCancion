from transformers import MarianMTModel, MarianTokenizer


MODELO_TRADUCCION = "Helsinki-NLP/opus-mt-en-es"


def cargar_modelo():

    print("Cargando modelo de traducción...")

    tokenizer = MarianTokenizer.from_pretrained(
        MODELO_TRADUCCION
    )

    modelo = MarianMTModel.from_pretrained(
        MODELO_TRADUCCION
    )

    return tokenizer, modelo


def traducir_texto(
    texto,
    tokenizer,
    modelo
):

    entradas = tokenizer(
        texto,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512
    )

    salida = modelo.generate(
        **entradas,
        max_length=512,
        num_beams=5,
        early_stopping=True
    )

    traduccion = tokenizer.decode(
        salida[0],
        skip_special_tokens=True
    )

    return traduccion


def limpiar_traduccion(texto):

    texto = texto.strip()

    # Eliminar espacios repetidos
    texto = " ".join(texto.split())

    return texto


def obtener_contexto(
    segmentos,
    indice
):

    contexto_anterior = ""

    contexto_posterior = ""

    # Segmento anterior
    if indice > 0:

        contexto_anterior = (
            segmentos[indice - 1]["text"]
            .strip()
        )

    # Segmento posterior
    if indice < len(segmentos) - 1:

        contexto_posterior = (
            segmentos[indice + 1]["text"]
            .strip()
        )

    return (
        contexto_anterior,
        contexto_posterior
    )


def traducir_segmentos_contextuales(
    segmentos,
    tokenizer,
    modelo
):

    resultados = []

    print("\n" + "=" * 50)
    print("TRADUCCIÓN CONTEXTUAL")
    print("=" * 50)

    for i, segmento in enumerate(segmentos):

        texto_actual = segmento["text"].strip()

        contexto_anterior, contexto_posterior = (
            obtener_contexto(
                segmentos,
                i
            )
        )

        print(
            f"\nSegmento {i + 1}/{len(segmentos)}"
        )

        print(
            f"Original: {texto_actual}"
        )

        # Traducción base
        traduccion = traducir_texto(
            texto_actual,
            tokenizer,
            modelo
        )

        traduccion = limpiar_traduccion(
            traduccion
        )

        resultado = {

            "start": segmento["start"],

            "end": segmento["end"],

            "original": texto_actual,

            "traduccion": traduccion,

            "contexto_anterior":
                contexto_anterior,

            "contexto_posterior":
                contexto_posterior
        }

        resultados.append(resultado)

        print(
            f"Traducción: {traduccion}"
        )

    return resultados
