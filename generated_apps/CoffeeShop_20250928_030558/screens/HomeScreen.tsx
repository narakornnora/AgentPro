import React from 'react';
import { View, Text, StyleSheet, FlatList } from 'react-native';

const menuData = [
    { id: '1', name: 'Espresso', price: '$3' },
    { id: '2', name: 'Latte', price: '$4' },
    { id: '3', name: 'Cappuccino', price: '$4.5' },
];

const HomeScreen = () => {
    return (
        <View style={styles.container}>
            <Text style={styles.title}>เมนูร้านกาแฟ</Text>
            <FlatList
                data={menuData}
                keyExtractor={item => item.id}
                renderItem={({ item }) => (
                    <View style={styles.item}>
                        <Text style={styles.itemText}>{item.name} - {item.price}</Text>
                    </View>
                )}
            />
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 20,
        backgroundColor: '#fff',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 20,
    },
    item: {
        padding: 15,
        borderBottomWidth: 1,
        borderBottomColor: '#ccc',
    },
    itemText: {
        fontSize: 18,
    },
});

export default HomeScreen;