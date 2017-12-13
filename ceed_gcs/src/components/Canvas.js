import React, { Component } from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import { drawMap, drawPath } from '../util';
import '../css/common.css';
export default class extends Component {

  updateMap = (map) => {
    const ctx = this.refs.canvas1.getContext('2d');
    ctx.lineWidth = 2;
    drawMap(ctx, map);
  }
  updatePath = (path) => {
    const ctx = this.refs.canvas2.getContext('2d');
    ctx.lineWidth = 2;
    drawPath(ctx, path);
  }

  handleClear = (isMap) => () => {
    const canvas = isMap ? this.refs.canvas1 : this.refs.canvas2;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height)
  }
  handleUpload = (isMap) => (e) => {
    this.handleClear(isMap)();
    const file = e.target.files[0];
    let reader = new FileReader();
    reader.onload = (event) => {
       const result = event.target.result;
       if(isMap) this.updateMap(result);
       else this.updatePath(result);
    } 
    reader.readAsText(file);
  }
  render() {
    return (
      <div style={{flex: 1, }} className="row-flex-container">
        <div className="column-flex-container" >
          <canvas height="700" width="700" ref="canvas1"/>
          <RaisedButton label="clear" onClick={this.handleClear(true)}/>
        </div>
        <div style={{width: 3, height: 650, backgroundColor: '#BDBDBD', marginLeft:10, marginRight: 10}}/>
        <div className="column-flex-container">
          <canvas height="700" width="700" ref="canvas2"/>
          <RaisedButton label="clear" onClick={this.handleClear(false)}/>
        </div>
        <div style={{marginTop: 30}}>
          <div>
            <p style={{fontSize: 20}}>Select map file.</p>
            <input type="file" onChange={this.handleUpload(true)}/>
          </div>
          <div>
            <p style={{fontSize: 20}}>Select path file.</p>
            <input type="file" onChange={this.handleUpload(false)}/>
          </div>
        </div>
      </div>
    )
  }
}
