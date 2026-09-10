from pathlib import Path
import subprocess


def extraer_audio(ruta_archivo):
    ruta_archivo = Path(ruta_archivo)

    if not ruta_archivo.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo: {ruta_archivo}"
        )

    extensiones_validas = [".mp3", ".mp4"]

    if ruta_archivo.suffix.lower() not in extensiones_validas:
        raise ValueError(
            "El archivo debe tener formato MP3 o MP4."
        )

    carpeta_audio = Path("audio")
    carpeta_audio.mkdir(exist_ok=True)

    ruta_salida = carpeta_audio / f"{ruta_archivo.stem}.wav"

    comando = [
        "ffmpeg",
        "-y",
        "-i",
        str(ruta_archivo),
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        str(ruta_salida)
    ]

    print("Extrayendo audio...")

    subprocess.run(comando, check=True)

    print(f"Audio generado: {ruta_salida}")

    return ruta_salida