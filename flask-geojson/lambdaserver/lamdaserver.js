/*
openssl genrsa -out key.pem
openssl req -new -key key.pem -out csr.pem
openssl x509 -req -days 9999 -in csr.pem -signkey key.pem -out cert.pem
rm csr.pem
*/
// This is demo Server code (NodeJS) which outputs "hello world".

const https = require('https');
const fs = require('fs');

const options = {
  hostname: '127.0.0.1',
  key: fs.readFileSync('key.pem'),
  cert: fs.readFileSync('cert.pem')
};


https.createServer(options, function (req, res) {
  res.writeHead(200);
  res.end("hello world\n");
}).listen(8000);

// https://127.0.0.1:8000/
