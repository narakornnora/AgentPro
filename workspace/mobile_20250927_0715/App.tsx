import React from 'react';
import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  Image,
} from 'react-native';
import {NavigationContainer} from '@react-navigation/native';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import {createStackNavigator} from '@react-navigation/stack';

// =================== SCREENS ===================

// หน้าแรก
function HomeScreen({navigation}: any) {
  const features = ['สะดวกใช้งาน', 'รวดเร็ว', 'ปลอดภัย', 'ทันสมัย'];
  
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentInsetAdjustmentBehavior="automatic">
        <View style={styles.header}>
          <Text style={styles.appTitle}>สร้าง mobile app เลียนแบบ instagram</Text>
          <Text style={styles.appSubtitle}>สร้าง mobile app เลียนแบบ instagram</Text>
        </View>
        
        <View style={styles.heroSection}>
          <Text style={styles.heroTitle}>ยินดีต้อนรับสู่แอปของเรา</Text>
          <Text style={styles.heroDescription}>
            แอปพลิเคชันที่ออกแบบมาเพื่อตอบสนองความต้องการของคุณ
          </Text>
          <TouchableOpacity 
            style={styles.primaryButton}
            onPress={() => navigation.navigate('Services')}
          >
            <Text style={styles.buttonText}>เริ่มใช้งาน</Text>
          </TouchableOpacity>
        </View>
        
        <View style={styles.featuresSection}>
          <Text style={styles.sectionTitle}>ฟีเจอร์หลัก</Text>
          {features.map((feature, index) => (
            <View key={index} style={styles.featureCard}>
              <Text style={styles.featureTitle}>{feature}</Text>
              <Text style={styles.featureDescription}>
                ระบบที่ออกแบบมาเพื่อให้การใช้งาน{feature.toLowerCase()}ที่สุด
              </Text>
            </View>
          ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

// หน้าบริการ
function ServicesScreen() {
  const services = [
    {id: 1, name: 'บริการหลัก', description: 'บริการหลักของเรา', icon: '🌟'},
    {id: 2, name: 'บริการพิเศษ', description: 'บริการพิเศษสำหรับลูกค้า VIP', icon: '💎'},
    {id: 3, name: 'ความช่วยเหลือ', description: 'ทีมซัพพอร์ต 24/7', icon: '🚀'},
    {id: 4, name: 'ตั้งค่า', description: 'ปรับแต่งการใช้งาน', icon: '⚙️'},
  ];

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView>
        <View style={styles.header}>
          <Text style={styles.pageTitle}>บริการของเรา</Text>
        </View>
        
        <View style={styles.servicesGrid}>
          {services.map(service => (
            <TouchableOpacity key={service.id} style={styles.serviceCard}>
              <Text style={styles.serviceIcon}>{service.icon}</Text>
              <Text style={styles.serviceTitle}>{service.name}</Text>
              <Text style={styles.serviceDescription}>{service.description}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

// หน้าโปรไฟล์
function ProfileScreen() {
  const profileOptions = [
    {title: 'แก้ไขโปรไฟล์', icon: '✏️'},
    {title: 'ตั้งค่า', icon: '⚙️'},
    {title: 'ประวัติการใช้งาน', icon: '📋'},
    {title: 'ช่วยเหลือ', icon: '❓'},
    {title: 'เกี่ยวกับ', icon: 'ℹ️'},
    {title: 'ออกจากระบบ', icon: '🚪'},
  ];
  
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView>
        <View style={styles.profileHeader}>
          <View style={styles.avatarContainer}>
            <Text style={styles.avatarText}>👤</Text>
          </View>
          <Text style={styles.profileName}>ผู้ใช้งาน</Text>
          <Text style={styles.profileEmail}>user@example.com</Text>
        </View>
        
        <View style={styles.profileOptions}>
          {profileOptions.map((option, index) => (
            <TouchableOpacity key={index} style={styles.optionItem}>
              <Text style={styles.optionIcon}>{option.icon}</Text>
              <Text style={styles.optionTitle}>{option.title}</Text>
              <Text style={styles.optionArrow}>→</Text>
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

// =================== NAVIGATION ===================

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={
        tabBarActiveTintColor: '#007AFF',
        tabBarInactiveTintColor: '#8E8E93',
        tabBarStyle: {
          backgroundColor: '#FFFFFF',
          borderTopWidth: 1,
          borderTopColor: '#E5E5EA',
        },
        headerShown: false,
      }
    >
      <Tab.Screen 
        name="หน้าแรก" 
        component={HomeScreen}
        options={{
          tabBarIcon: ({color}) => <Text style={{color, fontSize: 20}}>🏠</Text>,
        }}
      />
      <Tab.Screen 
        name="Services" 
        component={ServicesScreen}
        options={{
          tabBarLabel: 'บริการ',
          tabBarIcon: ({color}) => <Text style={{color, fontSize: 20}}>🛎️</Text>,
        }}
      />
      <Tab.Screen 
        name="โปรไฟล์" 
        component={ProfileScreen}
        options={{
          tabBarIcon: ({color}) => <Text style={{color, fontSize: 20}}>👤</Text>,
        }}
      />
    </Tab.Navigator>
  );
}

// =================== MAIN APP ===================

function App(): JSX.Element {
  return (
    <NavigationContainer>
      <StatusBar barStyle="dark-content" backgroundColor="#FFFFFF" />
      <Stack.Navigator screenOptions={{headerShown: false}}>
        <Stack.Screen name="MainTabs" component={MainTabs} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// =================== STYLES ===================

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
  },
  header: {
    padding: 20,
    backgroundColor: '#F8F9FA',
    borderBottomWidth: 1,
    borderBottomColor: '#E5E5EA',
  },
  appTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1D1D1F',
    textAlign: 'center',
  },
  appSubtitle: {
    fontSize: 16,
    color: '#86868B',
    textAlign: 'center',
    marginTop: 5,
  },
  pageTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1D1D1F',
    textAlign: 'center',
  },
  heroSection: {
    padding: 30,
    alignItems: 'center',
    backgroundColor: '#007AFF',
    margin: 20,
    borderRadius: 15,
  },
  heroTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FFFFFF',
    textAlign: 'center',
    marginBottom: 10,
  },
  heroDescription: {
    fontSize: 16,
    color: '#FFFFFF',
    textAlign: 'center',
    marginBottom: 20,
    lineHeight: 24,
  },
  primaryButton: {
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 25,
  },
  buttonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#007AFF',
  },
  featuresSection: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1D1D1F',
    marginBottom: 15,
  },
  featureCard: {
    backgroundColor: '#F8F9FA',
    padding: 20,
    borderRadius: 12,
    marginBottom: 15,
  },
  featureTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1D1D1F',
    marginBottom: 5,
  },
  featureDescription: {
    fontSize: 14,
    color: '#86868B',
    lineHeight: 20,
  },
  servicesGrid: {
    padding: 20,
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  serviceCard: {
    width: '48%',
    backgroundColor: '#F8F9FA',
    padding: 20,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: 15,
  },
  serviceIcon: {
    fontSize: 30,
    marginBottom: 10,
  },
  serviceTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1D1D1F',
    textAlign: 'center',
    marginBottom: 5,
  },
  serviceDescription: {
    fontSize: 12,
    color: '#86868B',
    textAlign: 'center',
    lineHeight: 16,
  },
  profileHeader: {
    alignItems: 'center',
    padding: 30,
    backgroundColor: '#F8F9FA',
  },
  avatarContainer: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#007AFF',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 15,
  },
  avatarText: {
    fontSize: 30,
    color: '#FFFFFF',
  },
  profileName: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1D1D1F',
    marginBottom: 5,
  },
  profileEmail: {
    fontSize: 14,
    color: '#86868B',
  },
  profileOptions: {
    padding: 20,
  },
  optionItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F8F9FA',
    padding: 15,
    borderRadius: 12,
    marginBottom: 10,
  },
  optionIcon: {
    fontSize: 20,
    marginRight: 15,
  },
  optionTitle: {
    flex: 1,
    fontSize: 16,
    color: '#1D1D1F',
  },
  optionArrow: {
    fontSize: 16,
    color: '#86868B',
  },
});

export default App;