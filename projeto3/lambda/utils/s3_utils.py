import boto3
import os
import json

s3 = boto3.client('s3')

def salvar_json_no_s3(bucket, caminho_imagem, dados_json):
    pasta = os.path.dirname(caminho_imagem) 
    nome_arquivo = os.path.splitext(os.path.basename(caminho_imagem))[0] + ".json"
    caminho_json = f"{pasta}/{nome_arquivo}"
    
    s3.put_object(
        Bucket=bucket,
        Key=caminho_json,
        Body=json.dumps(dados_json, ensure_ascii=False, indent=2),
        ContentType="application/json"
    )
    return caminho_json
