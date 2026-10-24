<<<<<<< HEAD
# RP_AD2026Q4

Repositorio de referencia: un notebook ejecutable por clase que deja un resumen `.txt` en `reportes/`.

## Estructura

```
src/rp_utils/            Clases reutilizables
  reporting.py           ClassReport: genera el resumen .txt de cada notebook
  hf_loader.py           HFDatasetLoader: conexión automática a Hugging Face y exportación
  summarizer.py          DatasetSummarizer: resumen de un DataFrame
sincronicas/             8 notebooks: teoría + demostración por clase
triplea/                 8 notebooks: práctica con ejercicios por clase
Actividades_Evaluativas/ 4 notebooks con la solución de referencia
reportes/                Resúmenes .txt generados (uno por notebook)
scripts/build_notebooks.py  Regenera todos los notebooks
```

## Temario (propuesto, ajustable en `scripts/build_notebooks.py`)

| Clase | Tema | Unidad |
|---|---|---|
| 1 | Introducción a Python y entorno de análisis | 1 |
| 2 | NumPy y computación vectorizada | 1 |
| 3 | pandas: carga y exploración | 1 |
| 4 | Limpieza y transformación | 2 |
| 5 | Visualización | 2 |
| 6 | Estadística descriptiva e inferencial | 2 |
| 7 | Ingeniería de características | 3 |
| 8 | Modelado básico y evaluación | 3 |

## Actividades evaluativas

1. Conexión automática a Hugging Face con `HFDatasetLoader` y resumen con `DatasetSummarizer`, orquestado desde el notebook.
2. Unidad 1: exploración con Python, NumPy y pandas.
3. Unidad 2: limpieza, visualización y estadística.
4. Unidad 3: ingeniería de características y modelado.

El dataset se cambia editando `DATASET`, `CONFIG`, `SPLIT` y `TARGET` en la primera celda de cada actividad.

## Uso

```bash
cd /workspaces/RP_AD2026Q4
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyarrow openpyxl  # opcional: parquet y xlsx
python scripts/build_notebooks.py   # opcional: regenerar notebooks
jupyter lab
```

En Bash, el entorno virtual debe activarse con `source` (o con un punto):

```bash
source .venv/bin/activate
# equivalente:
. .venv/bin/activate
```

No se debe ejecutar `.venv/bin/activate` directamente, porque `activate` es
un script que modifica la sesión actual de la terminal. Cuando se activa
correctamente, el prompt muestra `(.venv)`.

Cada notebook termina con `report.save()`, que escribe `reportes/<carpeta>/<notebook>.txt`.

## Autenticación en Hugging Face

Para descargar datasets públicos normalmente no se necesita un token. Si el
dataset es privado o requiere aceptación de condiciones de uso, configura un
token de Hugging Face siguiendo estos pasos.

### 1. Crear un token

