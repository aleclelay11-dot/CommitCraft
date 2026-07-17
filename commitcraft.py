import subprocess
import sys
import json
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"

def get_git_diff():
    try:
        result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print("❌ Erreur : Impossible d'exécuter 'git diff'. Es-tu dans un dépôt Git ?")
        sys.exit(1)

def generate_commit_message(diff):
    prompt = (
        "Tu es un expert Git. Génère un message de commit court, précis et en anglais, "
        "en respectant STRICTEMENT la convention 'Conventional Commits' (ex: 'feat: add auth login', 'fix: resolve memory leak'). "
        "Ne renvoie QUE le message de commit, aucun commentaire, aucune explication, pas de balises markdown."
        f"\n\nVoici le Git Diff :\n{diff}"
    )
    data = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
    try:
        req = urllib.request.Request(
            OLLAMA_URL, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data.get("response", "").strip()
    except Exception:
        return None

def main():
    diff = get_git_diff()
    if not diff:
        print("📭 Aucun changement indexé détecté. Fais un 'git add' d'abord !")
        return

    while True:
        print(f"🤖 L'IA ({MODEL_NAME}) génère ton message...")
        commit_msg = generate_commit_message(diff)

        if not commit_msg:
            print(f"❌ Impossible de joindre Ollama sur {OLLAMA_URL}.")
            print("💡 Astuce locale : Assure-toi qu'Ollama tourne sur ta machine ou dans ton Codespace.")
            break

        print("\n✨ Message suggéré :")
        print(f"\033[92m{commit_msg}\033[0m\n")

        choice = input("Appliquer ce commit ? [Y/n/r] (Yes / No / Regenerate) : ").strip().lower()

        if choice in ['', 'y', 'yes']:
            try:
                subprocess.run(["git", "commit", "-m", commit_msg], check=True)
                print("🚀 Changements commités avec succès !")
            except subprocess.CalledProcessError:
                print("❌ Échec lors de l'exécution du commit.")
            break
        elif choice == 'r':
            print("\n🔄 On recommence...\n")
            continue
        else:
            print("❌ Commit annulé.")
            break

if __name__ == "__main__":
    main()