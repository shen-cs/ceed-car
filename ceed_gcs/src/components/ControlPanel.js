import React, { Component } from 'react';
import Controller from './Controller';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import Sliders from './Sliders';
import '../css/common.css';
import '../css/controlPanel.css';

export default class extends Component {
  handleEnter = (e) => {
    if(e.key === 'Enter') {
      //console.log('connect');
      this.props.connBtnClick();
    }
  }
  render() {
    const { ipOnChange, errorIp, connBtnClick, handlePwm, pwm, cmd } = this.props;
    return (
      <div className="column-flex-container address-field">
        <div className="row-flex-container connect-container">
          <TextField id="address" hintText="Enter streaming address with port..."  
            onChange={ipOnChange} style={{marginRight: 20, flex: 1}} errorText={errorIp} onKeyPress={this.handleEnter}/>
          <RaisedButton label="connect" primary onClick={connBtnClick}/>
        </div>
        <Sliders pwm={pwm} handlePwm={handlePwm}/>
        <Controller style={{flex:1}} cmd={cmd} />
      </div>
    )
  }
}
