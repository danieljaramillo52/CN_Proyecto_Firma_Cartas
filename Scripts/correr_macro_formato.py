from pathlib import Path
import win32com.client as win32

# correr la macro que corrige los formatos. 
def ejecutar_macro_en_word(ruta_relativa: str = "Resultados\\", nombre_macro : str = "Normal.ThisDocument.ResaltarPalabrasEnNegrita", incluir_subcarpetas: bool = False) -> dict:
    """
    Ejecuta una macro de Word sobre todos los .docx de una carpeta.

    Parámetros:
        ruta_relativa : Ruta relativa a la carpeta con .docx (respecto a cwd del proceso).
        nombre_macro : Nombre completo de la macro, p.ej. "Normal.ResaltarPalabrasEnNegrita" o "Normal.Module1.ResaltarPalabrasEnNegrita".
        incluir_subcarpetas: Si True, procesa también subcarpetas.

    Retorna:
        dict con {'procesados': int, 'fallidos': [(ruta, error), ...]}
    """
    carpeta = (Path.cwd() / ruta_relativa).resolve()
    if not carpeta.exists():
        raise FileNotFoundError(f"No existe la carpeta: {carpeta}")

    patron = "**/*.docx" if incluir_subcarpetas else "*.docx"
    archivos = list(carpeta.glob(patron))

    word = win32.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0  # wdAlertsNone

    procesados = 0
    fallidos = []

    try:
        for f in archivos:
            try:
                doc = word.Documents.Open(str(f))
                # ejecuta la macro sobre el documento activo
                word.Run(nombre_macro)
                doc.Close(SaveChanges=True)
                procesados += 1
            except Exception as e:
                try:
                    # intenta cerrar si quedó abierto
                    doc.Close(SaveChanges=False)
                except Exception:
                    pass
                fallidos.append((str(f), str(e)))
    finally:
        word.Quit()

    return {"procesados": procesados, "fallidos": fallidos}

res = ejecutar_macro_en_word()