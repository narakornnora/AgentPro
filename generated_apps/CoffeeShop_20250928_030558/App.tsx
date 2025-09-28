import React, { useState, useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeScreen from './screens/HomeScreen';
import { SafeAreaView, ActivityIndicator, View } from 'react-native';

const Stack = createNativeStackNavigator();

const App = () => {
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // จำลองการโหลดข้อมูล
        const loadData = async () => {
            try {
                // ทำการโหลดข้อมูลที่จำเป็น
                await new Promise(resolve => setTimeout(resolve, 2000));
                setLoading(false);
            } catch (error) {
                console.error('Error loading data:', error);
                setLoading(false);
            }
        };
        loadData();
    }, []);

    if (loading) {
        return (
            <SafeAreaView style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
                <ActivityIndicator size="large" color="#0000ff" />
            </SafeAreaView>
        );
    }

    return (
        <NavigationContainer>
            <Stack.Navigator initialRouteName="Home">
                <Stack.Screen name="Home" component={HomeScreen} />
            </Stack.Navigator>
        </NavigationContainer>
    );
};

export default App;