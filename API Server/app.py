#-------------------------------------------------------------------------------
# Name:        app.py
# Purpose:     Crear un http api server para devolver json con la información que
#              que responde a las solicitudes expuestas      
#
# Author:      Ornaldo Hernandez Ramos
# email:       ornaldohernandezramos@gmail.com
# GitHub:      soyornaldo          
#
# Created:     16/01/2023
#-------------------------------------------------------------------------------

from flask import Flask
import pandas as pd
import numpy as np

# flask run --port 5001

# docker build -t data-engineering-api .

data = pd.read_csv("data.csv")

app = Flask(__name__)

############################################################################################
# 1-Cantidad de veces que aparece una keyword en el título de peliculas/series, por plataforma
#############################################################################################
@app.route("/keyword")
@app.route("/keyword/")
def keyword_sin_titulo():
  return {"message":"Error, especifique el keyword a buscar"}

@app.route("/keyword/<string:name>")
def keyword_titulo(name):
    '''Cantidad de veces que aparece una keyword en el título de peliculas/series, por plataforma'''
    if name == "": 
      return {"message":"Error, parametros incorrectos"}, 404
    else:
      respuesta = {"keyword":name,
                   "plataformas":[] 
                  }
      for plat in ['a','n','h','d']:
        local_data = data[data['id'].str.startswith(plat, na=False)]
        local_data = local_data[local_data['title'].str.contains(name, na=False, regex=False)]

        match plat:
          case 'a':
            nombre = 'Amazon'
          case 'n':
            nombre = 'Netflix'
          case 'h':
            nombre = 'Hulu'
          case _:
            nombre = 'Disney'

        cant = local_data.shape[0]
        if cant > 0:
          respuesta['plataformas'].append({"nombre":nombre,"cantidad":cant})
        
      return respuesta


@app.route("/keyword/<string:plataforma>/<string:name>")
def keyword_plataforma_titulo(plataforma,name):
    '''Cantidad de veces que aparece una keyword en el título de peliculas/series, por plataforma'''
    if (plataforma != '') and (name != "") \
       and ((plataforma.lower() == 'disney') or (plataforma.lower() == 'hulu')\
       or (plataforma.lower() == 'amazon') or (plataforma.lower() == 'netflix')):

      respuesta = {"keyword":name,
                   "plataforma":plataforma 
                  }
      local_data = data[data['id'].str.startswith(plataforma[0].lower(), na=False)]
      local_data = local_data[local_data['title'].str.contains(name, na=False, regex=False)]

      cant = local_data.shape[0]
      if cant > 0:
        respuesta['cantidad'] = str(cant)
        
      return respuesta      
    else:
      return {"message":"Error, parametros incorrectos"}, 404
      



#############################################################################
# 2- Cantidad de películas/series por plataforma con un puntaje mayor a XX en determinado año     
#############################################################################
@app.route("/score")
@app.route("/score/")
def score():
  return {"message":"Error, especifique al menos el score"}


@app.route("/score/<int:score>")
def score_score(score):
    '''Cantidad de películas/series por plataforma con un puntaje mayor a score '''
    if int(score) == score:
      respuesta = {"score >":score,
                   "plataformas":[] 
                  }
      for plat in ['a','n','h','d']:
        local_data = data[data['id'].str.startswith(plat, na=False)]
        local_data = local_data[local_data['score'] > score]

        match plat:
          case 'a':
            nombre = 'Amazon'
          case 'n':
            nombre = 'Netflix'
          case 'h':
            nombre = 'Hulu'
          case _:
            nombre = 'Disney'

        cant = local_data.shape[0]
        if cant > 0:
          respuesta['plataformas'].append({"nombre":nombre,"cantidad":cant})    
      
      return respuesta
    else:
      return {"message":"Error, parametros incorrectos"}    


@app.route("/score/<int:score>/<string:plataforma>")
def score_plataforma(score,plataforma):
    '''Cantidad de peliculas/series de una plataforma determinada con puntajes superior a score'''
    if (plataforma != '') and (int(score) == score) \
       and ((plataforma.lower() == 'disney') or (plataforma.lower() == 'hulu')\
       or (plataforma.lower() == 'amazon') or (plataforma.lower() == 'netflix')):
      respuesta = {"plataforma":plataforma,
                   "score >": score
                  }
      local_data = data[data['id'].str.startswith(plataforma[0].lower(), na=False)]
      local_data = local_data[local_data['score'] > score]
      respuesta['cantidad'] = local_data.shape[0]
      
      return respuesta
    else:
      return {"message":"Error, parametros incorrectos"}  




