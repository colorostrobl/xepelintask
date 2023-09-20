# Xepelin Technical Task :desktop_computer:

Una API creada utilizando Django, la cual tiene 2 apps internas:

## APIs :pencil:

- GSheet Editor: app que permite visualizar una [GSheet](https://docs.google.com/spreadsheets/d/1K7pAu91P8CLyjRk4rD1WuOg8gljC3IKml09SIxtCzww/) y editar los contenidos de esta mediante un form. Puedes encontrar el link al login [aqui](https://joaquin-apis-ed5ad9173cfb.herokuapp.com/login/).  
Las credenciales de prueba son:


    Username → TheXepelinator  
    Password → Xepelinrocks


- WebScrapping: api que recibe post requests y realiza web scrapping del [blog](https://xepelin.com/blog) de Xepelin. Los resultados de este son publicados en una [GSheet](https://docs.google.com/spreadsheets/d/1UlsvCxYmEUKC8aSl5WCd2zphNEUKYmUkxrZMR9Ujd1E/). Puedes ver un pequeño instructivo [aqui](https://joaquin-apis-ed5ad9173cfb.herokuapp.com/webscrapper/).
  El curl de este instructivo esta pensado para ser ejecutado localmente. Para eso seguir la siguiente guía:

## Guía de instalación :nerd_face:

Para simplificar la dependencia de librerias utilizaremos un virtual environment.

1. **Instalar venv** (si no ha sido instalado aún):

```bash
python3 -m pip install virtualenv
```

2. **Crear virtual environment** y crear una carpeta de trabajo

```bash
mkdir django_project_joaquin
cd django_project_joaquin
python3 -m venv new_venv
```

3. **Activar virtual environment**

- Con MacOs y Linux
```bash
source new_venv/bin/activate
```

- Con Windows
```bash
.\new_venv\Scripts\activate
```

- O en Powershell
```powershell
.\new_venv\Scripts\Activate.ps1
```

4. **Git clone** del repositorio
```bash
git clone https://github.com/colorostrobl/xepelintask
cd xepelintask
```

5. **Instalar dependencies**

```bash
pip3 install -r requirements.txt
```

6. **Runserver de manera local**
```bash
python3 manage.py runserver
```

7. **¡El servidor ya esta corriendo de manera local!**  
Ahora puedes acceder al login desde el siguiente dirección: http://127.0.0.1:8000/login/.  
También puedes ver 
intrucciones de como hacer POST request mediante el uso de curl en este url: http://127.0.0.1:8000/webscrapper/.

## Heroku bugs :space_invader:

Como bien se puede apreciar en los links de la sección APIs, la aplicación se encuentra deployed en heroku.  
En este deployed la [API](https://joaquin-apis-ed5ad9173cfb.herokuapp.com/login/) para ver y editar la GSheet funciona perfectamente. Sin embargo, la API que recibe POST requests
y realiza webscrapping del blog de Xepelin funciona de forma inconsistente.  
En particular, dependiendo de la categoría que se desee scrappear, este proceso toma mucho tiempo y heroku tiene un timeout de 30 segundos
lo que produce un HttpResponse 500.  
Así, si se desea por ejemplo scrappear la categoría 'Casos de éxito', no hay problema ya que actualmente solo tiene 7 posts.
Sin embargo, si se scrappea 'Pymes', para buscar toda la información requerida se hacen alrededor de 30 loads de diferentes urls.
Por lo que se alcanza el timeout antes de que termine el procesamiento del request.  
El tiempo escala rapidamente también dependiendo de la velocidad de conexión a internet. Esto
se vuelve evidente sobretodo al intentar scrappear todas las categorías con 'Blog' como keyword.

### Posibles soluciones :thinking:

Para solucionar este problema, se podría considerar hacer un upgrade de los DYNOS de heroku, para lo que hay que pagar :( , lo cual
habilitaría una mayor cantidad de workers para el procesamiento.  
Además de esto sería necesario un pequeño refactor del código para facilitar la integración con librerías
como [Celery](https://docs.celeryq.dev/en/stable/index.html) y [Redis](https://redis.io/) que permiten asignar
tasks a background workers. De esta forma se puede devolver un HttpResponse que indique que se recibió el POST request
y de forma asyncronica delegar el webscrapping a estos workers.  

