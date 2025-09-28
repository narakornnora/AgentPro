import React from 'react';
import { View, Text, Button } from 'react-native';
import { useSelector } from 'react-redux';

const CartScreen = ({ navigation }) => {
    const cartItems = useSelector(state => state.cart.items);

    return (
        <View>
            <Text>ตะกร้าของคุณ</Text>
            {cartItems.map(item => (
                <Text key={item.id}>{item.name} - {item.price} บาท</Text>
            ))}
            <Button title="ไปที่ชำระเงิน" onPress={() => navigation.navigate('Payment')} />
        </View>
    );
};

export default CartScreen;