fetch('/rss/data')
  .then(res => res.json())
  .then(data => {
    const container = document.getElementById('noticias')

    data.forEach(item => {
      const div = document.createElement('div')
      div.className = 'card-container'
      div.innerHTML = `
        <h3>${item.title}</h3>
        <p>${item.contentSnippet}</p>
        <div class="ctn-btn">
          <a href="${item.link}" target="_blank" class="button">
            <div class="ctn-btn-hr">
              <p>Ler Mais</p>
            </div>
          </a>
        </div>
        <span class="spn-footer">${item.pubDate}</span>
      `;
      container.appendChild(div)
    })
  })
.catch(err => {
    console.error("Erro ao carregar feed:", err)
    const container = document.getElementById('noticias')
    container.innerHTML = "<p>Erro ao carregar as notícias.</p>"
})
