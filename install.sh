#!/bin/bash

# Couleurs pour le terminal
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m' # Pas de couleur

echo -e "${CYAN}🤖 Installation de CommitCraft...${NC}"

# Téléchargement du script python directement depuis GitHub
# (Remplace 'aleclelay11-dot' par ton vrai pseudo si besoin)
URL="https://raw.githubusercontent.com/aleclelay11-dot/CommitCraft/main/commitcraft.py"

# Dossier de destination local (pas besoin de droits root/sudo)
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

echo "📥 Téléchargement de commitcraft.py..."
curl -sSL "$URL" -o "$BIN_DIR/commitcraft.py"

# Création d'un petit exécutable pour lancer le script proprement
cat << 'EOF' > "$BIN_DIR/commitcraft"
#!/bin/bash
python3 "$HOME/.local/bin/commitcraft.py" "$@"
EOF

# Rendre le script exécutable
chmod +x "$BIN_DIR/commitcraft"

echo -e "${GREEN}✨ CommitCraft a été installé avec succès dans $BIN_DIR/commitcraft !${NC}"
echo -e "💡 Assure-toi que ${CYAN}$BIN_DIR${NC} est bien dans ton PATH pour pouvoir taper juste 'commitcraft'."