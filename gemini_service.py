import json
import time
from google import genai
from google.genai import types, errors as genai_errors
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def symptoms_analyze(symptoms: str, pain_level: int) -> dict:
    prompt = f"""
    Você é um assistente médico de triagem hospitalar.
    
    Um paciente chegou com os seguintes sintomas: {symptoms}
    Nível de dor relatado: {pain_level}/10
    
    Com base nisso, responda APENAS no seguinte formato JSON:
    {{
        "urgency_level": "baixa" ou "média" ou "alta",
        "reasoning": "explicação breve do motivo"
    }}
    """

    max_tentativas = 3
    for tentativa in range(1, max_tentativas + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )

            resultado = json.loads(response.text)

            valid_values = ["baixa", "média", "alta"]
            if resultado.get("urgency_level") not in valid_values:
                resultado["urgency_level"] = "média"

            resultado["ai_analyzed"] = True
            return resultado

        except genai_errors.ServerError as e:
            print(f"Tentativa {tentativa}/{max_tentativas} falhou: {e}")
            if tentativa < max_tentativas:
                time.sleep(2)  # espera 2 segundos antes de tentar de novo
            else:
                return {"urgency_level": "média", "reasoning": "Serviço temporariamente indisponível", "ai_analyzed": False}

        except genai_errors.ClientError as e:
            print(f"Erro na API do Gemini: {e}")
            return {"urgency_level": "média", "reasoning": "Erro na análise automática", "ai_analyzed": False}

        except json.JSONDecodeError:
            print("Gemini retornou resposta fora do formato JSON esperado")
            return {"urgency_level": "média", "reasoning": "Erro no formato da resposta", "ai_analyzed": False}