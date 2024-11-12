const express = require('express')
const app = express()
const port = 3000

let nb = 0;

app.use(express.static('static_files'))

app.get('/', (req, res) => {
    res.send('Hello World!')
})

app.post('/api/click', (req, res) => {
    nb += 1;
    res.send(`<div>Vous avez cliqué ${nb} fois</div><button hx-post="/api/click" hx-swap="innerHTML" hx-target="#main">Clique pour remplacer</button>`);
})

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})
