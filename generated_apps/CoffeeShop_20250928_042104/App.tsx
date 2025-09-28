import React, { useState, useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeScreen from './screens/HomeScreen';
import { SafeAreaView, ActivityIndicator } from 'react-native';

const Stack = createNativeStackNavigator();

const App = () => {
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // จำลองการโหลดข้อมูล
        const loadData = async () => {
            try {
                // รอ 2 วินาทีเพื่อจำลองการโหลดข้อมูล
                await new Promise(resolve => setTimeout(resolve, 2000));
            } catch (error) {
                console.error('Error loading data:', error);
            } finally {
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
            <Stack.Navigator>
                <Stack.Screen name="Home" component={HomeScreen} />
            </Stack.Navigator>
        </NavigationContainer>
    );
};

export default App;