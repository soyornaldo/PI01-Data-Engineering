# PI01-Data-Engineering

Proyecto para limpiar y transformar datos y publicarlos en una API publica.

## Que nos dan:
 - Cuatro ficheros csv 
   amazon_prime_titles.csv
   disney_plus_titles-score.csv
   hulu_titles-score (2).csv
   netflix_titles-score.csv
   
## Con que voy a trabajar para lograr el objetivo.
  ### Herramientas
  - jupyter lab
  - Visual Studio Code
  - mito
  - docker
  ### Plataforma de programacion
  - Python
  - Pandas
  - Flask
  - Los datos los deje en csv
   
# Limpieza de datos
 - Generar campo **`id`**: Cada id se compondrá de la primera letra del nombre de la plataforma, seguido del show_id ya presente en los datasets (ejemplo para    títulos de Amazon = **`as123`**)

 - Los valores nulos del campo rating deberán reemplazarse por el string “**`G`**” (corresponde al maturity rating: “general for all audiences”

 - De haber fechas, deberán tener el formato **`AAAA-mm-dd`**

 - Los campos de texto deberán estar en **minúsculas**, sin excepciones

 - El campo ***duration*** debe convertirse en dos campos: **`duration_int`** y **`duration_type`**. El primero será un integer y el segundo un string        
   indicando la unidad de medición de duración: min (minutos) o season (temporadas)
   
   
   ## Fichero Ingenieria_Datos.jpyn  
   Aca voy a realizar lo que me piden y como resultado salvare toda la informacion en un fichero unico (data_origen.csv) que va a contener la informacion de los
   cuatro ficheros originales, gracias a que los cuatro comparten la misma estructura. El fichero lo voy a salvar en la carpeta API Server que es donde
   voy a desarrollar la api que me piden.
   
 
 # Desarrollo de la API
   El codigo esta ubicado en la carpeta API Server y tiene que responder a estas preguntas:
   - Cantidad de veces que aparece una keyword en el título de peliculas/series, por plataforma 
     ej de uso: 
       http://ornaldo.pythonanywhere/keyword/netflix/love  (ocurrencia de la palabra 'love' en la plataforma 'netflix')
       http://ornaldo.pythonanywhere/keyword/love          (ocurrencia de la palabra 'love' en todas las plataformas)
     

   - Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año
     ej de uso:
       http://ornaldo.pythonanywhere/score/90               (cantidad de peliculas por plataforma con puntaje superior a 90)
       http://ornaldo.pythonanywhere/score/90/amazon        (cantidad de peliculas de la plataforma amazon con puntaje superior a 90)
       http://ornaldo.pythonanywhere/score/90/2021          (cantidad de peliculas por plataforma con puntaje superior a 90 del año 2021)
       http://ornaldo.pythonanywhere/score/90/2020/netflix  (cantidad de peliculas de la plataforma netflix con puntaje superior a 90 del año 2020)

   - La segunda película con mayor score para una plataforma determinada, según el orden alfabético de los títulos.
     ej de uso:
       http://ornaldo.pythonanywhere/second_score/hulu  (segunda pelicula con mayor score segun orden alfabetico del titulo de la plataforma hulu)

   - Película que más duró según año, plataforma y tipo de duración
     ej de uso:
       http://ornaldo.pythonanywhere/mayor_duracion/min  (pelicula que mas duro en cada una de las plataformas en cada año)
       http://ornaldo.pythonanywhere/mayor_duracion/amazon/season  (serie que mas duro en amazon en cada año)
       http://ornaldo.pythonanywhere/mayor_duracion/hulu/min/2020  (pelicula que mas duro en hulo en el año 2020)

   - Cantidad de series y películas por rating
     ej de uso:
       http://ornaldo.pythonanywhere/rating     (cantidad de series y peliculas para cada rating)
       http://ornaldo.pythonanywhere/rating/18+ (cantidad de series y peliculas para cada el rating = 18+)
   
   ## Fichero Ingenieria_Datos_II.jpyn
   Aqui parto de data_origen.csv y primero sigo haciendo algo de limpieza, despues de salvar los cambios a data.csv para desarrollar la API.
   Aca adentro usando 'mito' hago pruebas al DataFrame que me ayudan en la confección de la API.
   Es decir en la confección de la API uso al unísono este fichero mientras programo en app.py, acá hago pruebas visuales a los datos usando 'mito' este
   me genera codigo python
   
   
   En la carpeta API Server esta el fichero app.py 
 
 
 # Uso de docker para publicar la API
 Dento de la carpeta API Server tengo creado el fichero dockerfile donde incluyo lo necesario para generar la imagen con lo necesario para ejecutar la API.
 
 FROM python:3.10
 EXPOSE 5000
 WORKDIR /app
 RUN pip install flask
 RUN pip install pandas
 RUN pip install numpy 
 COPY . .
 CMD ["flask","run","--host","0.0.0.0"]
 
 
 # Publicacion de la aplicacion
 Encontre muy poca informacion de como publicar el docker, las variantes que encontre eran de pago. El docker lo probé localmente y trabaja bien. 
 La solución encontrada fue publicar la API en www.pythonanywhere.com, abrí una cuenta y creé una Web app con el subdominio
 www.ornaldo.pythonanywhere.com en esa dirección se puede probar la API. Para lograrlo subí el contenido de app.py y lo puse dentro de flask_app.py mas 
 el fichero data.csv, 
 Solo fué necesario unas pequeñas transformaciones del código para poder ejecutarlo. Así que el código fuente que esta en la carpeta API Server
 en el repositorio responde al código que yo pruebo en mi máquina, después lo subo y lo transformo:
   - localhost:5001 por ornaldo.pythonanywhere 
   - la carga de 'data.csv' que en mi caso es local en la web tengo que usar '/home/ornaldo/mysite/data.csv')
 que es la carpeta donde está alojado el fichero en el servidor.
 
 # Video explicativo de todo el trabajo realizado
 https://youtu.be/xG6_kAAR79Y