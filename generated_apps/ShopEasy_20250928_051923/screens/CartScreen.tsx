import React from 'react';
import { View, Text, Button } from 'react-native';
import { useSelector } from 'react-redux';

const CartScreen = () => {
  const cartItems = useSelector(state => state.cart.items);

  return (
    <View>
      <Text>ตะกร้าสินค้า</Text>
      {cartItems.length === 0 ? (
        <Text>ไม่มีสินค้าในตะกร้า</Text>
      ) : (
        cartItems.map(item => (
          <View key={item.id}>
            <Text>{item.name}</Text>
          </View>
        ))
      )}
      <Button title="สั่งซื้อ" onPress={() => {/* ฟังก์ชันสั่งซื้อ */}} />
    </View>
  );
};

export default CartScreen;