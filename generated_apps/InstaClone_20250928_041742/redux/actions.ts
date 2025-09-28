import { FETCH_POSTS_REQUEST, FETCH_POSTS_SUCCESS, FETCH_POSTS_FAILURE } from './types';

export const fetchPosts = () => async dispatch => {
    dispatch({ type: FETCH_POSTS_REQUEST });
    try {
        const response = await fetch('https://jsonplaceholder.typicode.com/posts');
        const data = await response.json();
        dispatch({ type: FETCH_POSTS_SUCCESS, payload: data });
    } catch (error) {
        dispatch({ type: FETCH_POSTS_FAILURE, payload: error.message });
    }
};