# Taller de automatización de pruebas con Selenium, Python, Cucumber, Gherkin, y el patrón Page Object Model (POM).

## Instalación de Herramientas

### Antes de iniciar, asegúrate de tener instaladas las siguientes herramientas:
    - Navegador Google Chrome actualizado a su última versión (https://www.google.com/intl/es_us/chrome/)
	- Python (https://www.python.org/downloads/) 
	- Selenium (pip install selenium)
	- WebDriver para el navegador (Chrome o Firefox)
	- ChromeDriver (https://googlechromelabs.github.io/chrome-for-testing/#stable)
        - descargar el archivo chromedriver correspondiente a su sistema operativo
        - extraer los archivos de la carpeta y copiar el archivo webdriver.exe en la raiz del proyecto
	- Asegurarse de que el archivo del WebDriver.exe esté en el mismo directorio del proyecto.
	- Behave para Cucumber con Python (pip install behave)
	- Cucumber para casos de prueba con Gherkin (Esto ya viene con Behave.)

### Para correr los tests, usa el comando:
	debes correrlo en la terminal o consola de comandos desde la raíz de tu proyecto.
	- behave features/login.feature 
	- behave features/shopping_cart.feature 

# 🧪 Pruebas Automatizadas con Behave (BDD)

Este proyecto utiliza **BDD (Behavior Driven Development)** con **Behave** para escribir pruebas legibles por humanos, utilizando **Gherkin** como lenguaje y **Selenium** para interactuar con la interfaz web. El diseño sigue el **Page Object Model (POM)**.

---

## 🚀 Pasos para crear una nueva prueba

### 1. Crear o identificar la funcionalidad a probar
Define qué funcionalidad vas a automatizar. Por ejemplo: login, agregar productos al carrito, filtrado de ítems, etc.

### 2. Crear o actualizar la clase de página (`.py`)
Usa el patrón **Page Object Model**. Crea una clase para la página web si no existe, y define los métodos necesarios.

```bash
project/
└── pages/
    ├── login_page.py
    ├── inventory_page.py
    └── base_page.py
```

### 3. Crear el archivo `.feature`
Escribe el escenario en lenguaje Gherkin. Usa `Feature`, `Scenario`, `Given`, `When`, `Then` y `And`.

```gherkin
Feature: Add to cart functionality

  Scenario: User adds a product to the cart
    Given I am logged in on the inventory page
    When I add the product "Sauce Labs Backpack" to the cart
    Then I should see 1 item in the cart
```

Guárdalo en la carpeta `features/`.

### 4. Crear el archivo de `steps`
Aquí implementas en Python lo que hacen los pasos del `.feature`. Usa las clases del POM para interactuar con la UI.

```bash
project/
└── features/
    ├── steps/
    │   └── cart_steps.py
    └── shopping_cart.feature
```

Ejemplo de step:

```python
@when('I add the product "{product_name}" to the cart')
def step_impl(context, product_name):
    context.inventory_page.add_product_to_cart(product_name)
```

### 5. Ejecutar las pruebas

En la terminal, dentro del proyecto, ejecuta:

```bash
behave
```

También puedes correr un archivo específico:

```bash
behave features/shopping_cart.feature
```

---

# 🧑‍🏫 Ejercicios para el Taller de Pruebas Automatizadas con Selenium

A continuación se presentan dos ejercicios prácticos que los estudiantes deberán realizar durante el taller. Estos están diseñados para reforzar conceptos clave como la interacción con elementos web, localización por selectores y verificación de resultados.

---
## 🧪 Ejercicio 1: Ingresar a una lobby correctamente y validar mensaje de error
### 💡 Sitio:
https://lobby-global.vercel.app/

### 🎯 Escenarios:
- Ingresar con un nombre único a la lobby
- Validar mensaje de error al intentar ingresar con un nombre de usuario que contiene espacios

## 🧪 Ejercicio 2: Buscar una película en IMDb y validar su calificación
### 💡 Sitio:
https://www.imdb.com

### 🎯 Escenario:
Buscar la película “Pulp fiction”, abrir el primer resultado y verificar que en la página se muestre correctamente la calificación (rating).

## Ejecución multiplataforma

Instala las dependencias desde la raíz del proyecto:

```bash
python -m pip install -r requirements.txt
```

El proyecto detecta primero Google Chrome y después Brave. También se pueden
controlar el navegador y el driver mediante variables de entorno:

- `BROWSER=chrome` o `BROWSER=brave` fuerza el navegador detectado.
- `BROWSER_PATH` indica la ruta explícita al ejecutable del navegador.
- `CHROMEDRIVER_PATH` indica la ruta explícita a ChromeDriver.
- `HEADLESS=1` ejecuta sin ventana.
- `NO_SANDBOX=1` añade las opciones necesarias en contenedores Linux.

Ejemplos en Linux/macOS (bash):

```bash
BROWSER=brave HEADLESS=1 behave
BROWSER_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" behave
```

En fish:

```fish
env BROWSER=chrome HEADLESS=1 behave
env CHROMEDRIVER_PATH=/ruta/a/chromedriver behave
```

En Windows PowerShell:

```powershell
$env:BROWSER = "chrome"; $env:HEADLESS = "1"; behave
$env:BROWSER_PATH = "C:\Program Files\Google\Chrome\Application\chrome.exe"; behave
```

En Windows CMD:

```bat
set BROWSER=chrome
set HEADLESS=1
behave
```

Si no se encuentra un ChromeDriver local válido, o no es compatible con el
navegador, el proyecto muestra un warning y usa Selenium Manager para resolver
automáticamente un driver compatible. El binario `chromedriver` no se versiona,
por lo que cada equipo puede usar su propio ejecutable o este fallback.

IMDb puede responder `403 Forbidden` en redes, navegadores o entornos de
automatización con protección anti-bot. El escenario usa esperas explícitas,
ventana grande, idioma `en-US` y no intenta evadir esa protección; si el bloqueo
persiste, el escenario debe ejecutarse desde una red donde IMDb permita el
acceso automatizado.
