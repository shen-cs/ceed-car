import React, { Component } from 'react';
import Appbar from '../components/Appbar';
import Main from '../components/Main';
import Footer from '../components/Footer';
import Drawer from '../components/Drawer';
import classnames from 'classnames';
import '../css/App.css';
import '../css/common.css';
class App extends Component {
  state = {
    open: false,
  };
  handleToggle = () => {
    this.setState({open: !this.state.open});
  }
  render() {
    return (
      <div style={{height: '100vh'}} className="column-flex-container">
        <div>
          <Appbar openDrawer={this.handleToggle} open={this.state.open}/>
          <Drawer open={this.state.open} handleToggle={this.handleToggle}/>
        </div>
        <div style={{flex: 1}} className={classnames('app-content', 'column-flex-container', {'expanded': this.state.open})}>
          <div style={{flex: 1, padding: 24, justifyContent:'center'}} className="row-flex-container">
            <Main/>
          </div>
          <div>
            <Footer/>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
