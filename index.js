const express = require('express')
const {spawn} = require('child_process');
const path = require('path');
const app = express()
const port = 3000

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '/index.html'));
})

app.get('/python', (req, res) => {
var largeDataSet = [];
 // spawn new child process to call the python script
 const python = spawn('python3', ['bg_removal.py']);
 // collect data from script
 python.stdout.on('data', function (data) {
  console.log('Pipe data from python script ...');
  largeDataSet.push(data);
 });
 // in close event we are sure that stream is from child process is closed
 python.on('close', (code) => {
 console.log(`child process close all stdio with code ${code}`);
 // send data to browser
 res.sendFile(path.join(__dirname, '/success.html'));
 });
 
})
app.listen(port, () => console.log(`Image app listening on port ${port}!`))