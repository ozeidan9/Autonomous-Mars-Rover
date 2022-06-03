import React from "react";
import "./Level.css";

let inputval = 60;
const Level = () => (

    <div>
                
        <h3>Battery Level</h3>

        <meter id="fuel"
            
            min="0" max="100"
            low="33" high="66" optimum="80"
            value = {inputval} >
       
            
        </meter>
    </div>

);


export default Level;
