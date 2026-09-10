from pathlib import Path

from convertir_audio import extraer_audio
from separar_audio import separar_voz
from transcribir import transcribir_audio
from traducir import (cargar_modelo, traducir_segmentos_contextuales)

def main():

    print("=" * 50)
    print("TRADUCTOR DE CANCIONES")
    print("=" * 50)

    ruta = input(
        "\nIngrese la ruta de la canción MP4: "
    )

    try:

        # 1. EXTRAER AUDIO
        audio = extraer_audio(ruta)

        # 2. SEPARAR VOZ E INSTRUMENTAL
        voz, instrumental = separar_voz(audio)

        # 3. TRANSCRIBIR SOLO LA VOZ
        resultado = transcribir_audio(voz)

        segmentos = resultado["segments"]

        print("\n" + "=" * 50)
        print("SEGMENTOS DETECTADOS")
        print("=" * 50)

        print(
            f"Cantidad de segmentos: {len(segmentos)}"
        )

        for segmento in segmentos:

            print(
                f"[{segmento['start']:.2f}s - "
                f"{segmento['end']:.2f}s] "
                f"{segmento['text']}"
            )

        # 4. CARGAR MODELO DE TRADUCCIÓN
        tokenizer, modelo = cargar_modelo()

        # 5. TRADUCIR POR BLOQUES
        resultados = traducir_segmentos_contextuales(
            segmentos,
            tokenizer,
            modelo
            )

        # 6. GENERAR RESULTADO
        carpeta_resultados = Path("resultados")
        carpeta_resultados.mkdir(exist_ok=True)

        nombre_cancion = Path(ruta).stem

        ruta_txt = (
            carpeta_resultados
            / f"{nombre_cancion}_traducida.txt"
        )

        with open(
            ruta_txt,
            "w",
            encoding="utf-8"
        ) as archivo:

            archivo.write(
                "TRADUCCIÓN CONTEXTUAL DE LA CANCIÓN\n"
            )

            archivo.write("=" * 50)
            archivo.write("\n\n")

            for i, resultado in enumerate(
                resultados,
                start=1
            ):

                archivo.write(
                    f"BLOQUE {i}\n"
                )

                archivo.write(
                    f"[{resultado['start']:.2f}s - "
                    f"{resultado['end']:.2f}s]\n"
                )

                archivo.write(
                    f"Original: "
                    f"{resultado['original']}\n"
                )

                archivo.write(
                    f"Traducción: "
                    f"{resultado['traduccion']}\n"
                )

                archivo.write("\n")

        # 7. FINALIZAR
        print("\n" + "=" * 50)
        print("PROCESO FINALIZADO")
        print("=" * 50)

        print(
            f"\nArchivo generado:\n{ruta_txt}"
        )

        print(
            f"\nAudio vocal generado:\n{voz}"
        )

        print(
            f"Instrumental generado:\n{instrumental}"
        )

    except Exception as e:

        print("\nERROR:")
        print(e)


if __name__ == "__main__":
    main()