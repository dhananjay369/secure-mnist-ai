import subprocess,sys
commands = [
    [sys.executable, "-m", "src.train"],
    [sys.executable, "-m", "src.evaluate"],
    [sys.executable, "-m", "attacks.fgsm_attack"],
    [sys.executable, "-m", "attacks.poisoning_attack"],
    [sys.executable, "-m", "defense.adversarial_training"],
]
for c in commands:
    print('>>>',' '.join(c)); subprocess.run(c,check=True)
print('Experiment complete. Run bash security/run_sast.sh for SAST.')
