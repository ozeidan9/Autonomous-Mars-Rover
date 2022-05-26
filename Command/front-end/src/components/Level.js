import React from "react";
import "./Level.css";


const Level = () => (
    <div>
        <label for="fuel">Battery Level:</label>

        <meter id="fuel"
            
            min="0" max="100"
            low="33" high="66" optimum="80"
            value="70">
            
            at 70/100
        </meter>
    </div>


);


export default Level;