import React, { Component } from 'react';
import AppBar from 'material-ui/AppBar';
import classnames from 'classnames';
import '../css/appbar.css';
export default class extends Component {
  render() {
    return (
      <AppBar
        title="Ceed Car GCS"
        className={classnames('app-bar', {'expanded': this.props.open})}
        onLeftIconButtonTouchTap={this.props.openDrawer}/>
    )
  }
}
