// client/src/App.js

import "./App.css";
import React, { Component } from 'react';
import Home from "./components/Home";
import Level from "./components/Level";
import Map from "./components/Map";
import MovCtrl from "./components/MovCtrl";
import Switcher from "./components/Switcher";
import { Routes ,Route } from 'react-router-dom';










class App extends React.Component {
    
  constructor(props){

  super(props)

  this.state={apiResponse:""};

  }



  callAPI(){

    fetch("http://localhost:3001/level")

     .then(res =>res.text())

     .then(res =>this.setState({apiResponse: res}));

  }

  componentWillMount(){

    this.callAPI();

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
          <div class="App-controller">
            <div class="App-mov">
              <MovCtrl />
            </div>
            
            <div class="App-auto-text">AUTO</div>
            <div class="App-man-text">MANUAL</div>

            <div class="App-auto">
              <Switcher />
            </div>
          </div>
          {/* <p>{this.state.apiResponse}</p> */}
        </body>
    )

  }
}


export default App;