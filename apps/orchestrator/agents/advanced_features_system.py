"""
🎯 Advanced Features Integration System
เพิ่ม features ซับซ้อน เช่น AI/ML, blockchain, IoT, real-time collaboration, advanced security
"""
import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class AdvancedFeatureSpec:
    """Specification สำหรับ advanced features"""
    name: str
    category: str  # ai_ml, blockchain, iot, security, real_time
    complexity_level: str  # basic, advanced, enterprise
    dependencies: List[str]
    integration_points: List[str]
    configuration: Dict[str, Any]

class AdvancedFeaturesSystem:
    """ระบบเพิ่ม advanced features ให้กับ applications"""
    
    def __init__(self):
        self.feature_templates = self._initialize_feature_templates()
        self.integration_patterns = self._initialize_integration_patterns()
        
    def _initialize_feature_templates(self) -> Dict:
        """เริ่มต้น feature templates"""
        return {
            "ai_ml": {
                "recommendation_engine": self._create_recommendation_engine,
                "chatbot": self._create_ai_chatbot,
                "content_moderation": self._create_content_moderation,
                "image_recognition": self._create_image_recognition,
                "natural_language_processing": self._create_nlp_service,
                "fraud_detection": self._create_fraud_detection,
                "predictive_analytics": self._create_predictive_analytics
            },
            "blockchain": {
                "smart_contracts": self._create_smart_contracts,
                "nft_marketplace": self._create_nft_marketplace,
                "cryptocurrency_wallet": self._create_crypto_wallet,
                "decentralized_storage": self._create_decentralized_storage,
                "dao_governance": self._create_dao_system
            },
            "iot": {
                "device_management": self._create_iot_device_manager,
                "sensor_data_processing": self._create_sensor_processor,
                "real_time_monitoring": self._create_iot_monitoring,
                "edge_computing": self._create_edge_computing,
                "industrial_automation": self._create_industrial_automation
            },
            "security": {
                "multi_factor_auth": self._create_mfa_system,
                "encryption_service": self._create_encryption_service,
                "audit_logging": self._create_audit_system,
                "threat_detection": self._create_threat_detection,
                "compliance_framework": self._create_compliance_system
            },
            "real_time": {
                "live_collaboration": self._create_live_collaboration,
                "video_conferencing": self._create_video_system,
                "real_time_notifications": self._create_notification_system,
                "live_streaming": self._create_streaming_service,
                "multiplayer_gaming": self._create_multiplayer_system
            }
        }
    
    def _initialize_integration_patterns(self) -> Dict:
        """เริ่มต้น integration patterns"""
        return {
            "microservice": self._integrate_as_microservice,
            "library": self._integrate_as_library,
            "external_api": self._integrate_as_external_api,
            "middleware": self._integrate_as_middleware,
            "event_driven": self._integrate_event_driven
        }
    
    async def add_advanced_feature(
        self, 
        feature_spec: AdvancedFeatureSpec, 
        project_path: str,
        integration_pattern: str = "microservice"
    ) -> Dict[str, Any]:
        """เพิ่ม advanced feature ให้กับโปรเจกต์"""
        
        try:
            print(f"🚀 กำลังเพิ่ม {feature_spec.name} feature...")
            
            # เลือก feature creator
            category_templates = self.feature_templates.get(feature_spec.category, {})
            feature_creator = category_templates.get(feature_spec.name)
            
            if not feature_creator:
                return {
                    "success": False,
                    "message": f"ไม่พบ template สำหรับ {feature_spec.name}"
                }
            
            # สร้าง feature
            feature_result = await feature_creator(feature_spec, project_path)
            
            # Integrate กับโปรเจกต์
            integration_result = await self._integrate_feature(
                feature_result, project_path, integration_pattern
            )
            
            # สร้าง documentation
            docs_result = await self._create_feature_documentation(feature_spec, project_path)
            
            # สร้าง tests
            test_result = await self._create_feature_tests(feature_spec, project_path)
            
            return {
                "success": True,
                "feature_name": feature_spec.name,
                "category": feature_spec.category,
                "integration_pattern": integration_pattern,
                "files_created": feature_result.get("files_created", []),
                "dependencies_added": feature_result.get("dependencies", []),
                "api_endpoints": feature_result.get("api_endpoints", []),
                "documentation_created": docs_result,
                "tests_created": test_result
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"ไม่สามารถเพิ่ม {feature_spec.name} feature ได้"
            }
    
    # AI/ML Features
    async def _create_recommendation_engine(self, spec: AdvancedFeatureSpec, project_path: str) -> Dict:
        """สร้าง AI Recommendation Engine"""
        
        feature_path = os.path.join(project_path, "services", "recommendation-service")
        os.makedirs(feature_path, exist_ok=True)
        
        # ML Model Service
        ml_service_py = """
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import joblib
import asyncio
from typing import List, Dict, Optional
import logging

app = FastAPI(title="AI Recommendation Engine", version="1.0.0")

class RecommendationRequest(BaseModel):
    user_id: str
    item_type: str  # product, content, user
    limit: int = 10
    context: Optional[Dict] = None

class RecommendationResponse(BaseModel):
    user_id: str
    recommendations: List[Dict]
    confidence_scores: List[float]
    algorithm_used: str

class RecommendationEngine:
    def __init__(self):
        self.models = {}
        self.user_profiles = {}
        self.item_features = {}
        
    async def load_models(self):
        \"\"\"Load pre-trained ML models\"\"\"
        try:
            # Load collaborative filtering model
            self.models['collaborative'] = joblib.load('models/collaborative_model.pkl')
            
            # Load content-based model
            self.models['content_based'] = joblib.load('models/content_model.pkl')
            
            # Load hybrid model
            self.models['hybrid'] = joblib.load('models/hybrid_model.pkl')
            
        except FileNotFoundError:
            # Initialize new models if not found
            await self.train_initial_models()
    
    async def get_recommendations(self, request: RecommendationRequest) -> RecommendationResponse:
        \"\"\"Get personalized recommendations\"\"\"
        
        # Get user profile
        user_profile = await self.get_user_profile(request.user_id)
        
        # Choose recommendation algorithm based on data availability
        if len(user_profile.get('interactions', [])) > 10:
            # Use collaborative filtering for users with enough data
            recommendations = await self.collaborative_filtering(request)
            algorithm = "collaborative_filtering"
        else:
            # Use content-based for new users (cold start)
            recommendations = await self.content_based_filtering(request)
            algorithm = "content_based"
        
        # Apply business rules and filters
        filtered_recommendations = await self.apply_business_rules(
            recommendations, request.context
        )
        
        return RecommendationResponse(
            user_id=request.user_id,
            recommendations=filtered_recommendations[:request.limit],
            confidence_scores=[item['score'] for item in filtered_recommendations[:request.limit]],
            algorithm_used=algorithm
        )
    
    async def collaborative_filtering(self, request: RecommendationRequest) -> List[Dict]:
        \"\"\"Collaborative filtering using matrix factorization\"\"\"
        
        # Get user-item interaction matrix
        interaction_matrix = await self.get_interaction_matrix(request.item_type)
        
        # Use SVD for matrix factorization
        svd = TruncatedSVD(n_components=50, random_state=42)
        user_factors = svd.fit_transform(interaction_matrix)
        item_factors = svd.components_
        
        # Get user index
        user_idx = await self.get_user_index(request.user_id)
        
        # Calculate recommendations
        user_vector = user_factors[user_idx]
        scores = np.dot(user_vector, item_factors)
        
        # Get top items
        top_indices = np.argsort(scores)[::-1][:request.limit * 2]
        
        recommendations = []
        for idx in top_indices:
            item_id = await self.get_item_id_by_index(idx)
            item_data = await self.get_item_data(item_id)
            
            recommendations.append({
                'item_id': item_id,
                'score': float(scores[idx]),
                'data': item_data,
                'reason': 'Users with similar preferences also liked this'
            })
        
        return recommendations
    
    async def content_based_filtering(self, request: RecommendationRequest) -> List[Dict]:
        \"\"\"Content-based filtering using item features\"\"\"
        
        # Get user preferences
        user_preferences = await self.get_user_preferences(request.user_id)
        
        # Get item features
        item_features = await self.get_item_features(request.item_type)
        
        # Calculate similarity between user profile and items
        user_profile_vector = self.create_user_profile_vector(user_preferences)
        
        similarities = []
        for item_id, features in item_features.items():
            similarity = cosine_similarity(
                user_profile_vector.reshape(1, -1),
                features.reshape(1, -1)
            )[0][0]
            
            similarities.append({
                'item_id': item_id,
                'score': float(similarity),
                'data': await self.get_item_data(item_id),
                'reason': 'Based on your interests and preferences'
            })
        
        # Sort by similarity score
        similarities.sort(key=lambda x: x['score'], reverse=True)
        
        return similarities
    
    async def train_initial_models(self):
        \"\"\"Train initial ML models\"\"\"
        logging.info("Training initial recommendation models...")
        
        # This would typically involve:
        # 1. Loading historical data
        # 2. Feature engineering
        # 3. Model training
        # 4. Model evaluation
        # 5. Model saving
        
        pass
    
    async def update_user_profile(self, user_id: str, interaction_data: Dict):
        \"\"\"Update user profile with new interaction\"\"\"
        # Real-time learning from user interactions
        pass

# Initialize recommendation engine
recommendation_engine = RecommendationEngine()

@app.on_event("startup")
async def startup_event():
    await recommendation_engine.load_models()

@app.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    return await recommendation_engine.get_recommendations(request)

@app.post("/update-profile")
async def update_user_profile(user_id: str, interaction_data: Dict):
    await recommendation_engine.update_user_profile(user_id, interaction_data)
    return {"status": "updated"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "recommendation-engine"}
"""
        
        with open(os.path.join(feature_path, "main.py"), "w", encoding="utf-8") as f:
            f.write(ml_service_py)
        
        # Requirements
        requirements = """
fastapi==0.104.1
uvicorn[standard]==0.24.0
scikit-learn==1.3.2
numpy==1.24.4
pandas==2.1.4
joblib==1.3.2
pydantic==2.5.0
"""
        
        with open(os.path.join(feature_path, "requirements.txt"), "w") as f:
            f.write(requirements)
        
        return {
            "files_created": ["main.py", "requirements.txt"],
            "dependencies": ["scikit-learn", "numpy", "pandas"],
            "api_endpoints": ["/recommendations", "/update-profile"],
            "ml_algorithms": ["collaborative_filtering", "content_based", "hybrid"]
        }
    
    async def _create_ai_chatbot(self, spec: AdvancedFeatureSpec, project_path: str) -> Dict:
        """สร้าง AI Chatbot Service"""
        
        chatbot_path = os.path.join(project_path, "services", "chatbot-service")
        os.makedirs(chatbot_path, exist_ok=True)
        
        # AI Chatbot Service
        chatbot_service = """
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import openai
import asyncio
from typing import List, Dict, Optional
import json
import uuid
from datetime import datetime

app = FastAPI(title="AI Chatbot Service", version="1.0.0")

class ChatMessage(BaseModel):
    message: str
    user_id: str
    conversation_id: Optional[str] = None
    context: Optional[Dict] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    timestamp: str
    confidence: float
    suggested_actions: List[str] = []

class AIchatBot:
    def __init__(self, openai_api_key: str):
        self.openai_client = openai.AsyncOpenAI(api_key=openai_api_key)
        self.conversations = {}
        
    async def process_message(self, chat_message: ChatMessage) -> ChatResponse:
        \"\"\"Process incoming chat message\"\"\"
        
        # Get or create conversation
        conversation_id = chat_message.conversation_id or str(uuid.uuid4())
        
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = {
                "messages": [],
                "user_id": chat_message.user_id,
                "created_at": datetime.now().isoformat()
            }
        
        conversation = self.conversations[conversation_id]
        
        # Add user message to conversation
        conversation["messages"].append({
            "role": "user",
            "content": chat_message.message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Generate AI response
        ai_response = await self.generate_ai_response(
            conversation["messages"], 
            chat_message.context
        )
        
        # Add AI response to conversation
        conversation["messages"].append({
            "role": "assistant", 
            "content": ai_response["content"],
            "timestamp": datetime.now().isoformat()
        })
        
        # Generate suggested actions
        suggested_actions = await self.generate_suggested_actions(
            chat_message.message, ai_response["content"]
        )
        
        return ChatResponse(
            response=ai_response["content"],
            conversation_id=conversation_id,
            timestamp=datetime.now().isoformat(),
            confidence=ai_response["confidence"],
            suggested_actions=suggested_actions
        )
    
    async def generate_ai_response(self, messages: List[Dict], context: Optional[Dict]) -> Dict:
        \"\"\"Generate AI response using OpenAI\"\"\"
        
        # Prepare system prompt
        system_prompt = self.get_system_prompt(context)
        
        # Prepare messages for OpenAI
        openai_messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (last 10 messages)
        for msg in messages[-10:]:
            openai_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=openai_messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return {
                "content": response.choices[0].message.content,
                "confidence": 0.9  # You could implement confidence calculation
            }
            
        except Exception as e:
            return {
                "content": "ขออภัย เกิดข้อผิดพลาดในการประมวลผล กรุณาลองใหม่อีกครั้ง",
                "confidence": 0.1
            }
    
    def get_system_prompt(self, context: Optional[Dict]) -> str:
        \"\"\"Get system prompt based on context\"\"\"
        
        base_prompt = \"\"\"
        คุณเป็น AI assistant ที่เป็นมิตรและช่วยเหลือได้ดี
        ตอบคำถามด้วยความสุภาพและให้ข้อมูลที่มีประโยชน์
        \"\"\"
        
        if context:
            if context.get("domain") == "ecommerce":
                base_prompt += "คุณเชี่ยวชาญด้านการช็อปปิ้งออนไลน์และสินค้า"
            elif context.get("domain") == "support":
                base_prompt += "คุณเป็นทีมสนับสนุนลูกค้าที่พร้อมช่วยแก้ไขปัญหา"
        
        return base_prompt
    
    async def generate_suggested_actions(self, user_message: str, ai_response: str) -> List[str]:
        \"\"\"Generate suggested follow-up actions\"\"\"
        
        # Simple keyword-based suggestions
        suggestions = []
        
        if "ราคา" in user_message.lower():
            suggestions.append("ดูสินค้าแนะนำ")
            suggestions.append("เปรียบเทียบราคา")
        
        if "ช่วย" in user_message.lower():
            suggestions.append("ติดต่อตัวแทน")
            suggestions.append("ดู FAQ")
        
        if "สั่งซื้อ" in user_message.lower():
            suggestions.append("เพิ่มลงตะกร้า")
            suggestions.append("ดูตะกร้าสินค้า")
        
        return suggestions[:3]  # Return max 3 suggestions

# Initialize chatbot
chatbot = AIchatBot(openai_api_key="your-openai-api-key")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage):
    return await chatbot.process_message(message)

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Create chat message
            chat_message = ChatMessage(
                message=message_data["message"],
                user_id=user_id,
                conversation_id=message_data.get("conversation_id"),
                context=message_data.get("context")
            )
            
            # Process message
            response = await chatbot.process_message(chat_message)
            
            # Send response back
            await websocket.send_text(response.json())
            
    except WebSocketDisconnect:
        print(f"Client {user_id} disconnected")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "chatbot"}
"""
        
        with open(os.path.join(chatbot_path, "main.py"), "w", encoding="utf-8") as f:
            f.write(chatbot_service)
        
        return {
            "files_created": ["main.py"],
            "dependencies": ["openai", "websockets"],
            "api_endpoints": ["/chat", "/ws/{user_id}"],
            "features": ["real_time_chat", "conversation_memory", "suggested_actions"]
        }
    
    # Blockchain Features
    async def _create_smart_contracts(self, spec: AdvancedFeatureSpec, project_path: str) -> Dict:
        """สร้าง Smart Contracts"""
        
        contracts_path = os.path.join(project_path, "blockchain", "contracts")
        os.makedirs(contracts_path, exist_ok=True)
        
        # Simple ERC20 Token Contract
        token_contract = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

