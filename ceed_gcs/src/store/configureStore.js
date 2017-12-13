import { createStore } from 'redux';
import reducer from '../redux';


const store = createStore(
  reducer
);

export default store;