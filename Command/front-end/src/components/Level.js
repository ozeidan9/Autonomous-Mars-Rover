import React from "react";
import "./Level.css";

let inputval = 60;
const Level = () => (

    <div>
                
        <label for="fuel">Battery Level:</label>

        <meter id="fuel"
            
            min="0" max="100"
            low="33" high="66" optimum="80"
            // value= {this.state.apiResponse}>
            value = {inputval} >
       
            {/* refreshPage() */}

            
            
        </meter>
    </div>

);


export default Level;
