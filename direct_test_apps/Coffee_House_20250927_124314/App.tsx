import React, { useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import MenuScreen from './screens/MenuScreen';
import CartScreen from './screens/CartScreen';
import { CartProvider } from './context/CartContext';

const Stack = createStackNavigator();

const App = () => {
    return (
        <CartProvider>
            <NavigationContainer>
                <Stack.Navigator initialRouteName="Menu">
                    <Stack.Screen name="Menu" component={MenuScreen} />
                    <Stack.Screen name="Cart" component={CartScreen} />
                </Stack.Navigator>
            </NavigationContainer>
        </CartProvider>
    );
};

export default App;
