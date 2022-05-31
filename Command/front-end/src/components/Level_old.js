// import "./Level.css";
// import React, { Component } from 'react';
// import { useEffect, useCallback, useState } from "react";



// function refreshPage() {
//     window.location.reload(false);
//   }

// // function mountHandler () {
// //     useEffect(() => {
// //         return refreshPage
// //     },[])
// //     return null
// // }



// class Level extends Component {
    

//     constructor(props){

//         super(props);
      
//         this.state={apiResponse:""};
    
//     }
    
//     // componentDidMount() {
//     //     // Call this function so that it fetch first time right after mounting the component
    
//     //     // set Interval
//     //     this.interval = setInterval(, 7000);
//     // }
    
//     // componentWillUnmount() {
//     //     // Clear the interval right before component unmount
//     //     clearInterval(this.interval);
//     // }

    
      
//     callAPI(){
    
//         fetch("http://localhost:3001/level")
    
//         .then(res =>res.text())
    
//         .then(res =>this.setState({apiResponse: res}));
    
//     }
    
//     componentWillMount(){
    
//         this.callAPI();

//         inputval = 50;
    
//     }


//     render() {

//         return(
//             <div>
            
                
//                 <label for="fuel">Battery Level:</label>

//                 <meter id="fuel"
                    
//                     min="0" max="100"
//                     low="33" high="66" optimum="80"
//                     // value= {this.state.apiResponse}>
//                     value = {inputval} >

                    

//                     refreshPage()

                    
                    
//                 </meter>
//             </div>
//         )
//     }
    
// }



// export default Level;