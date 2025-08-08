# Controllers/procesador_formatos.py
import streamlit as st
import re
from docx import Document
from typing import Dict
from Utils.ui_components import ButtonTracker


class ProcesadorFormatosWord:
    @classmethod
    def _replace_in_paragraphs(cls, doc: Document, reemplazos: Dict[str, str]) -> None:
        for p in doc.paragraphs:
            texto_original = "".join(run.text for run in p.runs)
            texto_modificado = texto_original
            for clave, nuevo in reemplazos.items():
                if clave in texto_modificado:
                    texto_modificado = texto_modificado.replace(clave, nuevo)

            if texto_modificado != texto_original:
                estilo_base = p.runs[0].style if p.runs else None
                fuente_base = p.runs[0].font if p.runs else None
                for run in p.runs:
                    run.clear()
                nuevo_run = p.add_run(texto_modificado)
                if estilo_base:
                    nuevo_run.style = estilo_base
                if fuente_base:
                    nuevo_run.font.name = fuente_base.name
                    nuevo_run.font.size = fuente_base.size
                    nuevo_run.font.italic = fuente_base.italic

    @classmethod
    def _replace_in_tables(cls, doc: Document, reemplazos: Dict[str, str]) -> None:
        if not doc.tables:
            return

        # 1) Tomar valores del dict (acepta "$Salario variable" o "$Salario variable.")
        basico_raw = reemplazos.get("Salario Básico.", 0)
        variable_raw = reemplazos.get("Salario Variable.", 0)

        # 2) Parseo mínimo (quita símbolos y separadores); sin helpers, sin drama
        to_num = lambda s: float(re.sub(r"[^\d]", "", str(s)) or 0)
        basico = to_num(basico_raw)
        variable = to_num(variable_raw)
        total = basico + variable

        p_bas = 0 if total == 0 else basico / total
        p_var = 0 if total == 0 else variable / total

        cop = lambda n: "$ " + f"{int(round(n)):,}".replace(",", ".")
        pct = lambda x: f"{round(x*100)}%"

        datos = [
            (cop(basico), pct(p_bas)),  # fila 1: Básico
            (cop(variable), pct(p_var)),  # fila 2: Variable
            (cop(total), "100%"),  # fila 3: Total
        ]

        tabla = doc.tables[0]  # si no es la primera, cambia el índice
        for i, (valor, porcentaje) in enumerate(datos, start=1):  # fila 0 = encabezado
            if len(tabla.columns) > 1:
                tabla.cell(i, 1).text = valor
            if len(tabla.columns) > 2:
                tabla.cell(i, 2).text = porcentaje

    def procesar(
        self, nombre_formato: str, reemplazos: Dict[str, str], contiene_tablas: str
    ) -> Document:

        formatos_mem = st.session_state.get("formatos_cartas", {})
        if nombre_formato not in formatos_mem:
            raise ValueError(f"Formato '{nombre_formato}' no está cargado en memoria.")

        # Crear una copia para no modificar el original
        from io import BytesIO

        buffer = BytesIO()
        formatos_mem[nombre_formato].save(buffer)
        buffer.seek(0)
        doc_copia = Document(buffer)

        self._replace_in_paragraphs(doc_copia, reemplazos)

        if contiene_tablas.lower() == "sí":
            self._replace_in_tables(doc_copia, reemplazos)

        return doc_copia
