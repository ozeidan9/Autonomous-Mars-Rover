import "./Level.css";
import React, { Component } from 'react';

function refreshPage() {
    window.location.reload(false);
  }

  function refresh() {
    window .location.reload();
}


class Level extends Component {

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
            <div>
            
                
                refresh()

                <label for="fuel">Battery Level:</label>

                <meter id="fuel"
                    
                    min="0" max="100"
                    low="33" high="66" optimum="80"
                    value= {this.state.apiResponse}>
                    
                    refreshPage();

                    
                    
                </meter>
            </div>
        )
    }
    
}



export default Level;