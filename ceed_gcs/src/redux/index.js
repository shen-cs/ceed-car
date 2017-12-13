import { combineReducers } from 'redux';
import streaming from './streamingRedux';

const rootReducer = combineReducers({
  streaming,
})
export default rootReducer;