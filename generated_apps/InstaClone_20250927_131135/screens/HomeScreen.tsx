import React, { useEffect, useState } from 'react';
import { View, Text, ActivityIndicator, FlatList, StyleSheet } from 'react-native';
import { useSelector, useDispatch } from 'react-redux';
import { fetchPosts } from '../actions';

const HomeScreen = () => {
    const dispatch = useDispatch();
    const posts = useSelector(state => state.posts);
    const loading = useSelector(state => state.loading);

    useEffect(() => {
        dispatch(fetchPosts()); // เรียกข้อมูลโพสต์
    }, [dispatch]);

    if (loading) {
        return <ActivityIndicator size="large" color="#0000ff" />; // แสดง loading
    }

    return (
        <View style={styles.container}>
            <FlatList
                data={posts}
                keyExtractor={item => item.id.toString()}
                renderItem={({ item }) => (
                    <View style={styles.postContainer}>
                        <Text>{item.title}</Text>
                    </View>
                )}
            />
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 10,
    },
    postContainer: {
        marginBottom: 10,
        padding: 10,
        backgroundColor: '#f9f9f9',
        borderRadius: 5,
    },
});

export default HomeScreen;