@app.route("/score/<int:score>/<int:year>")
def score_score_year(score,year):
    '''Cantidad de peliculas/series de todas las plataformas del año 'year' con puntaje superior a 'score' '''
    if (int(year) == year) and (int(score) == score):
      respuesta = {"score >":score,
                   "año": year,
                   "plataformas":[] 
                  }
      for plat in ['a','n','h','d']:
        local_data = data[data['id'].str.startswith(plat, na=False)]
        local_data = local_data[local_data['release_year'] == year]
        local_data = local_data[local_data['score'] > score]

        match plat:
          case 'a':
            nombre = 'Amazon'
          case 'n':
            nombre = 'Netflix'
          case 'h':
            nombre = 'Hulu'
          case _:
            nombre = 'Disney'

        cant = local_data.shape[0]
        if cant > 0:
          respuesta['plataformas'].append({"nombre":nombre,"cantidad":cant})    
      
      return respuesta
    else:
      return {"message":"Error, parametros incorrectos"}  


@app.route("/score/<int:score>/<int:year>/<string:plataforma>")
def score_score_year_plataforma(score,year,plataforma):
    '''Cantidad de peliculas/series de una plataforma del año 'year' con puntaje superior a 'score' '''
    if (plataforma != '') and (int(score) == score) and (int(year) == year)\
       and ((plataforma.lower() == 'disney') or (plataforma.lower() == 'hulu')\
       or (plataforma.lower() == 'amazon') or (plataforma.lower() == 'netflix')):
      respuesta = {"plataforma":plataforma,
                   "score >": score,
                   "year": year
                  }
      local_data = data[data['id'].str.startswith(plataforma[0].lower(), na=False)]
      local_data = local_data[local_data['release_year'] == year]
      local_data = local_data[local_data['score'] > score]
      respuesta['cantidad'] = local_data.shape[0]
      
      return respuesta
    else:
      return {"message":"Error, parametros incorrectos"}       








#################################################################################################################
# 3- La segunda película con mayor score para una plataforma determinada, según el orden alfabético de los títulos.
##################################################################################################################
@app.route("/second_score")
@app.route("/second_score/")
def second_score():
  return {"message":"Error, parametros incorrectos"} 


@app.route("/second_score/<string:plataforma>")
def second_score_plataforma(plataforma):
  '''La segunda película con mayor score para una plataformas, según el orden alfabético de los títulos'''
  if (plataforma != '') and ((plataforma.lower() == 'disney') or (plataforma.lower() == 'hulu')\
    or (plataforma.lower() == 'amazon') or (plataforma.lower() == 'netflix')):
      #df = df[df['id'].str.startswith('a', na=False)]    
      local_data = data[data['id'].str.startswith(plataforma[0].lower(), na=False)]
      #df = df[df['score'] == df['score'].max()]
      local_data = local_data[local_data['score'] == local_data['score'].max()]
      if len(local_data) > 0:
        #df = df.sort_values(by='title', ascending=True, na_position='first')
        local_data = local_data.sort_values(by='title', ascending=True, na_position='first')
      
        score = local_data.iloc[1]['score']
        title = local_data.iloc[1]['title']

        respuesta = {"plataforma":plataforma,
                     "title": str(title),
                     "score": str(score)
                    }
        return respuesta
      else:  
        return {"message":"No existen datos para esa plataforma"}
  else:    
    return {"message":"Error, parametros incorrectos"}    




#############################################################################
# 4- Película o Serie que más duró según año, plataforma y tipo de duración
#############################################################################
@app.route("/mayor_duracion")
@app.route("/mayor_duracion/")
def mayor_duracion():
    return {"message":"Error, parametros incorrectos"}


