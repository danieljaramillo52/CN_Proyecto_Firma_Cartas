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

        # Configuración y boton para agregar un nuevo colaborador.

        cnfg_btn_agregar_colab_lv = self.config_lv["seccion_buscar_colab"][
            "btn_agregar_colab"
        ]

        btn_agregar_colab_lv = ui_comp.ButtonTracker(
            clave=cnfg_btn_agregar_colab_lv["clave"],
            etiqueta=cnfg_btn_agregar_colab_lv["etiqueta"],
            usar_sidebar=False,
        )
        cnfg_btn_agregar_colab_lv = self.config_lv["seccion_buscar_colab"][
            "btn_agregar_colab"
        ]
        from docx import Document

        if "formatos_cartas" not in st.session_state.keys():
            dict_cartas = {
                cada_archivo: Document(cada_archivo)
                for cada_archivo in [
                    "Controllers/F Carta De Nivelación Salarial - Salario Variable.docx",
                    "Controllers/F Carta De Nivelacion Salarial - Salario Integral.docx",
                ]
            }
            ui_comp.set_key_ss_st(clave="formatos_cartas", valor=dict_cartas)

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

        ui_comp.set_key_ss_st(clave="maestra_personal", valor=maestra_personal)

        # Crear lista de cedulas.
        df_maestra = st.session_state.get("maestra_personal")
        list_cedulas = df_maestra["CEDULA"].tolist()

        # Selecionar formato.
        ui_comp.SelectBoxManager(
            clave="select_box_colab",
            etiqueta="Seleecione Cedula/Código del trabajador",
            opciones=list_cedulas,
            placeholder="Seleccione Cedula/Código del trabajador",
            usar_sidebar=False,
        )

        formato_seleccionado = ui_comp.SelectBoxManager(
            clave="select_box_format",
            etiqueta="Seleecione Cedula/Código del trabajador",
            opciones=self.config_lv["list_formatos_cartas"],
            placeholder="Formato de carta",
        )
        ui_comp.set_key_ss_st(clave="formato_seleccionado", valor= formato_seleccionado.get_value())
        
        # Según el formato lanzar los campos a dígitar. 
        dict_formatos = self.config_lv["config_formatos"]
        
        if btn_agregar_colab_lv.fue_presionado():
            
            formato =  st.session_state.get("formato_seleccionado")
            
            for cada_campo, cada_text in dict_formatos[formato]["campos_digitar"].items():
                
                # Crear un selecbox dinamico según la necesidad.
                input_campos = ui_comp.TextInputManager(
                    clave=f"input_campo_{cada_campo}",
                    etiqueta=cada_text,
                    valor_por_defecto="",
                    usar_sidebar=True,
                    tipo=str,
                )
                valor_guardado = input_campos.get_value()
                input_campos.reset()
                
                print("Hola")
            

        # selector_colaborador = ui_comp.SelectBoxManager(
        #    clave=cnfg_select_box_colab["clave"],
        #    etiqueta=cnfg_select_box_colab["etiqueta"],
        #    opciones=cnfg_select_box_colab["list_rng_dctos"],
        #    usar_sidebar=True,
        # )

        # selector_colaborador = ui_comp.SelectBoxManager(
        #    clave=cnfg_select_box_lv["clave"],
        #    etiqueta=cnfg_select_box_lv["etiqueta"],
        #    opciones=cnfg_select_box_lv["list_rng_dctos"],
        #    usar_sidebar=True,
        # )

        # cnfg_btn_confirmar_rng_lv = self.config_lv["seccion_rango_descuento"][
        #    "btn_confirmar_rng"
        # ]
        #
        # btn_confirmar = ui_comp.ButtonTracker(
        #    clave=cnfg_btn_confirmar_rng_lv["clave"],
        #    etiqueta=cnfg_btn_confirmar_rng_lv["etiqueta"],
        #    usar_sidebar=True,
        # )

        # if btn_confirmar.fue_presionado() and selector_rango.is_valid():
        #    ui_comp.set_key_ss_st("rango_act", selector_rango.get_value())
        #    btn_confirmar.reiniciar()
        #    st.sidebar.success("✅ Rango confirmado")

        return st.session_state.get("rango_act", "")

    def ejecutar_proceso_lv(self):
        """Ejecuta el proceso secuencial para la construcción de la barra lateral"""
        self._renderizar_seccion_descuentos()
