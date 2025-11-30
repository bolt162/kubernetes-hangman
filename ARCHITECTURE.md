# Hangman Application Architecture

## Before: Monolithic Architecture

```
┌─────────────────────────────────────────┐
│                                         │
│        Monolithic Flask App             │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │     Frontend (Templates/Static)   │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │     Game Logic                    │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │     Leaderboard Logic             │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │     SQLite Database               │  │
│  └───────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

**Characteristics:**
- Single Flask application handling all responsibilities
- Tightly coupled components
- Single SQLite database
- Runs in a single Docker container
- Difficult to scale individual components
- All code in one file (hangman.py)

**Drawbacks:**
- Cannot scale frontend and backend independently
- Single point of failure
- Difficult to update individual components
- Limited horizontal scalability

---

## After: Microservices Architecture on Kubernetes

```
                                    ┌─────────────────────┐
                                    │   Load Balancer     │
                                    │   (NodePort/LB)     │
                                    └──────────┬──────────┘
                                               │
                        ┌──────────────────────┼──────────────────────┐
                        │                      │                      │
                        ▼                      ▼                      ▼
              ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
              │  Frontend        │   │  Game Service   │   │  Leaderboard    │
              │  Service         │   │                 │   │  Service        │
              │                  │   │                 │   │                 │
              │  - Serves HTML   │   │  - Game Logic   │   │  - High Scores  │
              │  - Static Files  │   │  - Word Select  │   │  - Rankings     │
              │  - Routes to APIs│   │  - State Mgmt   │   │  - Queries      │
              │                  │   │                 │   │                 │
              │  Port: 5000      │   │  Port: 5001     │   │  Port: 5002     │
              └─────────────────┘   └────────┬────────┘   └────────┬────────┘
                                             │                      │
                                             │                      │
                                    ┌────────▼──────────────────────▼────────┐
                                    │                                        │
                                    │   PostgreSQL Database (Persistent)     │
                                    │                                        │
                                    │   - Shared by Game & Leaderboard       │
                                    │   - Persistent Volume Claim            │
                                    │                                        │
                                    └────────────────────────────────────────┘
```

### Service Breakdown:

#### 1. Frontend Service
- **Responsibility**: Serves HTML templates and static files, routes user requests
- **Technology**: Flask
- **Endpoints**:
  - `GET /` - Home page
  - `GET /play` - Start new game (proxies to Game Service)
  - `GET /play/<game_id>` - Game page
- **Deployment**: 2 replicas for high availability
- **Service Type**: NodePort (accessible from outside cluster)

#### 2. Game Service
- **Responsibility**: Game logic, word selection, game state management
- **Technology**: Flask + SQLAlchemy
- **Endpoints**:
  - `POST /api/game/new` - Create new game
  - `GET /api/game/<id>` - Get game state
  - `POST /api/game/<id>/guess` - Submit a letter guess
- **Deployment**: 3 replicas for scalability
- **Service Type**: ClusterIP (internal only)
- **Database**: PostgreSQL

#### 3. Leaderboard Service
- **Responsibility**: Manage and retrieve high scores
- **Technology**: Flask + SQLAlchemy
- **Endpoints**:
  - `GET /api/leaderboard` - Get top 10 scores
  - `POST /api/leaderboard` - Add/update score
- **Deployment**: 2 replicas
- **Service Type**: ClusterIP (internal only)
- **Database**: PostgreSQL

### Kubernetes Components:

1. **Deployments**:
   - frontend-deployment (2 replicas)
   - game-service-deployment (3 replicas)
   - leaderboard-service-deployment (2 replicas)
   - postgres-deployment (1 replica with PVC)

2. **Services**:
   - frontend-service (NodePort)
   - game-service (ClusterIP)
   - leaderboard-service (ClusterIP)
   - postgres-service (ClusterIP)

3. **ConfigMaps**:
   - Database configuration
   - Application settings

4. **Persistent Volumes**:
   - PostgreSQL data storage

5. **Secrets**:
   - Database credentials

### Benefits of Microservices Architecture:

1. **Independent Scaling**: Scale game logic independently from frontend
2. **Fault Isolation**: Failure in one service doesn't crash entire app
3. **Independent Deployment**: Update services without full redeployment
4. **Technology Flexibility**: Can use different tech stacks per service
5. **Better Resource Utilization**: Kubernetes manages resources efficiently
6. **High Availability**: Multiple replicas ensure uptime
7. **Load Distribution**: Kubernetes load balances across pods

### Communication Flow:

1. User accesses frontend via NodePort
2. Frontend makes internal HTTP requests to game-service and leaderboard-service
3. Both backend services connect to shared PostgreSQL database
4. All services communicate via Kubernetes DNS (service names)

### Database Migration:

- **Before**: SQLite (file-based, not suitable for distributed systems)
- **After**: PostgreSQL (supports concurrent connections from multiple pods)
