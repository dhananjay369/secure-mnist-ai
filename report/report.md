# Secure AI Systems – Red and Blue Teaming an MNIST Classifier

**Team members:** ____________________ and ____________________  
**GitHub repository:** ____________________  
**Attack-code repository/folder:** ____________________

## 1. Introduction
This project demonstrates the security lifecycle of a CNN image classifier using MNIST. The model is trained and evaluated on clean data, threat-modeled using STRIDE, OWASP ML security concepts and LINDDUN, scanned with SAST, attacked using FGSM and label/data poisoning, and defended using adversarial training plus input validation.

## 2. System
MNIST contains 28×28 grayscale handwritten digits in ten classes. The CNN uses Conv2D(32) → ReLU → MaxPool → Conv2D(64) → ReLU → MaxPool → Flatten → Dense(128) → ReLU → Dropout(0.2) → Dense(10). Adam and cross-entropy loss are used.

## 3. Baseline Performance
Run `python -m src.train` and `python -m src.evaluate`. Copy actual values from `results/baseline_metrics.json`.

| Metric | Baseline |
|---|---:|
| Test accuracy | [ACTUAL] |
| Test loss | [ACTUAL] |
| Inference time | [ACTUAL] s |
| Average/image | [ACTUAL] ms |

Include `results/baseline_confusion_matrix.png`.

## 4. Attacker Model
The attacker can submit crafted inference inputs. For poisoning, the attacker has limited influence over part of the training-data/labeling pipeline. The attacker does not have root access or direct control of the training server. Objectives are to reduce integrity/accuracy, evade detection, or manipulate learned behavior.

## 5. STRIDE
| Category | MNIST threat | Control |
|---|---|---|
| Spoofing | Unauthorized access to ML service | Authentication/authorization |
| Tampering | Modified training images/labels | Provenance, hashes, validation |
| Repudiation | Missing attack logs | Audit logging |
| Information Disclosure | Training/model information leakage | Access control, minimization |
| Denial of Service | Excessive inference requests | Rate limiting |
| Elevation of Privilege | Unauthorized training/model access | Least privilege |

## 6. OWASP ML Mapping
The assignment should use the exact OWASP ML Top 10 version supplied in class. Conceptually, training-data poisoning maps to data/training integrity risk and FGSM maps to adversarial/evasion risk. Supply-chain, information-disclosure and availability risks are additional relevant concerns.

## 7. LINDDUN
For a real-world handwriting system: Linkability can connect multiple samples; Identifiability can expose identity; Non-repudiation can associate predictions with users; Detectability can reveal data presence; Disclosure can expose training information; Unawareness can occur if users do not know samples are retained; Non-compliance can arise from privacy/regulatory violations. MNIST itself is a benchmark dataset and is not representative of a sensitive deployment.

## 8. SAST
Run `bash security/run_sast.sh`. Bandit scans the intentional vulnerable fixture in `security/sast_before.py` and the fixed implementation in `security/sast_fixed.py`. The vulnerable version concatenates input into a shell command and uses `shell=True`; the fix passes an argument list with `shell=False`. Include the generated before/after reports and only claim findings confirmed by the scan.

## 9. Red Team Attack 1 – FGSM
Run `python attacks/fgsm_attack.py`. FGSM computes `x_adv = x + epsilon * sign(gradient(loss,x))` and clips pixels to [0,1]. Default epsilon is 0.20. This represents an inference-time adversarial/evasion threat because the model parameters are not changed.

Copy values from `results/fgsm_metrics.json`:

| Metric | Value |
|---|---:|
| Samples | [ACTUAL] |
| Clean accuracy | [ACTUAL] |
| Adversarial accuracy | [ACTUAL] |
| Prediction-change rate | [ACTUAL] |
| Attack success rate on initially correct samples | [ACTUAL] |

## 10. Red Team Attack 2 – Data Poisoning
Run `python attacks/poisoning_attack.py`. It creates a separate poisoned dataset by changing 5% of source-class 7 labels to target class 1. The original MNIST files are not modified. This demonstrates training-data tampering/poisoning.

Copy values from `results/poisoning_metadata.json`.

## 11. Blue Team
Run `python defense/adversarial_training.py`. The defended model is trained using clean samples plus FGSM samples. The additional defense is input validation: inputs are expected to have the correct shape/type and pixel range. A production service should also enforce request-size limits, rate limiting and stronger anomaly checks.

## 12. Final Comparison
Fill this table with measured results.

| Metric | Baseline | FGSM | Poisoned model | Blue team |
|---|---:|---:|---:|---:|
| Clean accuracy | [ACTUAL] | [ACTUAL] | [ACTUAL] | [ACTUAL] |
| Adversarial accuracy | N/A | [ACTUAL] | [ACTUAL] | [ACTUAL] |
| Loss | [ACTUAL] | [ACTUAL] | [ACTUAL] | [ACTUAL] |
| Inference time | [ACTUAL] | [ACTUAL] | [ACTUAL] | [ACTUAL] |

## 13. Conclusion
The experiment shows that clean accuracy alone is not sufficient to establish ML security. FGSM demonstrates inference-time evasion, while label poisoning demonstrates that the training pipeline is an attack surface. Threat modeling reveals additional risks around access, integrity, availability and privacy. SAST identifies source-level weaknesses, and adversarial training can improve robustness against the demonstrated perturbation. The final measured results should be used to discuss the trade-off between clean accuracy and robustness.

## References
- OWASP Machine Learning Security Top 10: https://owasp.org/projects/machine-learning-security-top-ten
- OWASP Source Code Analysis Tools: https://community.owasp.org/Source_Code_Analysis_Tools
- PyTorch: https://pytorch.org/
- torchvision MNIST documentation: https://pytorch.org/vision/stable/datasets.html
- Goodfellow et al., Explaining and Harnessing Adversarial Examples, 2015.
- STRIDE threat modeling methodology.
- LINDDUN privacy threat modeling framework.
