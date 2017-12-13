export const types = {
  IMAGE_UNLOAD: 'IMAGE_UNLOAD',
  IMAGE_LOADING: 'IMAGE_LOADING',
  IMAGE_LOADED: 'IMAGE_LOADED',
  IMAGE_FAIL: 'IMAGE_FAIL'
};

export const streamingActionCreator = {
  unload: () => {
    console.log('unload video');
    let img = document.getElementById('img#video');
    if(img) 
      img.parentElement.removeChild(img);
    return { type: types.IMAGE_UNLOAD }; 
  },
  loading: () => {
    console.log('loading video');
    return { type: types.IMAGE_LOADING}
  },
  loaded: () => {
    return { type: types.IMAGE_LOADED }
  },
  fail: () => {
    return { type: types.IMAGE_FAIL }
  }
};

const initialState = { status: types.IMAGE_UNLOAD };

const reducer = (state=initialState, action) => {
  const { type } = action;
  if(Object.values(types).includes(type)) {
    return { status: type };
  }
  return state;
};

export default reducer;
