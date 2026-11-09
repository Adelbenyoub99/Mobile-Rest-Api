# 📱 Mobile Product Catalog REST API

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black" alt="Swagger" />
</p>

API RESTful performante et conteneurisée conçue pour alimenter des applications mobiles (Flutter, React Native, Swift/Kotlin) et des interfaces web modernes.
Elle implémente les opérations CRUD complètes, la persistance relationnelle SQLite, le filtrage et la pagination, ainsi qu'une suite de tests automatisés.

---

## 🎯 Points Forts & Architecture

- **Framework FastAPI & Pydantic v2** : Validation stricte des données entrantes et sérialisation JSON haute vitesse.
- **Persistance SQLite** : Initialisation automatique de la base de données et des données de démonstration (seed data).
- **CORS Configuré** : Prêt pour une intégration immédiate avec des clients web front-end ou mobiles multiplateformes.
- **Documentation Interactive OpenAPI** : Swagger UI (`/docs`) et ReDoc (`/redoc`) générés automatiquement.
- **Double Environnement de Test** :
  - Tests unitaires et d'intégration automatisés avec **Pytest**.
  - Script de simulation client mobile automatisé en **Node.js** (`client.js`).
- **Conteneurisation Docker** : Déploiement et exécution en une seule ligne avec Docker Compose.

---

## 🛠️ Endpoints de l'API

| Méthode | Route | Description | Code Succès |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Informations sur l'API & statut | `200 OK` |
| `GET` | `/health` | Healthcheck pour orchestrateurs / load balancers | `200 OK` |
| `GET` | `/items` | Liste paginée des produits avec filtres (`search`, `category`, `limit`, `skip`) | `200 OK` |
| `GET` | `/items/{id}` | Détail d'un produit spécifique par identifiant | `200 OK` |
| `POST` | `/items` | Création d'un nouveau produit (validation Pydantic) | `201 Created` |
| `PUT` | `/items/{id}` | Mise à jour partielle ou totale des attributs | `200 OK` |
| `DELETE` | `/items/{id}` | Suppression d'un produit | `200 OK` |

---

## 🚀 Démarrage Rapide

### Option 1 : Avec Docker Compose (Recommandé)

```bash
# Lancer l'API conteneurisée
docker compose up -d

# Accéder à la documentation interactive
open http://localhost:8000/docs
```

### Option 2 : Installation Locale (Python)

```bash
# 1. Cloner le projet
git clone https://github.com/Adelbenyoub99/Mobile-Rest-Api.git
cd Mobile-Rest-Api

# 2. Installer les dépendances Python
pip install -r requirements.txt

# 3. Démarrer le serveur API
python main.py
```

Le serveur sera disponible sur `http://localhost:8000`.

---

## 🧪 Tests & Validation

### Exécuter la suite de tests automatisés (Pytest)

```bash
pytest -v
```

### Exécuter le client de démonstration Node.js

```bash
npm install
npm start
```

Le script exécutera automatiquement le cycle complet (Healthcheck ➔ Création ➔ Consultation ➔ Mise à jour ➔ Suppression).

---

## 👨‍💻 Auteur

**Adel BENYOUB**  
*Ingénieur d'État en Informatique • Master Génie Logiciel*  
- **Portfolio** : [benyoubadel-portfolio.netlify.app](https://benyoubadel-portfolio.netlify.app/)  
- **LinkedIn** : [linkedin.com/in/adel-benyoub](https://www.linkedin.com/in/adel-benyoub)  
- **GitHub** : [github.com/Adelbenyoub99](https://github.com/Adelbenyoub99)
