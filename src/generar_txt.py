def crear_txt(segmentos, traducciones, ruta_salida):

    with open(
        ruta_salida,
        "w",
        encoding="utf-8"
    ) as archivo:

        archivo.write("TRADUCCIÓN DE LA CANCIÓN\n")
        archivo.write("=" * 50)
        archivo.write("\n\n")

        for i, (segmento, traduccion) in enumerate(
            zip(segmentos, traducciones),
            start=1
        ):

            inicio = segmento["start"]
            fin = segmento["end"]

            archivo.write(
                f"[{inicio:.2f}s - {fin:.2f}s]\n"
            )

            archivo.write(
                f"Original: {segmento['text'].strip()}\n"
            )

            archivo.write(
                f"Traducción: {traduccion}\n"
            )

            archivo.write("\n")

    print(f"TXT generado: {ruta_salida}")