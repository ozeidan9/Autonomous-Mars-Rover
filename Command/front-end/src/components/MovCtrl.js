import React from "react";
import "./MovCtrl.css";
import { useState, useEffect, Components } from 'react';
import {io} from 'socket.io-client';
import Socket from "./Socket";
import Axios from 'axios';



// const [direction] = useState(null)

        


class MovCtrl extends React.Component {


    // state = {
    //     direction: []
    // }

    // constructor(props) {
    //     super(props);
    //     this.state =({
    //       direction: ['']
    //     })
    // }

    constructor(props) {
        super(props);
        this.state = {
            direction: ''
        }
        

    }
    
    
    

    // constructor(props){

    //     super(props);
      
    //     this.value='default';
    
    // }
    // direction = useState(null)

    // value = '0';

    
    componentDidMount() {
        // Simple POST request with a JSON body using axios
        const controls = { direction: 'UP-special' };
        Axios.post('http://localhost:3001/mov_ctrl', controls);
            // .then(response => this.setState({ articleId: response.data.id }));
    }

    // componentDidMount() {

        
    //     const controls = {
    //         direction: this.state.direction
        
    //     };


    //     Axios.post("http://localhost:3001/mov_ctrl", {...controls})
    //         .then(res => {
    //         // const direction_data = res.data;
    //         // // this.setState({ direction : res.data});
    //         // this.value = direction_data;
    //         console.log(res);
    //         console.log(res.data)
    //         })
        
        
    // }

    // upfunc(){
    //     this.value = 'UP';
    // }

    render() {
       
        // this.setState({
        //     direction : [...this.state.direction, 'UP']
        // })


        // this.state.direction.map (direction =>  {'UP'} );


        // this.setState({
        //     direction: 'UP'
        //   })


        // this.value = 'UP';

        // this.value = 'DOWN';

          
        // this.state.direction = 'down';
        // this.state.direction = 'down';

        

        return (
            
            <div class = "MovCtrl" id=""> 
                <button class="button forward" onClick={()=>alert("up")}>forward!</button> 
                <button class="button backward" onClick={()=>alert("down")}>backward!</button> 
                <button class="button left" onClick={()=>alert("left")}>left!</button> 
                <button class="button right" onClick={()=>alert("right")}>right!</button> 
                
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