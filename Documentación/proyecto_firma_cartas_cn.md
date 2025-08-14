# Resumen del Proyecto "PROYECTO_CARTAS"

Este proyecto automatiza la generación de cartas y documentos formales a partir de **formatos predeterminados**.  
La aplicación cuenta con una **interfaz que corre localmente** y permite diligenciar automáticamente las plantillas con información proveniente de una **maestra de personal**.

---

## Funcionamiento general

1. **Selección de formato**  
   El usuario elige uno de los formatos de carta disponibles dentro del sistema.
   Disponibles en ``📁Insumos/formatos_cartas`` Los formatos base se encuentran adaptados. Según las plantillas suministradas inicialmente por CN. Los formatos actuales deben respetar la estructura definida.

2. **Carga de datos**  
   La información se toma de la **maestra de personal**, ubicada en: ``📁Insumos/maestra_personal/Maestra de personal.xlsx``

- Este archivo debe tener su **estructura de columnas en la primera fila**.
- La información de la maestra se **actualiza mes a mes**, reemplazando el contenido existente 2da fila en adelante. 

3. **Generación automática**  
El sistema reemplaza los marcadores de las plantillas con los datos correspondientes, generando así un documento listo para uso.

4. **Resultados**  
Los documentos generados se almacenan en la carpeta: 📁Resultados


---

## Responsables

### Proveedor - XpertGroup  
- Daniel Jaramillo Bustamante - daniel.jaramillo@xpertgroup.co

### Receptor - Comercial Nutresa  
- **Área TI:**
  - Sebastián Caro Aguirre - scaro@comercialnutresa.com.co