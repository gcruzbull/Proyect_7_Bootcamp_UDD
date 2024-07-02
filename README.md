"# Proyect_7_Bootcamp_UDD"

El proyecto consiste en la creación de un modelo de machine learning de regresión, el cual toma los valores historicos de los raitings (en columna "Rating") de diferentes apps presentes en un dataset de Google Play Store para ser entrenado con el objetivo de predecir los raiting de nuevas aplicaciones ingresando las carcteristicas indicadas más abajo de la aplicación que se desea consultar.git

¿Como usar el modelo?

Set Up
- Asegurate de tener instalado Python==3.10.14
- Instalar las librerias indicadas en "requierements.txt"
- Importar las librerias instaladas que se van a ocupar.

¿Como consultar el modelo?
Utilizando Postman seguir las siguientes instrucciones:
- Usar el puerto (http://127.0.0.1:8000)
- Usar el endpoint /predict
- Usar el metodo POST
- Ingresar las diferentes variables en el orden indicado y sus correspondientes valores para realizar la consulta.
- Las variables deben contar con los siguientes requisitos:

1ro Reviews: Ingresar valores numericos

2do Size: Ingresar valores numericos

3ro Installs: Ingresar valores numericos

4to Type: Ingresar strings ("Free" o "Paid")

5to Content Rating: Ingresar string. Opciones son: "Everyone", "Teen", "Everyone 10+" , "Mature 17+", "Adults only 17+", "Unrated"

6to Genres: Ingresar string.

7mo Last Updated: Ingresar string. 

8vo Current Ver: Ingresar string.

9no Android Ver: Ingresar string.
