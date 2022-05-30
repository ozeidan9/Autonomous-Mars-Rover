
var express = require('express');
var router = express.Router();
// var io = require('socket.io');


const http = require('http');
// var io = require('socket.io')(http);



// const express = require("express"),
//   router = express(),
//   port = process.env.PORT || 10000,
//   cors = require("cors");


// router.use(cors());
// // console.log('50');
// // router.listen(port, () => console.log("Backend server live on " + port));
// router.listen(port, () => console.log());

// router.get("/", (req, res) => {
// //   res.send({ message: "We did it!" });

// });


// io.on("move_control", (socket) => {
//     socket.on("update item", (arg1, callback) => {
//       console.log(arg1); // UP/DOWN/LEFT/RIGHT
//       console.log('test');
//       callback({
//         status: "ok"
//       });
//     });
// });


router.post("", async (req,res)=>{
    // values coming from the client
    // const recv_direction = req.query.direction;
    // console.log(recv_direction); // this line return {} empty object
    // get data of that user by his/her mail
    // const buttondata = await myModel.findOne({
    // const buttondata = ({
    //     recv_direction
    // // // }).exec()
    // })


    const { 
        direction
       } = req.body.direction;

    res.status(200).json({
        status: 200,
        data: direction
    })

    console.log(direction); //omar added
    console.log('hi');
}) 



// router.get('', function(req, res, next) {
//     // res.send("Testing123")
//     const direction = req.params.direction;
    
//     print(direction)


//     if (direction == up){
//         req.status(200).json({
//             message: 'you pressed up on the controller',
//             direction : up
//         })
//     } if (direction == down){
//         req.status(200).json({
//             message: 'you pressed down on the controller',
//             direction : down
//         })
//     } if (direction == left){
//         req.status(200).json({
//             message: 'you pressed left on the controller',
//             direction : left
//         })
//     } if (direction == right){
//         req.status(200).json({
//             message: 'you pressed right on the controller',
//             direction : right
//         })
//     }

// });


module.exports = router;