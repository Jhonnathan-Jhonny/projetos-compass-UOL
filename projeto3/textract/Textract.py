import json
import boto3
import os
import re

s3_client = boto3.client('s3')
textract_client = boto3.client('textract')

BUCKET_NAME = 'bucket-api-nota-fiscal'

def call_llm_api(extracted_data):
    refined = {k.upper(): v for k, v in extracted_data.items()}
    return refined

def move_s3_object(bucket, old_key, new_key):
    s3_client.copy_object(Bucket=bucket, CopySource={'Bucket': bucket, 'Key': old_key}, Key=new_key)
    s3_client.delete_object(Bucket=bucket, Key=old_key)

def extract_text_with_textract(bucket, document_key):
    response = textract_client.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': bucket,
                'Name': document_key
            }
        }
    )
    
    lines = []
    for item in response.get('Blocks', []):
        if item['BlockType'] == 'LINE':
            lines.append(item['Text'])
    return '\n'.join(lines)

def simple_nlp_extract(text):
    valor_match = re.search(r'R\$\s?(\d+[\.,]?\d*)', text)
    valor = valor_match.group(1) if valor_match else None
    
    if 'pix' in text.lower():
        forma_pagamento = 'pix'
    elif 'dinheiro' in text.lower():
        forma_pagamento = 'dinheiro'
    else:
        forma_pagamento = 'outros'
    
    data_match = re.search(r'(\d{2}/\d{2}/\d{4})', text)
    data = data_match.group(1) if data_match else None
    
    return {
        'forma_pagamento': forma_pagamento,
        'valor': valor,
        'data': data
    }

def lambda_handler(event, context):
    try:
        original_file_key = event.get('original_file_key')
        
        if not original_file_key:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Parâmetro original_file_key faltando'})
            }
        
        extracted_text = extract_text_with_textract(BUCKET_NAME, original_file_key)
        
        extracted_data = simple_nlp_extract(extracted_text)
        
        refined_data = call_llm_api(extracted_data)
        
        forma_pagamento = extracted_data.get('forma_pagamento', '').lower()
        if forma_pagamento in ['dinheiro', 'pix']:
            destino_original = f"invoices/dinheiro/{os.path.basename(original_file_key)}"
        else:
            destino_original = f"invoices/outros/{os.path.basename(original_file_key)}"
        
        # Move arquivo original
        move_s3_object(BUCKET_NAME, original_file_key, destino_original)
        
        # Salva JSON refinado no mesmo diretório da imagem original
        pasta_origem = os.path.dirname(original_file_key)
        json_key = f"{pasta_origem}/{os.path.splitext(os.path.basename(original_file_key))[0]}.json"
        
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=json_key,
            Body=json.dumps(refined_data).encode('utf-8'),
            ContentType='application/json'
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Processamento concluído',
                'extracted_data': extracted_data,
                'refined_data': refined_data,
                'json_key': json_key,
                'arquivo_original_movido_para': destino_original
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
