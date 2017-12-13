import React, { Component } from 'react';
import { CSSTransitionGroup } from 'react-transition-group';
import ceedCar from '../assets/ceed_car.png';

export default class extends Component {
  render() {
    return (
      <CSSTransitionGroup 
        transitionName="wowo" 
        transitionEnterTimeout={1000} 
        transitionLeaveTimeout={1000}>
        <div style={{overflow: 'hidden'}}>
          <img style={{margin: -100, marginLeft: -130 }} width={1600} src={ceedCar} alt="ceed car"/>
        </div>
      </CSSTransitionGroup>
    )
  }
}