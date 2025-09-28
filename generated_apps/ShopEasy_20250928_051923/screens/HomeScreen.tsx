import React, { useEffect } from 'react';
import { View, Text, Button, FlatList, ActivityIndicator } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { fetchProducts } from '../actions';

const HomeScreen = ({ navigation }) => {
  const dispatch = useDispatch();
  const { products, loading, error } = useSelector(state => state.product);

  useEffect(() => {
    dispatch(fetchProducts()); // เรียกใช้ action เพื่อดึงข้อมูลสินค้า
  }, [dispatch]);

  if (loading) return <ActivityIndicator size="large" />;
  if (error) return <Text>เกิดข้อผิดพลาด: {error}</Text>;

  return (
    <View>
      <FlatList
        data={products}
        keyExtractor={item => item.id.toString()}
        renderItem={({ item }) => (
          <View>
            <Text>{item.name}</Text>
            <Button title="เพิ่มไปยังตะกร้า" onPress={() => {/* เพิ่มสินค้าไปยังตะกร้า */}} />
          </View>
        )}
      />
      <Button title="ไปที่ตะกร้า" onPress={() => navigation.navigate('Cart')} />
    </View>
  );
};

export default HomeScreen;