contract AppToken is ERC20, Ownable, Pausable {
    uint256 public constant INITIAL_SUPPLY = 1000000 * 10**18; // 1 million tokens
    uint256 public constant MAX_SUPPLY = 10000000 * 10**18; // 10 million max
    
    mapping(address => bool) public minters;
    
    event MinterAdded(address indexed minter);
    event MinterRemoved(address indexed minter);
    
    constructor() ERC20("AppToken", "APP") {
        _mint(msg.sender, INITIAL_SUPPLY);
    }
    
    modifier onlyMinter() {
        require(minters[msg.sender], "Not a minter");
        _;
    }
    
    function addMinter(address minter) external onlyOwner {
        minters[minter] = true;
        emit MinterAdded(minter);
    }
    
    function removeMinter(address minter) external onlyOwner {
        minters[minter] = false;
        emit MinterRemoved(minter);
    }
    
    function mint(address to, uint256 amount) external onlyMinter {
        require(totalSupply() + amount <= MAX_SUPPLY, "Exceeds max supply");
        _mint(to, amount);
    }
    
    function burn(uint256 amount) external {
        _burn(msg.sender, amount);
    }
    
    function pause() external onlyOwner {
        _pause();
    }
    
    function unpause() external onlyOwner {
        _unpause();
    }
    
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal override whenNotPaused {
        super._beforeTokenTransfer(from, to, amount);
    }
}
"""
        
        with open(os.path.join(contracts_path, "AppToken.sol"), "w") as f:
            f.write(token_contract)
        
        # NFT Contract
        nft_contract = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract AppNFT is ERC721, ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;
    
    Counters.Counter private _tokenIdCounter;
    uint256 public constant MAX_SUPPLY = 10000;
    uint256 public mintPrice = 0.1 ether;
    
    mapping(uint256 => string) private _tokenURIs;
    
    constructor() ERC721("App NFT Collection", "APPNFT") {
        _tokenIdCounter.increment(); // Start from 1
    }
    
    function mint(address to, string memory uri) external payable {
        require(_tokenIdCounter.current() <= MAX_SUPPLY, "Max supply reached");
        require(msg.value >= mintPrice, "Insufficient payment");
        
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
    }
    
    function ownerMint(address to, string memory uri) external onlyOwner {
        require(_tokenIdCounter.current() <= MAX_SUPPLY, "Max supply reached");
        
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
    }
    
    function setMintPrice(uint256 newPrice) external onlyOwner {
        mintPrice = newPrice;
    }
    
    function withdraw() external onlyOwner {
        uint256 balance = address(this).balance;
        payable(owner()).transfer(balance);
    }
    
    function totalSupply() public view returns (uint256) {
        return _tokenIdCounter.current() - 1;
    }
    
    // Override required functions
    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }
    
    function tokenURI(uint256 tokenId) public view override(ERC721, ERC721URIStorage) returns (string memory) {
        return super.tokenURI(tokenId);
    }
}
"""
        
        with open(os.path.join(contracts_path, "AppNFT.sol"), "w") as f:
            f.write(nft_contract)
        
        # Deployment script
        deploy_script = """
const { ethers } = require("hardhat");

async function main() {
    const [deployer] = await ethers.getSigners();
    
    console.log("Deploying contracts with account:", deployer.address);
    console.log("Account balance:", (await deployer.getBalance()).toString());
    
    // Deploy AppToken
    const AppToken = await ethers.getContractFactory("AppToken");
    const appToken = await AppToken.deploy();
    await appToken.deployed();
    console.log("AppToken deployed to:", appToken.address);
    
    // Deploy AppNFT
    const AppNFT = await ethers.getContractFactory("AppNFT");
    const appNFT = await AppNFT.deploy();
    await appNFT.deployed();
    console.log("AppNFT deployed to:", appNFT.address);
    
    // Save contract addresses
    const addresses = {
        AppToken: appToken.address,
        AppNFT: appNFT.address
    };
    
    require('fs').writeFileSync(
        'contract-addresses.json',
        JSON.stringify(addresses, null, 2)
    );
    
    console.log("Contract addresses saved to contract-addresses.json");
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
"""
        
        scripts_path = os.path.join(project_path, "blockchain", "scripts")
        os.makedirs(scripts_path, exist_ok=True)
        
        with open(os.path.join(scripts_path, "deploy.js"), "w") as f:
            f.write(deploy_script)
        
        return {
            "files_created": ["AppToken.sol", "AppNFT.sol", "deploy.js"],
            "dependencies": ["@openzeppelin/contracts", "hardhat", "ethers"],
            "contracts": ["ERC20Token", "ERC721NFT"],
            "features": ["token_minting", "nft_marketplace", "ownership_management"]
        }
    
    # IoT Features
    async def _create_iot_device_manager(self, spec: AdvancedFeatureSpec, project_path: str) -> Dict:
        """สร้าง IoT Device Management System"""
        
        iot_path = os.path.join(project_path, "services", "iot-manager")
        os.makedirs(iot_path, exist_ok=True)
        
        # IoT Device Manager
        device_manager = """
from fastapi import FastAPI, WebSocket, HTTPException
from pydantic import BaseModel
import asyncio
import json
import uuid
from typing import Dict, List, Optional
from datetime import datetime
import paho.mqtt.client as mqtt
import redis

app = FastAPI(title="IoT Device Manager", version="1.0.0")

class Device(BaseModel):
    device_id: str
    device_type: str  # sensor, actuator, gateway
    name: str
    location: str
    status: str = "offline"
    last_seen: Optional[datetime] = None
    configuration: Dict = {}

class SensorData(BaseModel):
    device_id: str
    sensor_type: str
    value: float
    unit: str
    timestamp: datetime
    metadata: Optional[Dict] = {}

class IoTDeviceManager:
    def __init__(self):
        self.devices: Dict[str, Device] = {}
        self.mqtt_client = None
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.websocket_connections: Dict[str, WebSocket] = {}
        
    async def initialize(self):
        \"\"\"Initialize MQTT and other connections\"\"\"
        self.setup_mqtt()
        
    def setup_mqtt(self):
        \"\"\"Setup MQTT client for device communication\"\"\"
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.on_message = self.on_mqtt_message
        
        # Connect to MQTT broker
        self.mqtt_client.connect("localhost", 1883, 60)
        self.mqtt_client.loop_start()
        
    def on_mqtt_connect(self, client, userdata, flags, rc):
        \"\"\"Callback when MQTT connects\"\"\"
        print(f"Connected to MQTT broker with result code {rc}")
        
        # Subscribe to device topics
        client.subscribe("devices/+/status")
        client.subscribe("devices/+/data")
        client.subscribe("devices/+/heartbeat")
        
    def on_mqtt_message(self, client, userdata, msg):
        \"\"\"Handle incoming MQTT messages\"\"\"
        topic_parts = msg.topic.split('/')
        device_id = topic_parts[1]
        message_type = topic_parts[2]
        
        try:
            payload = json.loads(msg.payload.decode())
            asyncio.create_task(self.process_device_message(device_id, message_type, payload))
        except Exception as e:
            print(f"Error processing MQTT message: {e}")
    
    async def process_device_message(self, device_id: str, message_type: str, payload: Dict):
        \"\"\"Process incoming device messages\"\"\"
        
        if message_type == "heartbeat":
            await self.update_device_heartbeat(device_id)
        elif message_type == "data":
            await self.store_sensor_data(device_id, payload)
        elif message_type == "status":
            await self.update_device_status(device_id, payload)
        
        # Broadcast to WebSocket connections
        await self.broadcast_to_websockets({
            "device_id": device_id,
            "message_type": message_type,
            "payload": payload,
            "timestamp": datetime.now().isoformat()
        })
    
    async def register_device(self, device: Device) -> Device:
        \"\"\"Register a new IoT device\"\"\"
        device.status = "online"
        device.last_seen = datetime.now()
        
        self.devices[device.device_id] = device
        
        # Store in Redis for persistence
        device_data = device.dict()
        device_data['last_seen'] = device_data['last_seen'].isoformat()
        self.redis_client.hset(f"device:{device.device_id}", mapping=device_data)
        
        # Subscribe to device-specific MQTT topics
        if self.mqtt_client:
            self.mqtt_client.subscribe(f"devices/{device.device_id}/+")
        
        return device
    
    async def store_sensor_data(self, device_id: str, data: Dict):
        \"\"\"Store sensor data with timestamp\"\"\"
        sensor_data = SensorData(
            device_id=device_id,
            sensor_type=data.get('sensor_type'),
            value=data.get('value'),
            unit=data.get('unit', ''),
            timestamp=datetime.now(),
            metadata=data.get('metadata', {})
        )
        
        # Store in time series format
        ts_key = f"sensor_data:{device_id}:{sensor_data.sensor_type}"
        ts_data = {
            "timestamp": sensor_data.timestamp.isoformat(),
            "value": sensor_data.value,
            "unit": sensor_data.unit,
            "metadata": json.dumps(sensor_data.metadata)
        }
        
        self.redis_client.zadd(ts_key, {json.dumps(ts_data): sensor_data.timestamp.timestamp()})
        
        # Keep only last 1000 readings per sensor
        self.redis_client.zremrangebyrank(ts_key, 0, -1001)
    
    async def send_command_to_device(self, device_id: str, command: Dict):
        \"\"\"Send command to IoT device via MQTT\"\"\"
        if self.mqtt_client and device_id in self.devices:
            topic = f"devices/{device_id}/commands"
            self.mqtt_client.publish(topic, json.dumps(command))
            return {"status": "sent", "command": command}
        else:
            raise HTTPException(status_code=404, detail="Device not found")
    
    async def get_device_data(self, device_id: str, sensor_type: str, hours: int = 24) -> List[Dict]:
        \"\"\"Get historical sensor data\"\"\"
        ts_key = f"sensor_data:{device_id}:{sensor_type}"
        
        # Get data from last N hours
        end_time = datetime.now().timestamp()
        start_time = end_time - (hours * 3600)
        
        data = self.redis_client.zrangebyscore(ts_key, start_time, end_time)
        
        result = []
        for item in data:
            sensor_reading = json.loads(item)
            result.append(sensor_reading)
        
        return result
    
    async def broadcast_to_websockets(self, message: Dict):
        \"\"\"Broadcast message to all WebSocket connections\"\"\"
        disconnected = []
        
        for connection_id, websocket in self.websocket_connections.items():
            try:
                await websocket.send_text(json.dumps(message))
            except:
                disconnected.append(connection_id)
        
        # Clean up disconnected connections
        for connection_id in disconnected:
            del self.websocket_connections[connection_id]

# Initialize IoT manager
iot_manager = IoTDeviceManager()

@app.on_event("startup")
async def startup_event():
    await iot_manager.initialize()

@app.post("/devices", response_model=Device)
async def register_device(device: Device):
    return await iot_manager.register_device(device)

@app.get("/devices")
async def list_devices():
    return list(iot_manager.devices.values())

@app.post("/devices/{device_id}/command")
async def send_device_command(device_id: str, command: Dict):
    return await iot_manager.send_command_to_device(device_id, command)

@app.get("/devices/{device_id}/data/{sensor_type}")
async def get_sensor_data(device_id: str, sensor_type: str, hours: int = 24):
    return await iot_manager.get_device_data(device_id, sensor_type, hours)

@app.websocket("/ws/{connection_id}")
async def websocket_endpoint(websocket: WebSocket, connection_id: str):
    await websocket.accept()
    iot_manager.websocket_connections[connection_id] = websocket
    
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except:
        if connection_id in iot_manager.websocket_connections:
            del iot_manager.websocket_connections[connection_id]

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "iot-manager"}
"""
        
        with open(os.path.join(iot_path, "main.py"), "w", encoding="utf-8") as f:
            f.write(device_manager)
        
        return {
            "files_created": ["main.py"],
            "dependencies": ["paho-mqtt", "redis"],
            "api_endpoints": ["/devices", "/devices/{id}/command", "/devices/{id}/data/{sensor}"],
            "features": ["device_registration", "real_time_monitoring", "command_sending", "data_storage"]
        }
    
    async def _integrate_feature(self, feature_result: Dict, project_path: str, pattern: str) -> Dict:
        """Integrate feature กับโปรเจกต์"""
        
        integration_method = self.integration_patterns.get(pattern, self._integrate_as_microservice)
        return await integration_method(feature_result, project_path)
    
    async def _integrate_as_microservice(self, feature_result: Dict, project_path: str) -> Dict:
        """Integrate เป็น microservice"""
        
        # Update docker-compose.yml
        compose_path = os.path.join(project_path, "docker-compose.yml")
        
        # Add service to compose file (simplified)
        return {"integration_type": "microservice", "status": "integrated"}
    
    def _create_content_moderation(self, project_path: str, config: Dict) -> str:
        """สร้าง Content Moderation System"""
        
        moderation_path = os.path.join(project_path, "content_moderation")
        os.makedirs(moderation_path, exist_ok=True)
        
        # Content moderation service
        moderation_service = """
from typing import Dict, List, Optional
import re
import asyncio
from datetime import datetime

class ContentModerationSystem:
    def __init__(self, api_key: str = None):
        self.openai_key = api_key
        self.banned_words = ["spam", "scam", "fake", "hate"]
        self.toxicity_threshold = 0.7
        self.spam_threshold = 0.8
        
    async def moderate_text(self, text: str, user_id: str = None) -> Dict:
        \"\"\"วิเคราะห์และจัดการข้อความ\"\"\"
        
        result = {
            "original_text": text,
            "is_approved": True,
            "violations": [],
            "severity": "low", 
            "filtered_text": text,
            "timestamp": datetime.now().isoformat()
        }
        
        # Basic checks
        if len(text.strip()) == 0:
            result["violations"].append("empty_text")
            result["is_approved"] = False
            return result
        
        return result
"""
        
        with open(os.path.join(moderation_path, "content_moderator.py"), "w") as f:
            f.write(moderation_service)
        
        return os.path.join(moderation_path, "content_moderator.py")
    
    def _create_image_recognition(self, project_path: str, config: Dict) -> str:
        """สร้าง Image Recognition System"""
        
        vision_path = os.path.join(project_path, "image_recognition")
        os.makedirs(vision_path, exist_ok=True)
        
        # Image recognition service
        vision_service = """
from typing import Dict, List, Optional
import cv2
import numpy as np
from PIL import Image
import base64
from io import BytesIO

class ImageRecognitionSystem:
    def __init__(self, model_path: str = None):
        self.model_path = model_path
        self.confidence_threshold = 0.7
        
    async def recognize_objects(self, image_path: str) -> Dict:
        \"\"\"ตรวจจับวัตถุในรูปภาพ\"\"\"
        
        result = {
            "image_path": image_path,
            "objects_detected": [],
            "confidence_scores": [],
            "processing_time": 0.0,
            "status": "success"
        }
        
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                result["status"] = "error"
                result["message"] = "Cannot load image"
                return result
            
            # Simplified object detection
            objects = ["person", "car", "building", "tree", "animal"]
            for obj in objects:
                confidence = np.random.uniform(0.3, 0.95)  # Mock confidence
                if confidence > self.confidence_threshold:
                    result["objects_detected"].append(obj)
                    result["confidence_scores"].append(confidence)
            
            return result
            
        except Exception as e:
            result["status"] = "error"
            result["message"] = str(e)
            return result
    
    async def classify_image(self, image_path: str) -> Dict:
        \"\"\"จำแนกประเภทรูปภาพ\"\"\"
        
        categories = ["nature", "people", "vehicle", "building", "food", "animal"]
        predicted_category = np.random.choice(categories)
        confidence = np.random.uniform(0.7, 0.98)
        
        return {
            "image_path": image_path,
            "predicted_category": predicted_category,
            "confidence": confidence,
            "all_predictions": {cat: np.random.uniform(0.1, 0.9) for cat in categories}
        }
    
    def process_base64_image(self, base64_string: str) -> Dict:
        \"\"\"ประมวลผลรูปภาพ base64\"\"\"
        
        try:
            # Decode base64 to image
            image_data = base64.b64decode(base64_string)
            image = Image.open(BytesIO(image_data))
            
            # Convert to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            return {
                "status": "success", 
                "image_size": image.size,
                "format": image.format
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
"""
        
        with open(os.path.join(vision_path, "image_recognizer.py"), "w") as f:
            f.write(vision_service)
        
        return os.path.join(vision_path, "image_recognizer.py")
    
    def _create_nlp_service(self, project_path: str, config: Dict) -> str:
        """สร้าง Natural Language Processing Service"""
        
        nlp_path = os.path.join(project_path, "nlp_service") 
        os.makedirs(nlp_path, exist_ok=True)
        
        nlp_service = """
from typing import Dict, List, Optional
import re
from datetime import datetime

class NLPService:
    def __init__(self):
        self.sentiment_keywords = {
            'positive': ['good', 'great', 'excellent', 'amazing', 'love'],
            'negative': ['bad', 'terrible', 'awful', 'hate', 'worst'],
            'neutral': ['okay', 'fine', 'normal', 'average']
        }
    
    def analyze_sentiment(self, text: str) -> Dict:
        \"\"\"วิเคราะห์อารมณ์ในข้อความ\"\"\"
        
        text_lower = text.lower()
        positive_count = sum(1 for word in self.sentiment_keywords['positive'] if word in text_lower)
        negative_count = sum(1 for word in self.sentiment_keywords['negative'] if word in text_lower) 
        
        if positive_count > negative_count:
            sentiment = 'positive'
            confidence = min(positive_count / len(text.split()) * 2, 1.0)
        elif negative_count > positive_count:
            sentiment = 'negative'
            confidence = min(negative_count / len(text.split()) * 2, 1.0)
        else:
            sentiment = 'neutral'
            confidence = 0.5
            
        return {
            'text': text,
            'sentiment': sentiment,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        }
    
    def extract_entities(self, text: str) -> Dict:
        \"\"\"แยกเอนทิตี้จากข้อความ\"\"\"
        
        # Simple entity extraction
        email_pattern = r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b'
        phone_pattern = r'\\b\\d{3}-\\d{3}-\\d{4}\\b|\\b\\d{10}\\b'
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        
        emails = re.findall(email_pattern, text)
        phones = re.findall(phone_pattern, text)
        urls = re.findall(url_pattern, text)
        
        return {
            'emails': emails,
            'phones': phones,
            'urls': urls,
            'text': text
        }
"""
        
        with open(os.path.join(nlp_path, "nlp_processor.py"), "w") as f:
            f.write(nlp_service)
        
        return os.path.join(nlp_path, "nlp_processor.py")
    
    def _create_fraud_detection(self, project_path: str, config: Dict) -> str:
        """สร้าง Fraud Detection System"""
        
        fraud_path = os.path.join(project_path, "fraud_detection")
        os.makedirs(fraud_path, exist_ok=True)
        
        fraud_service = """
from typing import Dict, List, Optional
import json
from datetime import datetime, timedelta

class FraudDetectionSystem:
    def __init__(self):
        self.risk_rules = {
            'max_transaction_amount': 10000,
            'max_daily_transactions': 50,
            'velocity_threshold': 5,  # transactions per hour
            'suspicious_locations': ['Unknown', 'VPN'],
            'blacklisted_ips': []
        }
    
    def analyze_transaction(self, transaction: Dict) -> Dict:
        \"\"\"วิเคราะห์ธุรกรรมเพื่อตรวจจับการฉ้อโกง\"\"\"
        
        risk_score = 0.0
        risk_factors = []
        
        # Amount-based risk
        amount = transaction.get('amount', 0)
        if amount > self.risk_rules['max_transaction_amount']:
            risk_score += 0.4
            risk_factors.append('high_amount')
        
        # Frequency-based risk  
        user_id = transaction.get('user_id')
        recent_transactions = self._get_recent_transactions(user_id)
        if len(recent_transactions) > self.risk_rules['velocity_threshold']:
            risk_score += 0.3
            risk_factors.append('high_velocity')
        
        # Location-based risk
        location = transaction.get('location', 'Unknown')
        if location in self.risk_rules['suspicious_locations']:
            risk_score += 0.2
            risk_factors.append('suspicious_location')
        
        # IP-based risk
        ip_address = transaction.get('ip_address')
        if ip_address in self.risk_rules['blacklisted_ips']:
            risk_score += 0.5
            risk_factors.append('blacklisted_ip')
        
        risk_level = self._calculate_risk_level(risk_score)
        
        return {
            'transaction_id': transaction.get('id'),
            'risk_score': min(risk_score, 1.0),
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'recommendation': self._get_recommendation(risk_level),
            'analyzed_at': datetime.now().isoformat()
        }
    
    def _calculate_risk_level(self, score: float) -> str:
        \"\"\"คำนวณระดับความเสี่ยง\"\"\"
        if score >= 0.7:
            return 'high'
        elif score >= 0.4:
            return 'medium'
        else:
            return 'low'
    
    def _get_recommendation(self, risk_level: str) -> str:
        \"\"\"แนะนำการดำเนินการ\"\"\"
        recommendations = {
            'low': 'approve',
            'medium': 'review', 
            'high': 'block'
        }
        return recommendations.get(risk_level, 'review')
    
    def _get_recent_transactions(self, user_id: str) -> List:
        \"\"\"ดึงธุรกรรมล่าสุด (mock data)\"\"\"
        # In production, this would query the database
        return []  # Mock empty list
"""
        
        with open(os.path.join(fraud_path, "fraud_detector.py"), "w") as f:
            f.write(fraud_service)
        
        return os.path.join(fraud_path, "fraud_detector.py")
    
    def _create_predictive_analytics(self, project_path: str, config: Dict) -> str:
        """สร้าง Predictive Analytics System"""
        
        analytics_path = os.path.join(project_path, "predictive_analytics")
        os.makedirs(analytics_path, exist_ok=True)
        
        analytics_service = """
from typing import Dict, List, Optional
import numpy as np
from datetime import datetime, timedelta
import json

class PredictiveAnalyticsSystem:
    def __init__(self):
        self.models = {}
        self.data_cache = {}
    
    def predict_user_behavior(self, user_id: str, historical_data: List[Dict]) -> Dict:
        \"\"\"ทำนายพฤติกรรมผู้ใช้\"\"\"
        
        if not historical_data:
            return {
                'user_id': user_id,
                'prediction': 'insufficient_data',
                'confidence': 0.0,
                'recommendations': []
            }
        
        # Simple behavior prediction based on patterns
        action_counts = {}
        for data in historical_data:
            action = data.get('action', 'unknown')
            action_counts[action] = action_counts.get(action, 0) + 1
        
        most_common_action = max(action_counts, key=action_counts.get)
        confidence = action_counts[most_common_action] / len(historical_data)
        
        return {
            'user_id': user_id,
            'predicted_next_action': most_common_action,
            'confidence': confidence,
            'action_pattern': action_counts,
            'recommendations': self._generate_recommendations(most_common_action),
            'predicted_at': datetime.now().isoformat()
        }
    
    def predict_sales_trends(self, sales_data: List[Dict]) -> Dict:
        \"\"\"ทำนายแนวโน้มยอดขาย\"\"\"
        
        if len(sales_data) < 2:
            return {'error': 'insufficient_data'}
        
        # Calculate simple trend
        amounts = [item.get('amount', 0) for item in sales_data]
        recent_avg = np.mean(amounts[-7:]) if len(amounts) >= 7 else np.mean(amounts)
        overall_avg = np.mean(amounts)
        
        trend = 'increasing' if recent_avg > overall_avg else 'decreasing'
        confidence = abs(recent_avg - overall_avg) / overall_avg if overall_avg > 0 else 0
        
        # Simple future prediction
        next_month_prediction = recent_avg * 1.1 if trend == 'increasing' else recent_avg * 0.9
        
        return {
            'current_trend': trend,
            'confidence': min(confidence, 1.0),
            'next_month_prediction': next_month_prediction,
            'recommendation': self._get_sales_recommendation(trend),
            'data_points_analyzed': len(sales_data),
            'analysis_date': datetime.now().isoformat()
        }
    
    def detect_anomalies(self, data_points: List[float]) -> Dict:
        \"\"\"ตรวจจับความผิดปกติในข้อมูล\"\"\"
        
        if len(data_points) < 5:
            return {'error': 'insufficient_data'}
        
        # Simple anomaly detection using standard deviation
        mean_val = np.mean(data_points)
        std_val = np.std(data_points)
        threshold = 2 * std_val
        
        anomalies = []
        for i, value in enumerate(data_points):
            if abs(value - mean_val) > threshold:
                anomalies.append({
                    'index': i,
                    'value': value,
                    'deviation': abs(value - mean_val)
                })
        
        return {
            'anomalies_detected': len(anomalies),
            'anomalies': anomalies,
            'mean_value': mean_val,
            'threshold': threshold,
            'anomaly_rate': len(anomalies) / len(data_points),
            'detected_at': datetime.now().isoformat()
        }
    
    def _generate_recommendations(self, predicted_action: str) -> List[str]:
        \"\"\"สร้างข้อแนะนำ\"\"\"
        recommendations_map = {
            'purchase': ['Show related products', 'Offer discount', 'Send follow-up email'],
            'browse': ['Suggest popular items', 'Show personalized content'],
            'search': ['Improve search results', 'Show search suggestions'],
            'login': ['Welcome back message', 'Show recent activity'],
            'logout': ['Save session', 'Send return incentive']
        }
        return recommendations_map.get(predicted_action, ['Monitor user behavior'])
    
    def _get_sales_recommendation(self, trend: str) -> str:
        \"\"\"แนะนำกลยุทธ์ยอดขาย\"\"\"
        if trend == 'increasing':
            return 'Capitalize on growth - increase marketing budget'
        else:
            return 'Focus on retention and new customer acquisition'
"""
        
        with open(os.path.join(analytics_path, "predictive_engine.py"), "w") as f:
            f.write(analytics_service)
        
        return os.path.join(analytics_path, "predictive_engine.py")
    
    def _create_nft_marketplace(self, project_path: str, config: Dict) -> str:
        """สร้าง NFT Marketplace"""
        
        nft_path = os.path.join(project_path, "nft_marketplace")
        os.makedirs(nft_path, exist_ok=True)
        
        nft_contract = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract NFTMarketplace is ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;
    
    mapping(uint256 => uint256) private _prices;
    mapping(uint256 => bool) private _forSale;
    
    event NFTMinted(uint256 tokenId, address owner, string tokenURI);
    event NFTListedForSale(uint256 tokenId, uint256 price);
    event NFTSold(uint256 tokenId, address buyer, uint256 price);
    
    constructor() ERC721("NFTMarketplace", "NFTM") {}
    
    function mintNFT(address recipient, string memory tokenURI) public onlyOwner returns (uint256) {
        _tokenIds.increment();
        uint256 newTokenId = _tokenIds.current();
        _mint(recipient, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
        
        emit NFTMinted(newTokenId, recipient, tokenURI);
        return newTokenId;
    }
    
    function listForSale(uint256 tokenId, uint256 price) public {
        require(ownerOf(tokenId) == msg.sender, "Not the owner");
        require(price > 0, "Price must be greater than 0");
        
        _prices[tokenId] = price;
        _forSale[tokenId] = true;
        approve(address(this), tokenId);
        
        emit NFTListedForSale(tokenId, price);
    }
    
    function buyNFT(uint256 tokenId) public payable {
        require(_forSale[tokenId], "NFT not for sale");
        require(msg.value >= _prices[tokenId], "Insufficient payment");
        
        address seller = ownerOf(tokenId);
        _transfer(seller, msg.sender, tokenId);
        _forSale[tokenId] = false;
        
        payable(seller).transfer(msg.value);
        
        emit NFTSold(tokenId, msg.sender, msg.value);
    }
}
"""
        
        with open(os.path.join(nft_path, "NFTMarketplace.sol"), "w") as f:
            f.write(nft_contract)
        
        return os.path.join(nft_path, "NFTMarketplace.sol")
    
    def _integrate_event_driven(self, project_path: str, integration_config: Dict) -> Dict:
        """สร้าง Event-Driven Architecture Integration"""
        
        event_path = os.path.join(project_path, "event_system")
        os.makedirs(event_path, exist_ok=True)
        
        # Event manager
        event_manager = """
from typing import Dict, List, Optional, Callable
import asyncio
import json
from datetime import datetime
import uuid

