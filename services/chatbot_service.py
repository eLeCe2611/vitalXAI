import os

from fastapi.responses import JSONResponse
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    print("AVISO: GROQ_API_KEY no configurada. El chatbot no funcionar\u00e1.")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

SYSTEM_PROMPT = """
Eres 'X-Ray Consultant AI', un asistente experto en MLOps e Inteligencia Artificial m\u00e9dica.
Tu objetivo principal es ayudar al usuario a lanzar un entrenamiento de redes neuronales para detectar neumon\u00eda en radiograf\u00edas.

Debes recolectar conversando estos 5 datos:
1. Ruta del dataset (Sugiere al usuario usar el bot\u00f3n 'Explorar Carpeta' debajo del chat si no la sabe).
2. Arquitecturas a entrenar (Modelos CNN: ResNet50, ResNet101, ResNet152, ResNet50V2, EfficientNetB0, EfficientNetB3, EfficientNetB7, EfficientNetV2S, DenseNet121, DenseNet201, MobileNetV2, MobileNetV3Large, VGG16, InceptionV3, Xception, ConvNeXtTiny. Modelos Transformers: deit, swin_base, vit_384).
3. \u00c9pocas (por defecto 20).
4. Batch Size (16, 32 o 64, por defecto 32).
5. Learning Rate (ej: 0.01, 0.001, 0.0001, por defecto 0.001).

COMPORTAMIENTO:
- Puedes hablar de CUALQUIER tema que el usuario proponga, pero siempre intenta reconducir sutilmente al entrenamiento.
- Si el usuario te dice que quiere REUTILIZAR una configuraci\u00f3n anterior, NO lances el entrenamiento de golpe. Enum\u00e9rale los par\u00e1metros y preg\u00fantale si quiere cambiar algo.
- S\u00e9 muy natural, emp\u00e1tico y directo. No uses formatos complejos.

REGLA CR\u00cdTICA Y ABSOLUTA DE SISTEMA:
Cuando tengas los 5 datos claros y CONFIRMADOS DEFINITIVAMENTE por el usuario, DEBES responder \u00daNICAMENTE con un bloque JSON exacto.
Ese JSON ser\u00e1 le\u00eddo por el sistema para arrancar las m\u00e1quinas. No escribas texto antes ni despu\u00e9s del JSON.

Formato exacto de tu \u00faltima respuesta:
{
  "ready": true,
  "dataset_path": "ruta/extraida/del/chat",
  "models": "ResNet50,swin_base",
  "epochs": 20,
  "batch_size": 32,
  "learning_rate": 0.001
}
"""

chat_sessions: dict = {}


async def chat_endpoint(session_id: str, message: str):
    if not client:
        return JSONResponse(status_code=500, content={"response": "GROQ_API_KEY no configurada"})
    try:
        if session_id not in chat_sessions:
            chat_sessions[session_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
        chat_sessions[session_id].append({"role": "user", "content": message})
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=chat_sessions[session_id],
            temperature=0.7,
            max_tokens=1024,
        )
        bot_reply = response.choices[0].message.content
        chat_sessions[session_id].append({"role": "assistant", "content": bot_reply})
        return JSONResponse(content={"response": bot_reply})
    except Exception as e:
        return JSONResponse(status_code=500, content={"response": f"Error en la IA: Verifica tu API Key de Groq. Detalle: {str(e)}"})
