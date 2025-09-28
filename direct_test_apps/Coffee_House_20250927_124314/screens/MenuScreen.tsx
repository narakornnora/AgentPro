import React, { useContext } from 'react';
import { View, Text, Button, FlatList, StyleSheet } from 'react-native';
import { CartContext } from '../context/CartContext';

const MenuScreen = () => {
    const { addToCart } = useContext(CartContext);

    const coffeeMenu = [
        { id: '1', name: 'Espresso', price: 50 },
        { id: '2', name: 'Latte', price: 60 },
        { id: '3', name: 'Cappuccino', price: 70 },
    ];

    return (
        <View style={styles.container}>
            <Text style={styles.title}>เมนูกาแฟ</Text>
            <FlatList
                data={coffeeMenu}
                keyExtractor={(item) => item.id}
                renderItem={({ item }) => (
                    <View style={styles.itemContainer}>
                        <Text>{item.name} - {item.price} บาท</Text>
                        <Button title="เพิ่มในตะกร้า" onPress={() => addToCart(item)} />
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
        backgroundColor: '#f5f5dc',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 20,
    },
    itemContainer: {
        marginBottom: 15,
        padding: 10,
        backgroundColor: '#fff',
        borderRadius: 5,
        shadowColor: '#000',
        shadowOpacity: 0.1,
        shadowRadius: 5,
        elevation: 3,
    },
});

export default MenuScreen;
