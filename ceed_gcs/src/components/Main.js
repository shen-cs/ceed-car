import React, { Component } from 'react';
import { Switch, Route } from 'react-router-dom';
import Home from './Home';
import Canvas from './Canvas';
import Streaming from './Streaming';
export default class extends Component {
  render() {
    return (
      <Switch>
        <Route exact path='/' component={Home}/>
        <Route exact path='/canvas' component={Canvas} />
        <Route exact path='/streaming' component={Streaming}/>
      </Switch>
    )
  }
}
