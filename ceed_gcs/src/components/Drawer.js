import React, { Component } from 'react';
import Drawer from 'material-ui/Drawer';
import MenuItem from 'material-ui/MenuItem';
import { Link } from 'react-router-dom';
import drawerCar from '../assets/drawerCar.jpg';
import '../css/App.css';

export default class extends Component {
  render() {
    const { handleToggle } = this.props;
    return (
      <Drawer open={this.props.open} docked={true} onRequestChange={handleToggle} width="20%">
        <div>
          <img src={drawerCar} width="100%" alt="ceed car GCS"/>
        </div>
        <div>
          <Link to='/' className="link"><MenuItem onClick={handleToggle}>Home</MenuItem></Link>
          <Link to='/canvas' className="link"><MenuItem onClick={handleToggle}>Map Visualizer</MenuItem></Link>
          <Link to='/streaming' className="link"><MenuItem onClick={handleToggle}>Video Streaming</MenuItem></Link>
        </div>
      </Drawer>
    )
  }
}