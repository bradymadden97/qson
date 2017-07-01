//Consts and imports
const express = require('express');
const path = require('path');
const spawn = require("child_process").spawn;
const app = express();

//Setup
app.use(express.static(__dirname + '/public'));

//Route functions
function index(req, res){
    var process =  spawn('python', ["qson.py", "-i", "test/test.txt", "-w"]);
    process.stdout.on('data', function (data) {
        res.send(JSON.parse(data));
    });
}

//Routes
app.get("/", function(req, res){
	index(req, res);
});


app.listen(8000);