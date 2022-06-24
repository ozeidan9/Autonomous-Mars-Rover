// client/src/App.js

import "./App.css";
import React, { Component } from 'react';
import Home from "./components/Home";
import Level from "./components/Level";
import Map from "./components/Map";


class App extends React.Component {
    
  constructor(props){

  super(props)


  }


  render() {

    return(
        <body>
          <div class="App-header">
            <Home /> 
          </div>
          <div class="App-level">
            <Level />
          </div>
          
          <div class="App-map">
            <Map />
          </div>
    

            </body>
    )

  }
}


export default App;