const express = require('express');
const app = express();
const path = require('path');
const bodyParser = require('body-parser');
const http = require('http');
const sys = require('sys');
const exec = require('child_process').exec;
const server = http.createServer(app);

app.use(bodyParser());
app.set('views', path.join(__dirname, '/views'));
app.set('view engine', 'jade');

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '/views/index.html'));
});

app.post('/', (req, res) => {
    let username = req.body.username;
    let pass = req.body.pass;
    let rounds = req.body.rounds;
    exec(`bash do_round.sh ${username} ${pass} ${rounds}`, (error, stdout, stderr) => {
        if (error) {
            console.log('Error: ', stderr);
            res.sendFile(path.join(__dirname, '/views/error.html'));
        }
        else
            res.sendFile(path.join(__dirname, '/views/success.html'));
        if (stdout)
            console.log('Result: ', stdout);
    });
    console.log(`Got round registration:\nUsername:${username}\nPassword:${pass}\nRound:${rounds}`);    
});

server.listen(80, "0.0.0.0", () => {
    console.log(`Running on ${server.address().address} port:${server.address().port}`);
});