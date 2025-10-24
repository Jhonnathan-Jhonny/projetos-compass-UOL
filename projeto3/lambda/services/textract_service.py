import json
import boto3
import os
import re
import urllib.parse
from datetime import datetime

s3 = boto3.client('s3')
textract = boto3.client('textract')
comprehend = boto3.client('comprehend')

def extract_with_comprehend(text):
    try:
        # Primeiro: Detecção de entidades
        entities_response = comprehend.detect_entities(
            Text=text,
            LanguageCode='pt'
        )
        
        # Segundo: Análise de sintaxe para melhorar a precisão
        syntax_response = comprehend.detect_syntax(
            Text=text,
            LanguageCode='pt'
        )

        def extract_after_marker(marker, text):
            marker_pos = text.find(marker)
            if marker_pos == -1:
                return None
            remaining_text = text[marker_pos + len(marker):]
            return remaining_text.split('\n')[0].strip()
        
        # Extração específica para CNPJ/CPF
        cnpj_emissor = extract_after_marker('CNPJ/CPF :', text)
        cpf_consumidor = extract_after_marker('CNPJ/CPF :', text.split('Destinatário')[-1])
        
        # Organizar entidades por tipo e score
        entities = {}
        for entity in entities_response['Entities']:
            if entity['Type'] not in entities or entity['Score'] > entities[entity['Type']]['Score']:
                entities[entity['Type']] = {
                    'Text': entity['Text'],
                    'Score': entity['Score']
                }
        
        # Extrair campos específicos
        result = {
            'nome_emissor': entities.get('ORGANIZATION', {}).get('Text'),
            'CNPJ_emissor': cnpj_emissor,
            'endereco_emissor': entities.get('LOCATION', {}).get('Text'),
            'CNPJ_CPF_consumidor': cpf_consumidor,
            'data_emissao': entities.get('DATE', {}).get('Text'),
            'valor_total': entities.get('QUANTITY', {}).get('Text')
        }
        
       # Processamento adicional para campos que podem não ser entidades
        lines = text.split('\n')
        for line in lines:
            if 'Forma de pagamento :' in line:
                result['forma_pgto'] = line.split(':')[-1].strip()
            elif 'Número :' in line:
                result['numero_nota_fiscal'] = line.split(':')[-1].strip()
            elif 'Série :' in line:
                result['serie_nota_fiscal'] = line.split(':')[-1].strip()
        
        # Garantir que todos os campos existam no resultado
        required_fields = ['numero_nota_fiscal', 'serie_nota_fiscal', 'forma_pgto']
        for field in required_fields:
            if field not in result:
                result[field] = None
        
        return result
        
    except Exception as e:
        print(f"Erro no Comprehend: {str(e)}")
        return {}

def lambda_handler(event, context):
    try:
        bucket_origem = os.environ['SOURCE_BUCKET']
        bucket_destino = os.environ['DEST_BUCKET']
        
        key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"])
        print(f"Processando arquivo: {key}")
        
        # Baixar arquivo do bucket origem
        file_obj = s3.get_object(Bucket=bucket_origem, Key=key)
        file_content = file_obj['Body'].read()
        
        # Extração de texto com Textract
        response = textract.analyze_document(
            Document={'Bytes': file_content},
            FeatureTypes=["FORMS", "TABLES"]
        )
        
        # Processar texto extraído
        blocks = response.get("Blocks", [])
        full_text = "\n".join([b['Text'] for b in blocks if b['BlockType'] == 'LINE'])
        print("Texto extraído:\n", full_text)
        
        # Extrair campos com Comprehend
        campos = extract_with_comprehend(full_text)
        
        # Adicionar metadados
        campos['arquivo_origem'] = key
        campos['timestamp_processamento'] = datetime.now().isoformat()
        campos['processador'] = 'textract+comprehend'
        
        # Salvar resultado
        if(campos['forma_pgto'] == 'Dinheiro' or campos['forma_pgto'] == 'Pix'):
            parsed_key = f"dinheiro_pix/{key.split('/')[-1].split('.')[0]}_result.json"
        else: 
            parsed_key = f"outros/{key.split('/')[-1].split('.')[0]}_result.json"
        s3.put_object(
            Bucket=bucket_destino,
            Key=parsed_key,
            Body=json.dumps(campos, ensure_ascii=False, indent=2)
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Processado com sucesso',
                'arquivo': parsed_key,
                'campos_extraidados': campos
            })
        }
        
    except Exception as e:
        print(f"Erro: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }