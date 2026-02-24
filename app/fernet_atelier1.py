import os
import sys
from cryptography.fernet import Fernet, InvalidToken


def get_fernet_from_env() -> Fernet:
    key = os.environ.get("FERNET_KEY")
    if not key:
        print("Erreur : la variable d'environnement FERNET_KEY n'est pas définie.")
        print("Assure-toi d'avoir créé le secret GitHub 'FERNET_KEY' et relancé ton Codespace.")
        sys.exit(1)

    try:
        # La clé est en Base64, donc on peut la passer directement à Fernet
        f = Fernet(key.encode() if isinstance(key, str) else key)
    except Exception as e:
        print("Erreur en construisant l'objet Fernet :", e)
        sys.exit(1)

    return f


def encrypt_file(in_path: str, out_path: str) -> None:
    fernet = get_fernet_from_env()

    with open(in_path, "rb") as f:
        data = f.read()

    token = fernet.encrypt(data)

    with open(out_path, "wb") as f:
        f.write(token)

    print(f"Fichier '{in_path}' chiffré vers '{out_path}'.")


def decrypt_file(in_path: str, out_path: str) -> None:
    fernet = get_fernet_from_env()

    with open(in_path, "rb") as f:
        token = f.read()

    try:
        data = fernet.decrypt(token)
    except InvalidToken:
        print("Erreur : token invalide (fichier modifié ou mauvaise clé).")
        sys.exit(1)

    with open(out_path, "wb") as f:
        f.write(data)

    print(f"Fichier '{in_path}' déchiffré vers '{out_path}'.")


def main():
    if len(sys.argv) != 4:
        print("Usage :")
        print("  python app/fernet_atelier1.py encrypt <input_file> <output_file>")
        print("  python app/fernet_atelier1.py decrypt <input_file> <output_file>")
        sys.exit(1)

    mode = sys.argv[1]
    in_path = sys.argv[2]
    out_path = sys.argv[3]

    if mode == "encrypt":
        encrypt_file(in_path, out_path)
    elif mode == "decrypt":
        decrypt_file(in_path, out_path)
    else:
        print("Mode inconnu :", mode)
        print("Utilise 'encrypt' ou 'decrypt'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
