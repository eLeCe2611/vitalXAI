# Guía de Despliegue — Demostración en Vivo

Guía para preparar y ejecutar la demostración en vivo el día de la defensa del TFG.
La plataforma corre en el **PC de casa** (MySQL, datasets y modelos) y se expone por un
**túnel HTTPS**; desde el portátil de la universidad solo se abre la URL en el navegador.

---

## 1. Arquitectura

```
PC de casa (siempre encendido)                 Portátil universidad (solo navegador)
  ├─ MySQL (XAMPP)                                └─ abre https://<url pública> →
  ├─ uvicorn  127.0.0.1:8000
  ├─ pesos de modelos + datasets
  └─ túnel  (cloudflared / ngrok)
```

- **Diagnóstico rápido**: desde el portátil se sube un único rayos X; se procesa en casa
  (modelo → heatmap → PDF) y el resultado vuelve al navegador. Solo viaja esa imagen.
- **Entrenamiento / validación externa**: el portátil envía solo la ruta del dataset
  (texto). Las miles de imágenes se leen del disco del PC de casa; por la red no viaja nada del dataset.

## 2. Requisitos en el PC de casa

| Requisito | Detalle |
|---|---|
| Python ≥ 3.11 | `python --version` |
| XAMPP (MySQL) | Servicio MySQL en `Start` |
| `.env` | Copiado de `.env.example` y configurado |
| Datasets | `pneumoniacnn-main/Images/` y `ExternalDataset/` (con `NORMAL/` y `PNEUMONIA/`) |
| cloudflared | Túnel por defecto. Instalación abajo. |
| ngrok (opcional) | Túnel alternativo con URL fija. |

> El PC de casa debe quedarse **encendido** y con **internet** durante toda la defensa.
> Ajusta la energía a "Nunca" para que no se duerma.

## 3. Instalación de los túneles

```powershell
# cloudflared (principal, sin cuenta)
winget install cloudflare.cloudflared

# ngrok (alternativo, requiere cuenta gratuita en ngrok.com)
#  1. Descarga desde https://ngrok.com/download
#  2. Registra el authtoken: ngrok config add-authtoken <TU_TOKEN>
```

## 4. Configuración (una sola vez, en casa)

Edita el `.env` real del proyecto y deja las rutas exactas de tu máquina:

```
GROQ_API_KEY=tu_clave_de_groq
JWT_SECRET_KEY=genera_una_clave_segura

# Rutas preconfiguradas para lanzar entrenamiento sin dialogo (PC desatendido)
TFG_DEMO_DATASET=C:\Users\luisc\Documents\GitHub\TFG\vitalXAI\pneumoniacnn-main\Images
TFG_DEMO_EXTERNAL_DATASET=C:\Users\luisc\Documents\GitHub\TFG\vitalXAI\pneumoniacnn-main\ExternalDataset

# Tunel: cloudflared (por defecto) o ngrok
TUNNEL_PROVIDER=cloudflared
```

Comprueba que esas rutas existen tal cual están escritas. Si se dejan vacías, el botón
"Explorar Carpeta" vuelve a abrir el diálogo Tkinter en el PC de casa.

## 5. Arranque (un solo comando)

```bat
scripts\demo_start.bat
```

O directamente:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\demo_start.ps1
```

El script:
1. Fija el directorio al proyecto (las rutas relativas dependen de él).
2. Comprueba `.env` y MySQL (3306) y avisa si falta algo.
3. Arranca `uvicorn` sin reload en `127.0.0.1:8000` y espera a que responda.
4. Arranca el túnel (`cloudflared` por defecto; `ngrok` con `-Tunnel ngrok`).
5. Muestra la **URL pública** y la guarda en `demo_url.txt`.

La demo queda corriendo; para detenerla, pulsa `Enter` en la ventana.

## 6. El día de la defensa

1. Enciende el PC de casa y arranca XAMPP → MySQL.
2. Doble clic en `scripts\demo_start.bat`. Anota la URL de la consola (o `demo_url.txt`).
3. Ábrela tú primero para verificar que carga (`/login`).
4. Desde el portátil de la universidad (o el dispositivo del tribunal) abre esa misma URL.
5. Login con una cuenta creada previamente.

### Flujo de la demo

- **Diagnóstico rápido**: sube un rayos X desde el portátil → heatmap y PDF en pantalla.
- **Entrenamiento en vivo**: en el Laboratorio, pulsa "Explorar Carpeta" → se rellena solo
  con la ruta del dataset de casa → envía el mensaje → se encola y arranca.
- **Validación externa**: desde una sesión, "Validación externa" usa la ruta preconfigurada.

> El primer diagnóstico de cada modelo carga los pesos en memoria (unos segundos);
> los siguientes son instantáneos.

## 7. Troubleshooting

| Síntoma | Solución |
|---|---|
| MySQL no responde | Arranca XAMPP (MySQL en `Start`) y relanza el script. |
| La URL pública no aparece | Revisa `demo_tunnel.log` / `demo_tunnel.err.log`; reinstala cloudflared. |
| La página da error 502/504 | El túnel está activo pero el servidor tardó en arrancar; espera y recarga. |
| `ERR_NAME_NOT_RESOLVED` en el navegador | El dominio resuelve bien desde el sistema (`Resolve-DnsName`); suele ser el VPN/proxy del navegador (p. ej. VPN de Opera) o caché DNS. Prueba en Edge/Chrome o `ipconfig /flushdns`. |
| "La ruta no existe" al entrenar | La ruta del dataset en `.env` no coincide con el disco; verifícala. |
| El asistente de entrenamiento falla | Comprueba `GROQ_API_KEY` e internet (el LLM parsea la configuración). |
| Primer diagnóstico lento | Es la carga del modelo en memoria; los siguientes son instantáneos. |

## 8. Plan B (emergencia)

1. **URL local**: la app siempre está en `http://127.0.0.1:8000` en el PC de casa.
2. **localhost.run** (sin instalar nada, usando el `ssh` de Windows):
   ```powershell
   ssh -R 80:localhost:8000 nokey@localhost.run
   ```
   Devuelve una URL aleatoria `*.localhost.run`.
3. **Solo diagnóstico desde el portátil**: si falla la red de casa, se puede repetir la demo
   de diagnóstico ejecutando la app en el propio portátil (los modelos y unas imágenes de
   prueba deben estar disponibles).
