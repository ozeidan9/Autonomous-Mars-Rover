import React, { useState, useEffect, useRef, setActive} from 'react'
import { View, Text, StyleSheet, Animated, TouchableOpacity, SafeAreaView, Dimensions } from 'react-native'


function sendAPI_manual(){

    try {
        fetch('http://192.168.43.50:11000/mode', {
        method : 'post',
        mode : 'no-cors',
        headers : {
            'Accept' : 'application/json',
            'Content-type' : 'application/json'
        },
        body : JSON.stringify({
            mode: '1793', 
                   
        })
        });
    }catch(e){
        console.log(e);
    }
}


function sendAPI_auto(){

    try {
        fetch('http://192.168.43.50:11000/mode', {
        method : 'post',
        mode : 'no-cors',
        headers : {
            'Accept' : 'application/json',
            'Content-type' : 'application/json'
        },
        body : JSON.stringify({
            mode: '1794', 
        })
        });
    }catch(e){
        console.log(e);
    }
}


const Slide = () => {
  const [active, setActive] = useState(false)
  let transformX = useRef(new Animated.Value(0)).current

  useEffect(() => {
    if (active) {
      Animated.timing(transformX, {
        toValue: 1,
        duration: 300,
        useNativeDriver: true
      }).start()
    } else {
      Animated.timing(transformX, {
        toValue: 0,
        duration: 300,
        useNativeDriver: true
      }).start()
    }
  }, [active]);


  const rotationX = transformX.interpolate({
    inputRange: [0, 1],
    outputRange: [2, Dimensions.get('screen').width / 2]
  })


  return (
    <SafeAreaView style={{
      flex: 1,
      alignItems: 'center',
      top: 140
    }}>
      <View style={{
        flexDirection: 'row',
        position: 'relative',
        height: 50,
        borderRadius: 10,
        backgroundColor: '#efebf0',
        marginHorizontal: 5
      }}>
        <Animated.View
          style={{
            position: 'absolute',
            height: 50 - 2*2,
            top: 2,
            bottom: 2,
            borderRadius: 10,
            width: Dimensions.get('screen').width / 2 - 2 - 5*2,
            transform: [
              {
                translateX: rotationX
              }
            ],
            backgroundColor: 'white',
          }}
        >
        </Animated.View>
        <TouchableOpacity style={{
          flex: 1,
          justifyContent: 'center',
          alignItems: 'center'
        }} onPress={() => { setActive(false);  sendAPI_manual(); }}>
          <Text>
            Manual
        </Text>
        </TouchableOpacity>
        <TouchableOpacity style={{
          flex: 1,
          justifyContent: 'center',
          alignItems: 'center'
        }} onPress={() => { setActive(true); sendAPI_auto(); }}>
          <Text>
            Auto
        </Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  )
}
export default Slide

