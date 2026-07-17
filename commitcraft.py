import subprocess
import sys
import json
import urllib.request

# Configuration par défaut (Modifiable via arguments plus tard)
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"  # Tu peux changer pour llama3, qwen2.5, etc.

def get_git_diff():
    """Réupère les changements indexés (staged) de Git."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print("❌ Erreur : Impossible d'exécuter 'git diff'. Es-tu dans un dépôt Git ?")
        sys.exit(1)

def generate_commit_message(diff):
    """Envoie le diff à Ollama pour générer le message de commit."""
    prompt = (
        "Tu es un expert Git. Génère un message de commit court, précis et en anglais, "
        "en respectant STRICTEMENT la convention 'Conventional Commits' (ex: 'feat: add auth login', 'fix: resolve memory leak'). "
        "Ne renvoie QUE le message de commit, aucun commentaire, aucune explication, pas de balises markdown."
        f"\n\nVoici le Git Diff :\n{diff}"
    )

    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        req = urllib.request.Request(
            OLLAMA_URL,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data.get("response", "").strip()
    except Exception as e:
        return f"❌ Impossible de joindre Ollama sur {OLLAMA_URL}. Vérifie qu'il est lancé. ({e})"

def main():
    print("🔍 Analyse de tes changements indexés...")
    diff = get_git_diff()

    if not diff:
        print("📭 Aucun changement détecté. Pense à faire un 'git add' d'abord !")
        return

    print(f"🤖 L'IA ({MODEL_NAME}) réfléchit...")
    commit_msg = generate_commit_message(diff)

    print("\n✨ Message de commit suggéré :")
    print(f"\033[92m{commit_msg}\033[0m") # Affichage en vert
    print("-" * 40)

if __name__ == "__main__":
    main()