const { S3Client, PutObjectCommand, GetObjectCommand } = require('@aws-sdk/client-s3');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

if (!process.env.S3_BUCKET_NAME || !process.env.AWS_REGION) {
  throw new Error('Variáveis de ambiente AWS não configuradas!');
}

const s3Client = new S3Client({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    sessionToken: process.env.AWS_SESSION_TOKEN
  }
});

async function uploadFile(fileName, data) {
  const filePath = path.join(__dirname, fileName)
  
  try {
    if (!fs.existsSync(filePath)) {
      console.warn(`Arquivo ${filePath} não encontrado. Criando novo com conteúdo padrão.`);
      fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
    }

    const fileContent = fs.readFileSync(filePath);

    const uploadParams = {
      Bucket: process.env.S3_BUCKET_NAME,
      Key: path.basename(filePath),
      Body: fileContent,
      ContentType: 'application/json'
    }

    const response = await s3Client.send(new PutObjectCommand(uploadParams));
    console.log('Upload realizado com sucesso!');
    console.log('URL do objeto:', `https://${uploadParams.Bucket}.s3.${process.env.AWS_REGION}.amazonaws.com/${uploadParams.Key}`);
    return response;
  } catch (error) {
    console.error('Erro no upload:', error);
    throw error;
  }
}

async function GetFileS3(filename = 'data.json') {
  const params = {
    Bucket: process.env.S3_BUCKET_NAME,
    Key: filename
  };

  try {
    const command = new GetObjectCommand(params);
    const response = await s3Client.send(command);

    const streamChunks = [];
    for await (const chunk of response.Body) {
      streamChunks.push(chunk);
    }

    const buffer = Buffer.concat(streamChunks);
    const jsonData = JSON.parse(buffer.toString('utf-8'));

    console.log(`Arquivo '${filename}' lido com sucesso do S3.`);
    return jsonData;

  } catch (error) {
    console.error('Erro ao ler o arquivo do S3:', error.message);
    throw error;
  }
}


module.exports = { uploadFile, GetFileS3 }