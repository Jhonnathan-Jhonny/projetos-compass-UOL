const express = require("express")
const rssRouter = express.Router()

const RssController = require('../controllers/RssController')
const rssController = new RssController()

rssRouter.get('/api/feed', async (req, res) => {
  await rssController.extrairRSS(req, res)
})


rssRouter.get('/data', async (req, res) => {
  await rssController.recuperar(req, res)
})

module.exports = rssRouter
