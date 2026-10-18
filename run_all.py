
import subprocess
import sys

commands = [
    [sys.executable, "-m", "src.train"],
    [sys.executable, "-m", "src.evaluate"],
    [sys.executable, "-m", "attacks.fgsm_attack"],
    [sys.executable, "-m", "attacks.poisoning_attack"],
    [sys.executable, "-m", "attacks.poisoned_train"],
    [sys.executable, "-m", "attacks.evaluate_poisoning"],
    [sys.executable, "-m", "defense.adversarial_training"],
    [sys.executable, "-m", "attacks.test_defense"],
]

for command in commands:
    print(">>>", " ".join(command), flush=True)
    subprocess.run(command, check=True)

print("Experiments complete.")
print("Run bash security/run_sast.sh for SAST.")
