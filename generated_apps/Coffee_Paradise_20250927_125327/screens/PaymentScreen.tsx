import React from 'react';
import { View, Text, Button } from 'react-native';
import { useSelector } from 'react-redux';

const PaymentScreen = () => {
    const cartItems = useSelector(state => state.cart.items);

    return (
        <View>
            <Text>หน้าชำระเงิน</Text>
            {cartItems.map(item => (
                <Text key={item.id}>{item.name} - {item.price} บาท</Text>
            ))}
            <Button title="ชำระเงิน" onPress={() => alert('ชำระเงินสำเร็จ')} />
        </View>
    );
};

export default PaymentScreen;