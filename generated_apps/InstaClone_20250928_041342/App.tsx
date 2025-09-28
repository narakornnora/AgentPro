import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Provider } from 'react-redux';
import { createStore } from 'redux';
import HomeScreen from './screens/HomeScreen';
import Header from './components/Header';

// Redux reducer
const initialState = { posts: [] };
const reducer = (state = initialState, action) => {
    switch (action.type) {
        case 'ADD_POST':
            return { ...state, posts: [...state.posts, action.payload] };
        default:
            return state;
    }
};

const store = createStore(reducer);

const Stack = createNativeStackNavigator();

const App = () => {
    return (
        <Provider store={store}>
            <NavigationContainer>
                <Header />
                <Stack.Navigator>
                    <Stack.Screen name="Home" component={HomeScreen} />
                </Stack.Navigator>
            </NavigationContainer>
        </Provider>
    );
};

export default App;