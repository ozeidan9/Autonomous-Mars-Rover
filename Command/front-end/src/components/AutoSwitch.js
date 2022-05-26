import React from "react";
import "./AutoSwitch.css";


// function Mswitch(state){
//     //send cmnd to API Node: move_right
//     state=0
//     return(state);
  
// }
// function Aswitch(state){
//     //send cmnd to API Node: move_right
    
//     state=1;
//     return(state);
// }


// function Auto() {
//     let state = 0
//     if (state==0) {

//         return(
//             <div class = "Auto" id=""> 
//                 <button class="button" onClick={state=1}>auto</button>
//                 <button class="button disabled">manual</button> 
//             </div>
//         ); 
        
//     }
//     else{
//         return(
//         <div class = "Auto" id=""> 
//             <button class="button disabled">auto</button>
//             <button class="button" onClick={state=0}>manual</button> 
//         </div>
//         );
//     }
// }

const Auto = ({ isOn, handleToggle, onColor }) => {
    return (
      <>
        <input
          checked={isOn}
          onChange={handleToggle}
          className="react-switch-checkbox"
          id={`react-switch-new`}
          type="checkbox"
        />
        <label
          style={{ background: isOn && onColor }}
          className="react-switch-label"
          htmlFor={`react-switch-new`}
        >
          <span className={`react-switch-button`} />
        </label>
      </>
    );
  };
  

export default Auto;

