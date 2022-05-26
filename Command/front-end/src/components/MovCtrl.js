import React from "react";
import "./MovCtrl.css";
import { useState, useEffect } from 'react';

// useEffect -> fetch instr
// sending: use header: how to interpret, body: contains data 



function move_up(){
    //send cmnd to API Node: move_up

    useEffect( () => {
        fetch('/mov_ctrl', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json'
            },
            body: JSON.stringify('UP')
        })
        .then(res => res.json())
        .then(data => console.log(data))
    },[])
  
}

function move_down(){
    //send cmnd to API Node: move_down
    
  
}


function move_left(){
    //send cmnd to API Node: move_left

  
}

function move_right(){
    //send cmnd to API Node: move_right

  
}


const MovCtrl = () => (

    <div class = "MovCtrl" id=""> 
         <button class="button forward" onClick="move_up()">forward!</button> 
         <button class="button backward" onClick="move_down()">backward!</button> 
         <button class="button left" onClick="move_left()">left!</button> 
         <button class="button right" onClick="move_right()">right!</button> 
    </div>

);


export default MovCtrl;