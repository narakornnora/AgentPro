import React, { useEffect } from 'react';
import { View, Text, FlatList, ActivityIndicator } from 'react-native';
import { useSelector } from 'react-redux';

const HomeScreen = () => {
    const posts = useSelector(state => state.posts);
    const loading = posts.length === 0;

    // Simulate fetching data
    useEffect(() => {
        // Fetch posts from API
    }, []);

    return (
        <View style={{ flex: 1, padding: 10 }}>
            {loading ? (
                <ActivityIndicator size="large" color="#0000ff" />
            ) : (
                <FlatList
                    data={posts}
                    keyExtractor={(item) => item.id}
                    renderItem={({ item }) => (
                        <View style={{ marginBottom: 10 }}>
                            <Text>{item.title}</Text>
                        </View>
                    )}
                />
            )}
        </View>
    );
};

export default HomeScreen;