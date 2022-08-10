import React, { useState, useEffect, useRef, setActive} from 'react'
import { View, Text, StyleSheet, Animated, TouchableOpacity, SafeAreaView, Dimensions } from 'react-native'

function sendAPI_radar_on(){

    try {
        fetch('http://192.168.43.50:11000/toggle', {
        method : 'post',
        mode : 'no-cors',
        headers : {
            'Accept' : 'application/json',
            'Content-type' : 'application/json'
        },
        body : JSON.stringify({
            toggle: '2049', //0001000000000001
        })
        });
    }catch(e){
        console.log(e);
    }
}

function sendAPI_radar_off(){

    try {
        fetch('http://192.168.43.50:11000/toggle', {
        method : 'post',
        mode : 'no-cors',
        headers : {
            'Accept' : 'application/json',
            'Content-type' : 'application/json'
        },
        body : JSON.stringify({
            toggle: '2050', //0001000000000010
        })
        });
    }catch(e){
        console.log(e);
    }
}


const ToggleVision = () => {
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
            top: 80
        }}>
            <View style={{
            flexDirection: 'row',
              position: 'relative',
            height: 35,
            borderRadius: 10,
            backgroundColor: '#efebf0',
            marginHorizontal: 5,
            }}>
            <Animated.View
                style={{
                position: 'absolute',
                height: 35 - 2*2,
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
            }} onPress={() => { setActive(false);  sendAPI_radar_off(); }}>
                <Text>
                Radar OFF
            </Text>
            </TouchableOpacity>
            <TouchableOpacity style={{
                flex: 1,
                justifyContent: 'center',
                alignItems: 'center'
            }} onPress={() => { setActive(true); sendAPI_radar_on(); }}>
                <Text>
                Radar ON
            </Text>
            </TouchableOpacity>
            </View>
        </SafeAreaView>
        )
      
}
export default ToggleVision

