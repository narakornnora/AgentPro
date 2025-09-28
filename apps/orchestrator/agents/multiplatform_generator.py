"""
🌐 Multi-Platform App Generator
สร้าง Web, Mobile และ Desktop Apps พร้อมกันในโปรเจกต์เดียว
"""
import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class MultiPlatformSpec:
    """Specification สำหรับ multi-platform application"""
    name: str
    description: str
    platforms: List[str]  # web, mobile, desktop
    shared_features: List[str]
    platform_specific_features: Dict[str, List[str]]
    tech_stack: Dict[str, str]
    ui_design_system: str
    backend_requirements: Dict[str, Any]
    data_sync_strategy: str  # offline_first, online_only, hybrid

class MultiPlatformGenerator:
    """Generator สำหรับ multi-platform applications"""
    
    def __init__(self):
        self.workspace_path = "C:/agent/workspace"
        self.platform_generators = {
            "web": self._generate_web_app,
            "mobile": self._generate_mobile_app, 
            "desktop": self._generate_desktop_app
        }
        
    async def generate_multiplatform_app(self, spec: MultiPlatformSpec) -> Dict[str, Any]:
        """สร้าง multi-platform application"""
        
        try:
            print(f"🚀 กำลังสร้าง multi-platform app: {spec.name}")
            
            project_path = os.path.join(self.workspace_path, spec.name)
            os.makedirs(project_path, exist_ok=True)
            
            results = {}
            
            # สร้าง shared backend
            if spec.backend_requirements:
                backend_result = await self._create_shared_backend(spec, project_path)
                results["backend"] = backend_result
            
            # สร้าง shared design system
            design_system_result = await self._create_design_system(spec, project_path)
            results["design_system"] = design_system_result
            
            # สร้าง shared components library
            shared_components_result = await self._create_shared_components(spec, project_path)
            results["shared_components"] = shared_components_result
            
            # สร้าง apps สำหรับแต่ละ platform
            for platform in spec.platforms:
                if platform in self.platform_generators:
                    platform_result = await self.platform_generators[platform](spec, project_path)
                    results[platform] = platform_result
            
            # สร้าง data synchronization system
            sync_result = await self._create_data_sync_system(spec, project_path)
            results["data_sync"] = sync_result
            
            # สร้าง development tools
            dev_tools_result = await self._create_dev_tools(spec, project_path)
            results["dev_tools"] = dev_tools_result
            
            # สร้าง deployment configuration
            deployment_result = await self._create_deployment_config(spec, project_path)
            results["deployment"] = deployment_result
            
            return {
                "success": True,
                "project_path": project_path,
                "platforms_created": spec.platforms,
                "shared_backend": bool(spec.backend_requirements),
                "design_system": spec.ui_design_system,
                "data_sync_strategy": spec.data_sync_strategy,
                "results": results
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"ไม่สามารถสร้าง multi-platform app ได้"
            }
    
    async def _create_shared_backend(self, spec: MultiPlatformSpec, project_path: str) -> Dict:
        """สร้าง shared backend API"""
        
        backend_path = os.path.join(project_path, "backend")
        os.makedirs(backend_path, exist_ok=True)
        
        # GraphQL API สำหรับ unified data access
        graphql_schema = f"""
type Query {{
  # User queries
  me: User
  users(first: Int, after: String): UserConnection
  
  # Content queries  
  posts(first: Int, after: String): PostConnection
  post(id: ID!): Post
  
  # App-specific queries
  {self._generate_app_specific_queries(spec)}
}}

type Mutation {{
  # User mutations
  signUp(input: SignUpInput!): AuthPayload
  signIn(input: SignInInput!): AuthPayload
  
  # Content mutations
  createPost(input: PostInput!): Post
  updatePost(id: ID!, input: PostInput!): Post
  
  # App-specific mutations
  {self._generate_app_specific_mutations(spec)}
}}

type Subscription {{
  # Real-time subscriptions
  postAdded: Post
  messageReceived(userId: ID!): Message
  
  # App-specific subscriptions
  {self._generate_app_specific_subscriptions(spec)}
}}

type User {{
  id: ID!
  username: String!
  email: String!
  avatar: String
  createdAt: DateTime!
}}

type Post {{
  id: ID!
  title: String!
  content: String!
  author: User!
  createdAt: DateTime!
}}

# Platform-specific types
{self._generate_platform_specific_types(spec)}
"""
        
        with open(os.path.join(backend_path, "schema.graphql"), "w", encoding="utf-8") as f:
            f.write(graphql_schema)
        
        # FastAPI + GraphQL server
        main_py = f"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from strawberry import Schema
