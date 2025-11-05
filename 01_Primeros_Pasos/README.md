# FastAPI Project

Aquest és un petit projecte fet amb **FastAPI** per aprendre a crear APIs modernes amb Python.

## 🚀 Instal·lació

1. Clona el repositori:

```bash
git clone https://github.com/skril349/fast_api.git
cd fastapi-project
```

## ⚙️ Configuració de l'entorn virtual i instal·lació de dependències

Per mantenir un entorn de treball net i aïllat, és recomanable crear un **entorn virtual** on instal·lar totes les dependències del projecte.  
Això evita conflictes amb altres versions de llibreries que puguis tenir al teu sistema.

### 1. Crear l'entorn virtual

Des de la carpeta del projecte, executa:

### 2. Activar l'entorn virtual

Per activar-lo a Windows (PowerShell):

```bash
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

Després de fer-ho, veuràs alguna cosa com això al principi de la línia de comandes

```
(.venv) PS C:\Users\antoni\Documents\Udemy\fast_api>

```

### 3. Instal·lar les dependències del projecte

Instal·la FastAPI i les seves dependències estàndard amb:

```
pip install "fastapi[standard]"

```

### Paquets principals instal·lats amb `fastapi[standard]`

1. **FastAPI** – framework principal per crear APIs modernes i asíncrones amb Python.  
2. **Uvicorn** – servidor **ASGI** lleuger i altament performant utilitzat per executar aplicacions FastAPI.  
3. **Pydantic** – eina per a la **validació i gestió de dades** basada en tipus de Python.  
4. **Starlette** – motor web subjacent que proporciona la base d’ASGI, rutes, middleware i gestió d’esdeveniments.
