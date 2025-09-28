import os
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

class MobileAppGenerator:
    """
    🚀 Mobile App Generator - สร้าง Mobile App จริง ๆ
    Support: React Native, Flutter, Ionic
    """
    
    def __init__(self, client=None):
        self.client = client
        self.workspace = Path("C:/agent/workspace")
        self.workspace.mkdir(parents=True, exist_ok=True)
    
    async def generate_mobile_app(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        สร้าง Mobile App ตาม requirements
        """
        try:
            # วิเคราะห์ requirements
            app_type = requirements.get('app_type', 'react_native')
            project_name = requirements.get('project_name', 'mobile_app')
            business_name = requirements.get('business_name', 'My App')
            description = requirements.get('description', 'Mobile Application')
            features = requirements.get('features', [])
            
            # สร้างโฟลเดอร์โปรเจ็กต์
            project_path = self.workspace / project_name
            project_path.mkdir(parents=True, exist_ok=True)
            
            if app_type == 'react_native':
                result = await self._create_react_native_app(project_path, requirements)
            elif app_type == 'flutter':
                result = await self._create_flutter_app(project_path, requirements)
            elif app_type == 'ionic':
                result = await self._create_ionic_app(project_path, requirements)
            else:
                result = await self._create_react_native_app(project_path, requirements)  # default
            
            return {
                'success': True,
                'app_type': app_type,
                'project_path': str(project_path),
                'project_name': project_name,
                'business_name': business_name,
                'files_created': result.get('files_created', 0),
                'features': features,
                'install_commands': result.get('install_commands', []),
                'run_commands': result.get('run_commands', []),
                'message': f'✅ {app_type} Mobile App "{business_name}" สร้างสำเร็จแล้ว!'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'❌ เกิดข้อผิดพลาดในการสร้าง Mobile App: {str(e)}'
            }
    
    async def _create_react_native_app(self, project_path: Path, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        สร้าง React Native App
        """
        business_name = requirements.get('business_name', 'My App')
        description = requirements.get('description', 'React Native Application')
        features = requirements.get('features', [])
        
        files_created = 0
        
        # 1. package.json
        package_json = {
            "name": requirements.get('project_name', 'mobile_app'),
            "version": "1.0.0",
            "description": description,
            "main": "index.js",
            "scripts": {
                "start": "npx react-native start",
                "android": "npx react-native run-android",
                "ios": "npx react-native run-ios",
                "test": "jest",
                "lint": "eslint ."
            },
            "dependencies": {
                "react": "18.2.0",
                "react-native": "0.72.6",
                "@react-navigation/native": "^6.1.9",
                "@react-navigation/stack": "^6.3.20",
                "@react-navigation/bottom-tabs": "^6.5.11",
                "react-native-screens": "^3.25.0",
                "react-native-safe-area-context": "^4.7.4",
                "react-native-gesture-handler": "^2.13.4",
                "react-native-vector-icons": "^10.0.2",
                "axios": "^1.5.0"
            },
            "devDependencies": {
                "@babel/core": "^7.20.0",
                "@babel/preset-env": "^7.20.0",
                "@babel/runtime": "^7.20.0",
                "@react-native/eslint-config": "^0.72.0",
                "@react-native/metro-config": "^0.72.0",
                "@tsconfig/react-native": "^3.0.0",
                "@types/react": "^18.0.24",
                "@types/react-test-renderer": "^18.0.0",
                "babel-jest": "^29.2.1",
                "eslint": "^8.19.0",
                "jest": "^29.2.1",
                "metro-react-native-babel-preset": "0.76.8",
                "prettier": "^2.4.1",
                "react-test-renderer": "18.2.0",
                "typescript": "4.8.4"
            }
        }
        
        with open(project_path / "package.json", "w", encoding="utf-8") as f:
            json.dump(package_json, f, indent=2, ensure_ascii=False)
        files_created += 1
        
        # 2. App.tsx - Main App Component
        app_tsx = f'''import React from 'react';
import {{
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  Image,
}} from 'react-native';
import {{NavigationContainer}} from '@react-navigation/native';
import {{createBottomTabNavigator}} from '@react-navigation/bottom-tabs';
import {{createStackNavigator}} from '@react-navigation/stack';

// =================== SCREENS ===================

// หน้าแรก
function HomeScreen({{navigation}}: any) {{
  const features = ['สะดวกใช้งาน', 'รวดเร็ว', 'ปลอดภัย', 'ทันสมัย'];
  
  return (
    <SafeAreaView style={{styles.container}}>
      <ScrollView contentInsetAdjustmentBehavior="automatic">
        <View style={{styles.header}}>
          <Text style={{styles.appTitle}}>{business_name}</Text>
          <Text style={{styles.appSubtitle}}>{description}</Text>
        </View>
        
        <View style={{styles.heroSection}}>
          <Text style={{styles.heroTitle}}>ยินดีต้อนรับสู่แอปของเรา</Text>
          <Text style={{styles.heroDescription}}>
            แอปพลิเคชันที่ออกแบบมาเพื่อตอบสนองความต้องการของคุณ
          </Text>
          <TouchableOpacity 
            style={{styles.primaryButton}}
            onPress={{() => navigation.navigate('Services')}}
          >
            <Text style={{styles.buttonText}}>เริ่มใช้งาน</Text>
          </TouchableOpacity>
        </View>
        
        <View style={{styles.featuresSection}}>
          <Text style={{styles.sectionTitle}}>ฟีเจอร์หลัก</Text>
          {{features.map((feature, index) => (
            <View key={{index}} style={{styles.featureCard}}>
              <Text style={{styles.featureTitle}}>{{feature}}</Text>
              <Text style={{styles.featureDescription}}>
                ระบบที่ออกแบบมาเพื่อให้การใช้งาน{{feature.toLowerCase()}}ที่สุด
              </Text>
            </View>
          ))}}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}}

// หน้าบริการ
function ServicesScreen() {{
  const services = [
    {{id: 1, name: 'บริการหลัก', description: 'บริการหลักของเรา', icon: '🌟'}},
    {{id: 2, name: 'บริการพิเศษ', description: 'บริการพิเศษสำหรับลูกค้า VIP', icon: '💎'}},
    {{id: 3, name: 'ความช่วยเหลือ', description: 'ทีมซัพพอร์ต 24/7', icon: '🚀'}},
    {{id: 4, name: 'ตั้งค่า', description: 'ปรับแต่งการใช้งาน', icon: '⚙️'}},
  ];

  return (
    <SafeAreaView style={{styles.container}}>
      <ScrollView>
        <View style={{styles.header}}>
          <Text style={{styles.pageTitle}}>บริการของเรา</Text>
        </View>
        
        <View style={{styles.servicesGrid}}>
          {{services.map(service => (
            <TouchableOpacity key={{service.id}} style={{styles.serviceCard}}>
              <Text style={{styles.serviceIcon}}>{{service.icon}}</Text>
              <Text style={{styles.serviceTitle}}>{{service.name}}</Text>
              <Text style={{styles.serviceDescription}}>{{service.description}}</Text>
            </TouchableOpacity>
          ))}}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}}

// หน้าโปรไฟล์
function ProfileScreen() {{
  const profileOptions = [
    {{title: 'แก้ไขโปรไฟล์', icon: '✏️'}},
    {{title: 'ตั้งค่า', icon: '⚙️'}},
    {{title: 'ประวัติการใช้งาน', icon: '📋'}},
    {{title: 'ช่วยเหลือ', icon: '❓'}},
    {{title: 'เกี่ยวกับ', icon: 'ℹ️'}},
    {{title: 'ออกจากระบบ', icon: '🚪'}},
  ];
  
  return (
    <SafeAreaView style={{styles.container}}>
      <ScrollView>
        <View style={{styles.profileHeader}}>
          <View style={{styles.avatarContainer}}>
            <Text style={{styles.avatarText}}>👤</Text>
          </View>
          <Text style={{styles.profileName}}>ผู้ใช้งาน</Text>
          <Text style={{styles.profileEmail}}>user@example.com</Text>
        </View>
        
        <View style={{styles.profileOptions}}>
          {{profileOptions.map((option, index) => (
            <TouchableOpacity key={{index}} style={{styles.optionItem}}>
              <Text style={{styles.optionIcon}}>{{option.icon}}</Text>
              <Text style={{styles.optionTitle}}>{{option.title}}</Text>
              <Text style={{styles.optionArrow}}>→</Text>
            </TouchableOpacity>
          ))}}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}}

// =================== NAVIGATION ===================

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

function MainTabs() {{
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: '#007AFF',
        tabBarInactiveTintColor: '#8E8E93',
        tabBarStyle: {{
          backgroundColor: '#FFFFFF',
          borderTopWidth: 1,
          borderTopColor: '#E5E5EA',
        }},
        headerShown: false,
      }}
    >
      <Tab.Screen 
        name="หน้าแรก" 
        component={{HomeScreen}}
        options={{{{
          tabBarIcon: ({{color}}) => <Text style={{{{color, fontSize: 20}}}}>🏠</Text>,
        }}}}
      />
      <Tab.Screen 
        name="Services" 
        component={{ServicesScreen}}
        options={{{{
          tabBarLabel: 'บริการ',
          tabBarIcon: ({{color}}) => <Text style={{{{color, fontSize: 20}}}}>🛎️</Text>,
        }}}}
      />
      <Tab.Screen 
        name="โปรไฟล์" 
        component={{ProfileScreen}}
        options={{{{
          tabBarIcon: ({{color}}) => <Text style={{{{color, fontSize: 20}}}}>👤</Text>,
        }}}}
      />
    </Tab.Navigator>
  );
}}

// =================== MAIN APP ===================

function App(): JSX.Element {{
  return (
    <NavigationContainer>
      <StatusBar barStyle="dark-content" backgroundColor="#FFFFFF" />
      <Stack.Navigator screenOptions={{{{headerShown: false}}}}>
        <Stack.Screen name="MainTabs" component={{MainTabs}} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}}

// =================== STYLES ===================

const styles = StyleSheet.create({{
  container: {{
    flex: 1,
    backgroundColor: '#FFFFFF',
  }},
  header: {{
    padding: 20,
    backgroundColor: '#F8F9FA',
    borderBottomWidth: 1,
    borderBottomColor: '#E5E5EA',
  }},
  appTitle: {{
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1D1D1F',
    textAlign: 'center',
  }},
  appSubtitle: {{
    fontSize: 16,
    color: '#86868B',
    textAlign: 'center',
    marginTop: 5,
  }},
  pageTitle: {{
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1D1D1F',
    textAlign: 'center',
  }},
  heroSection: {{
    padding: 30,
    alignItems: 'center',
    backgroundColor: '#007AFF',
    margin: 20,
    borderRadius: 15,
  }},
  heroTitle: {{
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FFFFFF',
    textAlign: 'center',
    marginBottom: 10,
  }},
  heroDescription: {{
    fontSize: 16,
    color: '#FFFFFF',
    textAlign: 'center',
    marginBottom: 20,
    lineHeight: 24,
  }},
  primaryButton: {{
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 25,
  }},
  buttonText: {{
    fontSize: 16,
    fontWeight: '600',
    color: '#007AFF',
  }},
  featuresSection: {{
    padding: 20,
  }},
  sectionTitle: {{
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1D1D1F',
    marginBottom: 15,
  }},
  featureCard: {{
    backgroundColor: '#F8F9FA',
    padding: 20,
    borderRadius: 12,
    marginBottom: 15,
  }},
  featureTitle: {{
    fontSize: 18,
    fontWeight: '600',
    color: '#1D1D1F',
    marginBottom: 5,
  }},
  featureDescription: {{
    fontSize: 14,
    color: '#86868B',
    lineHeight: 20,
  }},
  servicesGrid: {{
    padding: 20,
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  }},
  serviceCard: {{
    width: '48%',
    backgroundColor: '#F8F9FA',
    padding: 20,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: 15,
  }},
  serviceIcon: {{
    fontSize: 30,
    marginBottom: 10,
  }},
  serviceTitle: {{
    fontSize: 16,
    fontWeight: '600',
    color: '#1D1D1F',
    textAlign: 'center',
    marginBottom: 5,
  }},
  serviceDescription: {{
    fontSize: 12,
    color: '#86868B',
    textAlign: 'center',
    lineHeight: 16,
  }},
  profileHeader: {{
    alignItems: 'center',
    padding: 30,
    backgroundColor: '#F8F9FA',
  }},
  avatarContainer: {{
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#007AFF',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 15,
  }},
  avatarText: {{
    fontSize: 30,
    color: '#FFFFFF',
  }},
  profileName: {{
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1D1D1F',
    marginBottom: 5,
  }},
  profileEmail: {{
    fontSize: 14,
    color: '#86868B',
  }},
  profileOptions: {{
    padding: 20,
  }},
  optionItem: {{
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F8F9FA',
    padding: 15,
    borderRadius: 12,
    marginBottom: 10,
  }},
  optionIcon: {{
    fontSize: 20,
    marginRight: 15,
  }},
  optionTitle: {{
    flex: 1,
    fontSize: 16,
    color: '#1D1D1F',
  }},
  optionArrow: {{
    fontSize: 16,
    color: '#86868B',
  }},
}});

export default App;'''
        
        with open(project_path / "App.tsx", "w", encoding="utf-8") as f:
            f.write(app_tsx)
        files_created += 1
        
        # 3. index.js
        index_js = '''import {AppRegistry} from 'react-native';
import App from './App';
import {name as appName} from './app.json';

AppRegistry.registerComponent(appName, () => App);'''
        
        with open(project_path / "index.js", "w", encoding="utf-8") as f:
            f.write(index_js)
        files_created += 1
        
        # 4. app.json
        app_json = {
            "name": requirements.get('project_name', 'mobile_app'),
            "displayName": business_name
        }
        
        with open(project_path / "app.json", "w", encoding="utf-8") as f:
            json.dump(app_json, f, indent=2, ensure_ascii=False)
        files_created += 1
        
        # 5. README.md
        readme = f'''# {business_name}

{description}

## 🚀 React Native Mobile App

### การติดตั้ง

1. Install dependencies:
```bash
npm install
# or
yarn install
```

2. สำหรับ iOS:
```bash
cd ios && pod install && cd ..
npm run ios
```

3. สำหรับ Android:
```bash
npm run android
```

### ฟีเจอร์

- ✅ Navigation (Bottom Tabs + Stack)
- ✅ Beautiful UI Design
- ✅ TypeScript Support
- ✅ Responsive Layout
- ✅ Modern Components

### โครงสร้างแอป

- **หน้าแรก**: แสดงข้อมูลหลักและฟีเจอร์
- **บริการ**: รายการบริการทั้งหมด
- **โปรไฟล์**: ข้อมูลผู้ใช้และการตั้งค่า

### การพัฒนา

```bash
npm start          # เริ่ม Metro bundler
npm run android    # รัน Android
npm run ios        # รัน iOS
npm run test       # รันเทส
npm run lint       # ตรวจสอบโค้ด
```

### สร้างโดย AgentPro AI 🤖
วันที่สร้าง: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
'''
        
        with open(project_path / "README.md", "w", encoding="utf-8") as f:
            f.write(readme)
        files_created += 1
        
        return {
            'files_created': files_created,
            'install_commands': [
                'npm install',
                'cd ios && pod install && cd ..',  # สำหรับ iOS
            ],
            'run_commands': [
                'npm start',      # Metro bundler
                'npm run android', # Android
                'npm run ios'     # iOS
            ]
        }
    
    async def _create_flutter_app(self, project_path: Path, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        สร้าง Flutter App
        """
        business_name = requirements.get('business_name', 'My App')
        description = requirements.get('description', 'Flutter Application')
        
        files_created = 0
        
        # 1. pubspec.yaml
        pubspec_yaml = f'''name: {requirements.get('project_name', 'mobile_app').replace('-', '_')}
description: {description}
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'
  flutter: ">=3.10.0"

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2
  http: ^1.1.0
  provider: ^6.0.5
  shared_preferences: ^2.2.2
  cached_network_image: ^3.3.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0

flutter:
  uses-material-design: true'''
        
        with open(project_path / "pubspec.yaml", "w", encoding="utf-8") as f:
            f.write(pubspec_yaml)
        files_created += 1
        
        # 2. lib/main.dart
        lib_dir = project_path / "lib"
        lib_dir.mkdir(exist_ok=True)
        
        main_dart = f'''import 'package:flutter/material.dart';

void main() {{
  runApp(MyApp());
}}

class MyApp extends StatelessWidget {{
  @override
  Widget build(BuildContext context) {{
    return MaterialApp(
      title: '{business_name}',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: MainScreen(),
    );
  }}
}}

class MainScreen extends StatefulWidget {{
  @override
  _MainScreenState createState() => _MainScreenState();
}}

class _MainScreenState extends State<MainScreen> {{
  int _currentIndex = 0;
  
  final List<Widget> _screens = [
    HomeScreen(),
    ServicesScreen(),
    ProfileScreen(),
  ];

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      body: _screens[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {{
          setState(() {{
            _currentIndex = index;
          }});
        }},
        items: [
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'หน้าแรก',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.business),
            label: 'บริการ',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.person),
            label: 'โปรไฟล์',
          ),
        ],
      ),
    );
  }}
}}

// หน้าแรก
class HomeScreen extends StatelessWidget {{
  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: Text('{business_name}'),
        backgroundColor: Colors.blue[600],
        elevation: 0,
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Hero Section
            Container(
              width: double.infinity,
              padding: EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [Colors.blue[600]!, Colors.blue[800]!],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
              ),
              child: Column(
                children: [
                  Text(
                    'ยินดีต้อนรับสู่แอปของเรา',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height: 10),
                  Text(
                    '{description}',
                    style: TextStyle(
                      fontSize: 16,
                      color: Colors.white70,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: () {{}},
                    child: Text('เริ่มใช้งาน'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.white,
                      foregroundColor: Colors.blue[600],
                      padding: EdgeInsets.symmetric(horizontal: 30, vertical: 15),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(25),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            
            // Features Section
            Padding(
              padding: EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'ฟีเจอร์หลัก',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(height: 15),
                  ...['สะดวกใช้งาน', 'รวดเร็ว', 'ปลอดภัย', 'ทันสมัย'].map((feature) => 
                    Card(
                      margin: EdgeInsets.only(bottom: 10),
                      child: ListTile(
                        leading: Icon(Icons.check_circle, color: Colors.green),
                        title: Text(feature),
                        subtitle: Text('ระบบที่ออกแบบมาเพื่อให้การใช้งาน${{feature.toLowerCase()}}ที่สุด'),
                      ),
                    ),
                  ).toList(),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }}
}}

// หน้าบริการ
class ServicesScreen extends StatelessWidget {{
  final List<Map<String, dynamic>> services = [
    {{'name': 'บริการหลัก', 'description': 'บริการหลักของเรา', 'icon': Icons.star}},
    {{'name': 'บริการพิเศษ', 'description': 'บริการพิเศษสำหรับลูกค้า VIP', 'icon': Icons.diamond}},
    {{'name': 'ความช่วยเหลือ', 'description': 'ทีมซัพพอร์ต 24/7', 'icon': Icons.support_agent}},
    {{'name': 'ตั้งค่า', 'description': 'ปรับแต่งการใช้งาน', 'icon': Icons.settings}},
  ];

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: Text('บริการของเรา'),
        backgroundColor: Colors.blue[600],
      ),
      body: GridView.builder(
        padding: EdgeInsets.all(20),
        gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
          crossAxisSpacing: 15,
          mainAxisSpacing: 15,
          childAspectRatio: 0.8,
        ),
        itemCount: services.length,
        itemBuilder: (context, index) {{
          final service = services[index];
          return Card(
            elevation: 3,
            child: InkWell(
              onTap: () {{}},
              child: Padding(
                padding: EdgeInsets.all(15),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      service['icon'],
                      size: 40,
                      color: Colors.blue[600],
                    ),
                    SizedBox(height: 10),
                    Text(
                      service['name'],
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    SizedBox(height: 5),
                    Text(
                      service['description'],
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.grey[600],
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              ),
            ),
          );
        }},
      ),
    );
  }}
}}

// หน้าโปรไฟล์
class ProfileScreen extends StatelessWidget {{
  @override
  Widget build(BuildContext context) {{
    final profileOptions = [
      {{'title': 'แก้ไขโปรไฟล์', 'icon': Icons.edit}},
      {{'title': 'ตั้งค่า', 'icon': Icons.settings}},
      {{'title': 'ประวัติการใช้งาน', 'icon': Icons.history}},
      {{'title': 'ช่วยเหลือ', 'icon': Icons.help}},
      {{'title': 'เกี่ยวกับ', 'icon': Icons.info}},
      {{'title': 'ออกจากระบบ', 'icon': Icons.logout}},
    ];
    
    return Scaffold(
      appBar: AppBar(
        title: Text('โปรไฟล์'),
        backgroundColor: Colors.blue[600],
      ),
      body: Column(
        children: [
          // Profile Header
          Container(
            width: double.infinity,
            padding: EdgeInsets.all(30),
            color: Colors.grey[100],
            child: Column(
              children: [
                CircleAvatar(
                  radius: 40,
                  backgroundColor: Colors.blue[600],
                  child: Icon(
                    Icons.person,
                    size: 40,
                    color: Colors.white,
                  ),
                ),
                SizedBox(height: 15),
                Text(
                  'ผู้ใช้งาน',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                SizedBox(height: 5),
                Text(
                  'user@example.com',
                  style: TextStyle(
                    color: Colors.grey[600],
                  ),
                ),
              ],
            ),
          ),
          
          // Profile Options
          Expanded(
            child: ListView.builder(
              padding: EdgeInsets.all(20),
              itemCount: profileOptions.length,
              itemBuilder: (context, index) {{
                final option = profileOptions[index];
                return Card(
                  margin: EdgeInsets.only(bottom: 10),
                  child: ListTile(
                    leading: Icon(option['icon']),
                    title: Text(option['title']),
                    trailing: Icon(Icons.arrow_forward_ios),
                    onTap: () {{}},
                  ),
                );
              }},
            ),
          ),
        ],
      ),
    );
  }}
}}'''
        
        with open(lib_dir / "main.dart", "w", encoding="utf-8") as f:
            f.write(main_dart)
        files_created += 1
        
        # 3. README.md
        readme = f'''# {business_name}

{description}

## 🚀 Flutter Mobile App

### การติดตั้ง

1. ติดตั้ง Flutter dependencies:
```bash
flutter pub get
```

2. รันแอป:
```bash
flutter run
```

### ฟีเจอร์

- ✅ Material Design
- ✅ Bottom Navigation
- ✅ Responsive Layout
- ✅ Beautiful UI
- ✅ Cross Platform (iOS & Android)

### โครงสร้างแอป

- **หน้าแรก**: แสดงข้อมูลหลักและฟีเจอร์
- **บริการ**: รายการบริการทั้งหมด
- **โปรไฟล์**: ข้อมูลผู้ใช้และการตั้งค่า

### การพัฒนา

```bash
flutter run          # รันแอป
flutter build apk    # สร้าง APK สำหรับ Android
flutter build ios    # สร้างสำหรับ iOS
flutter test         # รันเทส
flutter analyze      # ตรวจสอบโค้ด
```

### สร้างโดย AgentPro AI 🤖
วันที่สร้าง: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
'''
        
        with open(project_path / "README.md", "w", encoding="utf-8") as f:
            f.write(readme)
        files_created += 1
        
        return {
            'files_created': files_created,
            'install_commands': [
                'flutter pub get'
            ],
            'run_commands': [
                'flutter run',
                'flutter build apk',  # Android
                'flutter build ios'   # iOS
            ]
        }
    
    async def _create_ionic_app(self, project_path: Path, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        สร้าง Ionic App
        """
        # Implementation for Ionic app creation
        # ตอนนี้ใช้ React Native เป็น default
        return await self._create_react_native_app(project_path, requirements)

# สร้าง instance
mobile_app_generator = MobileAppGenerator()