from pathlib import Path
import subprocess
import sys


def separar_voz(ruta_audio):

    ruta_audio = Path(ruta_audio)

    if not ruta_audio.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo: {ruta_audio}"
        )

    carpeta_salida = Path("separados")
    carpeta_salida.mkdir(exist_ok=True)

    print("\n" + "=" * 50)
    print("SEPARACIÓN DE VOZ E INSTRUMENTAL")
    print("=" * 50)

    comando = [
        sys.executable,
        "-m",
        "demucs",
        "--two-stems=vocals",
        "-n",
        "htdemucs",
        "-o",
        str(carpeta_salida),
        str(ruta_audio)
    ]

    print("\nEjecutando Demucs...")
    print("La separación puede tardar varios minutos.\n")

    subprocess.run(comando, check=True)

    nombre = ruta_audio.stem

    carpeta_demucs = (
        carpeta_salida
        / "htdemucs"
        / nombre
    )

    ruta_vocales = carpeta_demucs / "vocals.wav"
    ruta_instrumental = carpeta_demucs / "no_vocals.wav"

    if not ruta_vocales.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de voz: {ruta_vocales}"
        )

    if not ruta_instrumental.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo instrumental: {ruta_instrumental}"
        )

    print("\nSeparación completada.")
    print(f"Voz:          {ruta_vocales}")
    print(f"Instrumental: {ruta_instrumental}")

    return ruta_vocales, ruta_instrumental