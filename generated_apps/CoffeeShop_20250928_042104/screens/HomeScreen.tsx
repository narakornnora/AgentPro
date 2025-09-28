import React from 'react';
import { View, Text, StyleSheet, FlatList } from 'react-native';

const menuItems = [
    { id: '1', name: 'Espresso', price: '$3.00' },
    { id: '2', name: 'Latte', price: '$4.00' },
    { id: '3', name: 'Cappuccino', price: '$4.50' },
];

const HomeScreen = () => {
    return (
        <View style={styles.container}>
            <Text style={styles.title}>เมนูร้านกาแฟ</Text>
            <FlatList
                data={menuItems}
                keyExtractor={item => item.id}
                renderItem={({ item }) => (
                    <View style={styles.menuItem}>
                        <Text style={styles.itemName}>{item.name}</Text>
                        <Text style={styles.itemPrice}>{item.price}</Text>
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
    menuItem: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        padding: 15,
        borderBottomWidth: 1,
        borderBottomColor: '#ccc',
    },
    itemName: {
        fontSize: 18,
    },
    itemPrice: {
        fontSize: 18,
        color: '#888',
    },
});

export default HomeScreen;