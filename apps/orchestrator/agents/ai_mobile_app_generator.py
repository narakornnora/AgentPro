import os
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

class AIpoweredMobileAppGenerator:
    """
    🚀 AI-Powered Mobile App Generator - ใช้ OpenAI สร้างโค้ดจริง ๆ
    Support: React Native, Flutter, Ionic
    """
    
    def __init__(self, client):
        self.client = client
        self.workspace = Path("C:/agent/workspace")
        self.workspace.mkdir(parents=True, exist_ok=True)
    
    async def generate_mobile_app(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        สร้าง Mobile App ตาม requirements โดยใช้ AI จริง ๆ
        """
        try:
            # Extract requirements
            app_type = requirements.get('app_type', 'react_native')
            project_name = requirements.get('project_name', 'mobile_app')
            business_name = requirements.get('business_name', 'My App')
            description = requirements.get('description', 'Mobile Application')
            features = requirements.get('features', [])
            message = requirements.get('message', '')
            
            # สร้างโฟลเดอร์โปรเจ็กต์
            project_path = self.workspace / project_name
            project_path.mkdir(parents=True, exist_ok=True)
            
            if app_type == 'react_native':
                result = await self._create_ai_react_native_app(project_path, requirements)
            elif app_type == 'flutter':
                result = await self._create_ai_flutter_app(project_path, requirements)
            elif app_type == 'ionic':
                result = await self._create_ai_ionic_app(project_path, requirements)
            else:
                result = await self._create_ai_react_native_app(project_path, requirements)
            
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
                'message': f'✅ {app_type} Mobile App "{business_name}" สร้างด้วย AI สำเร็จแล้ว!'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'❌ เกิดข้อผิดพลาดในการสร้าง AI Mobile App: {str(e)}'
            }
    
    async def _create_ai_react_native_app(self, project_path: Path, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        สร้าง React Native App โดยใช้ AI สร้างโค้ดจริง ๆ
        """
        business_name = requirements.get('business_name', 'My App')
        description = requirements.get('description', 'React Native Application')
        features = requirements.get('features', [])
        message = requirements.get('message', '')
        
        files_created = 0
        
        # 1. สร้าง package.json
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
            },
            "jest": {
                "preset": "react-native"
            }
        }
        
        with open(project_path / "package.json", "w", encoding="utf-8") as f:
            json.dump(package_json, f, indent=2, ensure_ascii=False)
        files_created += 1
        
        # 2. ใช้ AI สร้าง App.tsx ตาม requirements
        app_tsx_content = await self._generate_ai_react_native_component(message, business_name, features)
        
        with open(project_path / "App.tsx", "w", encoding="utf-8") as f:
            f.write(app_tsx_content)
        files_created += 1
        
        # 3. สร้าง index.js
        index_js = """import {AppRegistry} from 'react-native';
import App from './App';
import {name as appName} from './app.json';

AppRegistry.registerComponent(appName, () => App);
"""
        
        with open(project_path / "index.js", "w", encoding="utf-8") as f:
            f.write(index_js)
        files_created += 1
        
        # 4. สร้าง app.json
        app_json = {
            "name": requirements.get('project_name', 'mobile_app'),
            "displayName": business_name,
            "expo": {
                "name": business_name,
                "slug": requirements.get('project_name', 'mobile_app'),
                "version": "1.0.0",
                "platforms": ["ios", "android", "web"]
            }
        }
        
        with open(project_path / "app.json", "w", encoding="utf-8") as f:
            json.dump(app_json, f, indent=2, ensure_ascii=False)
        files_created += 1
        
        # 5. สร้าง README.md ด้วย AI
        readme_content = await self._generate_ai_readme(business_name, description, features)
        
        with open(project_path / "README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        files_created += 1
        
        return {
            'files_created': files_created,
            'install_commands': [
                'npm install',
                'cd ios && pod install && cd ..',
                'npx react-native start'
            ],
            'run_commands': [
                'npx react-native run-android',
                'npx react-native run-ios'
            ]
        }
    
    async def _generate_ai_react_native_component(self, message: str, business_name: str, features: List[str]) -> str:
        """
        ใช้ OpenAI สร้าง React Native component ตาม requirements
        """
        prompt = f"""
สร้าง React Native App.tsx component สำหรับ: {message}

Requirements:
- Business Name: {business_name}
- Features ที่ต้องการ: {', '.join(features) if features else 'ไม่ระบุ'}
- ใช้ TypeScript
- ใช้ React Navigation (Stack + Bottom Tabs)
- มี SafeAreaView และ ScrollView
- UI ต้องสวยงาม มี StyleSheet
- เขียนคอมเมนต์เป็นภาษาไทย
- ต้องมีการทำงานจริง ไม่ใช่แค่ static template

ให้สร้าง component ที่:
1. สามารถทำงานได้จริง
2. มี navigation ระหว่างหน้าต่าง ๆ
3. มี UI elements ที่เหมาะสมกับธุรกิจ
4. มี state management
5. responsive design

โครงสร้างที่ต้องการ:
- HomeScreen (หน้าหลัก)
- หน้าที่เกี่ยวข้องกับธุรกิจ (เช่น MenuScreen สำหรับร้านอาหาร)
- ProfileScreen
- Navigation setup

ส่งกลับเฉพาะโค้ด React Native TypeScript เท่านั้น ไม่ต้องมี explanation
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "คุณเป็น expert React Native developer ที่สร้างแอป mobile ที่ทำงานได้จริง"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3000,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Fallback to basic template if AI fails
            print(f"AI generation failed: {e}")
            return self._get_fallback_react_native_template(business_name, features)
    
    async def _generate_ai_readme(self, business_name: str, description: str, features: List[str]) -> str:
        """
        ใช้ AI สร้าง README.md
        """
        prompt = f"""
สร้าง README.md สำหรับ React Native app:
- ชื่อแอป: {business_name}
- คำอธิบาย: {description}
- Features: {', '.join(features) if features else 'ไม่ระบุ'}

ต้องมี:
1. ชื่อโปรเจ็กต์และคำอธิบาย
2. Features ที่มี
3. วิธีติดตั้งและรัน
4. ความต้องการของระบบ
5. คำแนะนำการใช้งาน

เขียนเป็นภาษาไทยและอังกฤษ ให้ดูเป็นมืออาชีพ
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "คุณเป็น technical writer ที่เก่งในการเขียนเอกสาร"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.5
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Fallback template
            return f"""# {business_name}

{description}

## Features
{chr(10).join(['- ' + feature for feature in features]) if features else '- ไม่ระบุฟีเจอร์'}

## Installation
```bash
npm install
cd ios && pod install && cd ..
```

## Running
```bash
# Android
npx react-native run-android

# iOS
npx react-native run-ios
```

## Requirements
- Node.js >= 14
- React Native CLI
- Android Studio / Xcode
"""
    
    def _get_fallback_react_native_template(self, business_name: str, features: List[str]) -> str:
        """
        Fallback template หาก AI ไม่สามารถสร้างได้
        """
        return f'''import React, {{useState}} from 'react';
import {{
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  Alert,
}} from 'react-native';
import {{NavigationContainer}} from '@react-navigation/native';
import {{createBottomTabNavigator}} from '@react-navigation/bottom-tabs';

// หน้าหลัก
function HomeScreen({{navigation}}: any) {{
  const [counter, setCounter] = useState(0);
  
  return (
    <SafeAreaView style={{styles.container}}>
      <ScrollView contentInsetAdjustmentBehavior="automatic">
        <View style={{styles.header}}>
          <Text style={{styles.appTitle}}>{business_name}</Text>
          <Text style={{styles.appSubtitle}}>พัฒนาด้วย AI Technology</Text>
        </View>
        
        <View style={{styles.content}}>
          <Text style={{styles.welcomeText}}>ยินดีต้อนรับสู่แอปของเรา</Text>
          
          <TouchableOpacity 
            style={{styles.primaryButton}}
            onPress={{() => {{
              setCounter(prev => prev + 1);
              Alert.alert('สำเร็จ!', `คุณกดปุ่มไป ${{counter + 1}} ครั้งแล้ว`);
            }}}}
          >
            <Text style={{styles.buttonText}}>ทดสอบการทำงาน ({{counter}})</Text>
          </TouchableOpacity>
          
          {{features.length > 0 && (
            <View style={{styles.featuresSection}}>
              <Text style={{styles.sectionTitle}}>ฟีเจอร์</Text>
              {{features.map((feature, index) => (
                <View key={{index}} style={{styles.featureItem}}>
                  <Text style={{styles.featureText}}>✓ {{feature}}</Text>
                </View>
              ))}}
            </View>
          )}}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}}

function ProfileScreen() {{
  return (
    <SafeAreaView style={{styles.container}}>
      <View style={{styles.content}}>
        <Text style={{styles.pageTitle}}>โปรไฟล์</Text>
        <Text style={{styles.normalText}}>หน้านี้แสดงข้อมูลผู้ใช้</Text>
      </View>
    </SafeAreaView>
  );
}}

const Tab = createBottomTabNavigator();

export default function App(): JSX.Element {{
  return (
    <NavigationContainer>
      <StatusBar barStyle="dark-content" />
      <Tab.Navigator
        screenOptions={{{{
          tabBarActiveTintColor: '#007AFF',
          tabBarInactiveTintColor: '#8E8E93',
        }}}}
      >
        <Tab.Screen 
          name="Home" 
          component={{HomeScreen}} 
          options={{{{title: 'หน้าหลัก'}}}}
        />
        <Tab.Screen 
          name="Profile" 
          component={{ProfileScreen}} 
          options={{{{title: 'โปรไฟล์'}}}}
        />
      </Tab.Navigator>
    </NavigationContainer>
  );
}}

const styles = StyleSheet.create({{
  container: {{
    flex: 1,
    backgroundColor: '#FFFFFF',
  }},
  header: {{
    padding: 20,
    backgroundColor: '#F8F9FA',
    alignItems: 'center',
  }},
  appTitle: {{
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1C1C1E',
    marginBottom: 5,
  }},
  appSubtitle: {{
    fontSize: 16,
    color: '#6C6C70',
  }},
  content: {{
    padding: 20,
  }},
  welcomeText: {{
    fontSize: 20,
    fontWeight: '600',
    color: '#1C1C1E',
    textAlign: 'center',
    marginBottom: 30,
  }},
  primaryButton: {{
    backgroundColor: '#007AFF',
    paddingVertical: 15,
    paddingHorizontal: 30,
    borderRadius: 10,
    alignItems: 'center',
    marginBottom: 20,
  }},
  buttonText: {{
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  }},
  featuresSection: {{
    marginTop: 20,
  }},
  sectionTitle: {{
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1C1C1E',
    marginBottom: 15,
  }},
  featureItem: {{
    paddingVertical: 10,
    paddingHorizontal: 15,
    backgroundColor: '#F8F9FA',
    borderRadius: 8,
    marginBottom: 8,
  }},
  featureText: {{
    fontSize: 16,
    color: '#34C759',
  }},
  pageTitle: {{
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1C1C1E',
    marginBottom: 20,
    textAlign: 'center',
  }},
  normalText: {{
    fontSize: 16,
    color: '#6C6C70',
    textAlign: 'center',
  }},
}});
'''
    
    async def _create_ai_flutter_app(self, project_path: Path, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        สร้าง Flutter App โดยใช้ AI (placeholder for now)
        """
        # TODO: Implement Flutter AI generation
        return {'files_created': 0, 'install_commands': [], 'run_commands': []}
    
    async def _create_ai_ionic_app(self, project_path: Path, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        สร้าง Ionic App โดยใช้ AI (placeholder for now)
        """
        # TODO: Implement Ionic AI generation
        return {'files_created': 0, 'install_commands': [], 'run_commands': []}

# สร้าง instance ให้ใช้งาน
mobile_app_generator = None

def initialize_ai_mobile_generator(client):
    global mobile_app_generator
    mobile_app_generator = AIpoweredMobileAppGenerator(client)
    return mobile_app_generator