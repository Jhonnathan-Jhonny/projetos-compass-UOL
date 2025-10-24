import json
import boto3
import os
from urllib.parse import unquote_plus

s3_client = boto3.client('s3')

BUCKET_NAME = 'bucket-api-nota-fiscal'

def call_llm_api(extracted_data):
    refined = {k.upper(): v for k, v in extracted_data.items()}
    return refined

def move_s3_object(bucket, old_key, new_key):
    s3_client.copy_object(Bucket=bucket, CopySource={'Bucket': bucket, 'Key': old_key}, Key=new_key)
    s3_client.delete_object(Bucket=bucket, Key=old_key)

def lambda_handler(event, context):
    try:
        extracted_data = event.get('extracted_data')
        original_file_key = event.get('original_file_key')
        
        if not extracted_data or not original_file_key:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Parâmetros extraídos_data ou original_file_key faltando'})
            }
        
        refined_data = call_llm_api(extracted_data)
        
        forma_pagamento = extracted_data.get('forma_pagamento', '').lower()
        
        if forma_pagamento in ['dinheiro', 'pix']:
            destino_original = f"invoices/dinheiro/{os.path.basename(original_file_key)}"
        else:
            destino_original = f"invoices/outros/{os.path.basename(original_file_key)}"
        
        move_s3_object(BUCKET_NAME, original_file_key, destino_original)
        
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
                'message': 'Dados refinados processados com sucesso',
                'json_key': json_key,
                'arquivo_original_movido_para': destino_original
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