class EventManager:
    def __init__(self):
        self.listeners = {}
        self.event_history = []
        
    async def emit_event(self, event_type: str, data: Dict, source: str = None):
        \"\"\"ส่ง event\"\"\"
        
        event = {
            'id': str(uuid.uuid4()),
            'type': event_type,
            'data': data,
            'source': source,
            'timestamp': datetime.now().isoformat()
        }
        
        # เก็บประวัติ
        self.event_history.append(event)
        
        # ส่งให้ listeners
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                try:
                    if asyncio.iscoroutinefunction(listener):
                        await listener(event)
                    else:
                        listener(event)
                except Exception as e:
                    print(f"Error in event listener: {e}")
        
        return event['id']
    
    def add_listener(self, event_type: str, callback: Callable):
        \"\"\"เพิ่ม event listener\"\"\"
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)
    
    def remove_listener(self, event_type: str, callback: Callable):
        \"\"\"ลบ event listener\"\"\"
        if event_type in self.listeners:
            if callback in self.listeners[event_type]:
                self.listeners[event_type].remove(callback)
    
    def get_event_history(self, event_type: str = None, limit: int = 100):
        \"\"\"ดูประวัติ events\"\"\"
        if event_type:
            filtered = [e for e in self.event_history if e['type'] == event_type]
        else:
            filtered = self.event_history
        
        return filtered[-limit:]

# Global event manager
event_manager = EventManager()

# Example usage
async def example_listener(event):
    print(f"Received event: {event['type']} - {event['data']}")

# Register listeners
event_manager.add_listener('user_registered', example_listener)
event_manager.add_listener('order_created', example_listener)
"""
        
        with open(os.path.join(event_path, "event_manager.py"), "w") as f:
            f.write(event_manager)
        
        return {"integration_type": "event_driven", "status": "integrated"}
    
    def _create_crypto_wallet(self, project_path: str, config: Dict) -> str:
        """สร้าง Cryptocurrency Wallet"""
        
        wallet_path = os.path.join(project_path, "crypto_wallet")
        os.makedirs(wallet_path, exist_ok=True)
        
        wallet_service = """
from typing import Dict, List, Optional
import hashlib
import secrets
from cryptography.fernet import Fernet
import json
from datetime import datetime

class CryptoWallet:
    def __init__(self, password: str = None):
        self.password = password
        self.balances = {}
        self.transaction_history = []
        self._encryption_key = self._generate_key(password) if password else None
    
    def create_wallet(self, wallet_name: str) -> Dict:
        \"\"\"สร้าง wallet ใหม่\"\"\"
        
        # Generate new wallet address (simplified)
        private_key = secrets.token_hex(32)
        public_key = hashlib.sha256(private_key.encode()).hexdigest()
        wallet_address = f"0x{public_key[:40]}"
        
        wallet_info = {
            "wallet_name": wallet_name,
            "address": wallet_address,
            "private_key": private_key,  # Should be encrypted in production
            "created_at": datetime.now().isoformat(),
            "balance": {
                "BTC": 0.0,
                "ETH": 0.0,
                "USDT": 0.0
            }
        }
        
        return wallet_info
    
    def get_balance(self, address: str, currency: str = "BTC") -> float:
        \"\"\"ดูยอดเงิน\"\"\"
        return self.balances.get(address, {}).get(currency, 0.0)
    
    def send_transaction(self, from_address: str, to_address: str, 
                        amount: float, currency: str = "BTC") -> Dict:
        \"\"\"ส่งเหรียญ\"\"\"
        
        # Check balance
        current_balance = self.get_balance(from_address, currency)
        if current_balance < amount:
            return {
                "status": "failed",
                "message": "Insufficient balance",
                "transaction_id": None
            }
        
        # Create transaction
        transaction_id = hashlib.sha256(
            f"{from_address}{to_address}{amount}{datetime.now()}".encode()
        ).hexdigest()
        
        transaction = {
            "transaction_id": transaction_id,
            "from_address": from_address,
            "to_address": to_address,
            "amount": amount,
            "currency": currency,
            "timestamp": datetime.now().isoformat(),
            "status": "confirmed"
        }
        
        # Update balances (simplified)
        if from_address not in self.balances:
            self.balances[from_address] = {}
        if to_address not in self.balances:
            self.balances[to_address] = {}
        
        self.balances[from_address][currency] = current_balance - amount
        self.balances[to_address][currency] = self.balances[to_address].get(currency, 0) + amount
        
        self.transaction_history.append(transaction)
        
        return {
            "status": "success",
            "message": "Transaction completed",
            "transaction_id": transaction_id,
            "transaction": transaction
        }
    
    def get_transaction_history(self, address: str) -> List[Dict]:
        \"\"\"ดูประวัติธุรกรรม\"\"\"
        return [
            tx for tx in self.transaction_history
            if tx["from_address"] == address or tx["to_address"] == address
        ]
    
    def _generate_key(self, password: str) -> bytes:
        \"\"\"สร้างกุญแจเข้ารหัส\"\"\"
        return Fernet.generate_key()
"""
        
        with open(os.path.join(wallet_path, "crypto_wallet.py"), "w") as f:
            f.write(wallet_service)
        
        return os.path.join(wallet_path, "crypto_wallet.py")
    
    def _create_decentralized_storage(self, project_path: str, config: Dict) -> str:
        """สร้าง Decentralized Storage System"""
        
        storage_path = os.path.join(project_path, "decentralized_storage")
        os.makedirs(storage_path, exist_ok=True)
        
        storage_service = """
from typing import Dict, List, Optional
import hashlib
import json
import os
from datetime import datetime
import ipfshttpclient