1. Inicia sesión en [Hugging Face](https://huggingface.co/).
2. Abre [Settings > Access Tokens](https://huggingface.co/settings/tokens).
3. Selecciona **Create new token**.
4. Asigna un nombre descriptivo, por ejemplo `RP_AD2026Q4`.
5. Selecciona el permiso mínimo necesario: **Read**.
6. Presiona **Create token** y copia el token. Normalmente comienza por
   `hf_`.

Guarda el token de forma segura y no lo incluyas en el código fuente.

### 2. Instalar la CLI e iniciar sesión

Con el entorno virtual activado, instala o actualiza la librería de Hugging
Face:

```bash
python -m pip install --upgrade huggingface_hub
```

Inicia sesión desde la terminal:

```bash
hf auth login
```

Cuando la terminal solicite el token, pégalo y presiona **Enter**. Es normal
que no se muestren caracteres mientras lo escribes o pegas.

La sesión queda guardada localmente para que `HFDatasetLoader` pueda usarla
automáticamente. Comprueba que la autenticación funcionó:

```bash
hf auth whoami
```

Si tu instalación usa la CLI antigua, el comando equivalente es:

```bash
huggingface-cli login
```

### 3. Cargar el dataset autenticado

Después de iniciar sesión, no es necesario pasar el token al constructor:

```python
from rp_utils import HFDatasetLoader

loader = HFDatasetLoader(
    "Fast_Food_Restaurants",
    filename="datos/fast_food.csv",
)
df = loader.load()
```

No escribas tokens directamente en archivos Python ni los subas a GitHub.
Si un token se expone accidentalmente, revócalo desde [Access
Tokens](https://huggingface.co/settings/tokens) y crea uno nuevo.

## Carga de un dataset como DataFrame

`HFDatasetLoader` recibe el identificador del dataset, descarga la división
indicada y devuelve un `pandas.DataFrame`. `filename` y `file_type` son
opcionales; si se proporciona `filename`, el DataFrame también se guarda en
`csv`, `json`, `parquet` o `xlsx`.

```python
from rp_utils import HFDatasetLoader

loader = HFDatasetLoader(
    "Fast_Food_Restaurants",
    filename="datos/fast_food.csv",
)
df = loader.load()
```

Para ejecutar este ejemplo manualmente, crea un archivo `prueba_loader.py` en
la raíz del proyecto con el código anterior y ejecuta:

```bash
PYTHONPATH=src python prueba_loader.py
```

También se puede ejecutar directamente desde la terminal:

```bash
PYTHONPATH=src python -c '
from rp_utils import HFDatasetLoader

df = HFDatasetLoader(
    "Fast_Food_Restaurants",
    filename="datos/fast_food.csv",
).load()

print(df.head())
'
```

También se puede indicar el formato explícitamente:

```python
loader = HFDatasetLoader(
    "Fast_Food_Restaurants",
    filename="datos/fast_food",
    file_type="parquet",
)
df = loader.load()
```
=======

# EA1 – Carga y creación de Dataset

**Integrantes del equipo:**

- Justin Beckham Cardona
- Jorge Armando Rodríguez
- Lina Johana Seguro

**Asignatura:** 059-Machine Learning  
**Actividad:** EA1 – Carga y creación de Dataset

## Objetivo

Esta actividad tiene como objetivo cargar un conjunto de datos desde Hugging Face, inspeccionar su estructura, aplicar cuatro transformaciones con Python y pandas, y generar archivos de datos y reportes que documenten el procesamiento.

## Dataset

- **Nombre:** Auto MPG
- **Identificador en Hugging Face:** `scikit-learn/auto-mpg`
- **División utilizada:** `train`
- **Archivo generado:** `src/carga_datos/datos/auto_mpg.csv`

El dataset contiene información sobre automóviles, incluyendo consumo de combustible, cilindros, cilindrada, caballos de fuerza, peso, aceleración, año del modelo, origen y nombre del automóvil.

## Desarrollo de la actividad

El notebook [`EA1_Carga_de_Datos.ipynb`](src/carga_datos/EA1_Carga_de_Datos.ipynb) utiliza la clase `HFDatasetLoader` para cargar el dataset y la clase `Reportes` para generar los reportes del procesamiento.

### Carga inicial

El dataset se carga desde Hugging Face mediante el identificador:

```text
scikit-learn/auto-mpg
```

### Autenticación con Hugging Face

El notebook obtiene el token de acceso desde la variable de entorno `HF_TOKEN` y lo proporciona al parámetro `token` de `HFDatasetLoader`.

En GitHub Actions, el secreto `HF_TOKEN` se expone como variable de entorno durante la ejecución del notebook, sin necesidad de publicar su valor en el repositorio.

Esta configuración permite utilizar el token durante la carga del dataset y evita incluir credenciales directamente en el código.

La carga se convierte en un `pandas.DataFrame` y se guarda en:

```text
src/carga_datos/datos/auto_mpg.csv
```

### Transformaciones

El notebook aplica las siguientes transformaciones:

1. **Renombrado de columnas**

   Se crea `df_espanol`, que contiene el dataset completo con sus nueve columnas renombradas al español:

   - `mpg` → `millas_por_galon`
   - `cylinders` → `cilindros`
   - `displacement` → `cilindrada`
   - `horsepower` → `caballos_de_fuerza`
   - `weight` → `peso`
   - `acceleration` → `aceleracion`
   - `model year` → `anio_modelo`
   - `origin` → `origen`
   - `car name` → `nombre_automovil`

2. **Selección de variables**

   Se crea `df_seleccion` a partir de `df_espanol`. Este DataFrame conserva cinco variables:

   - `nombre_automovil`
   - `millas_por_galon`
   - `cilindros`
   - `caballos_de_fuerza`
   - `peso`

3. **Filtrado por rendimiento**

   Se crea `df_filtrado` a partir de `df_seleccion`. Conserva los registros cuyo valor de `millas_por_galon` es mayor o igual a 25:

   ```python
   millas_por_galon >= 25
   ```

4. **Clasificación de la eficiencia**

   Se crea `df_clasificado` a partir de `df_espanol`, por lo que conserva los registros completos y las nueve columnas del DataFrame renombrado. Luego se agrega la columna `nivel_eficiencia`.

   Los umbrales utilizados son:

   - **Alta:** `millas_por_galon >= 30`
   - **Media:** `20 <= millas_por_galon < 30`
   - **Baja:** `millas_por_galon < 20`

La clasificación se realiza sobre el DataFrame completo (`df_espanol`), no únicamente sobre `df_filtrado`.

## Reportes generados

La clase [`Reportes`](src/clases_po/reportes.py) genera informes de texto que incluyen:

- Número de filas.
- Número de columnas.
- Cantidad de registros duplicados.
- Nombres y tipos de las columnas.
- Valores nulos por columna.
- Estadísticas descriptivas de las columnas numéricas, cuando existen.

El notebook genera los siguientes reportes:

### Reporte inicial

Se genera a partir del DataFrame original cargado y se guarda en:

```text
src/carga_datos/reportes/auto_mpg.txt
```

### Reporte final

Se genera a partir de `df_clasificado`, después de agregar la columna `nivel_eficiencia`, y se guarda en:

```text
src/carga_datos/reportes/reporte_auto_mpg_clasificado.txt
```

## Resultados observados

Los siguientes resultados corresponden a la ejecución actualmente almacenada en el notebook:

- **Filas iniciales:** 398
- **Columnas iniciales:** 9
- **Filas después del filtro `millas_por_galon >= 25`:** 169
- **Duplicados registrados en el reporte inicial:** 0
- **Valores nulos registrados en el reporte inicial:** 0 en cada una de las columnas observadas

Estos valores describen esa ejecución concreta y pueden variar si cambia el dataset o la ejecución del procesamiento.

## Estructura relevante del repositorio

La siguiente es una estructura simplificada con los archivos relevantes de la actividad:

```text
Proyectos-Machine-Learning/
├── .github/
│   └── workflows/
│       └── ejecutar-ea1.yml
├── src/
│   ├── clases_po/
│   │   ├── __init__.py
│   │   ├── hf_loader.py
│   │   └── reportes.py
│   └── carga_datos/
│       ├── datos/
│       │   └── auto_mpg.csv
│       ├── reportes/
│       │   ├── auto_mpg.txt
│       │   └── reporte_auto_mpg_clasificado.txt
│       └── EA1_Carga_de_Datos.ipynb
└── requirements.txt
```

Esta es una estructura simplificada y solo incluye los archivos relevantes de la actividad.

## Clases reutilizables

### `HFDatasetLoader`

La clase [`HFDatasetLoader`](src/clases_po/hf_loader.py) permite:

- Recibir el identificador de un dataset de Hugging Face.
- Seleccionar una configuración y una división del dataset.
- Recibir opcionalmente un token y un directorio de caché.
- Limitar opcionalmente el número de filas.
- Convertir el resultado de `load_dataset` en un `pandas.DataFrame`.
- Guardar el DataFrame en formato CSV, JSON, Parquet o XLSX.
- Consultar información básica del último DataFrame cargado mediante `info()`.

Si se utiliza `file_type`, también se requiere indicar `filename`. Cuando no se especifica el tipo de archivo, la clase puede inferirlo a partir de la extensión de `filename`.

### `Reportes`

La clase [`Reportes`](src/clases_po/reportes.py) permite:

- Generar un reporte textual de un `pandas.DataFrame`.
- Validar que el objeto recibido sea un `pandas.DataFrame`.
- Imprimir el reporte en consola.
- Guardar el reporte en un archivo de texto y devolver su ruta.

El contenido del reporte incluye dimensiones, duplicados, tipos de columnas, valores nulos y estadísticas descriptivas de las columnas numéricas cuando existen.

## Tecnologías utilizadas

- Python
- pandas
- NumPy
- Hugging Face Datasets
- Jupyter Notebook
- Git y GitHub
- GitHub Actions

## Dependencias

Las dependencias declaradas en [`requirements.txt`](requirements.txt) son:

```text
numpy>=2.0,<3
pandas==2.2.3
matplotlib==3.9.4
ipykernel==6.29.5
datasets
nbconvert
```

Para instalar estas dependencias de forma local:

```bash
pip install -r requirements.txt
```

Además, el flujo de GitHub Actions instala explícitamente los siguientes paquetes:

```text
pyarrow
openpyxl
```

Estos paquetes se instalan en el flujo para proporcionar soporte a formatos utilizados por `HFDatasetLoader`, como Parquet y XLSX.

## Ejecución automática con GitHub Actions

El flujo definido en [`.github/workflows/ejecutar-ea1.yml`](.github/workflows/ejecutar-ea1.yml) se ejecuta cuando se realiza un `push` sobre la rama `main`.

El proceso realiza los siguientes pasos:

1. Descarga el repositorio mediante `actions/checkout`.
2. Configura Python 3.12.
3. Crea el entorno virtual `.venv`.
4. Actualiza `pip`.
5. Instala las dependencias de `requirements.txt`.
6. Instala adicionalmente `pyarrow` y `openpyxl`.
7. Crea los directorios de datos y reportes si no existen.
8. Elimina el contenido anterior de:
   - `src/carga_datos/datos/`
   - `src/carga_datos/reportes/`
9. Ejecuta el notebook `EA1_Carga_de_Datos.ipynb` mediante `jupyter nbconvert`, desde el directorio `src/carga_datos`.
10. Proporciona al proceso las variables de entorno `HF_TOKEN` y `PYTHONPATH`.
11. Agrega al control de versiones los datos, reportes y el notebook ejecutado.
12. Comprueba si existen cambios preparados.
13. Si existen cambios, crea un commit automático y realiza un push hacia la rama `main`.
14. Si no existen cambios, muestra el mensaje `No se generaron cambios.` y no crea ningún commit ni push.

La ejecución del notebook utiliza un tiempo máximo de 1800 segundos para el procesador de ejecución.

El commit automático utiliza el mensaje:

```text
chore: actualizar resultados de EA1 [skip ci]
```

## Configuración del secreto `HF_TOKEN`

Para que GitHub Actions tenga disponible el token de Hugging Face durante la ejecución, se configura un secreto del repositorio con el nombre:

```text
HF_TOKEN
```

El flujo lo expone como variable de entorno para el proceso que ejecuta el notebook. El valor del token debe configurarse directamente en los secretos de GitHub. No debe publicarse en el código, en los notebooks ni en este README.

La configuración del notebook utiliza una única instancia de `HFDatasetLoader`, que obtiene el token de acceso mediante la variable de entorno `HF_TOKEN`. Este token se proporciona al parámetro `token` del cargador para autenticar la conexión con Hugging Face cuando sea necesario.

## Resultados generados

Después de ejecutar el notebook, los resultados principales se encuentran en:

```text
src/carga_datos/datos/
```

y los reportes en:

```text
src/carga_datos/reportes/
```
>>>>>>> c3d6f6c1de076a72820286d1752a8aa2777e54d5
