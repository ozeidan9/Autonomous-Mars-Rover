import React, {useState, useEffect} from 'react';
import './App.css';
import Navbar from './components/Navbar';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import Home from './components/pages/Home';
import {Rect, Circle} from 'react-konva';

function App() { //RETURNS REACT ELEEMENT
  
  const [batteryLevel, setBattery] = useState(["unknown","unknown","unknown","unknown"]);

  useEffect(() => {
    Socket.on('batteryLevel', data => {
      setBattery(data);
    });
  }, []);


  return (
    <>
    
  );
}

export default App;