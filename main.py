from fastapi import FastAPI, HTTPException, status
from dotenv import load_dotenv
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware

import openai, os
from schemas import Message 
from scripts import create_prompt, clean_and_parse_response, validate_json_structure
load_dotenv('.env.dev')
openai.api_key = os.getenv("API_KEY_OPENAI")

app = FastAPI(
    title="Funnelchat - Intenciones",
    version="1.0.0",
    description="API de intenciones para poder detectar las intenciones de los usuarios.",
    contact={
        "name": "Soporte Funnelchat",
        "url": "https://funnelchat.com/"
    }
)


# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir el origen específico
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)



@app.get("/")
def root():
    return {"mensaje": "Welcime to Funnelchat 🚀",
             "status": status.HTTP_200_OK}


@app.post("/detect_intention")
async def detect_intention(user_promt: Message):

    print("🙋🏽 Mensaje: ", user_promt)

    try:
        # Crear el prompt para OpenAI
        prompt = create_prompt(user_promt)

        response = await openai.ChatCompletion.acreate(
            # model="gpt-4-turbo-2024-04-09", Buen rendimiento
            model="gpt-4o-mini-2024-07-18", # bueno   
              
            messages=[
                {"role": "system", "content": "Eres un experto en análisis de intenciones en texto. Respondes solo en JSON válido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0, # Desactivar la aleatoriedad
            max_tokens=120, # Limitar el número de tokens para evitar respuestas muy largas
            
        )

        # print("Monitoreo de la respuesta: ", response)

        message_content = response["choices"][0]["message"]["content"]

        # Limpiar el mensaje de posibles backticks y "json"
        json_response = clean_and_parse_response(message_content)

        # print("Mensaje limpio para parsear: ", json_response)

        # Validar la estructura del JSON
        validate_json_structure(json_response)
        if not validate_json_structure:
            return {"error": "La estructura del JSON no es válida."}

        UMBRAL_ALTO = 0.6 # Define un umbral alto más razonable
        UMBRAL_BAJO = 0.3 # Define un umbral bajo más razonable

        confidence = json_response["confidence"]


        if confidence >= UMBRAL_ALTO:
            intencion = "intencion detected"
            response = f"✅ Intención detectada: {json_response['detected_intention']} con una confianza de {confidence:.2f}"

            print(response) # Monitoreo de la respuesta
            return {"intencion": intencion, "response": True, "status": status.HTTP_200_OK}
        
        elif confidence <= UMBRAL_BAJO:
            intencion = "intencion not detected"
            response = f"❌ Intención no confiable detectada: {json_response['detected_intention']} con una confianza de {confidence:.2f}"

            print(response) # Monitoreo de la respuesta
            return {"intencion": intencion, "response": False, "status": status.HTTP_200_OK}

        return {"response": response, "status": status.HTTP_200_OK}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


handler = Mangum(app)

