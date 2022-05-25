// client/src/App.js

import "./App.css";
import React from "react";
import Home from "./Home";
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import ReactDOM from 'react-dom';



function App() {

  return (
    <Router>

      <Switch>
        <div className="App-body">
          <Route path='/' exact component={Home} />
        </div>

      </Switch>
    </Router>
      
  );
}

export default App;