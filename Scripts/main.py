# main.py
import config_path_routes
import pandas as pd
import streamlit as st
import Utils.utils as utils

from Controllers.sidebar_controller import ControladorBarraLateral
from Controllers.buscar_campos import buscar_y_agregar_colaborador_por_cedula
from Controllers.config_loader import ConfigLoader, ConfigClaves
from Controllers.procesador_formatos import ProcesadorFormatosWord
from Utils.ui_components import (
    add_key_ss_st,
    clean_key_ss_st,
)


class Aplicacion:
    """Clase principal que controla el flujo de la aplicación"""

    def __init__(self) -> None:
        self.config_loader = ConfigLoader()
        self.get_config = self.config_loader.get_config
        self.claves = ConfigClaves(self.config_loader)

        # Controlador de la barra lateral
        self.barra_lateral = ControladorBarraLateral(
            config_lv=self.get_config("config_lateral_var")
        )

    def ejecutar(self) -> None:
        """Controla todo el ciclo de ejecución de la aplicación"""
        self._inicializar_session()

        # Procesar barra lateral
        self.barra_lateral.ejecutar_proceso_lv()

        # Buscar colaborador por cédula
        df_maestra = st.session_state.get("maestra_personal", pd.DataFrame())
    
        buscar_y_agregar_colaborador_por_cedula(
            df_maestra, self.get_config("config_lateral_var"), self.get_config("dict_cols")
            )

        # Botón para procesar el formato seleccionado
        if st.session_state["proceso_documento_habilitado"]:
            if st.button("Procesar Formato", type="primary"):
                self._procesar_formato()

        # Botón para iniciar nueva incidencia
        if st.session_state["nueva_incidencia"]:
            if st.button("Agregar nueva incidencia"):
                self._reiniciar_estado()

    def _procesar_formato(self):
        """Genera el documento Word con los reemplazos definidos"""
        formato = st.session_state.get("formato_seleccionado")
        reemplazos = st.session_state.get("campos_guardados", {})

        if not formato:
            st.warning("Selecciona y confirma un formato primero.")
            return

        config_formato = self.get_config(
            "config_lateral_var", "config_formatos").get(formato, {})
        
        contiene_tablas = config_formato.get("contiene_tablas", "No")

        proc = ProcesadorFormatosWord()
        doc = proc.procesar(
            nombre_formato=formato,
            reemplazos=reemplazos,
            contiene_tablas=contiene_tablas,
        )

        # Guardar en sesión para posible descarga o vista previa
        st.session_state["documento_generado"] = doc 
        
        doc.save(f"Resultados\\{st.session_state['text_input_cedula']}_{formato}")

        st.success("📄 Formato procesado con éxito.")
        
        st.session_state["nueva_incidencia"] = True

    def _reiniciar_estado(self):
        """Limpia variables en session_state excepto las necesarias"""
        claves_preservar = set(
            self.get_config("cnf_session_keys",
                            "claves_preservar", por_defecto=[])
        )
        claves_a_eliminar = [
            clave
            for clave in st.session_state.keys()
            if clave not in claves_preservar
        ]
        clean_key_ss_st(keys=claves_a_eliminar)
        st.success("Estado reiniciado para nueva incidencia.")
        st.rerun()

    def _inicializar_session(self) -> None:
        """Inicializa claves necesarias en session_state"""
        for clave, opciones in self.get_config(
            "cnf_session_keys", "inicializacion", por_defecto={}
        ).items():
            add_key_ss_st(clave, opciones["valor_inicial"])


if __name__ == "__main__":
    utils.setup_ui()
    app = Aplicacion()
    app.ejecutar()
