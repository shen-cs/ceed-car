import React, { Component } from 'react';
import CopyRight from 'material-ui/svg-icons/action/copyright';
import '../css/common.css';
export default class extends Component {
  render() {
    return(
      <div style={{backgroundColor: '#333', height: 100, width: '100%', alignItems: 'center', justifyContent: 'center'}} 
           className="row-flex-container">
        <div style={{ alignItems: 'center'}} className="row-flex-container">
          <CopyRight color='#FFF'/> <span style={{color: '#FFF', marginLeft: 5}}>Created by 2t1t </span>
        </div>
      </div>
    )
  }
}