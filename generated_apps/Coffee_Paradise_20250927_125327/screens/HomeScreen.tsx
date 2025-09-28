import React from 'react';
import { View, Text, Button, FlatList } from 'react-native';
import { useDispatch } from 'react-redux';
import { addToCart } from '../actions/cartActions';

const menuItems = [
    { id: '1', name: 'Espresso', price: 50 },
    { id: '2', name: 'Latte', price: 60 },
    { id: '3', name: 'Cappuccino', price: 70 }
];

const HomeScreen = ({ navigation }) => {
    const dispatch = useDispatch();

    const renderItem = ({ item }) => (
        <View>
            <Text>{item.name} - {item.price} บาท</Text>
            <Button title="เพิ่มลงตะกร้า" onPress={() => dispatch(addToCart(item))} />
        </View>
    );

    return (
        <View>
            <Text>เมนูกาแฟ</Text>
            <FlatList
                data={menuItems}
                renderItem={renderItem}
                keyExtractor={item => item.id}
            />
            <Button title="ไปที่ตะกร้า" onPress={() => navigation.navigate('Cart')} />
        </View>
    );
};

export default HomeScreen;