import subprocess
import sys
import json
import urllib.request
import threading
import time
import itertools
import argparse

# Valeurs par défaut
DEFAULT_OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL_NAME = "mistral"

def get_git_diff():
    try:
        result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print("❌ Erreur : Impossible d'exécuter 'git diff'. Es-tu dans un dépôt Git ?")
        sys.exit(1)

def generate_commit_message(diff, url, model):
    prompt = (
        "Tu es un expert Git. Génère un message de commit court, précis et en anglais, "
        "en respectant STRICTEMENT la convention 'Conventional Commits' (ex: 'feat: add auth login', 'fix: resolve memory leak'). "
        "Ne renvoie QUE le message de commit, aucun commentaire, aucune explication, pas de balises markdown."
        f"\n\nVoici le Git Diff :\n{diff}"
    )
    data = {"model": model, "prompt": prompt, "stream": False}
    try:
        req = urllib.request.Request(
            url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data.get("response", "").strip()
    except Exception:
        return None

def spinner_animation(stop_event, model):
    spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
    while not stop_event.is_set():
        sys.stdout.write(f"\r\033[96m{next(spinner)}\033[0m CommitCraft ({model}) réfléchit...")
        sys.stdout.flush()
        time.sleep(0.08)
    sys.stdout.write('\r' + ' ' * 50 + '\r')
    sys.stdout.flush()

def main():
    # Configuration d'argparse
    parser = argparse.ArgumentParser(description="🤖 CommitCraft - Générateur de commits IA local")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL_NAME, help=f"Modèle Ollama à utiliser (par défaut: {DEFAULT_MODEL_NAME})")
    parser.add_argument("-u", "--url", default=DEFAULT_OLLAMA_URL, help=f"URL de l'API Ollama (par défaut: {DEFAULT_OLLAMA_URL})")
    args = parser.parse_args()

    diff = get_git_diff()
    if not diff:
        print("📭 Aucun changement indexé détecté. Fais un 'git add' d'abord !")
        return

    while True:
        stop_spinner = threading.Event()
        spinner_thread = threading.Thread(target=spinner_animation, args=(stop_spinner, args.model))
        spinner_thread.start()

        commit_msg = generate_commit_message(diff, args.url, args.model)

        stop_spinner.set()
        spinner_thread.join()

        if not commit_msg:
            print(f"❌ Impossible de joindre Ollama sur {args.url}.")
            print(f"💡 Vérifie qu'Ollama tourne et que le modèle '{args.model}' est bien installé (`ollama run {args.model}`).")
            break

        print("✨ Message suggéré :")
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
            print("\n🔄 On régénère un message...\n")
            continue
        else:
            print("❌ Commit annulé.")
            break

if __name__ == "__main__":
    main()