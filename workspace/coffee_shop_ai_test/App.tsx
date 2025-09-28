```tsx
// App.tsx
import React from 'react';
import { SafeAreaView } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import HomeScreen from './screens/HomeScreen';
import MenuScreen from './screens/MenuScreen';
import CartScreen from './screens/CartScreen';
import PaymentScreen from './screens/PaymentScreen';
import ProfileScreen from './screens/ProfileScreen';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

const App = () => {
  return (
    <NavigationContainer>
      <SafeAreaView style={{ flex: 1 }}>
        <Tab.Navigator>
          <Tab.Screen name="Home" component={HomeScreen} />
          <Tab.Screen name="Menu" component={MenuScreen} />
          <Tab.Screen name="Cart" component={CartScreen} />
          <Tab.Screen name="Profile" component={ProfileScreen} />
        </Tab.Navigator>
      </SafeAreaView>
    </NavigationContainer>
  );
};

export default App;

// screens/HomeScreen.tsx
import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';

const HomeScreen = () => {
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>ยินดีต้อนรับสู่ร้านกาแฟ AI Coffee</Text>
      <Text style={styles.description}>สำรวจเมนูกาแฟที่ดีที่สุดของเรา</Text>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5dc',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#6f4c3e',
  },
  description: {
    fontSize: 18,
    color: '#6f4c3e',
  },
});

export default HomeScreen;

// screens/MenuScreen.tsx
import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';

const MenuScreen = () => {
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>เมนูกาแฟ</Text>
      <Text style={styles.item}>1. เอสเพรสโซ</Text>
      <Text style={styles.item}>2. คาปูชิโน</Text>
      <Text style={styles.item}>3. ลาเต้</Text>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5dc',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#6f4c3e',
  },
  item: {
    fontSize: 18,
    color: '#6f4c3e',
  },
});

export default MenuScreen;

// screens/CartScreen.tsx
import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';

const CartScreen = () => {
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>ตะกร้าสินค้า</Text>
      <Text style={styles.item}>1. เอสเพรสโซ x 1</Text>
      <Text style={styles.item}>2. คาปูชิโน x 2</Text>
      <Text style={styles.total}>รวม: 150 บาท</Text>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5dc',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#6f4c3e',
  },
  item: {
    fontSize: 18,
    color: '#6f4c3e',
  },
  total: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#6f4c3e',
  },
});

export default CartScreen;

// screens/PaymentScreen.tsx
import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';

const PaymentScreen = () => {
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>หน้าชำระเงิน</Text>
      <Text style={styles.paymentInfo}>กรุณากรอกข้อมูลการชำระเงินของคุณ</Text>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5dc',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#6f4c3e',
  },
  paymentInfo: {
    fontSize: 18,
    color: '#6f4c3e',
  },
});

export default PaymentScreen;

// screens/ProfileScreen.tsx
import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';

const ProfileScreen = () => {
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>โปรไฟล์ผู้ใช้</Text>
      <Text style={styles.info}>ชื่อ: ผู้ใช้ตัวอย่าง</Text>
      <Text style={styles.info}>อีเมล: example@example.com</Text>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5dc',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#6f4c3e',
  },
  info: {
    fontSize: 18,
    color: '#6f4c3e',
  },
});

export default ProfileScreen;
```