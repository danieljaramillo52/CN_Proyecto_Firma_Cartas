# Controllers/buscador_campos.py
import streamlit as st
from Utils.utils import concatenar_columnas_pd
from Utils.ui_components import SelectBoxManager, ButtonTracker

def buscar_y_agregar_colaborador_por_cedula(df_maestra, config_lv):
    
        if df_maestra is not None and not df_maestra.empty:
        
            if st.session_state["colaborador_habilitado"]:
                
                st.markdown("## Documento del trabajador.")
                
                # Crear campos: 
                df_maestra = concatenar_columnas_pd(dataframe=df_maestra, cols_elegidas=["NOMBRE", "PRIMER APELLIDO", "SEGUNDO APELLIDO"], nueva_columna = "NOMBRE COMPLETO EMPLEADO", omitir_vacios=True, sep=" ")
                
                df_maestra = concatenar_columnas_pd(dataframe=df_maestra, cols_elegidas=["NOMBRE", "PRIMER APELLIDO"], nueva_columna= "NOMBRE EMPLEADO",omitir_vacios=True, sep=" ")
                
                df_maestra = concatenar_columnas_pd(dataframe=df_maestra, cols_elegidas=["CEDULA", "NOMBRE EMPLEADO"],nueva_columna="Concatenada", omitir_vacios=True, sep="_")
                
                input_cedula = SelectBoxManager(
                    clave="text_input_cedula",
                    etiqueta="Ingrese la cédula del trabajador",
                    opciones=df_maestra["Concatenada"].to_list(),
                    placeholder="Seleccione una cédula...",
                    usar_sidebar=False,
                )
                
                cnfg_btn_agregar_colab_lv = config_lv["seccion_buscar_colab"]["btn_agregar_colab"]
                btn_agregar_colab_lv = ButtonTracker(
                    clave=cnfg_btn_agregar_colab_lv["clave"],
                    etiqueta=cnfg_btn_agregar_colab_lv["etiqueta"],
                    usar_sidebar=False,
                )

                if btn_agregar_colab_lv.fue_presionado() and input_cedula.is_valid():
                    id_colaborador = input_cedula.get_value()
                    
                    fila = df_maestra[df_maestra["Concatenada"].astype(str) == str(id_colaborador)]

                    if not fila.empty:
                        formato = st.session_state.get("formato_seleccionado")
                        campos_buscar = config_lv["config_formatos"][formato]["campos_buscar"]

                        for clave_destino, columna_df in campos_buscar.items():
                            valor = fila.iloc[0][columna_df]
                            st.session_state["campos_guardados"][clave_destino] = valor

                        st.success("✅ Información del colaborador agregada exitosamente")
                        st.session_state["proceso_documento_habilitado"] = True
                    else:
                        st.warning("⚠️ No se encontró ningún colaborador con esa cédula")
                    btn_agregar_colab_lv.reiniciar()
                
        else:
            if df_maestra.empty:
                st.info("🔄 Cargue primero el archivo de maestra personal para buscar una cédula.")
    