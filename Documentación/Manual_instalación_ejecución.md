# Instalación y despliegue. 
# 📁 Guía de instalación y configuración del proyecto

Esta guía explica cómo descargar, preparar y configurar el **PROYECTO_CARTAS**, incluyendo la instalación del macro de Word y la actualización de la información de la maestra de personal.

---

## 1️⃣ Descargar el proyecto como archivo `.zip`
1. Ingresa al repositorio en línea del proyecto. (Suministrado al momento de instalación. )

2. Haz clic en el botón **Code**.

![alt text](/Img/image.png)

3. Selecciona **Download ZIP**.

![alt text](/Img/image-1.png)
---

## 2️⃣ Descomprimir la carpeta del proyecto
1. Ubica el archivo `.zip` descargado.

![alt text](/Img/image-2.png)

![alt text](/Img/image-3.png)

2. Elegimos una carpeta para guardar el proyecto. Preferiblemente una ruta de facil acceso. Al mover la carpeta allí podemos continuar. 

2. Haz clic derecho en la carpeta descargada y le damos un click y en la parte superior presionamos el boton **Extraer todo**.

![alt text](/Img/image-7.png)

Click en **Extraer**

![alt text](/Img/image-5.png)

Así ya tenemos la carpeta del proyecto. 

![alt text](/Img/image-6.png)

---

## 3️⃣ Descomprimir el entorno virtual
El proyecto incluye un entorno virtual comprimido (`python-3.12.5-emb.zip`).

> ⚠ **Importante:** No extraigas este archivo directamente en la carpeta raíz, ya que el descompresor de Windows creará una subcarpeta adicional.

Pasos recomendados:
1. Abre el `.zip` del entorno virtual.

2. Copia la carpeta completa  📁python-3.12.5-emb

3. Pégalo directamente dentro de la carpeta raíz del proyecto (no dentro de una subcarpeta nueva) es decir pegalo en la carpeta anterior. 

![alt text](/Img/image-8.png)
---

Nos debe quedar de esta manera. 

![alt text](/Img/image-9.png)

Podemos ver que los archivos,  📁python-3.12.5-emb y 📁python-3.12.5-emb.zip,  ahora están en la carpeta principal del proyecto.


## 4️⃣ Configurar macro para la automatización. (OPCIONAL PERO RECOMENDADO)

1. Entrar al archivo  (block de notas) en : 📁Insumos/**Macro_Word.txt**

2. Abrimos el archivo, selecionamos y copiamos todo su contenido. 

![alt text](/Img/image-11.png)

3. Abrimos **microsoft word** creando un docmuento en blanco.

4. Una vez allí vamos a la barra superior presionado en **``Vista->Macros_Ver Macros``**

![alt text](/Img/image-14.png)

Se nos abrirá esta ventana. 

![alt text](/Img/image-10.png)

Podemos asignarle el nombre deseado en la parte superior y luego presionamos el boton **Crear**

- Se nos abrira una ventana como esta:

![alt text](/Img/image-13.png)

- En la parte superior izquierda iremos a **``Microsoft word Objetos``** y dando doble click veremos **``ThisDocument``** ó **``EsteDocumento``**.  Y aí hacemos doble Click.

![alt text](/Img/image-12.png)

Dentro de esta hoja pegaremos el contenido copiado del archivo **Macro.txt** , **recomendación:  (Utilizar Click derecho + Pegar)**. Guardamos los cambios.

Aohra podemos cerrar esta ventana y el documento de word. 

![alt text](/Img/image-15.png)



## 4️⃣ Actualizar información de la **maestra de personal**
La información que se usa para diligenciar los formatos está en:

📁Insumos/maestra_personal/Maestra de personal.xlsx

Se debe ingresar al archivo de manera mensual para actualizar la información de empleados. Solo es requerido eliminar la información existente y pegar la nueva. 


## ️5️⃣ Conifiguracion dinal de la automatización. 

1. En la carpeta principal del proyecto.  Damos doble click en el archivo **``iniciar.bat``**

![alt text](/Img/image-9.png)

Se abrirá la siguiente ventana:

![alt text](/Img/instalación_paquete.png)

Aquí a instalar los paquetes del proyecto y todo lo que necesita para funcionar. 

### **La ventana se cerrará sola una vez termine el proceso no se requiere intervención adicional, finalizado este proceso la automatización está lista para ser utilizada**


## Ejecución proyecto.

1 . Para la ejecución de la automatización basta con ir a la carpeta principal del proyecto. 

![alt text](/Img/image-9.png)

Posteriormente realizamos un doble click en el archivo **ejecutar.bat** que hace le desplieuge automático de la solución. 
