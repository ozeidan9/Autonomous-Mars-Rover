var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var cors=require("cors");
var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');
var mov_ctrlRouter = require('./routes/mov_ctrl');
var testAPIRouter = require('./routes/testAPI');
var level = require('./routes/level');          //level added
var app = express();


// app.listen(3000) //added by omar


// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(cors());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);
app.use('/mov_ctrl', mov_ctrlRouter);
app.use('/testAPI', testAPIRouter);
app.use('/level', level);                       //level added




var net = require('net');
var server = net.createServer();    
server.on('connection', handleConnection);
server.listen(9000, function() {    
  console.log('server listening to %j', server.address());  
});

function handleConnection(conn) {    
  var remoteAddress = conn.remoteAddress + ':' + conn.remotePort;  
  console.log('new client connection from %s', remoteAddress);
  conn.setEncoding('utf8');

  conn.on('data', onConnData);  
  conn.once('close', onConnClose);  
  conn.on('error', onConnError);



  function onConnData(d) {  
    console.log('connection data from %s: %j', remoteAddress, d);  


    if (d.toUpperCase()=='0'){
      console.log(d.toUpperCase());
      conn.write('N'); 

    }

    if (d.toUpperCase()=='1'){
      console.log(d.toUpperCase());
      conn.write('Y');
    }

    // console.log(d.toUpperCase());

    
  }
  function onConnClose() {  
    console.log('connection from %s closed', remoteAddress);  
  }
  function onConnError(err) {  
    console.log('Connection %s error: %s', remoteAddress, err.message);  
  }  
}








// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});







module.exports = app;