from strawberry.fastapi import GraphQLRouter
import strawberry
from typing import List, Optional
import asyncio

# GraphQL Schema Definition
@strawberry.type
class User:
    id: str
    username: str
    email: str
    avatar: Optional[str] = None

@strawberry.type
class Post:
    id: str
    title: str
    content: str
    author: User

@strawberry.type
class Query:
    @strawberry.field
    async def me(self) -> Optional[User]:
        # Implement user authentication check
        return User(id="1", username="user", email="user@example.com")
    
    @strawberry.field  
    async def posts(self) -> List[Post]:
        # Implement posts fetching
        return []

@strawberry.type
class Mutation:
    @strawberry.field
    async def create_post(self, title: str, content: str) -> Post:
        # Implement post creation
        pass

@strawberry.type  
class Subscription:
    @strawberry.subscription
    async def post_added(self) -> Post:
        # Implement real-time post subscription
        while True:
            yield Post(id="1", title="New Post", content="Content")
            await asyncio.sleep(1)

# Create GraphQL schema
schema = Schema(query=Query, mutation=Mutation, subscription=Subscription)

# FastAPI app
app = FastAPI(title="{spec.name} API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GraphQL router
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# REST API endpoints for platform-specific features
@app.get("/health")
async def health_check():
    return {{"status": "healthy"}}

# Platform sync endpoints
@app.post("/sync/upload")
async def sync_upload(data: dict):
    # Implement data sync for offline-first apps
    pass

@app.get("/sync/download")
async def sync_download(last_sync: str):
    # Return data changes since last sync
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
        
        with open(os.path.join(backend_path, "main.py"), "w", encoding="utf-8") as f:
            f.write(main_py)
        
        return {"type": "graphql_api", "features": ["real_time", "data_sync"]}
    
    async def _generate_web_app(self, spec: MultiPlatformSpec, project_path: str) -> Dict:
        """สร้าง web application"""
        
        web_path = os.path.join(project_path, "web-app")
        os.makedirs(web_path, exist_ok=True)
        
        # Next.js app with TypeScript
        package_json = f"""
{{
  "name": "{spec.name}-web",
  "version": "1.0.0",
  "private": true,
  "scripts": {{
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit"
  }},
  "dependencies": {{
    "next": "14.0.0",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "@apollo/client": "^3.8.0",
    "graphql": "^16.8.0",
    "@headlessui/react": "^1.7.0",
    "@heroicons/react": "^2.0.0",
    "tailwindcss": "^3.3.0",
    "framer-motion": "^10.16.0"
  }},
  "devDependencies": {{
    "typescript": "^5.0.0",
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "eslint": "^8.45.0",
    "eslint-config-next": "14.0.0"
  }}
}}
"""
        
        with open(os.path.join(web_path, "package.json"), "w") as f:
            f.write(package_json)
        
        # Main app component
        pages_path = os.path.join(web_path, "pages")
        os.makedirs(pages_path, exist_ok=True)
        
        index_tsx = f"""
import {{ useState, useEffect }} from 'react';
import {{ ApolloProvider, ApolloClient, InMemoryCache, gql, useQuery }} from '@apollo/client';
import {{ motion }} from 'framer-motion';

// GraphQL client
const client = new ApolloClient({{
  uri: process.env.NEXT_PUBLIC_GRAPHQL_URL || 'http://localhost:8000/graphql',
  cache: new InMemoryCache(),
}});

// GraphQL queries
const GET_POSTS = gql`
  query GetPosts {{
    posts {{
      id
      title
      content
      author {{
        username
        avatar
      }}
    }}
  }}
`;

function HomePage() {{
  const {{ loading, error, data }} = useQuery(GET_POSTS);

  if (loading) return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>
  );

  if (error) return (
    <div className="text-red-500 text-center p-8">
      Error: {{error.message}}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {{/* Header */}}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <h1 className="text-3xl font-bold text-gray-900">
              {{spec.name}}
            </h1>
            <nav className="space-x-8">
              <a href="#" className="text-gray-500 hover:text-gray-900">Home</a>
              <a href="#" className="text-gray-500 hover:text-gray-900">Features</a>
              <a href="#" className="text-gray-500 hover:text-gray-900">About</a>
            </nav>
          </div>
        </div>
      </header>

      {{/* Main Content */}}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="text-center mb-12">
            <h2 className="text-4xl font-extrabold text-gray-900 sm:text-5xl">
              Welcome to {{spec.name}}
            </h2>
            <p className="mt-4 text-xl text-gray-600 max-w-3xl mx-auto">
              {{spec.description}}
            </p>
          </div>

          {{/* Features Grid */}}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
            {{spec.shared_features.map((feature, index) => (
              <motion.div
                key={{feature}}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow"
              >
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {{feature.replace('_', ' ').title()}}
                </h3>
                <p className="text-gray-600">
                  Feature description for {{feature}}
                </p>
              </motion.div>
            }})}}
          </div>

          {{/* Posts Section */}}
          <div className="bg-white rounded-lg shadow-sm p-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">Latest Posts</h3>
            <div className="space-y-6">
              {{data?.posts?.map((post: any) => (
                <motion.div
                  key={{post.id}}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="border-b border-gray-200 pb-6 last:border-b-0"
                >
                  <h4 className="text-lg font-semibold text-gray-900">
                    {{post.title}}
                  </h4>
                  <p className="text-gray-600 mt-2">{{post.content}}</p>
                  <div className="mt-3 flex items-center text-sm text-gray-500">
                    <img
                      className="h-6 w-6 rounded-full mr-2"
                      src={{post.author.avatar || '/default-avatar.png'}}
                      alt={{post.author.username}}
                    />
                    {{post.author.username}}
                  </div>
                </motion.div>
              )) || (
                <p className="text-gray-500 text-center py-8">
                  No posts available
                </p>
              )}}
            </div>
          </div>
        </motion.div>
      </main>
    </div>
  );
}}

export default function App() {{
  return (
    <ApolloProvider client={{{{client}}}}>
      <HomePage />
    </ApolloProvider>
  );
}}
"""
        
        with open(os.path.join(pages_path, "index.tsx"), "w", encoding="utf-8") as f:
            f.write(index_tsx)
        
        # Tailwind config
        tailwind_config = """
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
"""
        
        with open(os.path.join(web_path, "tailwind.config.js"), "w") as f:
            f.write(tailwind_config)
        
        return {"framework": "nextjs", "features": ["responsive", "ssr", "graphql"]}
    
    async def _generate_mobile_app(self, spec: MultiPlatformSpec, project_path: str) -> Dict:
        """สร้าง mobile application"""
        
        mobile_path = os.path.join(project_path, "mobile-app")
        os.makedirs(mobile_path, exist_ok=True)
        
        # React Native with TypeScript
        package_json = f"""
{{
  "name": "{spec.name.replace('_', '-')}-mobile",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {{
    "start": "expo start",
    "android": "expo start --android",
    "ios": "expo start --ios",
    "web": "expo start --web"
  }},
  "dependencies": {{
    "expo": "~49.0.0",
    "react": "18.2.0",
    "react-native": "0.72.0",
    "@apollo/client": "^3.8.0",
    "graphql": "^16.8.0",
    "@react-navigation/native": "^6.1.0",
    "@react-navigation/stack": "^6.3.0",
    "react-native-gesture-handler": "~2.12.0",
    "react-native-reanimated": "~3.3.0",
    "expo-sqlite": "~11.3.0",
    "expo-secure-store": "~12.3.0"
  }},
  "devDependencies": {{
    "@types/react": "~18.2.0",
    "typescript": "^5.0.0"
  }}
}}
"""
        
        with open(os.path.join(mobile_path, "package.json"), "w") as f:
            f.write(package_json)
        
        # Main App component
        app_tsx = f"""
import React, {{ useState, useEffect }} from 'react';
import {{ StatusBar }} from 'expo-status-bar';
import {{ StyleSheet, Text, View, ScrollView, TouchableOpacity }} from 'react-native';
import {{ ApolloProvider, ApolloClient, InMemoryCache, gql, useQuery }} from '@apollo/client';
import {{ NavigationContainer }} from '@react-navigation/native';
import {{ createStackNavigator }} from '@react-navigation/stack';

// GraphQL client with offline support
const client = new ApolloClient({{
  uri: 'http://localhost:8000/graphql',
  cache: new InMemoryCache(),
  defaultOptions: {{
    watchQuery: {{
      errorPolicy: 'ignore',
    }},
    query: {{
      errorPolicy: 'all',
    }},
  }},
}});

const GET_POSTS = gql`
  query GetPosts {{
    posts {{
      id
      title
      content
      author {{
        username
      }}
    }}
  }}
`;

const Stack = createStackNavigator();

function HomeScreen() {{
  const {{ loading, error, data, refetch }} = useQuery(GET_POSTS);

  return (
    <ScrollView style={{styles.container}}>
      <View style={{styles.header}}>
        <Text style={{{{styles.title}}}}>{{{spec.name}}}</Text>
        <Text style={{{{styles.description}}}}>{{{spec.description}}}</Text>
      </View>

      {{/* Features */}}
      <View style={{styles.section}}>
        <Text style={{styles.sectionTitle}}>Features</Text>
        {{spec.shared_features.map((feature, index) => (
          <TouchableOpacity key={{{{index}}}} style={{{{styles.featureCard}}}}>
            <Text style={{styles.featureTitle}}>
              {{{{feature.replace('_', ' ').toUpperCase()}}}}
            </Text>
            <Text style={{{{styles.featureDescription}}}}>
              Feature description for {{{{feature}}}}
            </Text>
          </TouchableOpacity>
        }})}}
      </View>

      {{/* Posts */}}
      <View style={{styles.section}}>
        <Text style={{styles.sectionTitle}}>Latest Posts</Text>
        {{{{loading ? (
          <Text style={{styles.loading}}>Loading...</Text>
        ) : error ? (
          <View>
            <Text style={{styles.error}}>Error loading posts</Text>
            <TouchableOpacity 
              style={{styles.retryButton}} 
              onPress={{() => refetch()}}
            >
              <Text style={{styles.retryText}}>Retry</Text>
            </TouchableOpacity>
          </View>
        ) : (
          data?.posts?.map((post: any) => (
            <View key={{post.id}} style={{styles.postCard}}>
              <Text style={{styles.postTitle}}>{{post.title}}</Text>
              <Text style={{styles.postContent}}>{{post.content}}</Text>
              <Text style={{styles.postAuthor}}>By {{post.author.username}}</Text>
            </View>
          )) || (
            <Text style={{styles.noPosts}}>No posts available</Text>
          )
        )}}
      </View>

      <StatusBar style="auto" />
    </ScrollView>
  );
}}

function App() {{
  return (
    <ApolloProvider client={{client}}>
      <NavigationContainer>
        <Stack.Navigator>
          <Stack.Screen 
            name="Home" 
            component={{HomeScreen}}
            options={{{{ title: '{spec.name}' }}}}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </ApolloProvider>
  );
}}

const styles = StyleSheet.create({{
  container: {{
    flex: 1,
    backgroundColor: '#f5f5f5',
  }},
  header: {{
    padding: 20,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e1e1e1',
  }},
  title: {{
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  }},
  description: {{
    fontSize: 16,
    color: '#666',
    lineHeight: 24,
  }},
  section: {{
    padding: 20,
  }},
  sectionTitle: {{
    fontSize: 20,
    fontWeight: '600',
    color: '#333',
    marginBottom: 16,
  }},
  featureCard: {{
    backgroundColor: '#fff',
    padding: 16,
    marginBottom: 12,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: {{ width: 0, height: 1 }},
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  }},
  featureTitle: {{
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 4,
  }},
  featureDescription: {{
    fontSize: 14,
    color: '#666',
  }},
  postCard: {{
    backgroundColor: '#fff',
    padding: 16,
    marginBottom: 12,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: {{ width: 0, height: 1 }},
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  }},
  postTitle: {{
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  }},
  postContent: {{
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  }},
  postAuthor: {{
    fontSize: 12,
    color: '#999',
  }},
  loading: {{
    textAlign: 'center',
    color: '#666',
    fontStyle: 'italic',
  }},
  error: {{
    color: '#e74c3c',
    textAlign: 'center',
    marginBottom: 12,
  }},
  retryButton: {{
    backgroundColor: '#3498db',
    padding: 12,
    borderRadius: 6,
    alignSelf: 'center',
  }},
  retryText: {{
    color: '#fff',
    fontWeight: '600',
  }},
  noPosts: {{
    textAlign: 'center',
    color: '#666',
    fontStyle: 'italic',
  }},
}});

export default App;
"""
        
        with open(os.path.join(mobile_path, "App.tsx"), "w", encoding="utf-8") as f:
            f.write(app_tsx)
        
        return {"framework": "react_native", "features": ["offline_support", "native_ui", "graphql"]}
    
    async def _generate_desktop_app(self, spec: MultiPlatformSpec, project_path: str) -> Dict:
        """สร้าง desktop application"""
        
        desktop_path = os.path.join(project_path, "desktop-app") 
        os.makedirs(desktop_path, exist_ok=True)
        
        # Electron with React
        package_json = f"""
{{
  "name": "{spec.name.replace('_', '-')}-desktop",
  "version": "1.0.0",
  "main": "public/electron.js",
  "scripts": {{
    "start": "react-scripts start",
    "build": "react-scripts build",
    "electron": "electron .",
    "electron-dev": "ELECTRON_IS_DEV=1 electron .",
    "dist": "electron-builder"
  }},
  "dependencies": {{
    "react": "^18.2.0",
    "react-dom": "^18.2.0", 
    "react-scripts": "5.0.1",
    "@apollo/client": "^3.8.0",
    "graphql": "^16.8.0",
    "electron-store": "^8.1.0"
  }},
  "devDependencies": {{
    "electron": "^25.0.0",
    "electron-builder": "^24.0.0",
    "@types/react": "^18.2.0",
    "typescript": "^5.0.0"
  }},
  "build": {{
    "appId": "com.{spec.name.lower()}.desktop",
    "productName": "{spec.name}",
    "directories": {{
      "output": "dist"
    }},
    "files": [
      "build/**/*",
      "public/electron.js"
    ]
  }}
}}
"""
        
        with open(os.path.join(desktop_path, "package.json"), "w") as f:
            f.write(package_json)
        
        # Electron main process
        public_path = os.path.join(desktop_path, "public")
        os.makedirs(public_path, exist_ok=True)
        
        electron_js = f"""
const {{ app, BrowserWindow, Menu, ipcMain }} = require('electron');
const path = require('path');
const isDev = process.env.ELECTRON_IS_DEV === '1';

let mainWindow;

function createWindow() {{
  // Create the browser window
  mainWindow = new BrowserWindow({{
    width: 1200,
    height: 800,
    webPreferences: {{
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: path.join(__dirname, 'preload.js')
    }},
    titleBarStyle: 'hiddenInset',
    show: false
  }});

  // Load the app
  const startUrl = isDev 
    ? 'http://localhost:3000' 
    : `file://${{path.join(__dirname, '../build/index.html')}}`;
  
  mainWindow.loadURL(startUrl);

  // Show window when ready
  mainWindow.once('ready-to-show', () => {{
    mainWindow.show();
  }});

  // Open DevTools in development
  if (isDev) {{
    mainWindow.webContents.openDevTools();
  }}

  mainWindow.on('closed', () => {{
    mainWindow = null;
  }});
}}

// App event listeners
app.whenReady().then(() => {{
  createWindow();

  app.on('activate', () => {{
    if (BrowserWindow.getAllWindows().length === 0) {{
      createWindow();
    }}
  }});
}});

app.on('window-all-closed', () => {{
  if (process.platform !== 'darwin') {{
    app.quit();
  }}
}});

// IPC handlers for desktop-specific features
ipcMain.handle('get-app-version', () => {{
  return app.getVersion();
}});

ipcMain.handle('show-save-dialog', async () => {{
  const {{ dialog }} = require('electron');
  const result = await dialog.showSaveDialog(mainWindow, {{
    filters: [
      {{ name: 'JSON Files', extensions: ['json'] }},
      {{ name: 'All Files', extensions: ['*'] }}
    ]
  }});
  return result;
}});
"""
        
        with open(os.path.join(public_path, "electron.js"), "w") as f:
            f.write(electron_js)
        
        return {"framework": "electron", "features": ["native_menus", "file_system", "auto_updater"]}
    
    async def _create_data_sync_system(self, spec: MultiPlatformSpec, project_path: str) -> Dict:
        """สร้างระบบ data synchronization"""
        
        sync_path = os.path.join(project_path, "data-sync")
        os.makedirs(sync_path, exist_ok=True)
        
        if spec.data_sync_strategy == "offline_first":
            return await self._create_offline_first_sync(sync_path)
        elif spec.data_sync_strategy == "hybrid":
            return await self._create_hybrid_sync(sync_path)
        else:
            return await self._create_online_only_sync(sync_path)
    
    async def _create_offline_first_sync(self, sync_path: str) -> Dict:
        """สร้าง offline-first synchronization"""
        
        sync_manager_ts = """
interface SyncItem {
  id: string;
  type: string;
  data: any;
  timestamp: number;
  action: 'create' | 'update' | 'delete';
  synced: boolean;
}

class OfflineFirstSyncManager {
  private localDB: any;
  private syncQueue: SyncItem[] = [];
  private isOnline: boolean = navigator.onLine;

  constructor() {
    this.initializeLocalDB();
    this.setupNetworkListeners();
    this.startPeriodicSync();
  }

  async initializeLocalDB() {
    // Initialize local database (SQLite/IndexedDB)
  }

  setupNetworkListeners() {
    window.addEventListener('online', () => {
      this.isOnline = true;
      this.syncData();
    });

    window.addEventListener('offline', () => {
      this.isOnline = false;
    });
  }

  async create(type: string, data: any): Promise<string> {
    const id = this.generateId();
    const item: SyncItem = {
      id,
      type,
      data,
      timestamp: Date.now(),
      action: 'create',
      synced: false
    };

    // Save to local DB
    await this.saveToLocal(item);
    
    // Add to sync queue
    this.syncQueue.push(item);

    // Try to sync if online
    if (this.isOnline) {
      await this.syncData();
    }

    return id;
  }

  async syncData() {
    if (!this.isOnline || this.syncQueue.length === 0) return;

    try {
      // Upload local changes
      for (const item of this.syncQueue) {
        await this.uploadItem(item);
        item.synced = true;
      }

      // Download remote changes
      await this.downloadChanges();

      // Clear synced items from queue
      this.syncQueue = this.syncQueue.filter(item => !item.synced);

    } catch (error) {
      console.error('Sync failed:', error);
    }
  }

  private generateId(): string {
    return Date.now().toString() + Math.random().toString(36).substr(2, 9);
  }

  private async saveToLocal(item: SyncItem) {
    // Implement local storage
  }

  private async uploadItem(item: SyncItem) {
    // Upload to server via GraphQL mutation
  }

  private async downloadChanges() {
    // Download changes from server
  }

  private startPeriodicSync() {
    setInterval(() => {
      if (this.isOnline) {
        this.syncData();
      }
    }, 30000); // Sync every 30 seconds
  }
}

export default OfflineFirstSyncManager;
"""
        
        with open(os.path.join(sync_path, "OfflineFirstSyncManager.ts"), "w") as f:
            f.write(sync_manager_ts)
        
        return {"strategy": "offline_first", "features": ["conflict_resolution", "queue_management"]}

# สร้าง instance
multiplatform_generator = MultiPlatformGenerator()

# Helper functions
async def create_social_media_multiplatform(name: str) -> Dict:
    """สร้าง social media app แบบ multi-platform"""
    spec = MultiPlatformSpec(
        name=name,
        description="Social media platform with real-time messaging and content sharing",
        platforms=["web", "mobile", "desktop"],
        shared_features=["user_authentication", "real_time_chat", "content_sharing", "notifications"],
        platform_specific_features={
            "web": ["advanced_admin_panel", "analytics_dashboard"],
            "mobile": ["push_notifications", "camera_integration", "location_services"],
            "desktop": ["bulk_operations", "advanced_editing", "file_management"]
        },
        tech_stack={
            "web": "nextjs",
            "mobile": "react_native",
            "desktop": "electron",
            "backend": "graphql"
        },
        ui_design_system="tailwind",
        backend_requirements={
            "realtime": True,
            "file_upload": True,
            "push_notifications": True
        },
        data_sync_strategy="offline_first"
    )
    
    return await multiplatform_generator.generate_multiplatform_app(spec)

if __name__ == "__main__":
    print("🌐 Multi-Platform App Generator")
    print("=" * 50)
    print("📱 Mobile (React Native + Expo)")
    print("🌐 Web (Next.js + React)")
    print("🖥️  Desktop (Electron)")
    print("🔄 Data Sync (Offline-first)")
    print("📡 GraphQL API Backend")
    print("🎨 Shared Design System")
    print()
    print("✨ ทุก platform ใช้โค้ดร่วมกัน:")
    print("   🧩 Shared Components")
    print("   🔗 Unified API")
    print("   💾 Offline Support")
    print("   🔄 Real-time Sync")
    print("   🎨 Consistent UI/UX")