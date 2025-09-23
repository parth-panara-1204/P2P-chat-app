import asyncio
import json
import uuid
import websockets

# Global client registry
clients: dict[str, websockets.WebSocketServerProtocol] = {}
names:   dict[str, str] = {}       # client_id -> display name
rooms:   dict[str, set[str]] = {}  # room_name -> set of client_ids

async def handler(ws):
    client_id = str(uuid.uuid4())
    clients[client_id] = ws
    names[client_id] = None
    client_room = None

    try:
        async for raw in ws:
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                print(f"[ERROR] Invalid JSON from {client_id}: {raw}")
                continue

            # 1. Handle the initial join message
            if msg.get("type") == "join":
                client_room = msg["room"]
                names[client_id] = msg["name"]

                # Add to room
                rooms.setdefault(client_room, set()).add(client_id)

                # Send back our new ID + existing peers in this room
                peers = [
                  {"id": pid, "name": names[pid]}
                  for pid in rooms[client_room]
                  if pid != client_id
                ]
                await ws.send(json.dumps({
                  "type": "id",
                  "id":    client_id,
                  "peers": peers
                }))

                # Notify others in the room
                notice = json.dumps({
                  "type": "peer-connected",
                  "id":    client_id,
                  "name":  names[client_id]
                })
                for pid in rooms[client_room]:
                    if pid != client_id and pid in clients:
                        try:
                            await clients[pid].send(notice)
                        except websockets.exceptions.ConnectionClosed:
                            # Clean up disconnected client
                            clients.pop(pid, None)
                continue

            # 2. Relay signaling messages (`signal` type)
            if msg.get("type") == "signal":
                target = msg.get("to")
                # Only forward if target exists and is connected
                if target in clients:
                    try:
                        await clients[target].send(raw)
                    except websockets.exceptions.ConnectionClosed:
                        # Clean up disconnected client
                        clients.pop(target, None)

    except websockets.exceptions.ConnectionClosed:
        pass

    finally:
        # 3. Clean up on disconnect
        if client_room and client_id in rooms.get(client_room, set()):
            rooms[client_room].remove(client_id)

            # Broadcast leave to the room (safely)
            leave_msg = json.dumps({
              "type": "peer-disconnected",
              "id":    client_id,
              "name":  names.get(client_id, "Unknown User")
            })
            for pid in rooms.get(client_room, set()).copy():
                if pid in clients:
                    try:
                        await clients[pid].send(leave_msg)
                    except websockets.exceptions.ConnectionClosed:
                        # Clean up disconnected client
                        clients.pop(pid, None)

            # Remove empty rooms
            if not rooms[client_room]:
                del rooms[client_room]

        # Clean up client data
        clients.pop(client_id, None)
        names.pop(client_id, None)
        print(f"[*] Client {client_id} disconnected")

async def main():
    print("[*] Listening on ws://0.0.0.0:8765")
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
