"# Proyect_7_Bootcamp_UDD"

# Descripcion:

El proyecto consiste en la creación de un modelo de machine learning de regresión, el cual toma los valores historicos de los raitings (en columna "Rating") de diferentes apps presentes en un dataset de Google Play Store para ser entrenado con el objetivo de predecir los raiting de nuevas aplicaciones ingresando las carcteristicas indicadas más abajo de la aplicación que se desea consultar.git

# Instalación

1ro Clonar Repositorio: Ir al repositorio, apretar el botón verde que dice CODE y en HTTPS copiar el link que aparece. Luego escribir el siguiente comando en tu máquina local:

git clone https://github.com/gcruzbull/Proyect_7_Bootcamp_UDD.git

2do Crear un entorno virtual nuevo con Conda:

conda create -n mi_entorno python=3.10.14

Activar el entorno local:

conda activate mi_entorno

En caso de querer desactivar el entorno y volver al entorno base escribir:

conda deactivate

3ro Con el entorno activo instalar las diferentes librerias indicadas en requirements.txt de la siguiente manera:

pip install -r requirements.txt

4to Descargar los archivos presentes en la carpeta Modelo. Asegurate que todo este dentro de la misma carpeta.

5to Con Visual Studio Code abrir la carpeta y hacer lo siguiente:

Primero correr el codigo de el archivo training_data.py (la clase que guarda el modelo entrenado)

Segundo ejecutar el archivo api.py

6to Abrir Postman

- Usar el puerto (http://127.0.0.1:8000)
- Usar el endpoint /predict
- Usar el metodo POST
- Ingresar las diferentes variables en el orden indicado y sus correspondientes valores según lo indicado abajo para realizar la consulta.
- Las variables deben contar con los siguientes requisitos y orden:

    1ro Reviews: Ingresar valores numericos

    2do Size: Ingresar valores numericos

    3ro Installs: Ingresar valores numericos

    4to Type: Ingresar strings ("Free" o "Paid")

    5to Content Rating: Ingresar string. Opciones son: "Everyone", "Teen", "Everyone 10+" , "Mature 17+", "Adults only 17+", "Unrated"

    6to Genres: Ingresar string.

    7mo Last Updated: Ingresar string. 

    8vo Current Ver: Ingresar string.

    9no Android Ver: Ingresar string.

7mo Apretar el botón SEND en Postman para que entregue la predicción.