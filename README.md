# TaskFlow

**TaskFlow** és una aplicació de gestió de tasques basada en microserveis. Està dissenyada per a equips de treball que necessiten una eina col·laborativa, escalable i fiable per crear, assignar i fer seguiment de tasques en temps real.

---

## Objectiu

Desenvolupar una aplicació distribuïda que:
- Permeti gestionar tasques col·laboratives.
- Ofereixi notificacions en temps real.
- Utilitzi arquitectura de microserveis amb comunicació asíncrona.
- Sigui tolerant a fallades i escalable.

---

## Funcionalitats

- Creació i assignació de tasques
- Gestió d'estats i prioritats
- Autenticació d'usuaris
- Notificacions en temps real
- Interfície web moderna i intuïtiva

---

## Arquitectura del Sistema

L’arquitectura de **TaskFlow** està basada en microserveis, amb els següents components principals:

- **Client Web (Vue.js):** Interfície d’usuari per gestionar tasques i rebre notificacions en temps real.
- **API Gateway (FastAPI):** Punt d’entrada que ruteja les peticions als diferents microserveis i gestiona la seguretat.
- **Servei d’Usuaris:** Gestió d’usuaris, autenticació i permisos.
- **Servei de Tasques:** Creació, actualització i assignació de tasques.
- **Servei de Notificacions:** Enviament de notificacions en temps real via WebSockets.
- **Servei d’Estats:** Control i sincronització de l’estat de les tasques per garantir coherència.
- **MongoDB:** Base de dades distribuïda per emmagatzemar dades d’usuaris i tasques.
- **RabbitMQ:** Sistema de missatgeria per a comunicació asíncrona entre serveis.
- **BetterStack / UptimeRobot:** Monitoratge i alertes per assegurar la disponibilitat i tolerància a fallades.

Aquest model permet una escalabilitat i mantenibilitat elevades, amb components independents que comuniquen mitjançant missatges asíncrons i bases de dades distribuïdes.

---

## Tecnologies

| Component       | Tecnologia         |
|----------------|--------------------|
| Backend         | Python + FastAPI   |
| Frontend        | Vue.js             |
| Base de dades   | MongoDB            |
| Missatgeria     | RabbitMQ           |
| Monitoratge     | BetterStack, UptimeRobot |
| Autenticació    | JWT                |

---

##  Estructura del projecte
```
TaskFlow/
├── backend/
│   ├── users/             # Servei d’usuaris (FastAPI)
│   └── tasks/             # Servei de tasques (en construcció)
├── frontend/
│   └── vue-app/           # Interfície web (en construcció)
├── requirements.txt       # Dependències de Python
├── README.md              # Documentació del projecte
```
---

## Funcionalitats previstes
Registre i login d’usuaris (JWT)

CRUD de tasques

Sistema de notificacions amb RabbitMQ

Control d’estats i coherència

Integració completa entre serveis
