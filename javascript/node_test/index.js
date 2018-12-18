var http = require('http');
var url = require('url');
var fs = require('fs');

var server = http.createServer(function(req, res) {
    let query = url.parse(req.url, true).query;
    let produce = 'text';
    if ('format' in query) {
        produce = query['format'];
    }
    if (produce == 'text') {
        res.writeHead(200, {'Content-Type': 'text/plain; charset=utf-8'});
        res.write('Hello Http\n');
        res.write(JSON.stringify(query) + '\n');
        let contents = fs.readFileSync('data.txt', 'utf8');
        res.write(contents + '\n');
        res.end('Goodbye');
    } else if (produce == 'html') {
        res.writeHead(200, {'Content-Type': 'text/html; charset=utf-8'});
        res.write('<h1>Hello Http</h1><br>');
        res.write('<pre>' + JSON.stringify(query) + '</pre><br>');
        let contents = fs.readFileSync('data.txt', 'utf8');
        res.write('<p>' + contents + '</p>');
        res.end('<p>Goodbye</p>');
    } else if (produce == 'json') {
        res.writeHead(200, {'Content-Type': 'application/json; charset=utf-8'});
        res.write(JSON.stringify(query, null, 4));
        res.end();
    }
});
server.listen(8080);