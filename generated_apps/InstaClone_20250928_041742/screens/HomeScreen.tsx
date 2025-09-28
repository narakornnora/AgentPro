import React, { useEffect } from 'react';
import { View, Text, FlatList, ActivityIndicator } from 'react-native';
import { useSelector, useDispatch } from 'react-redux';
import { fetchPosts } from '../redux/actions';

const HomeScreen = () => {
    const dispatch = useDispatch();
    const { posts, loading, error } = useSelector(state => state.posts);

    useEffect(() => {
        dispatch(fetchPosts()); // เรียกใช้ action เพื่อดึงข้อมูลโพสต์
    }, [dispatch]);

    if (loading) return <ActivityIndicator size="large" color="#0000ff" />;
    if (error) return <Text>เกิดข้อผิดพลาด: {error}</Text>;

    return (
        <View>
            <FlatList
                data={posts}
                keyExtractor={item => item.id.toString()}
                renderItem={({ item }) => <Text>{item.title}</Text>}
            />
        </View>
    );
};

export default HomeScreen;