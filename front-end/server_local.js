const express = require('express');
const serveStatic = require("serve-static");
const path = require('path');
const https = require('https');
const fs = require('fs');

serverOptions = {
    key: fs.readFileSync('SSLcerts/server.key'),
    cert: fs.readFileSync('SSLcerts/server.crt'),
    ca: fs.readFileSync('SSLcerts/rootCA.pem')
}

app = express();
app.use(serveStatic(path.join(__dirname, 'dist')));

const port = process.env.PORT || 8000;
https.createServer(serverOptions, app).listen(port);
