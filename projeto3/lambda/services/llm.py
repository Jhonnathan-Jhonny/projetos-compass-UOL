import os
import json
import openai

def refinar_dados_com_gpt4(dados_extraidos):
    prompt = f"""
Você é um assistente que formata dados extraídos de notas fiscais em JSON.
Aqui estão os dados extraídos parcialmente (via Textract e NLP):
{json.dumps(dados_extraidos, ensure_ascii=False)}

Por favor, gere um JSON formatado que contenha estes campos:
- numero_nota (string)
- data_emissao (no formato YYYY-MM-DD)
- cnpj_emitente (string)
- valor_total (número decimal)
- forma_pagamento (dinheiro, pix, cartao, boleto, outro)
- itens: lista de objetos com descricao (string), quantidade (inteiro), valor_unitario (decimal)

Retorne **apenas** o JSON válido, sem nenhuma explicação.
"""

    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=500
    )
    
    texto_resposta = resposta.choices[0].message.content
    
    dados_formatados = json.loads(texto_resposta)
    
    return dados_formatados

dados_extraidos = {
    "invoice_number": "1234",
    "date": "2025-08-10",
    "vendor": "Loja ABC",
    "total": "150.75",
    "payment": "pix",
    "items": [
        {"desc": "Produto 1", "qty": 1, "price": 100.00},
        {"desc": "Produto 2", "qty": 1, "price": 50.75}
    ]
}

resultado = refinar_dados_com_gpt4(dados_extraidos)
print(json.dumps(resultado, indent=2, ensure_ascii=False))  

def formatar_json_com_llm(dados_extraidos):
    client = OpenAI()
    prompt = f"""
    Formate os seguintes dados da nota fiscal em JSON no padrão:
    {{
        "numero": "",
        "data": "",
        "valor_total": "",
        "forma_pagamento": ""
    }}
    Dados: {dados_extraidos}
    """
    try:
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return json.loads(resposta.choices[0].message.content)
    except Exception as e:
        print(f"Erro na LLM: {e}")
        return None

