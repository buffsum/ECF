const express = require('express');
const http = require('http');
const mongoose = require('mongoose');
const path = require('path');
const app = express();
const port = 5500;

// Middleware pour parser le JSON
app.use(express.json());

// Servir des fichiers statiques depuis le dossier 'public'
app.use(express.static(path.join(__dirname, 'public')));

// Route pour servir register.html
app.get('/register', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'register.html'));
});

// Route de connexion
app.post('/login', (req, res) => {
    const { username, password } = req.body;
    if (username === 'testuser' && password === 'testpassword') {
        res.status(200).send('Login successful');
    } else {
        res.status(401).send('Invalid credentials');
    }
});

// Connexion à MongoDB
const mongoURI = 'mongodb://localhost:27017/mydatabase';
mongoose.connect(mongoURI, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('MongoDB connected'))
    .catch(err => console.error('MongoDB connection error:', err));

// Créez le serveur HTTP en utilisant l'application Express
const server = http.createServer(app);

// Définissez le timeout du serveur à 5 minutes (300000 millisecondes)
server.setTimeout(300000, () => {
    console.log('Server timeout after 5 minutes of inactivity');
});

// Démarrez le serveur
server.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});

// Gestion des erreurs non gérées
process.on('uncaughtException', (err) => {
    console.error('Uncaught Exception:', err);
    // Optionnel: Arrêter le serveur proprement
    process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled Rejection at:', promise, 'reason:', reason);
    // Optionnel: Arrêter le serveur proprement
    process.exit(1);
});