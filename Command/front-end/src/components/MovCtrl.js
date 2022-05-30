import React from "react";
import "./MovCtrl.css";
import { useState, useEffect, Components } from 'react';
import {io} from 'socket.io-client';
import Socket from "./Socket";
import Axios from 'axios';



        


class MovCtrl extends React.Component {


        
    state = {
        direction : ''
    }




    componentDidMount() {
        Axios.get("http://localhost:3001/mov_ctrl")
            .then(res => {
            const direction = res.data;
            this.setState({ direction });
            })
        
        
    }

    upfunc(){
        this.state.direction = 'UP';
    }

    render() {
       
        this.state.direction = 'down';
        this.state.direction = 'down';
        

        return (
            
            <div class = "MovCtrl" id=""> 
                <button onClick={this.upfunc()} class="button forward">forward!</button> 
                <button class="button backward" onClick={ Socket.emit('direction', 'DOWN')}>backward!</button> 
                <button class="button left" onClick={ Socket.emit('direction','LEFT')}>left!</button> 
                <button class="button right" onClick={ Socket.emit('direction','RIGHT')}>right!</button> 
                
            </div>
        )

    }
}


        
export default MovCtrl;  


// React.useEffect(()=>{
    //     // const socket = io('http://localhost:10000')
    //     Socket.on('connect', ()=>console.log(Socket.id))
    //     Socket.on('connect_error', ()=>{
    //       setTimeout(()=>Socket.connect(),10000)
    //     })


    // //    socket.on('move_up', ()=>move_up())
    // //    socket.on('move_down', ()=>move_down())
    // //    socket.on('move_left', ()=>move_left())
    // //    socket.on('move_right', ()=>move_right())
     
    //  },[])
// useEffect -> fetch instr
// sending: use header: how to interpret, body: contains data 


// const socket = io('http://localhost:10000');





// function move_up(){
//     //send cmnd to API Node: move_up

//     // fetch('http://localhost:3001/mov_ctrl', {
//     //     method: 'POST',
//     //     headers: {
//     //         'Content-type': 'application/json'
//     //     },
//     //     body: JSON.stringify('UP')
//     // }).then(()=> {
//     //     console.log('UP Pressed')
//     // })        



//     //  (res => res.json());
//     // .then(data => console.log(data));



//     sockets.emit('message', 'UP');
  
// }

// function move_down(){
//     //send cmnd to API Node: move_down
    
  
// }


// function move_left(){
//     //send cmnd to API Node: move_left

  
// }

// function move_right(){
//     //send cmnd to API Node: move_right

  
// }


// const url = "http://localhost:3000/loginAsTeacher";
// if(loginAs === "loginTeacher"){
//     Axios.get(url,{ 
//         params :{
//             email: "abc123@gmail.com",
//             password: "abc1234*"
//         }
//     })
//     .then(res => console.log(res)) // this line return status:200 and data:null
//     .catch(err => console.log(err.message))
// }


// const url = "http://localhost:3000/move_ctrl";
        
//         Axios.get(url,{ 
//             params :{
//                 direction: "UP"
//             }
//         })
//         .then(res => console.log(res)) // this line return status:200 and data:null
//         .catch(err => console.log(err.message))
    // constructor(props){

    //     super(props);
      
    //     this.state={apiResponse:""};
    
    // }