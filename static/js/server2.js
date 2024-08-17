const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();
const port = 3000;

app.use(bodyParser.json());

app.post('/enregistrer-clic', (req, res) => {
    const avisId = req.body.avisId;
    const timestamp = new Date().toISOString();
    const logEntry = `Avis ID: ${avisId}, Timestamp: ${timestamp}\n`;

    fs.appendFile('clics.log', logEntry, (err) => {
        if (err) {
            console.error('Erreur lors de l\'enregistrement du clic', err);
            res.status(500).send('Erreur serveur');
        } else {
            res.status(200).send('Clic enregistré');
        }
    });
});

app.listen(port, () => {
    console.log(`Serveur en écoute sur le port ${port}`);
});