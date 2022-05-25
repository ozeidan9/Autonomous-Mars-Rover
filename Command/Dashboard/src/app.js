import React, {useState, useEffect} from 'react';
import 'app.css';
import Navbar from './components/Navbar';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import Home from './components/pages/Home';
import {Rect, Circle} from 'react-konva';

function App() {
  
  const [batteryLevel, setBattery] = useState(["unknown","unknown","unknown","unknown"]);

  useEffect(() => {
    Socket.on('batteryLevel', data => {
      setBattery(data);
    });
  }, []);


  return (
    <>
    <Router>
      <Navbar />
      <Switch>
        <Route path='/' exact render={(props) => (
          <Home {...props} batteryLevel={(batteryLevel[0]+batteryLevel[1]+batteryLevel[2]+batteryLevel[3])/4}/>
        )} />
        <Route path='/view' render={(props) => (
          <View {...props} path={roverPath} pos={currPos} obstacle={obstacleSet} stage={[stageX,stageY,stageWidth,stageHeight]}/>
        )} />
        <Route path='/command' render={(props) => (
          <Command {...props} />
        )} />
        <Route path='/power' render={(props) => (
          <Power {...props} cell={energyData1[0]} energyLeft={energyData1[1]} energyFull={energyData1[2]} chargingCycle={energyData2[0]} currentCapacity={energyData2[1]} maxCapacity={energyData2[2]}/>
        )} />
      </Switch>
    </Router>
    </>
  );
}

export default App;