@app.route("/mayor_duracion/<string:duration_type>")
def mayor_duracion_type(duration_type):
  '''Película que más duró según tipo de duración'''
  if (str(duration_type).lower() == 'season') or (str(duration_type).lower() == 'min'):
    respuesta = {"duration_type":duration_type
                }
    for plat in ['n','h','d','a']:
      local_data = data[data['id'].str.startswith(plat, na=False)]
      local_data = local_data[local_data['duration_type'] == duration_type]
      local_data = local_data.sort_values(by='release_year', ascending=True, na_position='first')
      lista_year = list(local_data['release_year'].unique())

      match plat:
        case 'a':
          nombre = 'Amazon'
        case 'n':
          nombre = 'Netflix'
        case 'h':
          nombre = 'Hulu'
        case _:
          nombre = 'Disney'
      respuesta[nombre] = []

      for anno in lista_year:
        local_data1 = local_data[local_data['release_year'] == anno]
        local_data1 = local_data1.sort_values(by='duration_int', ascending=False, na_position='last')
        respuesta[nombre].append({
                                         "año": str(anno),
                                         "nombre": local_data1.iloc[0]['title'],
                                         "duracion": str(local_data1.iloc[0]['duration_int'])
                                       })
    return respuesta                                   
  else:
    return {"message":"Error, parametros incorrectos"}  




@app.route("/mayor_duracion/<string:plataforma>/<string:duration_type>")
def mayor_duracion_plataforma_type(plataforma,duration_type):
  '''Película que más duró según plataforma y tipo de duración'''
  if (plataforma != '') and ((plataforma.lower() == 'disney') or (plataforma.lower() == 'hulu')\
    or (plataforma.lower() == 'amazon') or (plataforma.lower() == 'netflix')) and \
    ((str(duration_type).lower() == 'season') or (str(duration_type).lower() == 'min')):

    respuesta = {"duration_type":duration_type,
                 "plataforma": plataforma  
                }
    local_data = data[data['id'].str.startswith(plataforma[0].lower(), na=False)]
    local_data = local_data[local_data['duration_type'] == duration_type]
    local_data = local_data.sort_values(by='release_year', ascending=True, na_position='first')
    lista_year = list(local_data['release_year'].unique())

      
    respuesta['items'] = []
    for anno in lista_year:
      local_data1 = local_data[local_data['release_year'] == anno]
      local_data1 = local_data1.sort_values(by='duration_int', ascending=False, na_position='last')
      respuesta['items'].append({
                                  "año": str(anno),
                                  "nombre": local_data1.iloc[0]['title'],
                                  "duracion": str(local_data1.iloc[0]['duration_int'])
                                })
    return respuesta                                   
  else:
    return {"message":"Error, parametros incorrectos"}  





@app.route("/mayor_duracion/<string:plataforma>/<string:duration_type>/<int:anno>")
def mayor_duracion_plataforma_type_anno(plataforma,duration_type,anno):
  '''Película que más duró según plataforma , tipo de duración y año '''
  if (plataforma != '') and ((plataforma.lower() == 'disney') or (plataforma.lower() == 'hulu')\
    or (plataforma.lower() == 'amazon') or (plataforma.lower() == 'netflix')) and \
    ((str(duration_type).lower() == 'season') or (str(duration_type).lower() == 'min')) and\
    (int(anno) == anno):

    respuesta = {"duration_type":duration_type,
                 "plataforma": plataforma,
                 "año": str(anno)
                }
    local_data = data[data['id'].str.startswith(plataforma[0].lower(), na=False)]
    local_data = local_data[local_data['duration_type'] == duration_type]
    local_data = local_data[local_data['release_year'] == anno]
      
    respuesta["nombre"] = local_data.iloc[0]['title']
    respuesta["duracion"] = str(local_data.iloc[0]['duration_int'])

    return respuesta                                   
  else:
    return {"message":"Error, parametros incorrectos"}  





###################################################################
# 5- Cantidad de Películas/Series por rating
###################################################################
@app.route("/rating")
def cant_movie_serie():
    '''Cantidad de series y películas por rating'''
    lista = data['rating'].unique()
    respuesta = {}
    for rate in lista:
        cant_movie = data[(data['rating'] == rate) & (data['type'] == 'movie')].shape[0]
        cant_show = data[(data['rating'] == rate) & (data['type'] == 'tv show')].shape[0]
        respuesta = {**respuesta, rate:{"movie":str(cant_movie),
                                        "tv show":str(cant_show),
                                        "total": str(cant_movie + cant_show)
                                       }}
    return respuesta




@app.route("/rating/<string:rate>")
def cant_movie_seri_rate(rate):
    '''Cantidad de series y películas para un rating especifico'''
    if rate == '': return {"message":"Error, parametros incorrectos"}

    rate = str(rate)
    local_data = data[data['rating'] == rate]   

    respuesta = {"rating":rate}
    cant_movie = local_data[local_data['type'] == 'movie'].shape[0]
    cant_show = local_data[local_data['type'] == 'tv show'].shape[0]
    respuesta["movie"] = str(cant_movie)
    respuesta["tv show"] = str(cant_show)
    respuesta["total"] = str(cant_movie + cant_show)
    
    return respuesta



