# Bonus – Multicast Networking

## What is Multicast?

Multicast is a communication method where a single sender transmits data to a group of receivers simultaneously using one data stream. Only receivers that have joined the multicast group will receive the data.

Unlike unicast (one-to-one) or broadcast (one-to-all), multicast is one-to-many but only to interested participants.

## Typical Use Cases

Common use cases for multicast include:
- Live video and audio streaming (IPTV)
- Financial data feeds (stock prices)
- Online multiplayer games
- Service discovery protocols
- Monitoring and alert systems

Multicast is efficient because the sender sends only one copy of the data, and the network distributes it.

## Moving Multicast Between Networks

By default, multicast traffic works only inside a single local network. Routers usually do not forward multicast packets between different networks.

To move multicast between networks, the following techniques are used:

### 1. Multicast Routing
Routers can use multicast routing protocols such as PIM (Protocol Independent Multicast) and IGMP to forward multicast traffic across networks.

### 2. Multicast Tunneling
Multicast traffic can be encapsulated inside unicast packets and sent through a tunnel between networks. The receiving side decapsulates and re-sends it as multicast.

### 3. Multicast Gateway / Relay
A relay service listens for multicast traffic in one network and forwards it to another network using unicast or a new multicast group.

### 4. Application-Level Relay
An application receives multicast messages and forwards them through application protocols like HTTP, Kafka, or message queues.

## Example Scenario

A stock exchange sends real-time stock prices using multicast inside its internal network.

Trading companies are located in different networks and cannot receive the multicast traffic directly.

A multicast gateway is deployed at the edge of the stock exchange network. It receives the multicast stream and forwards it through a unicast tunnel to the external trading networks.

In the trading network, the gateway re-broadcasts the data locally, allowing traders to receive live stock prices.
