import config_path_routes
from pandas import DataFrame
import streamlit as st
import Utils.utils as utils
from Controllers.sidebar_controller import ControladorBarraLateral
from Controllers.config_loader import ConfigLoader, ConfigClaves
from Utils.ui_components import (
    FileUploaderManager,
    ButtonTracker,
    add_key_ss_st,
    clean_key_ss_st,
    set_key_ss_st,
    set_multiple_keys,
)

class Aplicacion:
    """Clase principal que controla el flujo de la aplicación"""

    def __init__(self) -> None:
        """Inicializa las instancias necesarias para el funcionamiento de la aplicación."""
        self.config_loader = ConfigLoader()
        self.get_config = self.config_loader.get_config  # acceso simplificado
        self.claves = ConfigClaves(self.config_loader)
        
        # Controlador de la barra lateral
        self.barra_lateral = ControladorBarraLateral(
            config_lv=self.get_config("config_lateral_var")
        )
    
    def ejecutar(self) -> None:
        """
        Ejecuta el ciclo principal de la aplicación. Controla la lógica de:
        - Inicialización de estado
        - Procesamiento de barra lateral
        - Selección de Formatos
        - Edición y exportación de los formatos
        """
        # Inicializar variables en session_state si aún no existen
        self._inicializar_session()
        

        # Procesar selección de barra lateral
        self.barra_lateral.ejecutar_proceso_lv()
        
        print("Hola Mundo!")
        
    def _inicializar_session(self) -> None:
        """
        Inicializa las claves necesarias en el session_state según la configuración definida.
        """
        for clave, opciones in self.get_config("cnf_session_keys", "inicializacion", por_defecto={}).items():
            add_key_ss_st(clave, opciones["valor_inicial"])
        
          
            
if __name__=="__main__":
    utils.setup_ui()
    app = Aplicacion()
    app.ejecutar()