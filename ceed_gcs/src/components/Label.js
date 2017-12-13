import React, { Component } from 'react';
import { cyan500 } from 'material-ui/styles/colors';
const styles = {
  labelStyleOuter: {
    width: '30px',
    height: '30px',
    borderRadius: '50% 50% 50% 0',
    background: cyan500,
    position: 'absolute',
    transform: 'rotate(-45deg)',
    top: '-40px',
    left: '-9px',
    display: 'flex',
//    justifyContent: 'center',
//    alignItems: 'center'
  },
  labelStyleInner: {
    transform: 'rotate(45deg)',
    color: 'white',
    textAlign: 'center',
    position: 'relative',
    top: '6px',
    right: '-1px',
    fontSize: '14px',
    
  },
};

export default class extends Component {
  render() {
    
    return (
      <div style={styles.labelStyleOuter}>
        <div style={styles.labelStyleInner}>
          {this.props.children}
        </div>
      </div>
    )
  }
}
