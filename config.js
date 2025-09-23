// Configuration for P2P Chat App
const CONFIG = {
    // Debug mode - set to true for local development
    DEBUG_MODE: true,
    
    // WebSocket server configuration
    DEFAULT_SERVER: 'localhost:8765',  // Local development server
    PRODUCTION_SERVER: 'your-production-server:8765', // Change this to your production server IP
    
    // Auto-select server based on debug mode
    get SERVER_URL() {
        return this.DEBUG_MODE ? this.DEFAULT_SERVER : this.PRODUCTION_SERVER;
    },
    
    // Debug settings
    DEBUG_LOGGING: true,
    DEBUG_SHOW_CONNECTION_INFO: true,
    
    // You can also add other configuration options here
    MAX_MESSAGE_LENGTH: 1000,
    MAX_RECONNECT_ATTEMPTS: 5,
    RECONNECT_DELAY: 2000,
    
    // STUN servers for WebRTC
    ICE_SERVERS: [
        { urls: "stun:stun.l.google.com:19302" },
        { urls: "stun:stun1.l.google.com:19302" }
    ]
};