import React, { Component } from 'react';
import { connect } from 'react-redux';
import CircularProgress from 'material-ui/CircularProgress';
import ControlPanel from './ControlPanel';
import { types, streamingActionCreator } from '../redux/streamingRedux';
import '../css/common.css';
import '../css/streaming.css';

const mapStateToProps = (state) => ({
  status: state.streaming.status,
});

class Streaming extends Component {
  
  state = {
    cmd: 'stop',
    ip: null,
    errorText: "",
    pwm: {'l': 60, 'r': 100}
  }

  listenKeyDown = (e) => {
    const key2Cmd = {'ArrowUp': 'forward', 'ArrowDown': 'backward', 'ArrowLeft': 'left', 'ArrowRight': 'right'};
    if(Object.keys(key2Cmd).includes(e.key)) {
      this.handleCmd(key2Cmd[e.key]);
    }
  }

  listenKeyUp = (e) => {
    const key2Cmd = {'ArrowUp': 'forward', 'ArrowDown': 'backward', 'ArrowLeft': 'left', 'ArrowRight': 'right'};
    if(Object.keys(key2Cmd).includes(e.key)) {
      this.handleCmd('stop');
    }
  }
  handleCmd = (cmd) => {
    if(cmd !== this.state.cmd) {
      this.setState({cmd});
      if(this.validateIp(this.state.ip)) {
        fetch('http://'+ this.state.ip + '/' + cmd).then((res) => console.log(res.json()));
      }
    }
  }
  handleIp = (e) => {
    const ip = e.target.value;
    this.setState({ip, errorText:''});
    
  }

  validateIp = (str) => {
    if (/^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):[0-9]{1,5}$/.test(str)) {  
      return true;
    }  
    return false;
  }
  handleConnect = () => {
    const { dispatch } = this.props;
    const valid = this.validateIp(this.state.ip);
    if(valid) {
      dispatch(streamingActionCreator.unload());
      dispatch(streamingActionCreator.loading());
      this.setState({
        errorText: ''
      })
    }
    else {
      this.setState({
        errorText: 'You entered an invalid address.'
      })
    }
  }

  handlePwm = (direction) => (e, val) => {
    let pwmState = {};
    pwmState[direction] = val;
    this.setState({pwm: pwmState})
    let form = new FormData()
    form.append('val', val)
    if(this.state.ip != null) {
      fetch('http://' + this.state.ip + '/pwm_' + direction, {
        method: 'POST',
        body: form
      });
    }
  }
  renderVideo = (status) => {
    const { dispatch } = this.props;
    switch(status) {
      case types.IMAGE_UNLOAD: {
        return (
          <div>
            <p style={{fontSize: 25}}>Enter pi's ip address with port to connect...</p>
          </div>)
      }
      case types.IMAGE_LOADING:{
        return(
          <div>
            <img src={"http://" + this.state.ip + "/video_feed"}
              onLoad={() => dispatch(streamingActionCreator.loaded()) } 
              onError={()=> dispatch(streamingActionCreator.fail())} alt=""/>
            { this.props.status !== types.IMAGE_LOADED &&   
              <CircularProgress size={80} thickness={7}/>
            }
          </div>
        )
      }
      case types.IMAGE_FAIL: {
        return (
          <div>
            <p style={{fontSize: 25, color: 'red'}}>Error!</p>
          </div>
        )
      }
      // IMAGE_LOADED
      default: {
        return (
          <img src={"http://" + this.state.ip + "/video_feed#" + new Date().getTime()} alt=""/>
        )
      }
    }
  }
  componentDidMount() {
    document.addEventListener('keydown', this.listenKeyDown);
    document.addEventListener('keyup', this.listenKeyUp);
    this.handlePwm('l')('', this.state.pwm.l);
    this.handlePwm('r')('', this.state.pwm.r);
  }
  componentWillUnmount() {
    document.removeEventListener('keydown', this.listenKeyDown);
    document.removeEventListener('keyup', this.listenKeyUp);
  }
  render() {
    const { status } = this.props;
    return (
      <div className="row-flex-container" style={{flex: 1}}>
        <div className="stream-container">
          <center><h1>Ceed Car Live Streaming</h1></center>
          <div className="stream-field row-flex-container">
            <div>
              {this.renderVideo(status)}
            </div>
          </div>
        </div>
        <div className="divider"/>
        <ControlPanel ipOnChange={this.handleIp} errorIp={this.state.errorText} pwm={this.state.pwm}
        connBtnClick={this.handleConnect} handlePwm={this.handlePwm} cmd={this.state.cmd}/>
      </div>
    )
  }
}

export default connect(mapStateToProps)(Streaming);
