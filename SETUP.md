# P2P Chat App Setup Guide

## Prerequisites

- Python 3.10 or higher
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Network access for WebSocket connections

## Installation & Setup

### 1. Install Dependencies

Using pip:

```bash
pip install websockets aiohttp aiortc requests
```

Or using the project file:

```bash
pip install -e .
```

### 2. Start the Server

```bash
python server.py
```

The server will start listening on `ws://0.0.0.0:8765`

### 3. Open the Application

1. Open `index.html` in your web browser
2. Enter your display name
3. Choose a chat room (global or create/join private)
4. Start chatting!

## Configuration

### Debug Mode (for Development)

The app includes a debug mode for local development and troubleshooting:

1. **Enable Debug Mode**: Edit `config.js` and set `DEBUG_MODE: true`
2. **Debug Features**:
   - Real-time connection info panel
   - Detailed console logging
   - Debug toggle button (🐛) in chat header
   - WebSocket and WebRTC event tracking

**Debug Panel shows**:

- Server URL being used
- Your client ID
- Number of connected peers
- Current room name

**To disable debug mode**: Set `DEBUG_MODE: false` in `config.js`

### Server Configuration

By default, the client connects to `localhost:8765`. To configure the server:

**Method 1 - Edit config.js** (Recommended):

```javascript
const CONFIG = {
  DEBUG_MODE: false, // Set to true for debugging
  DEFAULT_SERVER: "your-server-ip:8765",
  PRODUCTION_SERVER: "your-production-server:8765",
};
```

**Method 2 - URL Parameter**:
Add `?server=your-server:port` to the chat room URL
Example: `chatRoom.html?name=John&room=global&server=192.168.1.100:8765`

### Network Configuration

- The server binds to `0.0.0.0:8765` by default
- Ensure port 8765 is not blocked by firewall
- For production, consider using a reverse proxy with SSL/TLS

## Troubleshooting

### Connection Issues

- Verify the server is running and accessible
- Check firewall settings
- Ensure WebSocket support in your browser

### WebRTC Issues

- Some networks block WebRTC connections
- STUN server may be needed for NAT traversal
- Check browser console for error messages

### Performance Issues

- Limit message length (currently set to 1000 characters)
- Monitor memory usage with many concurrent users
- Consider implementing message history limits

## Production Deployment

For production use, consider:

1. **Security**: Add authentication and rate limiting
2. **SSL/TLS**: Use secure WebSocket connections (wss://)
3. **Monitoring**: Add logging and health checks
4. **Scaling**: Consider using Redis for session management
5. **Validation**: Add server-side input validation

## Browser Compatibility

- Chrome/Chromium 60+
- Firefox 55+
- Safari 11+
- Edge 79+

WebRTC features require HTTPS in most browsers for production use.
