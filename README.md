# TaskFlow

**TaskFlow** és una aplicació web per a la gestió de tasques col·laboratives. Està pensada per facilitar el treball en equip, permetent la creació, assignació i seguiment de tasques amb notificacions en temps real i una interfície moderna i accessible.

Tot i que inicialment es va concebre sota una arquitectura de microserveis, finalment s’ha optat per un enfocament client-servidor, més adequat per a la complexitat del projecte i el temps disponible, mantenint igualment alguns principis de la computació distribuïda, com la comunicació asíncrona i la separació de responsabilitats lògiques.

---

## Objectiu

L’objectiu principal ha estat desenvolupar una aplicació distribuïda funcional, capaç de:
- Permetre la gestió eficient de tasques en equips de treball.
- Integrar notificacions en temps real a través de WebSockets.
- Implementar una arquitectura modular basada en client-servidor.
- Mantenir un sistema escalable i fàcilment extensible en un futur.

---

## Funcionalitats

- Registre i autenticació d’usuaris (basat en JSON Web Tokens).
- Creació, assignació i gestió de tasques amb estats i prioritats.
- Notificació en temps real dels canvis de tasca via WebSocket.
- Interfície SPA moderna desenvolupada amb Vue.js.
- Backend REST desenvolupat amb FastAPI i MongoDB com a base de dades.

---

## Arquitectura del Sistema

L’arquitectura de **TaskFlow** segueix el model client-servidor:

- **Frontend (Vue.js)**: Aplicació que permet interactuar amb les funcionalitats de l’aplicació de manera intuïtiva i reactiva.
- **Backend (FastAPI)**: Proporciona l’API REST per a la gestió de tasques i usuaris, incloent autenticació, lògica de negoci i notificacions.
- **WebSocket Server**: Integrat al backend per gestionar les notificacions en temps real.
- **MongoDB**: Base de dades NoSQL per emmagatzemar usuaris i tasques.
- **JWT**: Gestió segura de sessions i autenticació.

Aquesta arquitectura facilita la comunicació entre components, mantenint una separació clara entre la presentació i la lògica de negoci, amb suport per comunicació asíncrona (WebSocket).

---

## Tecnologies

| Component       | Tecnologia         |
|----------------|--------------------|
| Frontend         |Vue.js   |
| Backend API        | FastAPI (Python)           |
| Base de dades   | MongoDB            |
| Notificacions     | WebSocket (FastAPI)           |
| Autenticació     | JWT (Bearer tokens) |
| Control de versió    | Git + GitHub                |

---

##  Estructura del projecte
```
TaskFlow/
├── backend/
│   ├── api/                      # Endpoints REST i WebSocket
│   │   ├── notificacions.py
│   │   ├── projects.py
│   │   ├── tasks.py
│   │   ├── users.py
│   │   └── websocket.py
│   ├── db/                       # Connexió amb MongoDB
│   │   └── mongo.py
│   ├── models/                   # Esquemes Pydantic per a les dades
│   │   ├── commnet.py
│   │   ├── project.py
│   │   ├── task.py
│   │   └── user.py
│   ├── services/                # Lògica de negoci i gestió interna
│   │   ├── auth.py
│   │   ├── history.py
│   │   ├── notification.py
│   │   ├── project.py
│   │   └── websocket_manager.py
│   ├── config.py                # Configuració general del backend
│   └── main.py                  # Punt d’entrada FastAPI
│
├── frontend/
│   └── src/
│       ├── assets/              # Recursos visuals i estils globals
│       │   ├── styles.css
│       │   └── vue.svg
│       ├── components/          # Components reutilitzables Vue
│       │   ├── AuthForm.vue
│       │   ├── CommentSection.vue
│       │   ├── CreateProjectForm.vue
│       │   ├── ProjectList.vue
│       │   ├── ProjectNotifications.vue
│       │   ├── TaskForm.vue
│       │   └── TaskList.vue
│       ├── services/            # Connexió amb l'API backend
│       │   └── api.js
│       ├── views/               # Vistes principals de l'aplicació
│       │   ├── Home.vue
│       │   └── ProjectView.vue
│       ├── App.vue              # Component arrel de Vue
│       ├── main.js              # Inicialització de Vue
│       └── router.js            # Gestió de rutes
│
└── requirements.txt             # Dependències del backend (Python)
      
```
---

## Funcionalitats previstes
Registre i login d’usuaris (JWT)

CRUD de tasques

Sistema de notificacions amb RabbitMQ

Control d’estats i coherència

Integració completa entre serveis

# Sessions
Tota la documentació de les diferents sessions.

## Sessió 2 [15/05]: Disseny detallat i desenvolupament inicial

Presentació PDF: https://publuu.com/flip-book/882888/1933906

## Sessió 3 [19/05]: Prototip funcional bàsic

### Codi font actualitzat amb les funcionalitats implementades
Hem implementat els tres microserveis principal: users, tasks i notificacions

- Users: Podem iniciar sessio i registrar-nos.
- Tasks: Podem afegir, actualitzar i llistar les tasques.
- Notificacions: Tenom les notificacions a temps real.

### Canvis respecte a la proposta inicial

- No s’han introduït canvis importants respecte a les tecnologies definides inicialment.
- S’ha mantingut l’ús de FastAPI, MongoDB i RabbitMQ.
- El sistema de notificacions s’ha implementat amb WebSockets en lloc de polling, per oferir notificacions en temps real.
- S’ha afegit hashing de contrasenyes i autenticació JWT per protegir l’accés dels usuaris.

### Proposta de desplegament

El sistema es desplegarà utilitzant Docker. Cada microservei (usuaris, tasques i notificacions) tindrà el seu propi contenidor, juntament amb MongoDB i RabbitMQ.

Utilitzarem `docker-compose` per orquestrar els serveis:

- `users_service`: servei d’autenticació i registre.
- `tasks_service`: gestió de tasques i publicació a RabbitMQ.
- `notifications_service`: WebSocket i consumidor RabbitMQ.
- `mongo`: base de dades compartida entre serveis.
- `rabbitmq`: missatgeria per les notificacions.

Aquesta arquitectura permet fàcil escalabilitat. Per exemple, es poden replicar els serveis i afegir un balancejador de càrrega al front.

Monitoratge: s’hi podrà afegir un servei com Prometheus + Grafana per monitorar rendiment en entorns més grans.

### Presentació de l’arquitectura

Enllaç: https://publuu.com/flip-book/882888/1934217
