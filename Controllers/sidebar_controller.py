from typing import Dict, Any
import streamlit as st
import Utils.ui_components as ui_comp


class ControladorBarraLateral:
    """Clase que gestiona todos los componentes de la barra lateral"""

    def __init__(self, config_lv: Dict[str, Any]):
        """
        Args:
            config_lv (Dict): Configuración cargada desde el archivo de configuración
        """
        self.config_lv = config_lv

    def _renderizar_seccion_descuentos(self) -> str:
        """Renderiza los componentes para selección de rango de descuentos

        Returns:
            str: Rango de descuento seleccionado
        """
        st.sidebar.divider()

        # Cargar plantillas si no están en sesión
        if "formatos_cartas" not in st.session_state:
            from docx import Document
            dict_cartas = {
                cada_archivo: Document(f"Controllers/{cada_archivo}")
                for cada_archivo in self.config_lv["list_formatos_cartas"]
            }
            ui_comp.set_key_ss_st("formatos_cartas", dict_cartas)

        # Cargar archivo maestra
        cnfg_fileUp_maestra = self.config_lv["seccion_archivo"]["file_uploader_maestra"]
        gestor_maestra_per = ui_comp.FileUploaderManager(
            clave=cnfg_fileUp_maestra["clave"],
            titulo=cnfg_fileUp_maestra["titulo"],
            uploader_msg=cnfg_fileUp_maestra["uploader_msg"],
            limit_msg=cnfg_fileUp_maestra["limit_msg"],
            button_msg=cnfg_fileUp_maestra["button_msg"],
            tipo_archivos=cnfg_fileUp_maestra["tipo_archivos"],
            icon=cnfg_fileUp_maestra["icon"],
            usar_sidebar=True,
        )
        maestra_personal = gestor_maestra_per.leer_archivos()
        
        ui_comp.set_key_ss_st("maestra_personal", maestra_personal)

        # Obtener maestra de personal.
        
        # FORMATO DE CARTA (Selección temporal + confirmación)
        st.sidebar.markdown("### Formato de carta", unsafe_allow_html=True)

        formato_temp = ui_comp.SelectBoxManager(
            clave="select_box_format_temp",
            etiqueta="Seleccione el formato de carta deseado",
            opciones=self.config_lv["list_formatos_cartas"],
            placeholder="Seleccione...",
            usar_sidebar=True,
        )

        btn_confirmar_formato = ui_comp.ButtonTracker(
            clave="btn_confirmar_formato",
            etiqueta="Confirmar formato",
            usar_sidebar=True,
        )

        if btn_confirmar_formato.fue_presionado():
            ui_comp.set_key_ss_st("formato_seleccionado", formato_temp.get_value())
            btn_confirmar_formato.reiniciar()
            st.sidebar.success("✅ Formato confirmado")

        # Procesar ingreso de campos solo si hay formato confirmado
        dict_formatos = self.config_lv["config_formatos"]
        formato = st.session_state.get("formato_seleccionado")

        if formato:
            campos = list(dict_formatos[formato]["campos_digitar"].items())

            indice = st.session_state["indice_campo"]

            if indice < len(campos):
                cada_campo, cada_text = campos[indice]
                clave_input = f"input_campo_{cada_campo}"
                clave_boton = f"boton_guardar_{cada_campo}"

                st.sidebar.markdown("### Digite el valor indicado:", unsafe_allow_html=True)
                input_campos = ui_comp.TextInputManager(
                    clave=clave_input,
                    etiqueta=cada_text,
                    valor_por_defecto="",
                    usar_sidebar=True,
                    tipo=str,
                )

                boton_guardar = ui_comp.ButtonTracker(
                    clave=clave_boton,
                    etiqueta=f"Guardar {cada_campo}",
                    usar_sidebar=True,
                )

                if boton_guardar.fue_presionado():
                    valor_guardado = input_campos.get_value()
                    st.session_state["campos_guardados"][cada_campo] = valor_guardado

                    # Eliminar input del estado
                    if clave_input in st.session_state:
                        del st.session_state[clave_input]

                    boton_guardar.reiniciar()
                    st.session_state["indice_campo"] += 1
                    st.rerun()
                
            else:
                st.sidebar.success("¡Todos los campos fueron ingresados!")
                st.session_state["colaborador_habilitado"] = True

    def ejecutar_proceso_lv(self):
        """Ejecuta el proceso secuencial para la construcción de la barra lateral"""
        self._renderizar_seccion_descuentos()
        