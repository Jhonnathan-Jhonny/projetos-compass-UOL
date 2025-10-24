const fs = require('fs');
const rssParser = require('rss-parser')
const parser = new rssParser
const { uploadFile, GetFileS3 } = require('../services/s3Service')

class RssController {
    constructor(s3Service) {
        this.s3Service = s3Service;
        this.feedUrl = 'https://jcnoticias.jornaldaciencia.org.br/feed/'
    }

    async extrairRSS(req,res){
        try{
            const feed = await parser.parseURL(this.feedUrl)
            console.log(`Feed '${feed.title}' processado com sucesso.`)

            const formattedItems = feed.items.slice(0,5).map(item => ({
            title: item.title || 'Sem Titulo',
            link: item.link || '#',
            contentSnippet: item.contentSnippet || 'Nenhum resumo disponivel.',
            pubDate: item.pubDate || 'Data desconhecida',
            }))

            //fs.writeFileSync('data.json', JSON.stringify(formattedItems, null, 2));
            console.log('Arquivo data.json criado com sucesso!');

            await uploadFile("data.json", formattedItems)
            console.log('Arquivo data.json enviado para o bucket com sucesso')
            res.json(formattedItems)
        } catch{
            console.error(`Erro ao buscar ou parsear o feed da URL ${feedUrl}:`, error.message)
            res.status(500).json({ error: `Falha ao carregar o feed: ${error.message}` })
        }
    }


    async recuperar(req, res) {
        try {
            const data = await GetFileS3("data.json")
            res.json(data)

        } catch (error) {
            
            console.error('Erro ao recuperar dados do S3:', error.message)
            res.status(500).json({ error: 'Falha ao recuperar dados do S3' })
        }
    }
}

module.exports = RssController