# API Mobile Documentation

Cette API REST est conçue pour une application mobile, permettant la gestion d'items (produits) avec les opérations CRUD (Create, Read, Update, Delete).

## Structure du Projet

- `main.py` : Serveur API FastAPI
- `client.js` : Client de test Node.js
- `requirements.txt` : Dépendances Python
- `package.json` : Dépendances Node.js

## Installation

### Backend (Python)

1. Installer les dépendances Python :
```bash
python3 -m pip install -r requirements.txt
```

2. Lancer le serveur :
```bash
python3 main.py
```

Le serveur démarre sur http://localhost:8000

### Client de Test (Node.js)

1. Installer les dépendances Node.js :
```bash
npm install
```

2. Lancer le client de test :
```bash
npm start
```

## Endpoints API

### 1. Obtenir tous les items
- **GET** `/items`
- Retourne la liste de tous les items

### 2. Obtenir un item spécifique
- **GET** `/items/{item_id}`
- Retourne les détails d'un item spécifique

### 3. Créer un nouvel item
- **POST** `/items`
- Corps de la requête :
```json
{
    "name": "string",
    "description": "string",
    "price": float
}
```

### 4. Mettre à jour un item
- **PUT** `/items/{item_id}`
- Corps de la requête :
```json
{
    "name": "string",
    "description": "string",
    "price": float
}
```

### 5. Supprimer un item
- **DELETE** `/items/{item_id}`
- Supprime l'item spécifié

## Format des Données

### Item
```json
{
    "id": integer,
    "name": "string",
    "description": "string",
    "price": float
}
```

## Test avec le Client

Le fichier `client.js` fournit un exemple complet d'utilisation de l'API. Il effectue les opérations suivantes :
1. Crée un nouvel item (iPhone 13)
2. Récupère la liste des items
3. Récupère les détails d'un item spécifique
4. Met à jour l'item (iPhone 13 Pro)
5. Supprime l'item

## Documentation API

Une documentation interactive Swagger UI est disponible à l'adresse : http://localhost:8000/docs