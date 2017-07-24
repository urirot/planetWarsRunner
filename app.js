const express = require('express');
const app = express();
const path = require('path');
const bodyParser = require('body-parser');
const exec = require('exec');

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
    exec(['bash', 'admintools/do_turn.sh', username, pass, rounds], (err, out, code) => {
        if (err instanceof Error)
            throw err;
        process.stderr.write(err);
        process.stdout.write(out);
        process.exit(code);
    });
    console.log(`${username} ${pass} ${rounds}`);    
});

app.listen(8000, () => {
    console.log('Running on port: ' + 8000);
});