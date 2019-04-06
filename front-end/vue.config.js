var fs = require('fs');
var https = require('https');

module.exports = {
    devServer:{
        https: {
            key: fs.readFileSync('SSLcerts/server.key'),
            cert: fs.readFileSync('SSLcerts/server.crt'),
            ca: fs.readFileSync('SSLcerts/rootCA.pem'),
        }
    }
};