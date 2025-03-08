from fastapi import HTTPException
import json


def create_prompt(user_prompt):
    """
    Genera el prompt para enviar a OpenAI basado en el mensaje del usuario y las intenciones.
    """
    return f"""Analiza este mensaje y determina si coincide con alguna de las intenciones listadas.
    Mensaje del usuario: "{user_prompt.text}"
    Intenciones posibles:
    {json.dumps(user_prompt.intentions, indent=2)}
    Responde solo en formato JSON con esta estructura exacta:
    {{
        "detected_intention": "la intención detectada o 'unknown'",
        "confidence": número entre 0 y 1,
        "explanation": "tu explicación del análisis",
        "action": {{
            "type": "tipo de acción a tomar",
            "details": "detalles de la acción"
        }}
    }}"""




def clean_and_parse_response(content):
    """
    Limpia el contenido de la respuesta de OpenAI y lo convierte a un objeto JSON.
    """
    content = content.strip()
    if content.startswith('```json'):
        content = content[7:]
    elif content.startswith('```'):
        content = content[3:]
    if content.endswith('```'):
        content = content[:-3]
    content = content.strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError as decode_error:
        raise HTTPException(status_code=500, detail=f"Error al parsear el contenido JSON: {str(decode_error)}")




def validate_json_structure(json_response):
    """
    Valida que el JSON tenga la estructura esperada.
    """
    required_fields = ["detected_intention", "confidence", "explanation", "action"]
    for field in required_fields:
        if field not in json_response:
            raise HTTPException(status_code=500, detail=f"Respuesta incompleta: falta el campo '{field}'")

    # Validar estructura del campo 'action'
    if not isinstance(json_response["action"], dict) or \
       "type" not in json_response["action"] or \
       "details" not in json_response["action"]:
        raise HTTPException(status_code=500, detail="Campo 'action' mal formado")