@app.route('/')
def index():
  return '''<!DOCTYPE html>
<html>
    <head>       
        <meta charset="utf-8">
        <title>Ejemplo del uso de listas - aprenderaprogramar.com</title>
    </head>
    <body>
    <h2>PI01-Data-Engineering. API Server</h2>
<ul>
 
 <li type="circle">1 - Cantidad de veces que aparece una keyword en el título de Películas/Series.</li>
 <li><a href="http://localhost:5001/keyword/gun"> ej.  http://localhost:5001/keyword/gun    - palabra 'gun' en todas las Plataformas</a></li>
 <li><a href="http://localhost:5001/keyword/amazon/gun"> ej.  http://localhost:5001/keyword/amazon/gun    - palabra 'gun' en la Plataforma 'Amazon'</a></li>
 <br>
 
 <li type="circle">2 - Cantidad de Películas/Series con un puntaje mayor a XX.</li>
 <li><a href="http://localhost:5001/score/90">ej.  http://localhost:5001/score/90   - Score mayor a 90 en todas las Plataformas en cualquier Año</a></li>
 <li><a href="http://localhost:5001/score/90/amazon">ej.  http://localhost:5001/score/90/amazon   - Score mayor a 90 en la Plataforma 'Amazon' en cualquier Año</a></li>
 <li><a href="http://localhost:5001/score/90/2019">ej. http://localhost:5001/score/90/2019  - Score mayor a 90 en en todas las Plataformas en el Año '2019' </a></li>
 <li><a href="http://localhost:5001/score/90/2019/amazon">ej.  http://localhost:5001/score/90/2019/amazon  - Score mayor a 90 en la Plataforma 'Amazon' en el Año '2019'</a></li>
 <br>

 <li type="circle">3 - La segunda Película con mayor Score para una Plataforma determinada, según el orden alfabético de los títulos.</li>
 <li><a href="http://localhost:5001/second_score/amazon">ej.  http://localhost:5001/second_score/amazon   - Para la Plataforma 'Amazon'</a></li>
 <br>


 <li type="circle">4 - Película o Serie que más duró según año, Plataforma y Tipo de duración.</li>
 <li><a href="http://localhost:5001/mayor_duracion/min">ej.  http://localhost:5001/mayor_duracion/min   - Película que mas duró por Plataformas y para todos los Años</a></li>
 <li><a href="http://localhost:5001/mayor_duracion/disney/season">ej.  http://localhost:5001/mayor_duracion/disney/season   - Serie que mas duró para la Plataforma Disney para todos los Años</a></li>
 <li><a href="http://localhost:5001/mayor_duracion/netflix/min/2021">ej.  http://localhost:5001/mayor_duracion/netflix/min/2021   - Película que mas duró para la Plataforma Netflix para el Año 2021</a></li>
 <br> 

 
 <li type="circle">5- Cantidad de Películas/Series por Rating.</li>
 <li><a href="http://localhost:5001/rating">ej.  http://localhost:5001/rating   - Para todos los Ratings</a></li>
 <li><a href="http://localhost:5001/rating/18+">ej.  http://localhost:5001/rating/18+   - Para el Rating '18+'</a></li>
 <br><br><br><br>

 <h3>Nota aclaratoria:</h3>
 <p>
    Estos son ejemplos para indicar la estructura de como solicitar los JSON a la API que responden a las Consultas. Solo hay que sustituir los datos
    para obtener otro variantes de la información.</p> 
  <p>Por ejemplo, para el caso de Cantidad de Películas/Series con un puntaje mayor a XX en su primer ejemplo</p>
  <p>      http://localhost:5001/score/90</p>
  <p>   podemos sustituir el 90 por otro valor de Score.</p><br>  
  <p>  La parte fija quedaría:</p>
  <li>    http://localhost:5001/keyword</li>
  <li>    http://localhost:5001/score</li>
  <li>    http://localhost:5001/second_score</li>
  <li>    http://localhost:5001/mayor_duracion</li>
  <li>    http://localhost:5001/rating </li><br>

  <p> el resto se puede ir modificando para obtener JSON con variantes de la información. Siempre respetando la estructura presentada anteriormente.  
 </p>
 

</ul>

</body>
</html>  
  '''

if __name__ == '__main__':
  app.run(port=5001)