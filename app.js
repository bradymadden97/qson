//Consts and imports
const express = require('express');
const exphb = 	require('express-handlebars');
const path = require('path');
const spawn = require("child_process").spawn;
const bodyParser = require('body-parser');
const fs = require('fs');
const app = express();

//Handlebars
var hbs = exphb.create({
	defaultLayout: 'main',
	helpers: {
		section: function(name, options){
			if(!this._sections) this._sections = {};
			this._sections[name] = options.fn(this);
			return null;
		}
	},
	partialsDir: __dirname + '/views/partials/'
});

//Setup
app.use(express.static(__dirname + '/public'));
app.use('/css', express.static(__dirname + '/node_modules/materialize-css/dist/css'));
app.use('/js', express.static(__dirname + '/node_modules/materialize-css/dist/js'));
app.use('/js', express.static(__dirname + '/node_modules/materialize-css/node_modules/jquery/dist'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.engine('handlebars', hbs.engine);
app.set('view engine', 'handlebars');

//Route functions
function index(req, res){
    res.render('index', {

    });
};
function parse(req, res){
    var process =  spawn('python', ["qson.py", "-w"]);
    process.stdout.on('data', function (data) {
        res.send(data);
    });
    process.stdin.write(JSON.stringify(req.body.data));
	process.stdin.end();
};
function download(req, res){
	var data = req.body.output;
	fs.writeFile('output.json', data, 'utf8', function(err){
		if(err) throw err;
		res.download('output.json', function(err){
			fs.unlink('output.json', function(err){
				if(err) throw err;
			});
		});
	});
};

//Routes
app.get("/", function(req, res){
    index(req, res);
});
app.post("/parse", function(req, res){
	parse(req, res);
});
app.get("/parse", function(req, res){
	res.redirect("/");
});
app.post("/download", function(req, res){
	download(req, res);
});
app.get("/download", function(req, res){
	res.redirect("/");
});


app.listen(8000);