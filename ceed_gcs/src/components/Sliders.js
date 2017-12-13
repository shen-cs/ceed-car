import React, { Component } from 'react';
import Slider from 'material-ui-slider-label/Slider';
import Label from './Label';
import '../css/controlPanel.css';
import '../css/common.css';

export default class extends Component {
  state = {
    l_dragging: false,
    r_dragging: false
  }
  
  handleDrag = (direction) => () => {
    let dragState = {};
    dragState[direction + '_dragging'] = !this.state[direction + '_dragging'];
    this.setState(dragState);
  }
  render() {
    const { handlePwm, pwm } = this.props;
    return(
      <div className="slider-container">
        <div style={{width: 500}}>
          <div>
            <span>PWM value for left motor</span>
            <Slider min={0} max={100} step={1} value={pwm.l} onChange={handlePwm('l')} label={ this.state.l_dragging && <Label>{pwm.l}</Label>}
              onDragStart={this.handleDrag('l')} onDragStop={this.handleDrag('l')}/>
          </div>
          <div>
            <span>PWM value for right motor</span>
            <Slider min={0} max={100} step={1} value={pwm.r} onChange={handlePwm('r')} label={ this.state.r_dragging && <Label>{pwm.r}</Label>}
              onDragStart={this.handleDrag('r')} onDragStop={this.handleDrag('r')}/>
          </div>
        </div>
      </div>
    )
  }
}
