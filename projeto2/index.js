const express = require('express')
const cors = require('cors')
const rssRouter = require('./src/routes/rss.routes')
const path = require('path')

const app = express()
const PORT = process.env.PORT || 80


app.use(cors())
app.use('/rss', rssRouter)
app.use(express.static(path.join(__dirname, 'src', 'templates')))


app.get('/teste', async (req, res) => {
  try {
    res.json({"message" : "No ar..."})
  } catch (error) {
    console.error(error)
    res.status(500).send("Erro ao processar")
  }
})

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'src', 'templates', 'index.html'))
})

app.listen(PORT, async() => {
  console.log(`Servidor rodando em http://localhost:${PORT}`)
  try {
    const feedResponse = await fetch(`http://localhost:${PORT}/rss/api/feed`, { method: 'GET' });
    if (!feedResponse.ok) {
      throw new Error(`Falha no GET /rss/api/feed: ${feedResponse.status} ${feedResponse.statusText}`);
    }
    const feedResult = await feedResponse.json();
    console.log('GET /rss/api/feed invocado com sucesso na inicialização:');
  }catch (error) {
      console.error('Erro ao invocar GET /rss/api/feed na inicialização:', error.message);
  }

})