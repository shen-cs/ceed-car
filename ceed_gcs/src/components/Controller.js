import React, { Component } from 'react';
import right from '../assets/right-arrow.svg';
import '../css/controller.css';

export default class extends Component {
  render() {
    const { cmd } = this.props;
    return (
      <div {...this.props}>
        <table>
          <tbody>
          <tr>
            <td></td>
            <td><img className={'forward ' + (cmd === 'forward' && 'inverted')} src={right} width={75} alt="forward"/></td>
            <td></td>
          </tr>
          <tr>
            <td><img className={'left ' + (cmd === 'left' && 'inverted')} src={right} width={75} alt="left"/></td>
            <td></td>
            <td><img className={(cmd === 'right' && 'inverted') || ''} src={right} width={75} alt="right"/></td>
          </tr>
          <tr>
            <td></td>
            <td><img className={'backward ' + (cmd === 'backward' && 'inverted')} src={right} width={75} alt="backward"/></td>
            <td></td>
          </tr>
          </tbody>
        </table>
      </div>
    )
  }
}