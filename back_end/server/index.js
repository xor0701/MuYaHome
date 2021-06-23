var express = require('express');
const bodyparser = require('body-parser');
const cors = require('cors');
var app = express(); //express app 생성
var server = require('http').createServer(app);



app.use(bodyparser.json()); //json 형식 파싱하기
app.use(cors()); //cors 적용



require('./router.js')(app);

var port = 8080;

server.listen(port, function() { //8080포트로 서버를 연다.
    console.log("Listening on port: " + port);
});