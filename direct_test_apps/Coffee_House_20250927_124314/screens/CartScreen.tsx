import React, { useContext } from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import { CartContext } from '../context/CartContext';

const CartScreen = () => {
    const { cartItems, clearCart } = useContext(CartContext);

    return (
        <View style={styles.container}>
            <Text style={styles.title}>ตะกร้าสินค้า</Text>
            {cartItems.length === 0 ? (
                <Text>ไม่มีสินค้าในตะกร้า</Text>
            ) : (
                cartItems.map((item) => (
                    <Text key={item.id}>{item.name} - {item.price} บาท</Text>
                ))
            )}
            <Button title="ชำระเงิน" onPress={() => { /* Handle payment */ }} />
            <Button title="ล้างตะกร้า" onPress={clearCart} />
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
});

export default CartScreen;
