import time
from halo import Halo

# Frames pour le spinner personnalisé
spinner_frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']

def process():
    time.sleep(10)
    time.sleep(0.1)

def main():
    total_iterations = 50

    # Utilisez Halo pour créer un spinner personnalisé
    with Halo(spinner={'interval': 100, 'frames': spinner_frames}, text="Démarrage du processus...") as spinner:
        for _ in range(total_iterations):
            process()
        spinner.succeed("Processus terminé.")

if __name__ == "__main__":
    main()