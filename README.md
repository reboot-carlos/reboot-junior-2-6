# Chatbot Luffy - One Piece Edition 🏴‍☠️

Un chatbot professionnel créé avec **FastAPI** et alimenté par **Claude** ! 🧠

## 📋 Structure du Projet

```
RebootJR/
├── main.py                 # Application FastAPI + Claude
├── index.html              # Interface web du chatbot
├── requirements.txt        # Dépendances Python
├── background.png          # Image de fond
└── luffy.png              # Logo du chatbot
```

## 🚀 Installation et Lancement

### 1. Configure ta clé API Claude
```bash
export ANTHROPIC_API_KEY="ta-clé-api-ici"
```

### 2. Installe les dépendances
```bash
pip install -r requirements.txt
```

### 3. Démarre le serveur FastAPI
```bash
python main.py
```

Le serveur démarre sur `http://localhost:8000`

## 📡 Endpoints disponibles

### GET `/`
Infos sur le chatbot
```bash
curl http://localhost:8000/
```

### POST `/chat`
Envoie un message au chatbot
```bash
# Message simple
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"texte": "Bonjour"}'

# Message avec prompt personnalisé
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "texte": "Qui es-tu ?",
    "system_prompt": "Tu es un astronaute passionné par l'\''espace."
  }'
```

### GET `/aide`
Infos sur le chatbot
```bash
curl http://localhost:8000/aide
```

### POST `/config/prompt`
Change le système prompt par défaut
```bash
curl -X POST http://localhost:8000/config/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Tu es un professeur de mathématiques sérieux."}'
```

### GET `/config/prompt`
Obtient le système prompt actuel
```bash
curl http://localhost:8000/config/prompt
```

### POST `/config/prompt/reset`
Réinitialise le système prompt par défaut
```bash
curl -X POST http://localhost:8000/config/prompt/reset
```

## 📚 Documentation Interactive

Une fois le serveur lancé, accède à :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 🧠 Fonctionnement avec Claude

Le chatbot :
1. Reçoit un message texte via l'API
2. L'envoie à Claude via l'API Anthropic
3. Claude génère une réponse intelligente sur One Piece
4. Retourne la réponse au frontend

Claude comprend **n'importe quoi** ! Il peut parler de One Piece, répondre à tes questions, faire des blagues, etc.

## 🎨 Personnaliser le Chatbot

Tu as **3 façons** de personnaliser ton chatbot :

### 1️⃣ Prompt personnalisé par message
```json
{
  "texte": "Quel est le plus grand nombre ?",
  "system_prompt": "Tu es un génie en mathématiques."
}
```

### 2️⃣ Changer le prompt par défaut
```bash
curl -X POST http://localhost:8000/config/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Tu es un pirate amical de One Piece."}'
```

### 3️⃣ Réinitialiser le prompt
```bash
curl -X POST http://localhost:8000/config/prompt/reset
```

Tous les messages utilisont maintenant le nouveau prompt ! 🎯

## 📝 Code Propre et Professionnel

Ce code suit les bonnes pratiques :
- ✅ Commentaires explicites
- ✅ Types définis avec Pydantic
- ✅ Fonctions bien organisées
- ✅ Endpoints documentés
- ✅ Gestion d'erreurs basique
- ✅ CORS activé pour le frontend

Bon code ! 🎉