class DecentralizedStorage:
    def __init__(self, ipfs_api: str = "/ip4/127.0.0.1/tcp/5001"):
        self.ipfs_api = ipfs_api
        self.file_registry = {}
        
    def upload_file(self, file_path: str, metadata: Dict = None) -> Dict:
        \"\"\"อัพโหลดไฟล์ไป IPFS\"\"\"
        
        try:
            # Calculate file hash
            file_hash = self._calculate_file_hash(file_path)
            
            # Mock IPFS upload (in production, use actual IPFS)
            ipfs_hash = f"Qm{hashlib.sha256(file_path.encode()).hexdigest()[:44]}"
            
            file_info = {
                "file_path": file_path,
                "file_hash": file_hash,
                "ipfs_hash": ipfs_hash,
                "file_size": os.path.getsize(file_path) if os.path.exists(file_path) else 0,
                "uploaded_at": datetime.now().isoformat(),
                "metadata": metadata or {},
                "status": "uploaded"
            }
            
            # Store in registry
            self.file_registry[ipfs_hash] = file_info
            
            return {
                "status": "success",
                "ipfs_hash": ipfs_hash,
                "file_info": file_info
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def download_file(self, ipfs_hash: str, save_path: str) -> Dict:
        \"\"\"ดาวน์โหลดไฟล์จาก IPFS\"\"\"
        
        if ipfs_hash not in self.file_registry:
            return {
                "status": "error",
                "message": "File not found in registry"
            }
        
        file_info = self.file_registry[ipfs_hash]
        
        # Mock download process
        try:
            # In production, download from actual IPFS network
            return {
                "status": "success",
                "saved_to": save_path,
                "file_info": file_info
            }
        except Exception as e:
            return {
                "status": "error", 
                "message": str(e)
            }
    
    def get_file_info(self, ipfs_hash: str) -> Dict:
        \"\"\"ดูข้อมูลไฟล์\"\"\"
        return self.file_registry.get(ipfs_hash, {})
    
    def list_files(self) -> List[Dict]:
        \"\"\"ดูรายการไฟล์ทั้งหมด\"\"\"
        return list(self.file_registry.values())
    
    def _calculate_file_hash(self, file_path: str) -> str:
        \"\"\"คำนวณ hash ของไฟล์\"\"\"
        if not os.path.exists(file_path):
            return hashlib.sha256(file_path.encode()).hexdigest()
        
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
"""
        
        with open(os.path.join(storage_path, "ipfs_storage.py"), "w") as f:
            f.write(storage_service)
        
        return os.path.join(storage_path, "ipfs_storage.py")
    
    def _create_dao_system(self, project_path: str, config: Dict) -> str:
        """สร้าง DAO (Decentralized Autonomous Organization) System"""
        
        dao_path = os.path.join(project_path, "dao_system")
        os.makedirs(dao_path, exist_ok=True)
        
        dao_contract = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DAOGovernance {
    struct Proposal {
        uint256 id;
        string title;
        string description;
        uint256 votesFor;
        uint256 votesAgainst;
        uint256 deadline;
        bool executed;
        address proposer;
    }
    
    mapping(uint256 => Proposal) public proposals;
    mapping(uint256 => mapping(address => bool)) public hasVoted;
    mapping(address => uint256) public tokenBalance;
    
    uint256 public proposalCount;
    uint256 public totalSupply;
    string public name = "DAO Governance Token";
    
    event ProposalCreated(uint256 proposalId, string title, address proposer);
    event Voted(uint256 proposalId, address voter, bool support, uint256 weight);
    event ProposalExecuted(uint256 proposalId);
    
    constructor(uint256 _totalSupply) {
        totalSupply = _totalSupply;
        tokenBalance[msg.sender] = _totalSupply;
    }
    
    function createProposal(string memory _title, string memory _description) public {
        require(tokenBalance[msg.sender] > 0, "Must hold tokens to create proposal");
        
        proposalCount++;
        proposals[proposalCount] = Proposal({
            id: proposalCount,
            title: _title,
            description: _description,
            votesFor: 0,
            votesAgainst: 0,
            deadline: block.timestamp + 7 days,
            executed: false,
            proposer: msg.sender
        });
        
        emit ProposalCreated(proposalCount, _title, msg.sender);
    }
    
    function vote(uint256 _proposalId, bool _support) public {
        require(tokenBalance[msg.sender] > 0, "Must hold tokens to vote");
        require(!hasVoted[_proposalId][msg.sender], "Already voted");
        require(block.timestamp < proposals[_proposalId].deadline, "Voting period ended");
        
        uint256 weight = tokenBalance[msg.sender];
        
        if (_support) {
            proposals[_proposalId].votesFor += weight;
        } else {
            proposals[_proposalId].votesAgainst += weight;
        }
        
        hasVoted[_proposalId][msg.sender] = true;
        
        emit Voted(_proposalId, msg.sender, _support, weight);
    }
    
    function executeProposal(uint256 _proposalId) public {
        Proposal storage proposal = proposals[_proposalId];
        require(block.timestamp >= proposal.deadline, "Voting still active");
        require(!proposal.executed, "Proposal already executed");
        require(proposal.votesFor > proposal.votesAgainst, "Proposal rejected");
        
        proposal.executed = true;
        
        emit ProposalExecuted(_proposalId);
    }
}
"""
        
        with open(os.path.join(dao_path, "DAOGovernance.sol"), "w") as f:
            f.write(dao_contract)
        
        return os.path.join(dao_path, "DAOGovernance.sol")
    
    def _create_sensor_processor(self, project_path: str, config: Dict) -> str:
        """สร้าง Sensor Data Processor"""
        
        sensor_path = os.path.join(project_path, "sensor_processor")
        os.makedirs(sensor_path, exist_ok=True)
        
        sensor_service = """
from typing import Dict, List, Optional
import json
import asyncio
from datetime import datetime
import statistics

class SensorDataProcessor:
    def __init__(self):
        self.sensor_data = {}
        self.alert_thresholds = {
            'temperature': {'min': -10, 'max': 50},
            'humidity': {'min': 0, 'max': 100},
            'pressure': {'min': 900, 'max': 1100}
        }
        
    async def process_sensor_data(self, sensor_id: str, data: Dict) -> Dict:
        \"\"\"ประมวลผลข้อมูล sensor\"\"\"
        
        timestamp = datetime.now().isoformat()
        
        # Store raw data
        if sensor_id not in self.sensor_data:
            self.sensor_data[sensor_id] = []
        
        processed_data = {
            'sensor_id': sensor_id,
            'timestamp': timestamp,
            'raw_data': data,
            'processed_metrics': {},
            'alerts': []
        }
        
        # Process each metric
        for metric, value in data.items():
            if isinstance(value, (int, float)):
                processed_data['processed_metrics'][metric] = {
                    'current_value': value,
                    'status': self._check_threshold(metric, value),
                    'trend': self._calculate_trend(sensor_id, metric, value)
                }
                
                # Check for alerts
                alert = self._check_alert(metric, value)
                if alert:
                    processed_data['alerts'].append(alert)
        
        # Store processed data
        self.sensor_data[sensor_id].append(processed_data)
        
        # Keep only last 100 readings
        if len(self.sensor_data[sensor_id]) > 100:
            self.sensor_data[sensor_id] = self.sensor_data[sensor_id][-100:]
        
        return processed_data
    
    def get_sensor_analytics(self, sensor_id: str, metric: str = None) -> Dict:
        \"\"\"ดูสถิติ sensor\"\"\"
        
        if sensor_id not in self.sensor_data:
            return {'error': 'Sensor not found'}
        
        data_points = self.sensor_data[sensor_id]
        
        if not data_points:
            return {'error': 'No data available'}
        
        analytics = {
            'sensor_id': sensor_id,
            'total_readings': len(data_points),
            'time_range': {
                'start': data_points[0]['timestamp'],
                'end': data_points[-1]['timestamp']
            }
        }
        
        if metric:
            values = []
            for point in data_points:
                if metric in point['processed_metrics']:
                    values.append(point['processed_metrics'][metric]['current_value'])
            
            if values:
                analytics['metric_analytics'] = {
                    'metric': metric,
                    'min': min(values),
                    'max': max(values),
                    'avg': statistics.mean(values),
                    'count': len(values)
                }
        
        return analytics
    
    def _check_threshold(self, metric: str, value: float) -> str:
        \"\"\"ตรวจสอบค่าเกณฑ์\"\"\"
        
        if metric in self.alert_thresholds:
            thresholds = self.alert_thresholds[metric]
            if value < thresholds['min'] or value > thresholds['max']:
                return 'critical'
            elif value < thresholds['min'] * 1.1 or value > thresholds['max'] * 0.9:
                return 'warning'
        
        return 'normal'
    
    def _calculate_trend(self, sensor_id: str, metric: str, current_value: float) -> str:
        \"\"\"คำนวณแนวโน้ม\"\"\"
        
        if sensor_id not in self.sensor_data or len(self.sensor_data[sensor_id]) < 2:
            return 'stable'
        
        recent_readings = self.sensor_data[sensor_id][-5:]  # Last 5 readings
        values = []
        
        for reading in recent_readings:
            if metric in reading['processed_metrics']:
                values.append(reading['processed_metrics'][metric]['current_value'])
        
        if len(values) < 2:
            return 'stable'
        
        # Simple trend calculation
        avg_old = statistics.mean(values[:-1])
        if current_value > avg_old * 1.05:
            return 'increasing'
        elif current_value < avg_old * 0.95:
            return 'decreasing'
        else:
            return 'stable'
    
    def _check_alert(self, metric: str, value: float) -> Optional[Dict]:
        \"\"\"ตรวจสอบ alert\"\"\"
        
        if metric in self.alert_thresholds:
            thresholds = self.alert_thresholds[metric]
            
            if value < thresholds['min']:
                return {
                    'type': 'threshold_violation',
                    'severity': 'critical',
                    'message': f'{metric} too low: {value}',
                    'threshold': thresholds['min']
                }
            elif value > thresholds['max']:
                return {
                    'type': 'threshold_violation', 
                    'severity': 'critical',
                    'message': f'{metric} too high: {value}',
                    'threshold': thresholds['max']
                }
        
        return None
"""
        
        with open(os.path.join(sensor_path, "sensor_processor.py"), "w") as f:
            f.write(sensor_service)
        
        return os.path.join(sensor_path, "sensor_processor.py")
    
    def _create_iot_monitoring(self, project_path: str, config: Dict) -> str:
        """สร้าง IoT Real-time Monitoring System"""
        
        monitoring_path = os.path.join(project_path, "iot_monitoring")
        os.makedirs(monitoring_path, exist_ok=True)
        
        monitoring_service = """
from typing import Dict, List, Optional
import asyncio
import json
from datetime import datetime
import websockets

class IoTMonitoringSystem:
    def __init__(self):
        self.devices = {}
        self.alerts = []
        self.monitoring_rules = {}
        
    async def start_monitoring(self, device_list: List[str]):
        \"\"\"เริ่มการ monitoring\"\"\"
        
        for device_id in device_list:
            self.devices[device_id] = {
                'status': 'online',
                'last_seen': datetime.now().isoformat(),
                'data_points': []
            }
        
        print(f'Started monitoring {len(device_list)} devices')
        return {'status': 'monitoring_started', 'devices': len(device_list)}
    
    async def process_device_data(self, device_id: str, data: Dict):
        \"\"\"ประมวลผลข้อมูลจากอุปกรณ์\"\"\"
        
        if device_id not in self.devices:
            self.devices[device_id] = {
                'status': 'online',
                'last_seen': datetime.now().isoformat(),
                'data_points': []
            }
        
        # Update device status
        self.devices[device_id]['last_seen'] = datetime.now().isoformat()
        self.devices[device_id]['status'] = 'online'
        
        # Store data point
        data_point = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        
        self.devices[device_id]['data_points'].append(data_point)
        
        # Keep only last 100 data points
        if len(self.devices[device_id]['data_points']) > 100:
            self.devices[device_id]['data_points'] = self.devices[device_id]['data_points'][-100:]
        
        # Check monitoring rules
        await self._check_monitoring_rules(device_id, data)
        
        return {'status': 'processed', 'device_id': device_id}
    
    def get_device_status(self, device_id: str = None) -> Dict:
        \"\"\"ดูสถานะอุปกรณ์\"\"\"
        
        if device_id:
            return self.devices.get(device_id, {'error': 'Device not found'})
        
        return {
            'total_devices': len(self.devices),
            'online_devices': sum(1 for d in self.devices.values() if d['status'] == 'online'),
            'devices': self.devices
        }
    
    def add_monitoring_rule(self, rule_name: str, rule_config: Dict):
        \"\"\"เพิ่มกฎการ monitoring\"\"\"
        
        self.monitoring_rules[rule_name] = {
            'config': rule_config,
            'created_at': datetime.now().isoformat(),
            'triggered_count': 0
        }
        
        return {'status': 'rule_added', 'rule_name': rule_name}
    
    async def _check_monitoring_rules(self, device_id: str, data: Dict):
        \"\"\"ตรวจสอบกฎการ monitoring\"\"\"
        
        for rule_name, rule_info in self.monitoring_rules.items():
            rule_config = rule_info['config']
            
            # Simple rule checking
            if 'threshold' in rule_config:
                metric = rule_config.get('metric')
                threshold = rule_config.get('threshold')
                condition = rule_config.get('condition', 'greater_than')
                
                if metric in data:
                    value = data[metric]
                    triggered = False
                    
                    if condition == 'greater_than' and value > threshold:
                        triggered = True
                    elif condition == 'less_than' and value < threshold:
                        triggered = True
                    
                    if triggered:
                        alert = {
                            'rule_name': rule_name,
                            'device_id': device_id,
                            'metric': metric,
                            'value': value,
                            'threshold': threshold,
                            'timestamp': datetime.now().isoformat(),
                            'severity': rule_config.get('severity', 'medium')
                        }
                        
                        self.alerts.append(alert)
                        self.monitoring_rules[rule_name]['triggered_count'] += 1
                        
                        # Keep only last 50 alerts
                        if len(self.alerts) > 50:
                            self.alerts = self.alerts[-50:]
    
    def get_alerts(self, device_id: str = None) -> List[Dict]:
        \"\"\"ดู alerts\"\"\"
        
        if device_id:
            return [alert for alert in self.alerts if alert['device_id'] == device_id]
        
        return self.alerts
    
    async def generate_monitoring_report(self) -> Dict:
        \"\"\"สร้างรายงานการ monitoring\"\"\"
        
        total_devices = len(self.devices)
        online_devices = sum(1 for d in self.devices.values() if d['status'] == 'online')
        total_alerts = len(self.alerts)
        
        return {
            'report_generated_at': datetime.now().isoformat(),
            'summary': {
                'total_devices': total_devices,
                'online_devices': online_devices,
                'offline_devices': total_devices - online_devices,
                'total_alerts': total_alerts,
                'active_rules': len(self.monitoring_rules)
            },
            'device_details': self.devices,
            'recent_alerts': self.alerts[-10:] if self.alerts else []
        }
"""
        
        with open(os.path.join(monitoring_path, "iot_monitor.py"), "w") as f:
            f.write(monitoring_service)
        
        return os.path.join(monitoring_path, "iot_monitor.py")
    
    def _create_edge_computing(self, project_path: str, config: Dict) -> str:
        """สร้าง Edge Computing System"""
        
        edge_path = os.path.join(project_path, "edge_computing")
        os.makedirs(edge_path, exist_ok=True)
        
        edge_service = """
from typing import Dict, List, Optional
import asyncio
import json
from datetime import datetime

class EdgeComputingSystem:
    def __init__(self):
        self.edge_nodes = {}
        self.compute_tasks = {}
        self.load_balancer = EdgeLoadBalancer()
        
    def register_edge_node(self, node_id: str, capabilities: Dict) -> Dict:
        \"\"\"ลงทะเบียน edge node\"\"\"
        
        self.edge_nodes[node_id] = {
            'node_id': node_id,
            'capabilities': capabilities,
            'status': 'active',
            'current_load': 0.0,
            'registered_at': datetime.now().isoformat(),
            'tasks_completed': 0
        }
        
        return {
            'status': 'registered',
            'node_id': node_id,
            'capabilities': capabilities
        }
    
    async def submit_compute_task(self, task_data: Dict) -> Dict:
        \"\"\"ส่งงานไปประมวลผลที่ edge\"\"\"
        
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Find best edge node for this task
        selected_node = self.load_balancer.select_node(self.edge_nodes, task_data)
        
        if not selected_node:
            return {
                'status': 'failed',
                'message': 'No suitable edge node available'
            }
        
        # Create task
        task = {
            'task_id': task_id,
            'assigned_node': selected_node,
            'task_data': task_data,
            'status': 'submitted',
            'submitted_at': datetime.now().isoformat(),
            'estimated_completion': None
        }
        
        self.compute_tasks[task_id] = task
        
        # Simulate task processing
        await self._process_task_at_edge(task_id, selected_node, task_data)
        
        return {
            'status': 'submitted',
            'task_id': task_id,
            'assigned_node': selected_node
        }
    
    async def _process_task_at_edge(self, task_id: str, node_id: str, task_data: Dict):
        \"\"\"ประมวลผลงานที่ edge node\"\"\"
        
        # Update task status
        self.compute_tasks[task_id]['status'] = 'processing'
        self.compute_tasks[task_id]['started_at'] = datetime.now().isoformat()
        
        # Update node load
        self.edge_nodes[node_id]['current_load'] += 0.2
        
        # Simulate processing time based on task complexity
        processing_time = task_data.get('complexity', 1) * 2  # seconds
        await asyncio.sleep(processing_time)
        
        # Complete task
        result = {
            'processed_data': task_data,
            'processing_time': processing_time,
            'node_performance': self.edge_nodes[node_id]['capabilities']
        }
        
        self.compute_tasks[task_id].update({
            'status': 'completed',
            'completed_at': datetime.now().isoformat(),
            'result': result
        })
        
        # Update node stats
        self.edge_nodes[node_id]['current_load'] -= 0.2
        self.edge_nodes[node_id]['tasks_completed'] += 1
    
    def get_task_status(self, task_id: str) -> Dict:
        \"\"\"ดูสถานะงาน\"\"\"
        return self.compute_tasks.get(task_id, {'error': 'Task not found'})
    
    def get_edge_nodes_status(self) -> Dict:
        \"\"\"ดูสถานะ edge nodes\"\"\"
        
        total_nodes = len(self.edge_nodes)
        active_nodes = sum(1 for node in self.edge_nodes.values() if node['status'] == 'active')
        
        return {
            'total_nodes': total_nodes,
            'active_nodes': active_nodes,
            'nodes': self.edge_nodes,
            'load_distribution': {
                node_id: node['current_load'] 
                for node_id, node in self.edge_nodes.items()
            }
        }

class EdgeLoadBalancer:
    \"\"\"Load balancer สำหรับ edge computing\"\"\"
    
    def select_node(self, available_nodes: Dict, task_requirements: Dict) -> Optional[str]:
        \"\"\"เลือก edge node ที่เหมาะสมที่สุด\"\"\"
        
        if not available_nodes:
            return None
        
        # Filter active nodes with low load
        suitable_nodes = []
        
        for node_id, node_info in available_nodes.items():
            if (node_info['status'] == 'active' and 
                node_info['current_load'] < 0.8):  # Less than 80% load
                
                # Check if node has required capabilities
                required_capability = task_requirements.get('required_capability')
                if (not required_capability or 
                    required_capability in node_info['capabilities'].get('supported_operations', [])):
                    suitable_nodes.append((node_id, node_info['current_load']))
        
        if not suitable_nodes:
            return None
        
        # Select node with lowest load
        suitable_nodes.sort(key=lambda x: x[1])
        return suitable_nodes[0][0]
"""
        
        with open(os.path.join(edge_path, "edge_computing.py"), "w") as f:
            f.write(edge_service)
        
        return os.path.join(edge_path, "edge_computing.py")
    
    def _create_industrial_automation(self, project_path: str, config: Dict) -> str:
        """สร้าง Industrial Automation System"""
        
        automation_path = os.path.join(project_path, "industrial_automation")
        os.makedirs(automation_path, exist_ok=True)
        
        automation_service = """
from typing import Dict, List, Optional
import asyncio
from datetime import datetime
from enum import Enum

class MachineState(Enum):
    IDLE = "idle"
    RUNNING = "running"  
    MAINTENANCE = "maintenance"
    ERROR = "error"

class IndustrialAutomationSystem:
    def __init__(self):
        self.machines = {}
        self.production_lines = {}
        self.automation_rules = {}
        
    def register_machine(self, machine_id: str, machine_config: Dict) -> Dict:
        \"\"\"ลงทะเบียนเครื่องจักร\"\"\"
        
        self.machines[machine_id] = {
            'machine_id': machine_id,
            'type': machine_config.get('type', 'generic'),
            'state': MachineState.IDLE,
            'production_rate': machine_config.get('production_rate', 0),
            'efficiency': 100.0,
            'last_maintenance': datetime.now().isoformat(),
            'total_runtime': 0,
            'error_count': 0,
            'config': machine_config
        }
        
        return {
            'status': 'registered',
            'machine_id': machine_id,
            'initial_state': MachineState.IDLE.value
        }
    
    async def start_production_line(self, line_id: str, machine_list: List[str]) -> Dict:
        \"\"\"เริ่มสายการผลิต\"\"\"
        
        # Verify all machines exist
        for machine_id in machine_list:
            if machine_id not in self.machines:
                return {
                    'status': 'failed',
                    'message': f'Machine {machine_id} not found'
                }
        
        self.production_lines[line_id] = {
            'line_id': line_id,
            'machines': machine_list,
            'state': 'active',
            'started_at': datetime.now().isoformat(),
            'products_produced': 0,
            'target_production': 0
        }
        
        # Start all machines in the line
        for machine_id in machine_list:
            await self._start_machine(machine_id)
        
        return {
            'status': 'started',
            'line_id': line_id,
            'machines_count': len(machine_list)
        }
    
    async def _start_machine(self, machine_id: str):
        \"\"\"เริ่มเครื่องจักร\"\"\"
        
        if machine_id in self.machines:
            self.machines[machine_id]['state'] = MachineState.RUNNING
            
            # Start production simulation
            asyncio.create_task(self._simulate_machine_production(machine_id))
    
    async def _simulate_machine_production(self, machine_id: str):
        \"\"\"จำลองการผลิต\"\"\"
        
        machine = self.machines[machine_id]
        
        while machine['state'] == MachineState.RUNNING:
            # Simulate production cycle
            await asyncio.sleep(1)  # 1 second per cycle
            
            # Update runtime
            machine['total_runtime'] += 1
            
            # Random efficiency variation
            import random
            efficiency_change = random.uniform(-2, 2)
            machine['efficiency'] = max(50, min(100, machine['efficiency'] + efficiency_change))
            
            # Check for maintenance needs
            if machine['total_runtime'] > 0 and machine['total_runtime'] % 3600 == 0:  # Every hour
                await self._schedule_maintenance(machine_id)
                break
            
            # Random error chance
            if random.random() < 0.001:  # 0.1% chance per cycle
                await self._trigger_machine_error(machine_id)
                break
    
    async def _schedule_maintenance(self, machine_id: str):
        \"\"\"กำหนดการซ่อมบำรุง\"\"\"
        
        self.machines[machine_id]['state'] = MachineState.MAINTENANCE
        self.machines[machine_id]['last_maintenance'] = datetime.now().isoformat()
        
        # Simulate maintenance time (5 seconds)
        await asyncio.sleep(5)
        
        # Reset efficiency after maintenance
        self.machines[machine_id]['efficiency'] = 100.0
        self.machines[machine_id]['state'] = MachineState.IDLE
    
    async def _trigger_machine_error(self, machine_id: str):
        \"\"\"เกิดข้อผิดพลาด\"\"\"
        
        self.machines[machine_id]['state'] = MachineState.ERROR
        self.machines[machine_id]['error_count'] += 1
        
        # Auto-recovery after 10 seconds
        await asyncio.sleep(10)
        self.machines[machine_id]['state'] = MachineState.IDLE
    
    def get_production_status(self, line_id: str = None) -> Dict:
        \"\"\"ดูสถานะการผลิต\"\"\"
        
        if line_id:
            return self.production_lines.get(line_id, {'error': 'Line not found'})
        
        return {
            'total_lines': len(self.production_lines),
            'active_lines': sum(1 for line in self.production_lines.values() 
                              if line['state'] == 'active'),
            'lines': self.production_lines
        }
    
    def get_machine_status(self, machine_id: str = None) -> Dict:
        \"\"\"ดูสถานะเครื่องจักร\"\"\"
        
        if machine_id:
            return self.machines.get(machine_id, {'error': 'Machine not found'})
        
        status_summary = {}
        for state in MachineState:
            status_summary[state.value] = sum(
                1 for machine in self.machines.values() 
                if machine['state'] == state
            )
        
        return {
            'total_machines': len(self.machines),
            'status_breakdown': status_summary,
            'machines': self.machines
        }
    
    def create_automation_rule(self, rule_name: str, conditions: Dict, actions: Dict) -> Dict:
        \"\"\"สร้างกฎอัตโนมัติ\"\"\"
        
        self.automation_rules[rule_name] = {
            'conditions': conditions,
            'actions': actions,
            'created_at': datetime.now().isoformat(),
            'triggered_count': 0
        }
        
        return {
            'status': 'created',
            'rule_name': rule_name
        }
"""
        
        with open(os.path.join(automation_path, "industrial_automation.py"), "w") as f:
            f.write(automation_service)
        
        return os.path.join(automation_path, "industrial_automation.py")
    
    def _create_mfa_system(self, project_path: str, config: Dict) -> str:
        """สร้าง Multi-Factor Authentication System"""
        
        mfa_path = os.path.join(project_path, "mfa_system")
        os.makedirs(mfa_path, exist_ok=True)
        
        mfa_service = """
from typing import Dict, List, Optional
import random
import time
import hashlib
from datetime import datetime, timedelta

class MFASystem:
    def __init__(self):
        self.users = {}
        self.active_sessions = {}
        self.backup_codes = {}
        
    def setup_mfa(self, user_id: str, phone_number: str = None, email: str = None) -> Dict:
        \"\"\"ตั้งค่า MFA สำหรับผู้ใช้\"\"\"
        
        self.users[user_id] = {
            'user_id': user_id,
            'phone_number': phone_number,
            'email': email,
            'mfa_enabled': True,
            'setup_at': datetime.now().isoformat(),
            'backup_codes_used': 0
        }
        
        # Generate backup codes
        backup_codes = [self._generate_backup_code() for _ in range(10)]
        self.backup_codes[user_id] = backup_codes
        
        return {
            'status': 'mfa_setup_complete',
            'user_id': user_id,
            'backup_codes': backup_codes,
            'message': 'Store backup codes safely'
        }
    
    def send_verification_code(self, user_id: str, method: str = 'sms') -> Dict:
        \"\"\"ส่งรหัสยืนยัน\"\"\"
        
        if user_id not in self.users:
            return {'status': 'error', 'message': 'User not found'}
        
        # Generate 6-digit code
        code = f'{random.randint(100000, 999999):06d}'
        
        # Store code with expiration (5 minutes)
        code_key = f'{user_id}_{method}_{int(time.time())}'
        self.active_sessions[code_key] = {
            'code': code,
            'user_id': user_id,
            'method': method,
            'expires_at': datetime.now() + timedelta(minutes=5),
            'attempts': 0
        }
        
        # Simulate sending code
        if method == 'sms':
            phone = self.users[user_id].get('phone_number', 'XXX-XXX-XXXX')
            message = f'SMS sent to {phone}: Your code is {code}'
        elif method == 'email':
            email = self.users[user_id].get('email', 'user@example.com')
            message = f'Email sent to {email}: Your code is {code}'
        else:
            message = f'Verification code: {code}'
        
        return {
            'status': 'code_sent',
            'method': method,
            'message': message,
            'code_key': code_key  # In production, don't return this
        }
    
    def verify_code(self, code_key: str, submitted_code: str) -> Dict:
        \"\"\"ยืนยันรหัส\"\"\"
        
        if code_key not in self.active_sessions:
            return {'status': 'error', 'message': 'Invalid or expired code'}
        
        session = self.active_sessions[code_key]
        
        # Check expiration
        if datetime.now() > session['expires_at']:
            del self.active_sessions[code_key]
            return {'status': 'error', 'message': 'Code expired'}
        
        # Check attempts
        session['attempts'] += 1
        if session['attempts'] > 3:
            del self.active_sessions[code_key]
            return {'status': 'error', 'message': 'Too many attempts'}
        
        # Verify code
        if session['code'] == submitted_code:
            user_id = session['user_id']
            del self.active_sessions[code_key]
            
            # Create authenticated session
            session_token = self._generate_session_token(user_id)
            
            return {
                'status': 'verified',
                'user_id': user_id,
                'session_token': session_token,
                'message': 'Authentication successful'
            }
        else:
            return {
                'status': 'error',
                'message': 'Invalid code',
                'attempts_remaining': 3 - session['attempts']
            }
    
    def verify_backup_code(self, user_id: str, backup_code: str) -> Dict:
        \"\"\"ยืนยันด้วย backup code\"\"\"
        
        if user_id not in self.backup_codes:
            return {'status': 'error', 'message': 'No backup codes found'}
        
        if backup_code in self.backup_codes[user_id]:
            # Remove used backup code
            self.backup_codes[user_id].remove(backup_code)
            self.users[user_id]['backup_codes_used'] += 1
            
            # Create session
            session_token = self._generate_session_token(user_id)
            
            return {
                'status': 'verified',
                'user_id': user_id,
                'session_token': session_token,
                'remaining_codes': len(self.backup_codes[user_id]),
                'message': 'Backup code verified'
            }
        else:
            return {'status': 'error', 'message': 'Invalid backup code'}
    
    def disable_mfa(self, user_id: str) -> Dict:
        \"\"\"ปิด MFA\"\"\"
        
        if user_id in self.users:
            self.users[user_id]['mfa_enabled'] = False
            self.users[user_id]['disabled_at'] = datetime.now().isoformat()
            
            # Clear backup codes
            if user_id in self.backup_codes:
                del self.backup_codes[user_id]
            
            return {'status': 'mfa_disabled', 'user_id': user_id}
        
        return {'status': 'error', 'message': 'User not found'}
    
    def get_mfa_status(self, user_id: str) -> Dict:
        \"\"\"ดูสถานะ MFA\"\"\"
        
        if user_id in self.users:
            user_info = self.users[user_id].copy()
            user_info['backup_codes_remaining'] = len(self.backup_codes.get(user_id, []))
            return user_info
        
        return {'status': 'error', 'message': 'User not found'}
    
    def _generate_backup_code(self) -> str:
        \"\"\"สร้าง backup code\"\"\"
        return f'{random.randint(10000000, 99999999):08d}'
    
    def _generate_session_token(self, user_id: str) -> str:
        \"\"\"สร้าง session token\"\"\"
        data = f'{user_id}_{int(time.time())}_{random.randint(1000, 9999)}'
        return hashlib.sha256(data.encode()).hexdigest()[:32]
"""
        
        with open(os.path.join(mfa_path, "mfa_system.py"), "w") as f:
            f.write(mfa_service)
        
        return os.path.join(mfa_path, "mfa_system.py")
    
    def _create_encryption_service(self, project_path: str, config: Dict) -> str:
        """สร้าง Encryption Service"""
        
        encryption_path = os.path.join(project_path, "encryption_service")
        os.makedirs(encryption_path, exist_ok=True)
        
        encryption_service = """
from typing import Dict, List, Optional, Union
import base64
import hashlib
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class EncryptionService:
    def __init__(self, master_key: str = None):
        self.master_key = master_key or self._generate_master_key()
        self.fernet = self._create_fernet_cipher(self.master_key)
        
    def encrypt_data(self, data: Union[str, bytes], password: str = None) -> Dict:
        \"\"\"เข้ารหัสข้อมูล\"\"\"
        
        try:
            # Convert to bytes if string
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
            
            if password:
                # Use password-based encryption
                cipher = self._create_password_cipher(password)
                encrypted_data = cipher.encrypt(data_bytes)
            else:
                # Use master key encryption
                encrypted_data = self.fernet.encrypt(data_bytes)
            
            # Encode to base64 for storage/transmission
            encrypted_b64 = base64.b64encode(encrypted_data).decode('utf-8')
            
            return {
                'status': 'success',
                'encrypted_data': encrypted_b64,
                'encryption_method': 'password' if password else 'master_key',
                'data_size': len(data_bytes)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def decrypt_data(self, encrypted_data: str, password: str = None) -> Dict:
        \"\"\"ถอดรหัสข้อมูล\"\"\"
        
        try:
            # Decode from base64
            encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            
            if password:
                # Use password-based decryption
                cipher = self._create_password_cipher(password)
                decrypted_bytes = cipher.decrypt(encrypted_bytes)
            else:
                # Use master key decryption
                decrypted_bytes = self.fernet.decrypt(encrypted_bytes)
            
            # Try to decode as UTF-8 string
            try:
                decrypted_data = decrypted_bytes.decode('utf-8')
            except UnicodeDecodeError:
                # Return as bytes if not valid UTF-8
                decrypted_data = decrypted_bytes
            
            return {
                'status': 'success',
                'decrypted_data': decrypted_data,
                'data_type': 'string' if isinstance(decrypted_data, str) else 'bytes'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Decryption failed: {str(e)}'
            }
    
    def hash_data(self, data: str, algorithm: str = 'sha256') -> Dict:
        \"\"\"สร้าง hash ของข้อมูล\"\"\"
        
        try:
            data_bytes = data.encode('utf-8')
            
            if algorithm == 'sha256':
                hash_obj = hashlib.sha256(data_bytes)
            elif algorithm == 'sha512':
                hash_obj = hashlib.sha512(data_bytes)
            elif algorithm == 'md5':
                hash_obj = hashlib.md5(data_bytes)
            else:
                return {'status': 'error', 'message': 'Unsupported algorithm'}
            
            hash_hex = hash_obj.hexdigest()
            
            return {
                'status': 'success',
                'hash': hash_hex,
                'algorithm': algorithm,
                'original_length': len(data)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def verify_hash(self, data: str, expected_hash: str, algorithm: str = 'sha256') -> Dict:
        \"\"\"ยืนยัน hash\"\"\"
        
        hash_result = self.hash_data(data, algorithm)
        
        if hash_result['status'] == 'success':
            is_valid = hash_result['hash'] == expected_hash
            
            return {
                'status': 'success',
                'is_valid': is_valid,
                'calculated_hash': hash_result['hash'],
                'expected_hash': expected_hash
            }
        else:
            return hash_result
    
    def generate_key_pair(self) -> Dict:
        \"\"\"สร้าง key pair สำหรับ asymmetric encryption\"\"\"
        
        # Simplified key pair generation
        private_key = secrets.token_hex(32)
        public_key = hashlib.sha256(private_key.encode()).hexdigest()
        
        return {
            'status': 'success',
            'private_key': private_key,
            'public_key': public_key,
            'key_type': 'simplified_pair'
        }
    
    def _generate_master_key(self) -> str:
        \"\"\"สร้าง master key\"\"\"
        return base64.urlsafe_b64encode(Fernet.generate_key()).decode()
    
    def _create_fernet_cipher(self, key: str) -> Fernet:
        \"\"\"สร้าง Fernet cipher\"\"\"
        # Ensure key is proper Fernet key
        if len(key) < 44:
            key = base64.urlsafe_b64encode(key.encode().ljust(32)[:32])
        else:
            key = key.encode()
        return Fernet(key)
    
    def _create_password_cipher(self, password: str) -> Fernet:
        \"\"\"สร้าง password-based cipher\"\"\"
        
        # Generate salt
        salt = b'salt1234'  # In production, use random salt
        
        # Derive key from password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return Fernet(key)
"""
        
        with open(os.path.join(encryption_path, "encryption_service.py"), "w") as f:
            f.write(encryption_service)
        
        return os.path.join(encryption_path, "encryption_service.py")
    
    def _create_audit_system(self, project_path: str, config: Dict) -> str:
        """สร้าง Audit Logging System"""
        
        audit_path = os.path.join(project_path, "audit_system")
        os.makedirs(audit_path, exist_ok=True)
        
        audit_service = """
from typing import Dict, List, Optional
import json
from datetime import datetime
from enum import Enum

class AuditLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class AuditSystem:
    def __init__(self):
        self.audit_logs = []
        self.max_logs = 10000  # Keep last 10k logs
        
    def log_event(self, event_type: str, user_id: str = None, 
                  details: Dict = None, level: AuditLevel = AuditLevel.INFO) -> Dict:
        \"\"\"บันทึก audit event\"\"\"
        
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'user_id': user_id,
            'level': level.value,
            'details': details or {},
            'session_id': self._get_session_id(),
            'ip_address': self._get_client_ip(),
            'user_agent': 'System'
        }
        
        # Add to logs
        self.audit_logs.append(audit_entry)
        
        # Maintain log size limit
        if len(self.audit_logs) > self.max_logs:
            self.audit_logs = self.audit_logs[-self.max_logs:]
        
        return {
            'status': 'logged',
            'log_id': len(self.audit_logs) - 1,
            'timestamp': audit_entry['timestamp']
        }
    
    def log_user_action(self, user_id: str, action: str, resource: str = None, 
                       result: str = 'success', details: Dict = None) -> Dict:
        \"\"\"บันทึกการกระทำของผู้ใช้\"\"\"
        
        event_details = {
            'action': action,
            'resource': resource,
            'result': result,
            'additional_details': details or {}
        }
        
        level = AuditLevel.ERROR if result == 'failed' else AuditLevel.INFO
        
        return self.log_event(
            event_type='user_action',
            user_id=user_id,
            details=event_details,
            level=level
        )
    
    def log_security_event(self, event_type: str, user_id: str = None,
                          threat_level: str = 'low', details: Dict = None) -> Dict:
        \"\"\"บันทึก security event\"\"\"
        
        level_map = {
            'low': AuditLevel.INFO,
            'medium': AuditLevel.WARNING,
            'high': AuditLevel.ERROR,
            'critical': AuditLevel.CRITICAL
        }
        
        event_details = {
            'threat_level': threat_level,
            'security_details': details or {}
        }
        
        return self.log_event(
            event_type=f'security_{event_type}',
            user_id=user_id,
            details=event_details,
            level=level_map.get(threat_level, AuditLevel.INFO)
        )
    
    def log_system_event(self, event: str, component: str, 
                        status: str = 'normal', details: Dict = None) -> Dict:
        \"\"\"บันทึก system event\"\"\"
        
        event_details = {
            'component': component,
            'status': status,
            'system_details': details or {}
        }
        
        level = AuditLevel.ERROR if status == 'error' else AuditLevel.INFO
        
        return self.log_event(
            event_type='system_event',
            details=event_details,
            level=level
        )
    
    def search_logs(self, filters: Dict = None, limit: int = 100) -> List[Dict]:
        \"\"\"ค้นหา audit logs\"\"\"
        
        if not filters:
            return self.audit_logs[-limit:]
        
        filtered_logs = []
        
        for log in self.audit_logs:
            match = True
            
            # Filter by event type
            if 'event_type' in filters:
                if log['event_type'] != filters['event_type']:
                    match = False
            
            # Filter by user
            if 'user_id' in filters:
                if log['user_id'] != filters['user_id']:
                    match = False
            
            # Filter by level
            if 'level' in filters:
                if log['level'] != filters['level']:
                    match = False
            
            # Filter by time range
            if 'start_time' in filters:
                if log['timestamp'] < filters['start_time']:
                    match = False
            
            if 'end_time' in filters:
                if log['timestamp'] > filters['end_time']:
                    match = False
            
            if match:
                filtered_logs.append(log)
                
                if len(filtered_logs) >= limit:
                    break
        
        return filtered_logs
    
    def get_audit_summary(self, hours: int = 24) -> Dict:
        \"\"\"สรุปสถิติ audit logs\"\"\"
        
        # Calculate time threshold
        from datetime import timedelta
        threshold = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        recent_logs = [log for log in self.audit_logs if log['timestamp'] >= threshold]
        
        # Count by event type
        event_counts = {}
        level_counts = {}
        user_activity = {}
        
        for log in recent_logs:
            # Event types
            event_type = log['event_type']
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
            
            # Levels
            level = log['level']
            level_counts[level] = level_counts.get(level, 0) + 1
            
            # User activity
            user_id = log.get('user_id')
            if user_id:
                user_activity[user_id] = user_activity.get(user_id, 0) + 1
        
        return {
            'time_range_hours': hours,
            'total_events': len(recent_logs),
            'event_types': event_counts,
            'severity_levels': level_counts,
            'top_active_users': sorted(user_activity.items(), 
                                     key=lambda x: x[1], reverse=True)[:10],
            'generated_at': datetime.now().isoformat()
        }
    
    def export_logs(self, format: str = 'json', filters: Dict = None) -> Dict:
        \"\"\"Export audit logs\"\"\"
        
        logs = self.search_logs(filters) if filters else self.audit_logs
        
        if format == 'json':
            exported_data = json.dumps(logs, indent=2)
        elif format == 'csv':
            # Simple CSV export
            lines = ['timestamp,event_type,user_id,level,details']
            for log in logs:
                details_str = json.dumps(log['details']).replace(',', ';')
                lines.append(f"{log['timestamp']},{log['event_type']},{log.get('user_id', '')},{log['level']},{details_str}")
            exported_data = '\\n'.join(lines)
        else:
            return {'status': 'error', 'message': 'Unsupported format'}
        
        return {
            'status': 'success',
            'format': format,
            'records_count': len(logs),
            'data': exported_data
        }
    
    def _get_session_id(self) -> str:
        \"\"\"Get current session ID (mock)\"\"\"
        return 'session_12345'
    
    def _get_client_ip(self) -> str:
        \"\"\"Get client IP (mock)\"\"\"
        return '127.0.0.1'
"""
        
        with open(os.path.join(audit_path, "audit_system.py"), "w") as f:
            f.write(audit_service)
        
        return os.path.join(audit_path, "audit_system.py")
    
    def _create_threat_detection(self, project_path: str, config: Dict) -> str:
        """สร้าง Threat Detection System"""
        
        threat_path = os.path.join(project_path, "threat_detection")
        os.makedirs(threat_path, exist_ok=True)
        
        threat_detector = """
from typing import Dict, List, Optional
import json
import re
from datetime import datetime, timedelta
from enum import Enum

class ThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high" 
    CRITICAL = "critical"

class ThreatType(Enum):
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    BRUTE_FORCE = "brute_force"
    DDoS = "ddos"
    MALWARE = "malware"
    PHISHING = "phishing"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"

class ThreatDetectionSystem:
    def __init__(self):
        self.threat_patterns = self._load_threat_patterns()
        self.blocked_ips = set()
        self.failed_attempts = {}
        self.suspicious_activities = []
        
    def _load_threat_patterns(self) -> Dict:
        \"\"\"โหลด threat patterns\"\"\"
        
        return {
            'sql_injection': [
                r"('|(\\x27)|(\\x2D)|(\\x23)|(\\x3B))",
                r"(\\s*(or|and)\\s+[\\w\\(\\)'\"=<>]+\\s*(=|<|>))",
                r"(union|select|insert|update|delete|drop|create|alter)\\s+",
                r"(exec|execute|sp_|xp_)\\w+",
            ],
            'xss': [
                r"<script[^>]*>.*?</script>",
                r"javascript:",
                r"on\\w+\\s*=",
                r"<iframe[^>]*>.*?</iframe>",
                r"eval\\s*\\(",
            ],
            'path_traversal': [
                r"\\.\\./",
                r"\\.\\.\\\\",
                r"%2e%2e%2f",
                r"%2e%2e\\\\",
            ],
            'command_injection': [
                r";\\s*(ls|cat|pwd|whoami|id|ps|netstat)",
                r"\\||&|`|\\$\\(",
                r"(nc|netcat|wget|curl)\\s+",
            ]
        }
    
    def analyze_request(self, request_data: Dict) -> Dict:
        \"\"\"วิเคราะห์ request เพื่อหา threat\"\"\"
        
        threats_found = []
        threat_score = 0
        
        # Extract data to analyze
        url = request_data.get('url', '')
        params = request_data.get('params', {})
        headers = request_data.get('headers', {})
        body = request_data.get('body', '')
        ip_address = request_data.get('ip_address', '')
        
        # Check for SQL Injection
        sql_threats = self._check_sql_injection(url, params, body)
        if sql_threats:
            threats_found.extend(sql_threats)
            threat_score += 50
        
        # Check for XSS
        xss_threats = self._check_xss(url, params, body)
        if xss_threats:
            threats_found.extend(xss_threats)
            threat_score += 30
        
        # Check for Path Traversal
        path_threats = self._check_path_traversal(url, params)
        if path_threats:
            threats_found.extend(path_threats)
            threat_score += 40
        
        # Check for Command Injection
        cmd_threats = self._check_command_injection(params, body)
        if cmd_threats:
            threats_found.extend(cmd_threats)
            threat_score += 60
        
        # Check suspicious headers
        header_threats = self._check_suspicious_headers(headers)
        if header_threats:
            threats_found.extend(header_threats)
            threat_score += 20
        
        # Check IP reputation
        ip_threat = self._check_ip_reputation(ip_address)
        if ip_threat:
            threats_found.append(ip_threat)
            threat_score += 25
        
        # Determine threat level
        if threat_score >= 80:
            level = ThreatLevel.CRITICAL
        elif threat_score >= 50:
            level = ThreatLevel.HIGH
        elif threat_score >= 25:
            level = ThreatLevel.MEDIUM
        else:
            level = ThreatLevel.LOW if threats_found else None
        
        return {
            'threats_found': threats_found,
            'threat_score': threat_score,
            'threat_level': level.value if level else None,
            'recommendation': self._get_recommendation(threats_found, level),
            'should_block': threat_score >= 60,
            'timestamp': datetime.now().isoformat()
        }
    
    def _check_sql_injection(self, url: str, params: Dict, body: str) -> List[Dict]:
        \"\"\"ตรวจสอบ SQL Injection\"\"\"
        
        threats = []
        test_strings = [url, json.dumps(params), body]
        
        for test_str in test_strings:
            for pattern in self.threat_patterns['sql_injection']:
                if re.search(pattern, test_str, re.IGNORECASE):
                    threats.append({
                        'type': ThreatType.SQL_INJECTION.value,
                        'pattern_matched': pattern,
                        'location': 'url' if test_str == url else 'params' if test_str == json.dumps(params) else 'body',
                        'severity': 'high'
                    })
        
        return threats
    
    def _check_xss(self, url: str, params: Dict, body: str) -> List[Dict]:
        \"\"\"ตรวจสอบ XSS\"\"\"
        
        threats = []
        test_strings = [url, json.dumps(params), body]
        
        for test_str in test_strings:
            for pattern in self.threat_patterns['xss']:
                if re.search(pattern, test_str, re.IGNORECASE):
                    threats.append({
                        'type': ThreatType.XSS.value,
                        'pattern_matched': pattern,
                        'location': 'url' if test_str == url else 'params' if test_str == json.dumps(params) else 'body',
                        'severity': 'medium'
                    })
        
        return threats
    
    def _check_path_traversal(self, url: str, params: Dict) -> List[Dict]:
        \"\"\"ตรวจสอบ Path Traversal\"\"\"
        
        threats = []
        test_strings = [url, json.dumps(params)]
        
        for test_str in test_strings:
            for pattern in self.threat_patterns['path_traversal']:
                if re.search(pattern, test_str):
                    threats.append({
                        'type': 'path_traversal',
                        'pattern_matched': pattern,
                        'location': 'url' if test_str == url else 'params',
                        'severity': 'high'
                    })
        
        return threats
    
    def _check_command_injection(self, params: Dict, body: str) -> List[Dict]:
        \"\"\"ตรวจสอบ Command Injection\"\"\"
        
        threats = []
        test_strings = [json.dumps(params), body]
        
        for test_str in test_strings:
            for pattern in self.threat_patterns['command_injection']:
                if re.search(pattern, test_str):
                    threats.append({
                        'type': 'command_injection',
                        'pattern_matched': pattern,
                        'location': 'params' if test_str == json.dumps(params) else 'body',
                        'severity': 'critical'
                    })
        
        return threats
    
    def _check_suspicious_headers(self, headers: Dict) -> List[Dict]:
        \"\"\"ตรวจสอบ headers ที่น่าสงสัย\"\"\"
        
        threats = []
        suspicious_patterns = [
            'bot', 'crawler', 'spider', 'scan', 'hack', 'exploit'
        ]
        
        user_agent = headers.get('User-Agent', '').lower()
        for pattern in suspicious_patterns:
            if pattern in user_agent:
                threats.append({
                    'type': ThreatType.SUSPICIOUS_ACTIVITY.value,
                    'pattern_matched': pattern,
                    'location': 'user-agent',
                    'severity': 'low'
                })
        
        return threats
    
    def _check_ip_reputation(self, ip_address: str) -> Optional[Dict]:
        \"\"\"ตรวจสอบ IP reputation\"\"\"
        
        # Check if IP is in blocked list
        if ip_address in self.blocked_ips:
            return {
                'type': 'blocked_ip',
                'ip_address': ip_address,
                'severity': 'high'
            }
        
        # Check failed attempts
        if ip_address in self.failed_attempts:
            attempts = self.failed_attempts[ip_address]
            if attempts['count'] > 10:
                return {
                    'type': ThreatType.BRUTE_FORCE.value,
                    'ip_address': ip_address,
                    'failed_attempts': attempts['count'],
                    'severity': 'high'
                }
        
        return None
    
    def _get_recommendation(self, threats: List[Dict], level: ThreatLevel) -> str:
        \"\"\"แนะนำการจัดการ threat\"\"\"
        
        if not threats:
            return "No threats detected"
        
        if level == ThreatLevel.CRITICAL:
            return "BLOCK IMMEDIATELY - Critical threat detected"
        elif level == ThreatLevel.HIGH:
            return "Block request and investigate"
        elif level == ThreatLevel.MEDIUM:
            return "Monitor closely and consider rate limiting"
        else:
            return "Log for analysis"
    
    def log_failed_attempt(self, ip_address: str, reason: str = 'authentication'):
        \"\"\"บันทึกความพยายามที่ล้มเหลว\"\"\"
        
        if ip_address not in self.failed_attempts:
            self.failed_attempts[ip_address] = {
                'count': 0,
                'first_attempt': datetime.now(),
                'last_attempt': datetime.now(),
                'reasons': []
            }
        
        self.failed_attempts[ip_address]['count'] += 1
        self.failed_attempts[ip_address]['last_attempt'] = datetime.now()
        self.failed_attempts[ip_address]['reasons'].append({
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        })
        
        # Auto-block if too many attempts
        if self.failed_attempts[ip_address]['count'] > 20:
            self.block_ip(ip_address, 'Too many failed attempts')
    
    def block_ip(self, ip_address: str, reason: str = 'Security policy'):
        \"\"\"บล็อค IP address\"\"\"
        
        self.blocked_ips.add(ip_address)
        
        # Log the block
        self.suspicious_activities.append({
            'action': 'ip_blocked',
            'ip_address': ip_address,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        })
    
    def unblock_ip(self, ip_address: str):
        \"\"\"ปลดบล็อค IP address\"\"\"
        
        if ip_address in self.blocked_ips:
            self.blocked_ips.remove(ip_address)
            
            # Reset failed attempts
            if ip_address in self.failed_attempts:
                del self.failed_attempts[ip_address]
    
    def get_threat_summary(self, hours: int = 24) -> Dict:
        \"\"\"สรุปข้อมูล threat\"\"\"
        
        # Calculate time threshold
        threshold = datetime.now() - timedelta(hours=hours)
        
        # Count recent activities
        recent_activities = [
            activity for activity in self.suspicious_activities
            if datetime.fromisoformat(activity['timestamp']) >= threshold
        ]
        
        return {
            'time_range_hours': hours,
            'total_blocked_ips': len(self.blocked_ips),
            'recent_suspicious_activities': len(recent_activities),
            'active_monitoring_ips': len(self.failed_attempts),
            'threat_categories': self._count_threat_types(recent_activities),
            'generated_at': datetime.now().isoformat()
        }
    
    def _count_threat_types(self, activities: List[Dict]) -> Dict:
        \"\"\"นับจำนวน threat แต่ละประเภท\"\"\"
        
        counts = {}
        for activity in activities:
            threat_type = activity.get('action', 'unknown')
            counts[threat_type] = counts.get(threat_type, 0) + 1
        
        return counts
"""
        
        with open(os.path.join(threat_path, "threat_detection.py"), "w") as f:
            f.write(threat_detector)
        
        return os.path.join(threat_path, "threat_detection.py")
    
    def _create_compliance_system(self, project_path: str, config: Dict) -> str:
        """สร้าง Compliance Framework System"""
        
        compliance_path = os.path.join(project_path, "compliance_framework")
        os.makedirs(compliance_path, exist_ok=True)
        
        compliance_framework = """
from typing import Dict, List, Optional, Any
import json
from datetime import datetime
from enum import Enum

class ComplianceStandard(Enum):
    GDPR = "gdpr"                    # General Data Protection Regulation
    HIPAA = "hipaa"                  # Health Insurance Portability 
    PCI_DSS = "pci_dss"             # Payment Card Industry Data Security
    SOX = "sox"                     # Sarbanes-Oxley Act
    ISO_27001 = "iso_27001"         # Information Security Management
    CCPA = "ccpa"                   # California Consumer Privacy Act
    SOC2 = "soc2"                   # Service Organization Control 2

class ComplianceLevel(Enum):
    COMPLIANT = "compliant"
    PARTIAL = "partial"
    NON_COMPLIANT = "non_compliant"
    UNKNOWN = "unknown"

class ComplianceFramework:
    def __init__(self):
        self.compliance_rules = self._load_compliance_rules()
        self.audit_logs = []
        self.compliance_status = {}
        
    def _load_compliance_rules(self) -> Dict:
        \"\"\"โหลดกฎ compliance ต่าง ๆ\"\"\"
        
        return {
            ComplianceStandard.GDPR.value: {
                'data_protection': {
                    'description': 'Personal data must be protected',
                    'requirements': [
                        'Data encryption at rest and in transit',
                        'Right to be forgotten implementation',
                        'Data minimization practices',
                        'Consent management system',
                        'Data breach notification (72 hours)'
                    ]
                },
                'user_rights': {
                    'description': 'Users must have control over their data',
                    'requirements': [
                        'Data access request handling',
                        'Data portability features',
                        'Consent withdrawal mechanism',
                        'Data deletion capabilities'
                    ]
                }
            },
            ComplianceStandard.HIPAA.value: {
                'phi_protection': {
                    'description': 'Protected Health Information security',
                    'requirements': [
                        'Access controls and user authentication',
                        'Audit logs for all PHI access',
                        'Data encryption (AES-256)',
                        'Secure transmission protocols',
                        'Business associate agreements'
                    ]
                }
            },
            ComplianceStandard.PCI_DSS.value: {
                'payment_security': {
                    'description': 'Payment card data protection',
                    'requirements': [
                        'Secure cardholder data storage',
                        'Strong access control measures',
                        'Regular security testing',
                        'Network security monitoring',
                        'Vulnerability management program'
                    ]
                }
            },
            ComplianceStandard.SOX.value: {
                'financial_reporting': {
                    'description': 'Financial data accuracy and transparency',
                    'requirements': [
                        'Internal controls documentation',
                        'Financial data audit trails',
                        'Change management processes',
                        'Segregation of duties',
                        'Executive certification requirements'
                    ]
                }
            },
            ComplianceStandard.ISO_27001.value: {
                'information_security': {
                    'description': 'Information Security Management System',
                    'requirements': [
                        'Risk assessment and treatment',
                        'Security policy framework',
                        'Asset management',
                        'Human resource security',
                        'Physical and environmental security',
                        'Communications and operations management',
                        'Access control',
                        'Information systems acquisition, development and maintenance',
                        'Information security incident management',
                        'Business continuity management',
                        'Compliance monitoring'
                    ]
                }
            }
        }
    
    def assess_compliance(self, system_config: Dict, standards: List[str]) -> Dict:
        \"\"\"ประเมินความสอดคล้องของระบบ\"\"\"
        
        results = {}
        
        for standard in standards:
            if standard not in self.compliance_rules:
                results[standard] = {
                    'status': ComplianceLevel.UNKNOWN.value,
                    'message': f'Standard {standard} not supported'
                }
                continue
            
            compliance_result = self._assess_standard(system_config, standard)
            results[standard] = compliance_result
            
            # Update overall status
            self.compliance_status[standard] = compliance_result
        
        return {
            'assessment_date': datetime.now().isoformat(),
            'standards_assessed': standards,
            'results': results,
            'overall_score': self._calculate_overall_score(results)
        }
    
    def _assess_standard(self, system_config: Dict, standard: str) -> Dict:
        \"\"\"ประเมินมาตรฐานเฉพาะ\"\"\"
        
        rules = self.compliance_rules[standard]
        total_requirements = 0
        met_requirements = 0
        issues_found = []
        
        for category, details in rules.items():
            category_score = self._assess_category(system_config, details['requirements'])
            
            total_requirements += len(details['requirements'])
            met_requirements += category_score['met']
            
            if category_score['issues']:
                issues_found.extend([
                    f"{category}: {issue}" for issue in category_score['issues']
                ])
        
        # Calculate compliance percentage
        compliance_percentage = (met_requirements / total_requirements * 100) if total_requirements > 0 else 0
        
        # Determine compliance level
        if compliance_percentage >= 95:
            level = ComplianceLevel.COMPLIANT
        elif compliance_percentage >= 70:
            level = ComplianceLevel.PARTIAL
        else:
            level = ComplianceLevel.NON_COMPLIANT
        
        return {
            'status': level.value,
            'compliance_percentage': round(compliance_percentage, 2),
            'total_requirements': total_requirements,
            'met_requirements': met_requirements,
            'issues_found': issues_found,
            'recommendations': self._get_recommendations(standard, issues_found)
        }
    
    def _assess_category(self, system_config: Dict, requirements: List[str]) -> Dict:
        \"\"\"ประเมินหมวดหมู่ของข้อกำหนด\"\"\"
        
        met = 0
        issues = []
        
        # Check encryption
        if any('encryption' in req.lower() for req in requirements):
            if system_config.get('encryption_enabled', False):
                met += 1
            else:
                issues.append("Encryption not configured")
        
        # Check access controls
        if any('access control' in req.lower() for req in requirements):
            if system_config.get('access_controls', {}).get('enabled', False):
                met += 1
            else:
                issues.append("Access controls not properly configured")
        
        # Check audit logging
        if any('audit' in req.lower() for req in requirements):
            if system_config.get('audit_logging', False):
                met += 1
            else:
                issues.append("Audit logging not enabled")
        
        # Check authentication
        if any('authentication' in req.lower() for req in requirements):
            if system_config.get('authentication', {}).get('mfa_enabled', False):
                met += 1
            else:
                issues.append("Multi-factor authentication not implemented")
        
        # Check data protection
        if any('data protection' in req.lower() for req in requirements):
            if system_config.get('data_protection', {}).get('enabled', False):
                met += 1
            else:
                issues.append("Data protection measures not sufficient")
        
        return {
            'met': met,
            'issues': issues
        }
    
    def _get_recommendations(self, standard: str, issues: List[str]) -> List[str]:
        \"\"\"แนะนำการปรับปรุงเพื่อความสอดคล้อง\"\"\"
        
        recommendations = []
        
        if 'encryption' in ' '.join(issues).lower():
            recommendations.append("Implement AES-256 encryption for data at rest and TLS 1.3 for data in transit")
        
        if 'access control' in ' '.join(issues).lower():
            recommendations.append("Implement role-based access control (RBAC) with principle of least privilege")
        
        if 'audit' in ' '.join(issues).lower():
            recommendations.append("Enable comprehensive audit logging for all system activities")
        
        if 'authentication' in ' '.join(issues).lower():
            recommendations.append("Implement multi-factor authentication (MFA) for all user accounts")
        
        if 'data protection' in ' '.join(issues).lower():
            if standard == ComplianceStandard.GDPR.value:
                recommendations.append("Implement GDPR-compliant data handling: consent management, right to be forgotten, data minimization")
            elif standard == ComplianceStandard.HIPAA.value:
                recommendations.append("Implement HIPAA-compliant PHI protection: encryption, access controls, audit trails")
        
        return recommendations
    
    def generate_compliance_report(self, format: str = 'json') -> Dict:
        \"\"\"สร้างรายงานความสอดคล้อง\"\"\"
        
        report_data = {
            'report_date': datetime.now().isoformat(),
            'compliance_status': self.compliance_status,
            'summary': {
                'total_standards_assessed': len(self.compliance_status),
                'compliant_standards': len([s for s in self.compliance_status.values() if s['status'] == ComplianceLevel.COMPLIANT.value]),
                'partial_compliance': len([s for s in self.compliance_status.values() if s['status'] == ComplianceLevel.PARTIAL.value]),
                'non_compliant_standards': len([s for s in self.compliance_status.values() if s['status'] == ComplianceLevel.NON_COMPLIANT.value])
            },
            'recommendations': self._get_overall_recommendations(),
            'next_assessment_date': self._calculate_next_assessment_date()
        }
        
        if format == 'json':
            return report_data
        elif format == 'html':
            return self._generate_html_report(report_data)
        else:
            return {'error': f'Unsupported format: {format}'}
    
    def _get_overall_recommendations(self) -> List[str]:
        \"\"\"แนะนำการปรับปรุงโดยรวม\"\"\"
        
        all_recommendations = []
        
        for standard, status in self.compliance_status.items():
            if 'recommendations' in status:
                all_recommendations.extend(status['recommendations'])
        
        # Remove duplicates and prioritize
        unique_recommendations = list(set(all_recommendations))
        
        # Sort by priority (security-related first)
        priority_keywords = ['encryption', 'authentication', 'access control', 'audit']
        
        prioritized = []
        for keyword in priority_keywords:
            for rec in unique_recommendations:
                if keyword in rec.lower() and rec not in prioritized:
                    prioritized.append(rec)
        
        # Add remaining recommendations
        for rec in unique_recommendations:
            if rec not in prioritized:
                prioritized.append(rec)
        
        return prioritized[:10]  # Top 10 recommendations
    
    def _calculate_overall_score(self, results: Dict) -> float:
        \"\"\"คำนวณคะแนนรวม\"\"\"
        
        if not results:
            return 0.0
        
        total_percentage = 0
        valid_results = 0
        
        for standard, result in results.items():
            if result.get('compliance_percentage') is not None:
                total_percentage += result['compliance_percentage']
                valid_results += 1
        
        return round(total_percentage / valid_results, 2) if valid_results > 0 else 0.0
    
    def _calculate_next_assessment_date(self) -> str:
        \"\"\"คำนวณวันที่ประเมินครั้งต่อไป\"\"\"
        
        from datetime import timedelta
        next_date = datetime.now() + timedelta(days=90)  # Quarterly assessment
        return next_date.isoformat()
    
    def _generate_html_report(self, report_data: Dict) -> str:
        \"\"\"สร้างรายงาน HTML\"\"\"
        
        html_template = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Compliance Assessment Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; }}
                .summary {{ background-color: #e8f4fd; padding: 15px; margin: 20px 0; }}
                .compliant {{ color: green; }}
                .partial {{ color: orange; }}
                .non-compliant {{ color: red; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Compliance Assessment Report</h1>
                <p>Generated on: {report_data['report_date']}</p>
            </div>
            
            <div class="summary">
                <h2>Summary</h2>
                <p>Overall Compliance Score: <strong>{report_data.get('summary', {}).get('compliant_standards', 0)} / {report_data.get('summary', {}).get('total_standards_assessed', 0)}</strong></p>
            </div>
            
            <h2>Recommendations</h2>
            <ul>
            {''.join(f'<li>{rec}</li>' for rec in report_data.get('recommendations', []))}
            </ul>
        </body>
        </html>
        '''
        
        return html_template
    
    def log_compliance_activity(self, activity: str, standard: str = None, details: Dict = None):
        \"\"\"บันทึกกิจกรรมที่เกี่ยวข้องกับ compliance\"\"\"
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'activity': activity,
            'standard': standard,
            'details': details or {},
        }
        
        self.audit_logs.append(log_entry)
        
        # Maintain log size
        if len(self.audit_logs) > 1000:
            self.audit_logs = self.audit_logs[-1000:]
"""
        
        with open(os.path.join(compliance_path, "compliance_framework.py"), "w") as f:
            f.write(compliance_framework)
        
        return os.path.join(compliance_path, "compliance_framework.py")
    
    def _create_live_collaboration(self, project_path: str, config: Dict) -> str:
        """สร้าง Live Collaboration System"""
        
        collaboration_path = os.path.join(project_path, "live_collaboration")
        os.makedirs(collaboration_path, exist_ok=True)
        
        collaboration_system = """
from typing import Dict, List, Optional, Any, Set
import json
import asyncio
import websocket
from datetime import datetime
from enum import Enum
import uuid

class CollaborationType(Enum):
    DOCUMENT = "document"
    CODE = "code"
    DESIGN = "design"
    WHITEBOARD = "whiteboard"
    VIDEO_CALL = "video_call"
    CHAT = "chat"

class UserRole(Enum):
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"
    COMMENTER = "commenter"

class CollaborationEvent(Enum):
    USER_JOINED = "user_joined"
    USER_LEFT = "user_left"
    CONTENT_CHANGED = "content_changed"
    CURSOR_MOVED = "cursor_moved"
    SELECTION_CHANGED = "selection_changed"
    COMMENT_ADDED = "comment_added"
    MESSAGE_SENT = "message_sent"

class LiveCollaborationSystem:
    def __init__(self):
        self.active_sessions = {}
        self.user_sessions = {}
        self.collaboration_history = []
        self.websocket_connections = {}
        
    def create_collaboration_session(self, session_config: Dict) -> Dict:
        \"\"\"สร้าง collaboration session ใหม่\"\"\"
        
        session_id = str(uuid.uuid4())
        
        session = {
            'session_id': session_id,
            'title': session_config.get('title', 'Untitled Collaboration'),
            'type': session_config.get('type', CollaborationType.DOCUMENT.value),
            'created_at': datetime.now().isoformat(),
            'created_by': session_config.get('user_id'),
            'participants': {},
            'content': session_config.get('initial_content', ''),
            'version': 1,
            'settings': {
                'max_participants': session_config.get('max_participants', 50),
                'allow_anonymous': session_config.get('allow_anonymous', False),
                'require_approval': session_config.get('require_approval', False),
                'enable_chat': session_config.get('enable_chat', True),
                'enable_voice': session_config.get('enable_voice', False),
                'enable_video': session_config.get('enable_video', False)
            },
            'permissions': session_config.get('permissions', {}),
            'status': 'active'
        }
        
        # Add creator as owner
        creator_id = session_config.get('user_id')
        if creator_id:
            session['participants'][creator_id] = {
                'user_id': creator_id,
                'role': UserRole.OWNER.value,
                'joined_at': datetime.now().isoformat(),
                'last_active': datetime.now().isoformat(),
                'cursor_position': None,
                'selection': None,
                'is_online': True
            }
        
        self.active_sessions[session_id] = session
        
        return {
            'status': 'success',
            'session_id': session_id,
            'join_url': f'/collaborate/{session_id}',
            'settings': session['settings']
        }
    
    def join_session(self, session_id: str, user_info: Dict) -> Dict:
        \"\"\"เข้าร่วม collaboration session\"\"\"
        
        if session_id not in self.active_sessions:
            return {'status': 'error', 'message': 'Session not found'}
        
        session = self.active_sessions[session_id]
        user_id = user_info.get('user_id')
        
        # Check permissions
        if not self._check_join_permissions(session, user_info):
            return {'status': 'error', 'message': 'Permission denied'}
        
        # Check max participants
        current_participants = len([p for p in session['participants'].values() if p['is_online']])
        if current_participants >= session['settings']['max_participants']:
            return {'status': 'error', 'message': 'Session is full'}
        
        # Add or update participant
        participant = {
            'user_id': user_id,
            'name': user_info.get('name', 'Anonymous'),
            'avatar': user_info.get('avatar'),
            'role': user_info.get('role', UserRole.VIEWER.value),
            'joined_at': datetime.now().isoformat(),
            'last_active': datetime.now().isoformat(),
            'cursor_position': None,
            'selection': None,
            'is_online': True
        }
        
        session['participants'][user_id] = participant
        
        # Broadcast join event
        self._broadcast_event(session_id, {
            'type': CollaborationEvent.USER_JOINED.value,
            'user': participant,
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'status': 'success',
            'session': {
                'session_id': session_id,
                'title': session['title'],
                'type': session['type'],
                'content': session['content'],
                'version': session['version'],
                'participants': list(session['participants'].values()),
                'your_role': participant['role']
            }
        }
    
    def leave_session(self, session_id: str, user_id: str) -> Dict:
        \"\"\"ออกจาก collaboration session\"\"\"
        
        if session_id not in self.active_sessions:
            return {'status': 'error', 'message': 'Session not found'}
        
        session = self.active_sessions[session_id]
        
        if user_id in session['participants']:
            session['participants'][user_id]['is_online'] = False
            session['participants'][user_id]['left_at'] = datetime.now().isoformat()
            
            # Broadcast leave event
            self._broadcast_event(session_id, {
                'type': CollaborationEvent.USER_LEFT.value,
                'user_id': user_id,
                'timestamp': datetime.now().isoformat()
            })
        
        return {'status': 'success'}
    
    def update_content(self, session_id: str, user_id: str, changes: Dict) -> Dict:
        \"\"\"อัปเดตเนื้อหา (Operational Transform)\"\"\"
        
        if session_id not in self.active_sessions:
            return {'status': 'error', 'message': 'Session not found'}
        
        session = self.active_sessions[session_id]
        
        # Check permissions
        if not self._check_edit_permissions(session, user_id):
            return {'status': 'error', 'message': 'No edit permission'}
        
        # Apply operational transform
        transformed_changes = self._apply_operational_transform(
            session['content'], 
            changes, 
            session['version']
        )
        
        # Update content and version
        session['content'] = transformed_changes['new_content']
        session['version'] += 1
        session['last_modified'] = datetime.now().isoformat()
        session['last_modified_by'] = user_id
        
        # Update user activity
        if user_id in session['participants']:
            session['participants'][user_id]['last_active'] = datetime.now().isoformat()
        
        # Broadcast changes
        self._broadcast_event(session_id, {
            'type': CollaborationEvent.CONTENT_CHANGED.value,
            'user_id': user_id,
            'changes': transformed_changes['changes'],
            'version': session['version'],
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'status': 'success',
            'version': session['version'],
            'changes_applied': transformed_changes['changes']
        }
    
    def update_cursor(self, session_id: str, user_id: str, cursor_data: Dict) -> Dict:
        \"\"\"อัปเดตตำแหน่ง cursor\"\"\"
        
        if session_id not in self.active_sessions:
            return {'status': 'error', 'message': 'Session not found'}
        
        session = self.active_sessions[session_id]
        
        if user_id in session['participants']:
            session['participants'][user_id]['cursor_position'] = cursor_data.get('position')
            session['participants'][user_id]['selection'] = cursor_data.get('selection')
            session['participants'][user_id]['last_active'] = datetime.now().isoformat()
            
            # Broadcast cursor update (except to sender)
            self._broadcast_event(session_id, {
                'type': CollaborationEvent.CURSOR_MOVED.value,
                'user_id': user_id,
                'cursor_position': cursor_data.get('position'),
                'selection': cursor_data.get('selection'),
                'timestamp': datetime.now().isoformat()
            }, exclude_user=user_id)
        
        return {'status': 'success'}
    
    def send_chat_message(self, session_id: str, user_id: str, message: Dict) -> Dict:
        \"\"\"ส่งข้อความ chat\"\"\"
        
        if session_id not in self.active_sessions:
            return {'status': 'error', 'message': 'Session not found'}
        
        session = self.active_sessions[session_id]
        
        if not session['settings']['enable_chat']:
            return {'status': 'error', 'message': 'Chat is disabled'}
        
        chat_message = {
            'message_id': str(uuid.uuid4()),
            'user_id': user_id,
            'content': message.get('content', ''),
            'type': message.get('type', 'text'),  # text, image, file, etc.
            'timestamp': datetime.now().isoformat(),
            'edited': False
        }
        
        # Initialize chat history if needed
        if 'chat_history' not in session:
            session['chat_history'] = []
        
        session['chat_history'].append(chat_message)
        
        # Broadcast message
        self._broadcast_event(session_id, {
            'type': CollaborationEvent.MESSAGE_SENT.value,
            'message': chat_message,
            'timestamp': datetime.now().isoformat()
        })
        
        return {'status': 'success', 'message_id': chat_message['message_id']}
    
    def add_comment(self, session_id: str, user_id: str, comment_data: Dict) -> Dict:
        \"\"\"เพิ่มความคิดเห็น\"\"\"
        
        if session_id not in self.active_sessions:
            return {'status': 'error', 'message': 'Session not found'}
        
        session = self.active_sessions[session_id]
        
        comment = {
            'comment_id': str(uuid.uuid4()),
            'user_id': user_id,
            'content': comment_data.get('content', ''),
            'position': comment_data.get('position'),  # Position in document
            'thread_id': comment_data.get('thread_id'),  # For replies
            'created_at': datetime.now().isoformat(),
            'resolved': False,
            'replies': []
        }
        
        # Initialize comments if needed
        if 'comments' not in session:
            session['comments'] = []
        
        session['comments'].append(comment)
        
        # Broadcast comment
        self._broadcast_event(session_id, {
            'type': CollaborationEvent.COMMENT_ADDED.value,
            'comment': comment,
            'timestamp': datetime.now().isoformat()
        })
        
        return {'status': 'success', 'comment_id': comment['comment_id']}
    
    def _check_join_permissions(self, session: Dict, user_info: Dict) -> bool:
        \"\"\"ตรวจสอบสิทธิ์การเข้าร่วม\"\"\"
        
        # Allow anonymous if enabled
        if session['settings']['allow_anonymous'] and not user_info.get('user_id'):
            return True
        
        # Check if user is already invited
        permissions = session.get('permissions', {})
        user_id = user_info.get('user_id')
        
        if user_id in permissions:
            return True
        
        # Check if approval is required
        if session['settings']['require_approval']:
            return False  # Would need approval process
        
        return True  # Default allow
    
    def _check_edit_permissions(self, session: Dict, user_id: str) -> bool:
        \"\"\"ตรวจสอบสิทธิ์การแก้ไข\"\"\"
        
        if user_id not in session['participants']:
            return False
        
        role = session['participants'][user_id]['role']
        return role in [UserRole.OWNER.value, UserRole.EDITOR.value]
    
    def _apply_operational_transform(self, current_content: str, changes: Dict, version: int) -> Dict:
        \"\"\"ใช้ Operational Transform สำหรับ concurrent editing\"\"\"
        
        # Simplified OT implementation
        # In production, use a proper OT library like ShareJS
        
        operation_type = changes.get('type')
        position = changes.get('position', 0)
        content = changes.get('content', '')
        
        if operation_type == 'insert':
            new_content = current_content[:position] + content + current_content[position:]
        elif operation_type == 'delete':
            length = changes.get('length', len(content))
            new_content = current_content[:position] + current_content[position + length:]
        elif operation_type == 'replace':
            length = changes.get('length', 0)
            new_content = current_content[:position] + content + current_content[position + length:]
        else:
            new_content = current_content
        
        return {
            'new_content': new_content,
            'changes': changes  # Would be transformed changes in real OT
        }
    
    def _broadcast_event(self, session_id: str, event: Dict, exclude_user: str = None):
        \"\"\"ส่งข้อมูลไปยังผู้เข้าร่วมทั้งหมด\"\"\"
        
        if session_id not in self.active_sessions:
            return
        
        session = self.active_sessions[session_id]
        
        for participant_id, participant in session['participants'].items():
            if participant['is_online'] and participant_id != exclude_user:
                # In real implementation, send via WebSocket
                self._send_to_user(participant_id, event)
    
    def _send_to_user(self, user_id: str, data: Dict):
        \"\"\"ส่งข้อมูลไปยังผู้ใช้เฉพาะ (mock WebSocket)\"\"\"
        
        # Mock implementation - would use real WebSocket in production
        if user_id in self.websocket_connections:
            # websocket.send(json.dumps(data))
            pass
    
    def get_session_info(self, session_id: str) -> Dict:
        \"\"\"ดึงข้อมูล session\"\"\"
        
        if session_id not in self.active_sessions:
            return {'status': 'error', 'message': 'Session not found'}
        
        session = self.active_sessions[session_id]
        
        return {
            'status': 'success',
            'session': {
                'session_id': session_id,
                'title': session['title'],
                'type': session['type'],
                'created_at': session['created_at'],
                'version': session['version'],
                'participant_count': len([p for p in session['participants'].values() if p['is_online']]),
                'settings': session['settings']
            }
        }
    
    def close_session(self, session_id: str, user_id: str) -> Dict:
        \"\"\"ปิด session\"\"\"
        
        if session_id not in self.active_sessions:
            return {'status': 'error', 'message': 'Session not found'}
        
        session = self.active_sessions[session_id]
        
        # Check if user is owner
        if session['participants'].get(user_id, {}).get('role') != UserRole.OWNER.value:
            return {'status': 'error', 'message': 'Only owner can close session'}
        
        # Broadcast closure
        self._broadcast_event(session_id, {
            'type': 'session_closed',
            'message': 'Session has been closed by the owner',
            'timestamp': datetime.now().isoformat()
        })
        
        # Move to history
        session['status'] = 'closed'
        session['closed_at'] = datetime.now().isoformat()
        session['closed_by'] = user_id
        
        self.collaboration_history.append(session)
        del self.active_sessions[session_id]
        
        return {'status': 'success'}
"""
        
        with open(os.path.join(collaboration_path, "live_collaboration.py"), "w") as f:
            f.write(collaboration_system)
        
        return os.path.join(collaboration_path, "live_collaboration.py")
    
    def _create_video_system(self, project_path: str, config: Dict) -> str:
        """สร้าง Video Conferencing System"""
        
        video_path = os.path.join(project_path, "video_conferencing")
        os.makedirs(video_path, exist_ok=True)
        
        video_system = """
from typing import Dict, List, Optional, Any
import json
import asyncio
from datetime import datetime, timedelta
from enum import Enum
import uuid

class CallStatus(Enum):
    WAITING = "waiting"
    ACTIVE = "active"
    ENDED = "ended"
    RECORDING = "recording"

class ParticipantRole(Enum):
    HOST = "host"
    MODERATOR = "moderator"
    PARTICIPANT = "participant"
    OBSERVER = "observer"

class MediaType(Enum):
    AUDIO_ONLY = "audio_only"
    VIDEO = "video"
    SCREEN_SHARE = "screen_share"

class VideoConferencingSystem:
    def __init__(self):
        self.active_calls = {}
        self.call_history = []
        self.recording_sessions = {}
        self.webrtc_connections = {}
        
    def create_meeting(self, meeting_config: Dict) -> Dict:
        \"\"\"สร้างการประชุมใหม่\"\"\"
        
        meeting_id = str(uuid.uuid4())
        
        meeting = {
            'meeting_id': meeting_id,
            'title': meeting_config.get('title', 'Video Meeting'),
            'description': meeting_config.get('description', ''),
            'host_id': meeting_config.get('host_id'),
            'created_at': datetime.now().isoformat(),
            'scheduled_start': meeting_config.get('scheduled_start'),
            'scheduled_end': meeting_config.get('scheduled_end'),
            'status': CallStatus.WAITING.value,
            'participants': {},
            'settings': {
                'max_participants': meeting_config.get('max_participants', 100),
                'require_password': meeting_config.get('require_password', False),
                'password': meeting_config.get('password'),
                'enable_waiting_room': meeting_config.get('enable_waiting_room', False),
                'enable_recording': meeting_config.get('enable_recording', True),
                'allow_screen_share': meeting_config.get('allow_screen_share', True),
                'mute_on_join': meeting_config.get('mute_on_join', True),
                'camera_off_on_join': meeting_config.get('camera_off_on_join', False),
                'enable_chat': meeting_config.get('enable_chat', True),
                'enable_whiteboard': meeting_config.get('enable_whiteboard', True),
                'auto_record': meeting_config.get('auto_record', False)
            },
            'media_settings': {
                'video_quality': meeting_config.get('video_quality', 'hd'),  # sd, hd, fhd
                'audio_quality': meeting_config.get('audio_quality', 'high'),
                'enable_noise_cancellation': meeting_config.get('enable_noise_cancellation', True),
                'enable_echo_cancellation': meeting_config.get('enable_echo_cancellation', True)
            },
            'security': {
                'end_to_end_encryption': meeting_config.get('e2e_encryption', False),
                'participant_authentication': meeting_config.get('require_auth', False),
                'meeting_lock': False
            }
        }
        
        self.active_calls[meeting_id] = meeting
        
        return {
            'status': 'success',
            'meeting_id': meeting_id,
            'join_url': f'/meeting/{meeting_id}',
            'host_url': f'/meeting/{meeting_id}?role=host',
            'meeting_info': {
                'title': meeting['title'],
                'scheduled_start': meeting.get('scheduled_start'),
                'settings': meeting['settings']
            }
        }
    
    def join_meeting(self, meeting_id: str, participant_info: Dict) -> Dict:
        \"\"\"เข้าร่วมการประชุม\"\"\"
        
        if meeting_id not in self.active_calls:
            return {'status': 'error', 'message': 'Meeting not found'}
        
        meeting = self.active_calls[meeting_id]
        participant_id = participant_info.get('participant_id', str(uuid.uuid4()))
        
        # Check password if required
        if meeting['settings']['require_password']:
            if meeting_config.get('password') != meeting['settings']['password']:
                return {'status': 'error', 'message': 'Invalid password'}
        
        # Check participant limit
        active_participants = len([p for p in meeting['participants'].values() if p['status'] == 'connected'])
        if active_participants >= meeting['settings']['max_participants']:
            return {'status': 'error', 'message': 'Meeting is full'}
        
        # Create participant object
        participant = {
            'participant_id': participant_id,
            'name': participant_info.get('name', 'Anonymous'),
            'email': participant_info.get('email'),
            'role': participant_info.get('role', ParticipantRole.PARTICIPANT.value),
            'joined_at': datetime.now().isoformat(),
            'status': 'waiting' if meeting['settings']['enable_waiting_room'] else 'connected',
            'media': {
                'audio_enabled': not meeting['settings']['mute_on_join'],
                'video_enabled': not meeting['settings']['camera_off_on_join'],
                'screen_sharing': False,
                'media_type': MediaType.VIDEO.value
            },
            'permissions': {
                'can_share_screen': meeting['settings']['allow_screen_share'],
                'can_record': participant_info.get('role') in [ParticipantRole.HOST.value, ParticipantRole.MODERATOR.value],
                'can_mute_others': participant_info.get('role') in [ParticipantRole.HOST.value, ParticipantRole.MODERATOR.value],
                'can_remove_participants': participant_info.get('role') == ParticipantRole.HOST.value
            }
        }
        
        meeting['participants'][participant_id] = participant
        
        # Start meeting if this is the first participant
        if meeting['status'] == CallStatus.WAITING.value:
            meeting['status'] = CallStatus.ACTIVE.value
            meeting['started_at'] = datetime.now().isoformat()
            
            # Auto-record if enabled
            if meeting['settings']['auto_record']:
                self.start_recording(meeting_id, participant_id)
        
        # Notify other participants
        self._broadcast_to_meeting(meeting_id, {
            'type': 'participant_joined',
            'participant': participant,
            'timestamp': datetime.now().isoformat()
        }, exclude_participant=participant_id)
        
        return {
            'status': 'success',
            'participant_id': participant_id,
            'meeting_info': {
                'meeting_id': meeting_id,
                'title': meeting['title'],
                'status': meeting['status'],
                'participants': list(meeting['participants'].values()),
                'settings': meeting['settings'],
                'your_role': participant['role'],
                'your_permissions': participant['permissions']
            }
        }
    
    def leave_meeting(self, meeting_id: str, participant_id: str) -> Dict:
        \"\"\"ออกจากการประชุม\"\"\"
        
        if meeting_id not in self.active_calls:
            return {'status': 'error', 'message': 'Meeting not found'}
        
        meeting = self.active_calls[meeting_id]
        
        if participant_id in meeting['participants']:
            participant = meeting['participants'][participant_id]
            participant['status'] = 'disconnected'
            participant['left_at'] = datetime.now().isoformat()
            
            # Stop any media streams
            if participant['media']['screen_sharing']:
                self.stop_screen_share(meeting_id, participant_id)
            
            # Notify other participants
            self._broadcast_to_meeting(meeting_id, {
                'type': 'participant_left',
                'participant_id': participant_id,
                'timestamp': datetime.now().isoformat()
            })
            
            # End meeting if host leaves or no participants left
            active_participants = [p for p in meeting['participants'].values() if p['status'] == 'connected']
            if not active_participants or (participant['role'] == ParticipantRole.HOST.value and len(active_participants) == 0):
                self.end_meeting(meeting_id, participant_id)
        
        return {'status': 'success'}
    
    def toggle_audio(self, meeting_id: str, participant_id: str, enabled: bool) -> Dict:
        \"\"\"เปิด/ปิดเสียง\"\"\"
        
        if meeting_id not in self.active_calls:
            return {'status': 'error', 'message': 'Meeting not found'}
        
        meeting = self.active_calls[meeting_id]
        
        if participant_id in meeting['participants']:
            meeting['participants'][participant_id]['media']['audio_enabled'] = enabled
            
            # Broadcast audio status
            self._broadcast_to_meeting(meeting_id, {
                'type': 'audio_toggled',
                'participant_id': participant_id,
                'audio_enabled': enabled,
                'timestamp': datetime.now().isoformat()
            })
        
        return {'status': 'success'}
    
    def toggle_video(self, meeting_id: str, participant_id: str, enabled: bool) -> Dict:
        \"\"\"เปิด/ปิดกล้อง\"\"\"
        
        if meeting_id not in self.active_calls:
            return {'status': 'error', 'message': 'Meeting not found'}
        
        meeting = self.active_calls[meeting_id]
        
        if participant_id in meeting['participants']:
            meeting['participants'][participant_id]['media']['video_enabled'] = enabled
            
            # Broadcast video status
            self._broadcast_to_meeting(meeting_id, {
                'type': 'video_toggled',
                'participant_id': participant_id,
                'video_enabled': enabled,
                'timestamp': datetime.now().isoformat()
            })
        
        return {'status': 'success'}
    
    def start_screen_share(self, meeting_id: str, participant_id: str) -> Dict:
        \"\"\"เริ่มแชร์หน้าจอ\"\"\"
        
        if meeting_id not in self.active_calls:
            return {'status': 'error', 'message': 'Meeting not found'}
        
        meeting = self.active_calls[meeting_id]
        
        if participant_id not in meeting['participants']:
            return {'status': 'error', 'message': 'Participant not found'}
        
        participant = meeting['participants'][participant_id]
        
        # Check permission
        if not participant['permissions']['can_share_screen']:
            return {'status': 'error', 'message': 'Screen sharing not allowed'}
        
        # Stop others' screen sharing (only one at a time)
        for pid, p in meeting['participants'].items():
            if p['media']['screen_sharing']:
                self.stop_screen_share(meeting_id, pid)
        
        # Start screen sharing for this participant
        participant['media']['screen_sharing'] = True
        participant['media']['media_type'] = MediaType.SCREEN_SHARE.value
        
        # Broadcast screen share start
        self._broadcast_to_meeting(meeting_id, {
            'type': 'screen_share_started',
            'participant_id': participant_id,
            'timestamp': datetime.now().isoformat()
        })
        
        return {'status': 'success'}
    
    def stop_screen_share(self, meeting_id: str, participant_id: str) -> Dict:
        \"\"\"หยุดแชร์หน้าจอ\"\"\"
        
        if meeting_id not in self.active_calls:
            return {'status': 'error', 'message': 'Meeting not found'}
        
        meeting = self.active_calls[meeting_id]
        
        if participant_id in meeting['participants']:
            participant = meeting['participants'][participant_id]
            participant['media']['screen_sharing'] = False
            participant['media']['media_type'] = MediaType.VIDEO.value
            
            # Broadcast screen share stop
            self._broadcast_to_meeting(meeting_id, {
                'type': 'screen_share_stopped',
                'participant_id': participant_id,
                'timestamp': datetime.now().isoformat()
            })
        
        return {'status': 'success'}
    
    def start_recording(self, meeting_id: str, requester_id: str) -> Dict:
        \"\"\"เริ่มบันทึกการประชุม\"\"\"
        
        if meeting_id not in self.active_calls:
            return {'status': 'error', 'message': 'Meeting not found'}
        
        meeting = self.active_calls[meeting_id]
        
        # Check permission
        if requester_id not in meeting['participants']:
            return {'status': 'error', 'message': 'Participant not found'}
        
        if not meeting['participants'][requester_id]['permissions']['can_record']:
            return {'status': 'error', 'message': 'Recording not allowed'}
        
        if not meeting['settings']['enable_recording']:
            return {'status': 'error', 'message': 'Recording disabled for this meeting'}
        
        # Create recording session
        recording_id = str(uuid.uuid4())
        recording = {
            'recording_id': recording_id,
            'meeting_id': meeting_id,
            'started_by': requester_id,
            'started_at': datetime.now().isoformat(),
            'status': 'recording',
            'file_path': f'/recordings/{recording_id}.mp4',
            'settings': {
                'include_video': True,
                'include_audio': True,
                'include_screen_share': True,
                'quality': meeting['media_settings']['video_quality']
            }
        }
        
        self.recording_sessions[recording_id] = recording
        meeting['status'] = CallStatus.RECORDING.value
        meeting['current_recording'] = recording_id
        
        # Broadcast recording start
        self._broadcast_to_meeting(meeting_id, {
            'type': 'recording_started',
            'recording_id': recording_id,
            'started_by': requester_id,
            'timestamp': datetime.now().isoformat()
        })
        
        return {'status': 'success', 'recording_id': recording_id}
    
    def stop_recording(self, meeting_id: str, requester_id: str) -> Dict:
        \"\"\"หยุดบันทึกการประชุม\"\"\"
        
        if meeting_id not in self.active_calls:
            return {'status': 'error', 'message': 'Meeting not found'}
        
        meeting = self.active_calls[meeting_id]
        
        if 'current_recording' not in meeting:
            return {'status': 'error', 'message': 'No active recording'}
        
        recording_id = meeting['current_recording']
        recording = self.recording_sessions[recording_id]
        
        # Stop recording
        recording['status'] = 'completed'
        recording['ended_at'] = datetime.now().isoformat()
        recording['file_size'] = '1.2 GB'  # Mock file size
        
        meeting['status'] = CallStatus.ACTIVE.value
        del meeting['current_recording']
        
        # Broadcast recording stop
        self._broadcast_to_meeting(meeting_id, {
            'type': 'recording_stopped',
            'recording_id': recording_id,
            'file_path': recording['file_path'],
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'status': 'success',
            'recording_id': recording_id,
            'file_path': recording['file_path']
        }
    
    def end_meeting(self, meeting_id: str, requester_id: str) -> Dict:
        \"\"\"จบการประชุม\"\"\"
        
        if meeting_id not in self.active_calls:
            return {'status': 'error', 'message': 'Meeting not found'}
        
        meeting = self.active_calls[meeting_id]
        
        # Stop any active recording
        if 'current_recording' in meeting:
            self.stop_recording(meeting_id, requester_id)
        
        # Update meeting status
        meeting['status'] = CallStatus.ENDED.value
        meeting['ended_at'] = datetime.now().isoformat()
        meeting['ended_by'] = requester_id
        
        # Calculate meeting duration
        if 'started_at' in meeting:
            started = datetime.fromisoformat(meeting['started_at'])
            ended = datetime.fromisoformat(meeting['ended_at'])
            meeting['duration_minutes'] = round((ended - started).total_seconds() / 60, 2)
        
        # Notify all participants
        self._broadcast_to_meeting(meeting_id, {
            'type': 'meeting_ended',
            'ended_by': requester_id,
            'timestamp': datetime.now().isoformat()
        })
        
        # Move to history
        self.call_history.append(meeting)
        del self.active_calls[meeting_id]
        
        return {'status': 'success', 'meeting_summary': self._generate_meeting_summary(meeting)}
    
    def _generate_meeting_summary(self, meeting: Dict) -> Dict:
        \"\"\"สร้างสรุปการประชุม\"\"\"
        
        return {
            'meeting_id': meeting['meeting_id'],
            'title': meeting['title'],
            'duration_minutes': meeting.get('duration_minutes', 0),
            'participant_count': len(meeting['participants']),
            'recordings': [r for r in self.recording_sessions.values() if r['meeting_id'] == meeting['meeting_id']],
            'started_at': meeting.get('started_at'),
            'ended_at': meeting.get('ended_at')
        }
    
    def _broadcast_to_meeting(self, meeting_id: str, message: Dict, exclude_participant: str = None):
        \"\"\"ส่งข้อความไปยังผู้เข้าร่วมทั้งหมด\"\"\"
        
        if meeting_id not in self.active_calls:
            return
        
        meeting = self.active_calls[meeting_id]
        
        for participant_id, participant in meeting['participants'].items():
            if participant['status'] == 'connected' and participant_id != exclude_participant:
                # In real implementation, send via WebSocket/WebRTC
                self._send_to_participant(participant_id, message)
    
    def _send_to_participant(self, participant_id: str, data: Dict):
        \"\"\"ส่งข้อมูลไปยังผู้เข้าร่วม (mock)\"\"\"
        
        # Mock implementation - would use real WebRTC/WebSocket
        pass
    
    def get_meeting_info(self, meeting_id: str) -> Dict:
        \"\"\"ดึงข้อมูลการประชุม\"\"\"
        
        if meeting_id in self.active_calls:
            meeting = self.active_calls[meeting_id]
            return {
                'status': 'success',
                'meeting': {
                    'meeting_id': meeting_id,
                    'title': meeting['title'],
                    'status': meeting['status'],
                    'participant_count': len([p for p in meeting['participants'].values() if p['status'] == 'connected']),
                    'duration': self._calculate_duration(meeting),
                    'settings': meeting['settings']
                }
            }
        
        return {'status': 'error', 'message': 'Meeting not found'}
    
    def _calculate_duration(self, meeting: Dict) -> str:
        \"\"\"คำนวณระยะเวลาการประชุม\"\"\"
        
        if 'started_at' not in meeting:
            return '0 minutes'
        
        started = datetime.fromisoformat(meeting['started_at'])
        now = datetime.now()
        duration_minutes = round((now - started).total_seconds() / 60, 1)
        
        return f'{duration_minutes} minutes'
"""
        
        with open(os.path.join(video_path, "video_conferencing.py"), "w") as f:
            f.write(video_system)
        
        return os.path.join(video_path, "video_conferencing.py")
    
    def _create_notification_system(self, project_path: str, config: Dict) -> str:
        """สร้าง Real-time Notification System"""
        
        notification_path = os.path.join(project_path, "notification_system")
        os.makedirs(notification_path, exist_ok=True)
        
        notification_system = """
from typing import Dict, List, Optional, Any, Set
import json
import asyncio
from datetime import datetime, timedelta
from enum import Enum
import uuid

class NotificationType(Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    URGENT = "urgent"

class NotificationChannel(Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"
    WEBHOOK = "webhook"
    SLACK = "slack"
    DISCORD = "discord"

class NotificationPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class NotificationSystem:
    def __init__(self):
        self.notification_queue = []
        self.user_subscriptions = {}
        self.notification_templates = {}
        self.delivery_channels = {}
        self.sent_notifications = []
        
    def send_notification(self, notification_data: Dict) -> Dict:
        \"\"\"ส่งการแจ้งเตือน\"\"\"
        
        notification_id = str(uuid.uuid4())
        
        notification = {
            'notification_id': notification_id,
            'title': notification_data.get('title', 'Notification'),
            'message': notification_data.get('message', ''),
            'type': notification_data.get('type', NotificationType.INFO.value),
            'priority': notification_data.get('priority', NotificationPriority.MEDIUM.value),
            'created_at': datetime.now().isoformat(),
            'scheduled_at': notification_data.get('scheduled_at'),
            'expires_at': notification_data.get('expires_at'),
            'sender': notification_data.get('sender'),
            'recipients': notification_data.get('recipients', []),
            'channels': notification_data.get('channels', [NotificationChannel.IN_APP.value]),
            'data': notification_data.get('data', {}),
            'template_id': notification_data.get('template_id'),
            'tags': notification_data.get('tags', []),
            'status': 'pending'
        }
        
        # Apply template if specified
        if notification['template_id'] and notification['template_id'] in self.notification_templates:
            notification = self._apply_template(notification)
        
        # Add to queue
        self.notification_queue.append(notification)
        
        # Send immediately or schedule
        if notification['scheduled_at']:
            self._schedule_notification(notification)
        else:
            self._deliver_notification(notification)
        
        return {
            'status': 'success',
            'notification_id': notification_id,
            'estimated_delivery': self._estimate_delivery_time(notification)
        }
    
    def send_bulk_notification(self, notification_data: Dict, recipients: List[str]) -> Dict:
        \"\"\"ส่งการแจ้งเตือนแบบ bulk\"\"\"
        
        batch_id = str(uuid.uuid4())
        sent_notifications = []
        
        for recipient in recipients:
            # Customize notification for each recipient
            recipient_notification = notification_data.copy()
            recipient_notification['recipients'] = [recipient]
            recipient_notification['batch_id'] = batch_id
            
            # Personalize message if needed
            if 'personalization' in notification_data:
                recipient_notification = self._personalize_notification(
                    recipient_notification, recipient
                )
            
            result = self.send_notification(recipient_notification)
            sent_notifications.append({
                'recipient': recipient,
                'notification_id': result.get('notification_id'),
                'status': result.get('status')
            })
        
        return {
            'status': 'success',
            'batch_id': batch_id,
            'total_sent': len(sent_notifications),
            'notifications': sent_notifications
        }
    
    def subscribe_user(self, user_id: str, subscription_config: Dict) -> Dict:
        \"\"\"ผู้ใช้สมัครรับการแจ้งเตือน\"\"\"
        
        subscription = {
            'user_id': user_id,
            'channels': subscription_config.get('channels', [NotificationChannel.IN_APP.value]),
            'types': subscription_config.get('types', [t.value for t in NotificationType]),
            'priorities': subscription_config.get('priorities', [p.value for p in NotificationPriority]),
            'tags': subscription_config.get('tags', []),
            'schedule': subscription_config.get('schedule', {
                'enabled': True,
                'quiet_hours': {'start': '22:00', 'end': '08:00'},
                'days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            }),
            'preferences': {
                'group_similar': subscription_config.get('group_similar', True),
                'max_frequency': subscription_config.get('max_frequency', 'unlimited'),  # per hour
                'delivery_method': subscription_config.get('delivery_method', 'immediate')  # immediate, batched, digest
            },
            'created_at': datetime.now().isoformat(),
            'active': True
        }
        
        self.user_subscriptions[user_id] = subscription
        
        return {
            'status': 'success',
            'message': 'Subscription created successfully',
            'subscription': subscription
        }
    
    def unsubscribe_user(self, user_id: str, channels: List[str] = None) -> Dict:
        \"\"\"ยกเลิกการสมัครรับการแจ้งเตือน\"\"\"
        
        if user_id not in self.user_subscriptions:
            return {'status': 'error', 'message': 'User not subscribed'}
        
        if channels:
            # Unsubscribe from specific channels
            current_channels = self.user_subscriptions[user_id]['channels']
            self.user_subscriptions[user_id]['channels'] = [
                ch for ch in current_channels if ch not in channels
            ]
        else:
            # Unsubscribe completely
            self.user_subscriptions[user_id]['active'] = False
        
        return {'status': 'success', 'message': 'Unsubscribed successfully'}
    
    def create_template(self, template_config: Dict) -> Dict:
        \"\"\"สร้าง template สำหรับการแจ้งเตือน\"\"\"
        
        template_id = template_config.get('template_id', str(uuid.uuid4()))
        
        template = {
            'template_id': template_id,
            'name': template_config.get('name', 'Untitled Template'),
            'title_template': template_config.get('title_template', '{title}'),
            'message_template': template_config.get('message_template', '{message}'),
            'type': template_config.get('type', NotificationType.INFO.value),
            'priority': template_config.get('priority', NotificationPriority.MEDIUM.value),
            'channels': template_config.get('channels', [NotificationChannel.IN_APP.value]),
            'variables': template_config.get('variables', []),
            'styling': template_config.get('styling', {}),
            'created_at': datetime.now().isoformat(),
            'active': True
        }
        
        self.notification_templates[template_id] = template
        
        return {
            'status': 'success',
            'template_id': template_id,
            'template': template
        }
    
    def _apply_template(self, notification: Dict) -> Dict:
        \"\"\"ใช้ template กับการแจ้งเตือน\"\"\"
        
        template = self.notification_templates[notification['template_id']]
        
        # Apply template values
        notification['type'] = template['type']
        notification['priority'] = template['priority']
        notification['channels'] = template['channels']
        
        # Apply template formatting
        template_vars = notification.get('data', {})
        template_vars.update({
            'title': notification['title'],
            'message': notification['message']
        })
        
        try:
            notification['title'] = template['title_template'].format(**template_vars)
            notification['message'] = template['message_template'].format(**template_vars)
        except KeyError as e:
            notification['_template_error'] = f'Missing variable: {e}'
        
        return notification
    
    def _personalize_notification(self, notification: Dict, recipient: str) -> Dict:
        \"\"\"ปรับแต่งการแจ้งเตือนสำหรับผู้รับ\"\"\"
        
        # Mock personalization - in real app, fetch user preferences
        user_preferences = {
            'name': f'User_{recipient[-4:]}',
            'timezone': 'UTC+7',
            'language': 'th'
        }
        
        # Apply personalization
        message = notification['message']
        for key, value in user_preferences.items():
            message = message.replace(f'{{{key}}}', str(value))
        
        notification['message'] = message
        notification['personalized'] = True
        
        return notification
    
    def _schedule_notification(self, notification: Dict):
        \"\"\"กำหนดเวลาส่งการแจ้งเตือน\"\"\"
        
        # Mock scheduling - in real app, use task queue like Celery
        notification['status'] = 'scheduled'
        
        # Would implement actual scheduling here
        print(f'Scheduled notification {notification[\"notification_id\"]} for {notification[\"scheduled_at\"]}')
    
    def _deliver_notification(self, notification: Dict) -> Dict:
        \"\"\"ส่งการแจ้งเตือน\"\"\"
        
        delivery_results = []
        
        for channel in notification['channels']:
            for recipient in notification['recipients']:
                # Check user subscription
                if not self._can_deliver_to_user(recipient, notification, channel):
                    continue
                
                # Deliver via channel
                result = self._deliver_via_channel(notification, recipient, channel)
                delivery_results.append(result)
        
        # Update notification status
        successful_deliveries = [r for r in delivery_results if r['status'] == 'success']
        if successful_deliveries:
            notification['status'] = 'delivered'
            notification['delivered_at'] = datetime.now().isoformat()
        else:
            notification['status'] = 'failed'
        
        notification['delivery_results'] = delivery_results
        self.sent_notifications.append(notification)
        
        return {
            'notification_id': notification['notification_id'],
            'status': notification['status'],
            'delivery_results': delivery_results
        }
    
    def _can_deliver_to_user(self, user_id: str, notification: Dict, channel: str) -> bool:
        \"\"\"ตรวจสอบว่าสามารถส่งให้ผู้ใช้ได้หรือไม่\"\"\"
        
        if user_id not in self.user_subscriptions:
            return True  # Default allow if no subscription
        
        subscription = self.user_subscriptions[user_id]
        
        if not subscription['active']:
            return False
        
        # Check channel
        if channel not in subscription['channels']:
            return False
        
        # Check type
        if notification['type'] not in subscription['types']:
            return False
        
        # Check priority
        if notification['priority'] not in subscription['priorities']:
            return False
        
        # Check quiet hours
        schedule = subscription['schedule']
        if schedule['enabled'] and 'quiet_hours' in schedule:
            current_time = datetime.now().strftime('%H:%M')
            quiet_start = schedule['quiet_hours']['start']
            quiet_end = schedule['quiet_hours']['end']
            
            # Simple quiet hours check (doesn't handle midnight crossing)
            if quiet_start <= current_time <= quiet_end:
                return notification['priority'] == NotificationPriority.CRITICAL.value
        
        return True
    
    def _deliver_via_channel(self, notification: Dict, recipient: str, channel: str) -> Dict:
        \"\"\"ส่งผ่านช่องทางเฉพาะ\"\"\"
        
        delivery_id = str(uuid.uuid4())
        
        # Mock delivery - in real app, integrate with actual services
        if channel == NotificationChannel.EMAIL.value:
            result = self._send_email(notification, recipient)
        elif channel == NotificationChannel.SMS.value:
            result = self._send_sms(notification, recipient)
        elif channel == NotificationChannel.PUSH.value:
            result = self._send_push(notification, recipient)
        elif channel == NotificationChannel.IN_APP.value:
            result = self._send_in_app(notification, recipient)
        elif channel == NotificationChannel.WEBHOOK.value:
            result = self._send_webhook(notification, recipient)
        elif channel == NotificationChannel.SLACK.value:
            result = self._send_slack(notification, recipient)
        else:
            result = {'status': 'error', 'message': f'Unsupported channel: {channel}'}
        
        result['delivery_id'] = delivery_id
        result['channel'] = channel
        result['recipient'] = recipient
        result['delivered_at'] = datetime.now().isoformat()
        
        return result
    
    def _send_email(self, notification: Dict, recipient: str) -> Dict:
        \"\"\"ส่งอีเมล (mock)\"\"\"
        return {'status': 'success', 'message': 'Email sent successfully'}
    
    def _send_sms(self, notification: Dict, recipient: str) -> Dict:
        \"\"\"ส่ง SMS (mock)\"\"\"
        return {'status': 'success', 'message': 'SMS sent successfully'}
    
    def _send_push(self, notification: Dict, recipient: str) -> Dict:
        \"\"\"ส่ง Push notification (mock)\"\"\"
        return {'status': 'success', 'message': 'Push notification sent successfully'}
    
    def _send_in_app(self, notification: Dict, recipient: str) -> Dict:
        \"\"\"ส่งแจ้งเตือนในแอป (mock)\"\"\"
        return {'status': 'success', 'message': 'In-app notification sent successfully'}
    
    def _send_webhook(self, notification: Dict, recipient: str) -> Dict:
        \"\"\"ส่ง Webhook (mock)\"\"\"
        return {'status': 'success', 'message': 'Webhook sent successfully'}
    
    def _send_slack(self, notification: Dict, recipient: str) -> Dict:
        \"\"\"ส่ง Slack (mock)\"\"\"
        return {'status': 'success', 'message': 'Slack message sent successfully'}
    
    def _estimate_delivery_time(self, notification: Dict) -> str:
        \"\"\"ประมาณเวลาส่ง\"\"\"
        
        if notification['scheduled_at']:
            return notification['scheduled_at']
        
        # Estimate based on priority and channels
        if notification['priority'] == NotificationPriority.CRITICAL.value:
            return 'Immediate'
        elif NotificationChannel.EMAIL.value in notification['channels']:
            return 'Within 1 minute'
        else:
            return 'Within 30 seconds'
    
    def get_notification_status(self, notification_id: str) -> Dict:
        \"\"\"ตรวจสอบสถานะการแจ้งเตือน\"\"\"
        
        # Search in sent notifications
        for notification in self.sent_notifications:
            if notification['notification_id'] == notification_id:
                return {
                    'status': 'found',
                    'notification': notification
                }
        
        # Search in queue
        for notification in self.notification_queue:
            if notification['notification_id'] == notification_id:
                return {
                    'status': 'found',
                    'notification': notification
                }
        
        return {'status': 'not_found', 'message': 'Notification not found'}
    
    def get_user_notifications(self, user_id: str, filters: Dict = None) -> Dict:
        \"\"\"ดึงการแจ้งเตือนของผู้ใช้\"\"\"
        
        user_notifications = []
        
        for notification in self.sent_notifications:
            if user_id in notification['recipients']:
                # Apply filters if provided
                if filters:
                    if 'type' in filters and notification['type'] != filters['type']:
                        continue
                    if 'read' in filters and notification.get('read', False) != filters['read']:
                        continue
                
                user_notifications.append(notification)
        
        return {
            'status': 'success',
            'user_id': user_id,
            'notifications': user_notifications,
            'count': len(user_notifications)
        }
    
    def mark_as_read(self, notification_id: str, user_id: str) -> Dict:
        \"\"\"มาร์คว่าอ่านแล้ว\"\"\"
        
        for notification in self.sent_notifications:
            if (notification['notification_id'] == notification_id and 
                user_id in notification['recipients']):
                
                if 'read_by' not in notification:
                    notification['read_by'] = {}
                
                notification['read_by'][user_id] = datetime.now().isoformat()
                
                return {'status': 'success', 'message': 'Marked as read'}
        
        return {'status': 'error', 'message': 'Notification not found'}
    
    def get_notification_analytics(self, days: int = 7) -> Dict:
        \"\"\"สถิติการแจ้งเตือน\"\"\"
        
        # Calculate time threshold
        threshold = datetime.now() - timedelta(days=days)
        
        recent_notifications = [
            n for n in self.sent_notifications 
            if datetime.fromisoformat(n['created_at']) >= threshold
        ]
        
        # Count by type
        type_counts = {}
        channel_counts = {}
        status_counts = {}
        
        for notification in recent_notifications:
            # Types
            ntype = notification['type']
            type_counts[ntype] = type_counts.get(ntype, 0) + 1
            
            # Channels
            for channel in notification['channels']:
                channel_counts[channel] = channel_counts.get(channel, 0) + 1
            
            # Status
            status = notification['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            'period_days': days,
            'total_notifications': len(recent_notifications),
            'type_breakdown': type_counts,
            'channel_breakdown': channel_counts,
            'status_breakdown': status_counts,
            'delivery_rate': (status_counts.get('delivered', 0) / len(recent_notifications) * 100) if recent_notifications else 0,
            'generated_at': datetime.now().isoformat()
        }
"""
        
        with open(os.path.join(notification_path, "notification_system.py"), "w") as f:
            f.write(notification_system)
        
        return os.path.join(notification_path, "notification_system.py")
    
    def _create_streaming_service(self, project_path: str, config: Dict) -> str:
        """สร้าง Live Streaming Service"""
        
        streaming_path = os.path.join(project_path, "live_streaming")
        os.makedirs(streaming_path, exist_ok=True)
        
        streaming_service = """
from typing import Dict, List, Optional, Any
import json
from datetime import datetime, timedelta
from enum import Enum
import uuid

class StreamStatus(Enum):
    PREPARING = "preparing"
    LIVE = "live"
    PAUSED = "paused"
    ENDED = "ended"
    ERROR = "error"

class StreamQuality(Enum):
    LOW = "480p"
    MEDIUM = "720p"
    HIGH = "1080p"
    ULTRA = "4K"

class LiveStreamingService:
    def __init__(self):
        self.active_streams = {}
        self.stream_history = []
        self.viewers = {}
        
    def create_stream(self, stream_config: Dict) -> Dict:
        \"\"\"สร้าง live stream ใหม่\"\"\"
        
        stream_id = str(uuid.uuid4())
        
        stream = {
            'stream_id': stream_id,
            'title': stream_config.get('title', 'Live Stream'),
            'description': stream_config.get('description', ''),
            'streamer_id': stream_config.get('streamer_id'),
            'created_at': datetime.now().isoformat(),
            'status': StreamStatus.PREPARING.value,
            'settings': {
                'quality': stream_config.get('quality', StreamQuality.HIGH.value),
                'max_viewers': stream_config.get('max_viewers', 10000),
                'enable_chat': stream_config.get('enable_chat', True),
                'enable_recording': stream_config.get('enable_recording', False),
                'is_private': stream_config.get('is_private', False),
                'password': stream_config.get('password'),
                'scheduled_start': stream_config.get('scheduled_start'),
                'tags': stream_config.get('tags', [])
            },
            'stats': {
                'viewers': 0,
                'peak_viewers': 0,
                'total_views': 0,
                'likes': 0,
                'comments': 0
            }
        }
        
        self.active_streams[stream_id] = stream
        
        return {
            'status': 'success',
            'stream_id': stream_id,
            'rtmp_url': f'rtmp://streaming.server.com/live/{stream_id}',
            'stream_key': f'sk_{stream_id}',
            'watch_url': f'/stream/{stream_id}'
        }
    
    def start_stream(self, stream_id: str, streamer_id: str) -> Dict:
        \"\"\"เริ่ม live stream\"\"\"
        
        if stream_id not in self.active_streams:
            return {'status': 'error', 'message': 'Stream not found'}
        
        stream = self.active_streams[stream_id]
        
        if stream['streamer_id'] != streamer_id:
            return {'status': 'error', 'message': 'Unauthorized'}
        
        stream['status'] = StreamStatus.LIVE.value
        stream['started_at'] = datetime.now().isoformat()
        
        # Notify subscribers
        self._notify_stream_start(stream)
        
        return {'status': 'success', 'message': 'Stream started'}
    
    def end_stream(self, stream_id: str, streamer_id: str) -> Dict:
        \"\"\"จบ live stream\"\"\"
        
        if stream_id not in self.active_streams:
            return {'status': 'error', 'message': 'Stream not found'}
        
        stream = self.active_streams[stream_id]
        
        if stream['streamer_id'] != streamer_id:
            return {'status': 'error', 'message': 'Unauthorized'}
        
        stream['status'] = StreamStatus.ENDED.value
        stream['ended_at'] = datetime.now().isoformat()
        
        # Calculate duration
        if 'started_at' in stream:
            started = datetime.fromisoformat(stream['started_at'])
            ended = datetime.fromisoformat(stream['ended_at'])
            stream['duration_seconds'] = int((ended - started).total_seconds())
        
        # Move to history
        self.stream_history.append(stream)
        del self.active_streams[stream_id]
        
        # Notify viewers
        self._notify_stream_end(stream)
        
        return {
            'status': 'success',
            'stream_summary': {
                'duration_seconds': stream.get('duration_seconds', 0),
                'peak_viewers': stream['stats']['peak_viewers'],
                'total_views': stream['stats']['total_views']
            }
        }
    
    def join_stream(self, stream_id: str, viewer_info: Dict) -> Dict:
        \"\"\"เข้าร่วมดู live stream\"\"\"
        
        if stream_id not in self.active_streams:
            return {'status': 'error', 'message': 'Stream not found'}
        
        stream = self.active_streams[stream_id]
        
        if stream['status'] != StreamStatus.LIVE.value:
            return {'status': 'error', 'message': 'Stream not live'}
        
        viewer_id = viewer_info.get('viewer_id', str(uuid.uuid4()))
        
        # Check max viewers
        if len(self.viewers.get(stream_id, {})) >= stream['settings']['max_viewers']:
            return {'status': 'error', 'message': 'Stream is full'}
        
        # Add viewer
        if stream_id not in self.viewers:
            self.viewers[stream_id] = {}
        
        self.viewers[stream_id][viewer_id] = {
            'viewer_id': viewer_id,
            'name': viewer_info.get('name', 'Anonymous'),
            'joined_at': datetime.now().isoformat(),
            'is_active': True
        }
        
        # Update stats
        current_viewers = len([v for v in self.viewers[stream_id].values() if v['is_active']])
        stream['stats']['viewers'] = current_viewers
        stream['stats']['total_views'] += 1
        
        if current_viewers > stream['stats']['peak_viewers']:
            stream['stats']['peak_viewers'] = current_viewers
        
        return {
            'status': 'success',
            'stream_info': {
                'title': stream['title'],
                'streamer_id': stream['streamer_id'],
                'quality': stream['settings']['quality'],
                'current_viewers': current_viewers
            },
            'viewer_id': viewer_id
        }
    
    def leave_stream(self, stream_id: str, viewer_id: str) -> Dict:
        \"\"\"ออกจากการดู live stream\"\"\"
        
        if stream_id in self.viewers and viewer_id in self.viewers[stream_id]:
            self.viewers[stream_id][viewer_id]['is_active'] = False
            self.viewers[stream_id][viewer_id]['left_at'] = datetime.now().isoformat()
            
            # Update viewer count
            if stream_id in self.active_streams:
                current_viewers = len([v for v in self.viewers[stream_id].values() if v['is_active']])
                self.active_streams[stream_id]['stats']['viewers'] = current_viewers
        
        return {'status': 'success'}
    
    def _notify_stream_start(self, stream: Dict):
        \"\"\"แจ้งเตือนการเริ่มสตรีม\"\"\"
        # Mock notification - would integrate with notification system
        pass
    
    def _notify_stream_end(self, stream: Dict):
        \"\"\"แจ้งเตือนการจบสตรีม\"\"\"
        # Mock notification - would integrate with notification system  
        pass
"""
        
        with open(os.path.join(streaming_path, "live_streaming.py"), "w") as f:
            f.write(streaming_service)
        
        return os.path.join(streaming_path, "live_streaming.py")
    
    def _create_multiplayer_system(self, project_path: str, config: Dict) -> str:
        """สร้าง Multiplayer Gaming System"""
        
        multiplayer_path = os.path.join(project_path, "multiplayer_gaming")
        os.makedirs(multiplayer_path, exist_ok=True)
        
        multiplayer_system = """
from typing import Dict, List, Optional, Any
import json
from datetime import datetime, timedelta
from enum import Enum
import uuid

class GameState(Enum):
    WAITING = "waiting"
    ACTIVE = "active" 
    PAUSED = "paused"
    FINISHED = "finished"

class PlayerState(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    IN_GAME = "in_game"
    SPECTATING = "spectating"

class MultiplayerGamingSystem:
    def __init__(self):
        self.game_rooms = {}
        self.players = {}
        self.matchmaking_queue = []
        
    def create_game_room(self, room_config: Dict) -> Dict:
        \"\"\"สร้างห้องเกม\"\"\"
        
        room_id = str(uuid.uuid4())
        
        room = {
            'room_id': room_id,
            'name': room_config.get('name', 'Game Room'),
            'game_type': room_config.get('game_type', 'generic'),
            'host_id': room_config.get('host_id'),
            'created_at': datetime.now().isoformat(),
            'state': GameState.WAITING.value,
            'settings': {
                'max_players': room_config.get('max_players', 4),
                'is_private': room_config.get('is_private', False),
                'password': room_config.get('password'),
                'allow_spectators': room_config.get('allow_spectators', True),
                'game_mode': room_config.get('game_mode', 'classic')
            },
            'players': {},
            'spectators': {},
            'game_data': {}
        }
        
        self.game_rooms[room_id] = room
        
        return {
            'status': 'success',
            'room_id': room_id,
            'join_code': f'GAME-{room_id[-6:].upper()}'
        }
    
    def join_room(self, room_id: str, player_info: Dict) -> Dict:
        \"\"\"เข้าร่วมห้องเกม\"\"\"
        
        if room_id not in self.game_rooms:
            return {'status': 'error', 'message': 'Room not found'}
        
        room = self.game_rooms[room_id]
        player_id = player_info.get('player_id')
        
        # Check room capacity
        if len(room['players']) >= room['settings']['max_players']:
            if room['settings']['allow_spectators']:
                return self._join_as_spectator(room_id, player_info)
            else:
                return {'status': 'error', 'message': 'Room is full'}
        
        # Add player to room
        player = {
            'player_id': player_id,
            'name': player_info.get('name', f'Player{len(room[\"players\"]) + 1}'),
            'joined_at': datetime.now().isoformat(),
            'state': PlayerState.ONLINE.value,
            'score': 0,
            'ready': False
        }
        
        room['players'][player_id] = player
        
        # Notify other players
        self._broadcast_to_room(room_id, {
            'type': 'player_joined',
            'player': player
        })
        
        return {
            'status': 'success',
            'room_info': {
                'room_id': room_id,
                'name': room['name'],
                'players': list(room['players'].values()),
                'game_state': room['state']
            }
        }
    
    def start_game(self, room_id: str, host_id: str) -> Dict:
        \"\"\"เริ่มเกม\"\"\"
        
        if room_id not in self.game_rooms:
            return {'status': 'error', 'message': 'Room not found'}
        
        room = self.game_rooms[room_id]
        
        if room['host_id'] != host_id:
            return {'status': 'error', 'message': 'Only host can start game'}
        
        # Check if all players are ready
        ready_players = [p for p in room['players'].values() if p['ready']]
        if len(ready_players) < 2:
            return {'status': 'error', 'message': 'Need at least 2 ready players'}
        
        # Initialize game
        room['state'] = GameState.ACTIVE.value
        room['started_at'] = datetime.now().isoformat()
        room['game_data'] = self._initialize_game_data(room)
        
        # Update player states
        for player in room['players'].values():
            player['state'] = PlayerState.IN_GAME.value
        
        # Broadcast game start
        self._broadcast_to_room(room_id, {
            'type': 'game_started',
            'game_data': room['game_data']
        })
        
        return {'status': 'success', 'game_data': room['game_data']}
    
    def _join_as_spectator(self, room_id: str, player_info: Dict) -> Dict:
        \"\"\"เข้าร่วมในฐานะผู้ชม\"\"\"
        
        room = self.game_rooms[room_id]
        spectator_id = player_info.get('player_id')
        
        spectator = {
            'spectator_id': spectator_id,
            'name': player_info.get('name', 'Spectator'),
            'joined_at': datetime.now().isoformat()
        }
        
        room['spectators'][spectator_id] = spectator
        
        return {
            'status': 'success',
            'role': 'spectator',
            'room_info': {
                'room_id': room_id,
                'name': room['name'],
                'players': list(room['players'].values()),
                'game_state': room['state']
            }
        }
    
    def _initialize_game_data(self, room: Dict) -> Dict:
        \"\"\"เริ่มต้นข้อมูลเกม\"\"\"
        
        return {
            'turn': 0,
            'current_player': list(room['players'].keys())[0],
            'game_board': {},  # Game-specific data
            'rules': room['settings'].get('game_mode', 'classic')
        }
    
    def _broadcast_to_room(self, room_id: str, message: Dict):
        \"\"\"ส่งข้อความไปยังทุกคนในห้อง\"\"\"
        
        # Mock broadcast - would use WebSocket in real implementation
        pass
"""
        
        with open(os.path.join(multiplayer_path, "multiplayer_gaming.py"), "w") as f:
            f.write(multiplayer_system)
        
        return os.path.join(multiplayer_path, "multiplayer_gaming.py")
    
    def _integrate_as_library(self, feature_path: str, project_path: str, config: Dict) -> Dict:
        """รวมฟีเจอร์เป็น library"""
        
        library_integration = {
            'integration_type': 'library',
            'feature_path': feature_path,
            'library_name': config.get('library_name', 'advanced_feature'),
            'version': config.get('version', '1.0.0'),
            'dependencies': config.get('dependencies', []),
            'export_methods': config.get('export_methods', []),
            'documentation': f'{feature_path}/README.md',
            'examples': f'{feature_path}/examples/',
            'tests': f'{feature_path}/tests/',
            'integration_code': self._generate_library_integration_code(config)
        }
        
        return {
            'status': 'success',
            'integration': library_integration,
            'usage_example': f"import {library_integration['library_name']}",
            'documentation_url': f'/docs/{library_integration['library_name']}'
        }
    
    def _integrate_as_external_api(self, feature_path: str, project_path: str, config: Dict) -> Dict:
        """รวมฟีเจอร์เป็น external API"""
        
        api_integration = {
            'integration_type': 'external_api',
            'feature_path': feature_path,
            'api_endpoint': config.get('api_endpoint', '/api/v1/feature'),
            'authentication': config.get('authentication', 'api_key'),
            'rate_limiting': config.get('rate_limiting', {'requests_per_minute': 100}),
            'documentation': f'{feature_path}/api_docs.json',
            'sdk_languages': config.get('sdk_languages', ['python', 'javascript', 'curl']),
            'integration_code': self._generate_api_integration_code(config)
        }
        
        return {
            'status': 'success',
            'integration': api_integration,
            'usage_example': f"curl -H 'Authorization: Bearer YOUR_API_KEY' {api_integration['api_endpoint']}",
            'sdk_downloads': f'/sdks/{api_integration['api_endpoint'].replace('/', '_')}'
        }
    
    def _integrate_as_middleware(self, feature_path: str, project_path: str, config: Dict) -> Dict:
        """รวมฟีเจอร์เป็น middleware"""
        
        middleware_integration = {
            'integration_type': 'middleware',
            'feature_path': feature_path,
            'middleware_name': config.get('middleware_name', 'AdvancedFeatureMiddleware'),
            'framework': config.get('framework', 'express'),  # express, flask, django, etc.
            'priority': config.get('priority', 100),
            'configuration': config.get('configuration', {}),
            'hooks': config.get('hooks', ['before_request', 'after_response']),
            'integration_code': self._generate_middleware_integration_code(config)
        }
        
        return {
            'status': 'success',
            'integration': middleware_integration,
            'usage_example': f"app.use({middleware_integration['middleware_name']}({middleware_integration['configuration']}))",
            'installation_guide': f'/docs/middleware/{middleware_integration['middleware_name']}'
        }

# สร้าง instance
advanced_features_system = AdvancedFeaturesSystem()

if __name__ == "__main__":
    print("🎯 Advanced Features Integration System")
    print("=" * 50)
    print("🤖 AI/ML Features:")
    print("   • Recommendation Engine")
    print("   • AI Chatbot")
    print("   • Content Moderation") 
    print("   • Image Recognition")
    print("   • Fraud Detection")
    print()
    print("⛓️  Blockchain Features:")
    print("   • Smart Contracts")
    print("   • NFT Marketplace")
    print("   • Crypto Wallet")
    print("   • DAO Governance")
    print()
    print("🏭 IoT Features:")
    print("   • Device Management")
    print("   • Sensor Processing")
    print("   • Edge Computing")
    print("   • Industrial Automation")
    print()
    print("🛡️ Security Features:")
    print("   • Multi-Factor Auth")
    print("   • Encryption Service")
    print("   • Threat Detection")
    print("   • Compliance Framework")
    print()
    print("⚡ Real-time Features:")
    print("   • Live Collaboration")
    print("   • Video Conferencing")  
    print("   • Live Streaming")
    print("   • Multiplayer Gaming")