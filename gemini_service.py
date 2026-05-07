import json
import time
from google import genai
from google.genai import types, errors as genai_errors
from config import GEMINI_API_KEY

# Initialize Gemini client once at module level
client = genai.Client(api_key=GEMINI_API_KEY)

def symptoms_analyze(symptoms: str, pain_level: int, age: int) -> dict:
    prompt = f"""
Você é um assistente médico especialista em triagem hospitalar, com anos de experiência clínica.

Dados do paciente:
- Idade: {age} anos
- Sintomas relatados: {symptoms}
- Nível de dor autorrelatado: {pain_level}/10

Sua tarefa é classificar a urgência do atendimento em: "baixa", "média" ou "alta".

Diretrizes para classificação:
- Priorize sempre os sintomas clínicos acima do nível de dor relatado, pois pacientes podem superestimar ou subestimar a dor
- Considere a idade do paciente — idosos e crianças merecem atenção especial para os mesmos sintomas
- Sintomas que indicam risco de vida imediato (dificuldade respiratória, dor no peito, AVC, desmaio) → sempre "alta"
- Sintomas moderados que precisam de atenção mas não são emergência → "média"
- Sintomas leves sem risco aparente → "baixa"

Responda APENAS no seguinte formato JSON, sem texto adicional:
{{
    "urgency_level": "baixa" ou "média" ou "alta",
    "reasoning": "explicação clínica breve e objetiva do motivo da classificação"
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

            # Validate urgency level — fallback to "média" if unexpected value
            valid_values = ["baixa", "média", "alta"]
            if resultado.get("urgency_level") not in valid_values:
                resultado["urgency_level"] = "média"

            resultado["ai_analyzed"] = True
            return resultado

        except genai_errors.ServerError as e:
            # Retry on server errors with 2 second delay
            print(f"Tentativa {tentativa}/{max_tentativas} falhou: {e}")
            if tentativa < max_tentativas:
                time.sleep(2) 
            else:
                return {"urgency_level": "média", "reasoning": "Serviço temporariamente indisponível", "ai_analyzed": False}

        except genai_errors.ClientError as e:
            # Invalid API key or malformed request
            print(f"Erro na API do Gemini: {e}")
            return {"urgency_level": "média", "reasoning": "Erro na análise automática", "ai_analyzed": False}

        except json.JSONDecodeError:
            # Gemini returned response outside expected JSON format
            print("Gemini retornou resposta fora do formato JSON esperado")
            return {"urgency_level": "média", "reasoning": "Erro no formato da resposta", "ai_analyzed": False}