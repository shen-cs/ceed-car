import React from 'react';
import ReactDOM from 'react-dom';
import './css/index.css';
import App from './containers/App';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import { BrowserRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import store from './store/configureStore';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(
  <Provider store={store}>
    <MuiThemeProvider>
        <BrowserRouter>
          <App />
        </BrowserRouter>
    </MuiThemeProvider>
  </Provider>, 
document.getElementById('root'));
registerServiceWorker();
