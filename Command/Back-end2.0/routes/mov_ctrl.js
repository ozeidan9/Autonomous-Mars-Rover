

var express = require('express');
var router = express.Router();




router.get('', function(req, res, next) {
    res.send("Testing123")
    const direction = req.params.direction;
    
    print(direction)


    if (direction == up){
        req.status(200).json({
            message: 'you pressed up on the controller',
            direction : up
        })
    } if (direction == down){
        req.status(200).json({
            message: 'you pressed down on the controller',
            direction : down
        })
    } if (direction == left){
        req.status(200).json({
            message: 'you pressed left on the controller',
            direction : left
        })
    } if (direction == right){
        req.status(200).json({
            message: 'you pressed right on the controller',
            direction : right
        })
    }

});


module.exports = router;