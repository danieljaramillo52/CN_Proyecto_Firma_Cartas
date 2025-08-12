# Controllers/buscador_campos.py
import locale 
import streamlit as st
from pandas import to_datetime
from Utils.utils import concatenar_columnas_pd
from Utils.ui_components import SelectBoxManager, ButtonTracker

class BuscadorColaboradorPorCedula:
    def __init__(self, df_maestra, config_lv, dict_cols):
        self.df_maestra = df_maestra
        self.config_lv = config_lv
        self.dict_cols = dict_cols

        # Widgets (se crean más adelante)
        self.input_cedula = None
        self.btn_agregar_colab_lv = None

    # ------------------ Paso a paso (misma lógica) ------------------ #
    def _validar_df(self) -> bool:
        return self.df_maestra is not None and not self.df_maestra.empty

    def _mostrar_titulo(self) -> None:
        st.markdown("## Documento del trabajador.")

    def _crear_campos_concatenados(self) -> None:
        # NOMBRE COMPLETO EMPLEADO
        self.df_maestra = concatenar_columnas_pd(
            dataframe=self.df_maestra,
            cols_elegidas=[
                self.dict_cols["NOMBRE"],
                self.dict_cols["PRIMER_APELLIDO"],
                self.dict_cols["SEGUNDO_APELLIDO"],
            ],
            nueva_columna=self.dict_cols["NOMBRE_COMPLETO_EMPLEADO"],
            omitir_vacios=True,
            sep=" ",
        )

        # NOMBRE EMPLEADO
        self.df_maestra = concatenar_columnas_pd(
            dataframe=self.df_maestra,
            cols_elegidas=[
                self.dict_cols["NOMBRE"],
                self.dict_cols["PRIMER_APELLIDO"],
            ],
            nueva_columna=self.dict_cols["NOMBRE_EMPLEADO"],
            omitir_vacios=True,
            sep=" ",
        )

        # CONCATENADA
        self.df_maestra = concatenar_columnas_pd(
            dataframe=self.df_maestra,
            cols_elegidas=[
                self.dict_cols["CEDULA"],
                self.dict_cols["NOMBRE_EMPLEADO"],
            ],
            nueva_columna=self.dict_cols["CONCATENADA"],
            omitir_vacios=True,
            sep="_",
        )

    def _configurar_locale_fecha(self) -> None:
        """Configura el idioma para la regíon actual."""
        locale.setlocale(locale.LC_TIME, "Spanish_Spain")

    def _parsear_fechas(self) -> None:
        """Transforma los formatos de fecha a Object(type: datetime)
        Permite modifcar su formato y extraer componentes necesarios. 
        
        Actualiza resultados sobre la misma columna del Dataframe (df_maestra)
        Manejo de errores
        """
        self.df_maestra[self.dict_cols["FECHA_ANTIGUEDAD"]] = to_datetime(
            self.df_maestra[self.dict_cols["FECHA_ANTIGUEDAD"]],
            errors="coerce",
            dayfirst=True,
            format="mixed",
        )

        self.df_maestra[self.dict_cols["FECHA_INGRESO_CIA"]] = to_datetime(
            self.df_maestra[self.dict_cols["FECHA_INGRESO_CIA"]],
            errors="coerce",
            dayfirst=True,
            format="mixed",
        )

    def _crear_widgets(self) -> None:
        self.input_cedula = SelectBoxManager(
            clave="text_input_cedula",
            etiqueta="Ingrese la cédula del trabajador",
            opciones=self.df_maestra[self.dict_cols["CONCATENADA"]].to_list(),
            placeholder="Seleccione una cédula...",
            usar_sidebar=False,
        )

        cnfg_btn = self.config_lv["seccion_buscar_colab"]["btn_agregar_colab"]
        self.btn_agregar_colab_lv = ButtonTracker(
            clave=cnfg_btn["clave"],
            etiqueta=cnfg_btn["etiqueta"],
            usar_sidebar=False,
        )

    def _procesar_click(self) -> None:
        if self.btn_agregar_colab_lv.fue_presionado() and self.input_cedula.is_valid():
            id_colaborador = self.input_cedula.get_value()

            
            fila = self.df_maestra[self.df_maestra[self.dict_cols["CONCATENADA"]].astype(str) == str(id_colaborador)]

            if not fila.empty:
                formato = st.session_state.get("formato_seleccionado")
                campos_buscar = self.config_lv["config_formatos"][formato]["campos_buscar"]

                # Mantener la misma condición (scalar year sobre la fila seleccionada)
                if fila.iloc[0][self.dict_cols["FECHA_ANTIGUEDAD"]].year < 2010:
                    fila.loc[:,self.dict_cols["FECHA_ANTIGUEDAD_FORMATEADA"]] = \
                        fila[self.dict_cols["FECHA_ANTIGUEDAD"]].dt.strftime("%d de %B de %Y")
                else:
                    fila.loc[:,self.dict_cols["FECHA_ANTIGUEDAD_FORMATEADA"]] = \
                        self.df_maestra[self.dict_cols["FECHA_INGRESO_CIA"]].dt.strftime("%d de %B de %Y")

                for clave_destino, columna_df in campos_buscar.items():
                    valor = fila.iloc[0][columna_df]
                    st.session_state["campos_guardados"][clave_destino] = valor

                st.success("✅ Información del colaborador agregada exitosamente")
                st.session_state["proceso_documento_habilitado"] = True
            else:
                st.warning("⚠️ No se encontró ningún colaborador con esa cédula")

            self.btn_agregar_colab_lv.reiniciar()

    # Método orquestador
    def ejecutar(self) -> None:
        if self._validar_df():
            if st.session_state["colaborador_habilitado"]:
                self._mostrar_titulo()
                self._crear_campos_concatenados()
                self._configurar_locale_fecha()
                self._parsear_fechas()
                self._crear_widgets()
                self._procesar_click()
        else:
            if self.df_maestra is not None and self.df_maestra.empty:
                st.info("🔄 Cargue primero el archivo de maestra personal para buscar una cédula.")

def buscar_y_agregar_colaborador_por_cedula(df_maestra, config_lv, dict_cols):
    BuscadorColaboradorPorCedula(df_maestra, config_lv, dict_cols).ejecutar()
