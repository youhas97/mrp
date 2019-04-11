/* eslint-disable */

const express = require('express');
const serveStatic = require("serve-static");
const path = require('path');

app = express();

app.use(
    (req, res, next) => {
    if(req.header('x-forwarded-proto') !== 'https')
        res.redirect(`https://${req.header('host')}${req.url}`);
    else
        next();
});

app.use(serveStatic(path.join(__dirname, 'dist')));

const port = process.env.PORT || 8000;
app.listen(port);
