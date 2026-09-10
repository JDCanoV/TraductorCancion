import whisper


MODELO_WHISPER = "small"


def transcribir_audio(ruta_audio):

    print("\n" + "=" * 50)
    print("TRANSCRIPCIÓN DE LA VOZ")
    print("=" * 50)

    print(f"\nCargando modelo Whisper: {MODELO_WHISPER}")

    modelo = whisper.load_model(MODELO_WHISPER)

    print("Transcribiendo voz...")

    resultado = modelo.transcribe(
        str(ruta_audio),
        language="en",
        task="transcribe",
        fp16=False,
        temperature=0,
        condition_on_previous_text=True,
        word_timestamps=True
    )

    return resultado