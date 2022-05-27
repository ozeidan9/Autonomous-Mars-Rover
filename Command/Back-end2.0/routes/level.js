var express = require('express');
var router = express.Router();

const prompt = require('prompt');


// const readline = require('readline').createInterface({
//     input: process.stdin,
//     output: process.stdout,
//   });
  
//   readline.question(`What's the battery level?`, value => {
//     console.log(`Level is: ${value}!`);
//     readline.close();

    
//   });


const properties = [
    {
      name: 'level',
      validator: /^[0-9]+$/,
      warning: 'battery level must be only a number'
    }
  ];
  

prompt.start();



// prompt.get(properties, function (err, result) {

//     if (err) {
//         return onErr(err);
//     }
//     console.log('Command-line input received:');
//     console.log('  Battery level: ' + result.level);

//     router.get('', function(req, res, next) {
//         res.send(result.level);
//     });

//     });

// function onErr(err) {
// console.log(err);
// return 1;
// }

let prevlevel = 0;

function ask() {
    // Ask for name until user inputs "done"
    prompt.get(properties, function (err, result) {
        console.log('Command-line input received:');
        console.log('  Battery level: ' + result.level)
        


        if (result.level !== prevlevel) {
            console.log('different value -> send');

            router.get('', function(req, res, next) {
                res.send(result.level);
            });
        } else{
            console.log('same value -> not send');
        }


        prevlevel = result.level;

        ask();
        
    });
}

ask();

module.exports = router;



// let bat_level = {
//     'level' : {value : 100}
// }

// router.get('/battery/:value', (request, response) => {
//     let value = request.params.value
//     if (bat_level[value]){
//         response.json(bat_level[value])
//     }else{
//         response.json('Level Not Found')
//     }
// });


