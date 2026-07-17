🤖 CommitCraft

Générez de superbes messages de commit Git conformes aux standards, localement grâce à l'IA, en moins de 90 lignes de code. Zéro cloud, 100% privé.

✨ Fonctionnalités

💻 100% Local : Propulsé par Ollama. Aucune clé API ou connexion internet requise. Vos données de code restent sur votre machine.

⚡ Ultra-léger : Du pur Python, zéro dépendance tierce à installer (pas de packages lourds à télécharger).

🎨 Interface soignée (TUI) : Une animation de chargement (spinner) fluide dans le terminal et un prompt interactif.

🎯 Standardisé : Respecte STRICTEMENT la spécification mondiale Conventional Commits (feat:, fix:, docs:, etc.).

🚀 Démarrage rapide

1. Prérequis

Assurez-vous d'avoir Ollama installé et lancé sur votre machine avec votre modèle préféré (exemple : mistral, llama3, ou qwen2.5) :

ollama run mistral


2. Installation Instantanée (1 seconde)

Copiez-collez simplement cette commande unique dans votre terminal pour télécharger et configurer automatiquement CommitCraft sur votre système :

curl -sSL [https://raw.githubusercontent.com/aleclelay11-dot/CommitCraft/main/install.sh](https://raw.githubusercontent.com/aleclelay11-dot/CommitCraft/main/install.sh) | bash


💡 Configuration du PATH : Assurez-vous que le dossier ~/.local/bin est bien présent dans la variable $PATH de votre système afin de pouvoir taper la commande commitcraft depuis n'importe quel dossier.

3. Utilisation

Ajoutez vos modifications à l'index Git avec un git add classique, puis lancez simplement l'outil :

commitcraft


🛠️ Options de Personnalisation (CLI)

Vous pouvez changer de modèle d'IA ou d'adresse d'API locale à la volée directement à l'aide des options du terminal :

# Utiliser un autre modèle installé sur Ollama
commitcraft --model llama3

# Spécifier une adresse d'API ou un port personnalisé pour Ollama
commitcraft --url http://localhost:11434/api/generate


📄 Licence

Ce projet est publié sous Licence MIT. Vous pouvez l'utiliser, le copier, le modifier, le fusionner et le distribuer de façon totalement libre et gratuite. Consultez le fichier LICENSE pour plus de détails.

📢 Un gain de temps pour vos commits ? N'hésitez pas à laisser une ⭐ sur ce dépôt pour soutenir le projet et l'aider à grandir