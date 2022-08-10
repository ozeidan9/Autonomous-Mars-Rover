import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { Image, ImageBackground, StyleSheet, Text, View } from 'react-native';

import LEFTButton from './components/left_button'
import RIGHTButton from './components/right_button'
import UPButton from './components/up_button'
import DOWNButton from './components/down_button'
import Slide from './components/slide'
import ToggleRadar from  './components/toggle_radar';
import Title from  './components/title';
import Start1 from './components/start1.js';
import Start2 from './components/start2.js';
import Start3 from './components/start3.js';
import Start4 from './components/start4.js';



export default function App() {
 
  return (
    
    <View style={styles.container}>
      {/* <Text style={{fontFamily: 'Mars', fontSize: 25}}>Mars Rover</Text> */}
      <Title/>
      <LEFTButton/>
      <RIGHTButton/>
      <UPButton/>
      <DOWNButton/>
      <Text style={styles.text}>Enter Start Coordinate:</Text>
      <Start1/>
      <Start2/>
      <Start3/>
      <Start4/>
      <Slide/>  
      <ToggleRadar/>

    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#90949C',
    alignItems: 'center',
    justifyContent: 'center',
  },

  text: {
    fontSize: 15,
    position: 'absolute',
    fontWeight: 'bold',
    color: '#036',
    top: 450,
    right: 195
},
 
  
});
