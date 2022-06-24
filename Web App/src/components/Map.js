import React, { useState, useEffect } from 'react';
import "./Map.css";
import Image from "./comp-resources/Mapped_Unknown.jpg"

// function Map(e){
//     e.preventDefault();

//     return(
//         <div class = "map" id=""> 
//             <h2>Arena Map</h2>
//             <img src = {Image}/> 
//         </div>
//     );
// }

const Map = () => (

    // <meta http-equiv="refresh" content="5" >
        <div class = "map" id=""> 
            <h2>Arena Map</h2>
            <img src={Image} /> 
        </div>
    // </meta>
);

export default Map;