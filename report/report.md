
# Secure AI Systems: Red and Blue Teaming an MNIST Classifier

**Name:** DHANANJAY KUMAR  
**Roll Number:** CS26MTECH13007

**GitHub Repository:** [Secure AI Systems – MNIST Classifier](https://github.com/dhananjay369/secure-mnist-ai)

## 1. GitHub Repository of CNN Implementation

This project implements a Convolutional Neural Network (CNN) for handwritten digit classification using the MNIST dataset.

**GitHub Repository:** https://github.com/dhananjay369/secure-mnist-ai

### Main Implementation Files

- `src/model.py` — CNN model architecture.
- `src/train.py` — model training.
- `src/evaluate.py` — model evaluation.
- `src/utils.py` — supporting utilities.
- `run_all.py` — project workflow.

The repository contains the CNN implementation, red-team attack scripts, blue-team defense code, experiment results, and documentation.

**Dataset note:** The MNIST dataset files are excluded from GitHub. They must be downloaded or made available locally before running the experiments.

## 2. Performance Metrics of Classification

The baseline CNN was evaluated on clean MNIST test data.

| Metric | Baseline CNN |
|---|---:|
| Clean test accuracy | 98.82% |
| Evaluation loss | 0.03282 |
| Inference time | 0.898 seconds |
| Average time per image | 0.0898 milliseconds |

The baseline model achieved 98.82% accuracy on clean test data. These results serve as the reference for evaluating the red-team attacks and blue-team defense.

## 3. Threat Model of the Implementation

### 3.1 System Overview

The system classifies handwritten digit images from the MNIST dataset using a trained CNN.

The main assets are:

- Training and test images.
- Training labels and their integrity.
- Trained model parameters and saved model files.
- Prediction accuracy and availability.
- Experiment results and evaluation code.

### 3.2 Attacker Model

This project considers two attack scenarios.

**A. Adversarial Example Attacker**

- The attacker modifies input images to cause incorrect predictions.
- The attack evaluated is the Fast Gradient Sign Method (FGSM).
- The experiment uses epsilon = 0.2.
- In this experimental setting, the attacker can use model gradients to construct adversarial examples.

**B. Data Poisoning Attacker**

- The attacker influences a portion of the training data or its labels.
- The experiment targets a source digit of 7 and a target digit of 1.
- The recorded poisoning configuration uses a 5% fraction of the source class and 313 poisoned samples.
- The intended goal is to make source-class examples be classified as the target class.

These scenarios describe the experiments conducted in this project. They do not prove that an attacker can modify data in a real-world deployment.

### 3.3 STRIDE Threat Analysis

| STRIDE Category | Potential Threat |
|---|---|
| Spoofing | An attacker may submit inputs intended to be mistaken for another digit. |
| Tampering | Training images, labels, or model files could be modified. |
| Repudiation | Missing audit logs may make it difficult to trace changes to datasets or models. |
| Information Disclosure | Model outputs, logs, or stored data may expose information in some deployment settings. |
| Denial of Service | Excessive requests may affect system availability. |
| Elevation of Privilege | Weak access controls could allow unauthorized modification of models or datasets. |

These are potential risks identified through threat modeling, not confirmed vulnerabilities in every category.

### 3.4 LINDDUN Privacy Notes

LINDDUN is a privacy threat-modeling framework. The following considerations are relevant if the classifier is deployed in a setting that processes sensitive data.

| LINDDUN Category | Potential Privacy Concern |
|---|---|
| Linkability | Multiple images or records may be linked to the same user through identifiers or logs. |
| Identifiability | Metadata associated with images may identify a person. |
| Non-repudiation | Detailed logs may make user actions traceable. |
| Detectability | An observer may infer whether a particular input was processed. |
| Disclosure of Information | Stored inputs, logs, or outputs may expose sensitive information. |
| Unawareness | Users may not know that their images or predictions are stored. |
| Non-compliance | Data collection or retention may violate applicable privacy requirements if not handled appropriately. |

MNIST is a public benchmark dataset. These LINDDUN notes describe potential deployment concerns and do not establish that a privacy breach occurred in this project.

## 4. SAST Findings and Fixes

### 4.1 Tool Used

Bandit was used to perform Static Application Security Testing (SAST) on:

- `security/sast_before.py`
- `security/sast_fixed.py`

**Scope limitation:** These scans cover the two demonstration scripts, not the entire MNIST application.

### 4.2 Findings Before Fix

The initial Bandit scan reported two findings.

| Bandit Rule | Severity | Description |
|---|---|---|
| B404 | Low | Import of the `subprocess` module requires security review. |
| B602 | High | A subprocess call uses `shell=True`, creating a potential command-injection risk. |

The B602 finding was associated with CWE-78 (OS Command Injection).

The original code concatenated user input into a shell command:

```python
subprocess.run(
    'echo ' + user_value,
    shell=True,
    capture_output=True,
    text=True
)
```

Using `shell=True` with untrusted input can allow input to alter the command executed by the shell.

### 4.3 Security Fix Applied

The code was modified to pass the command and input as separate arguments and disable shell interpretation.

**Before:**

```python
subprocess.run(
    'echo ' + user_value,
    shell=True,
    capture_output=True,
    text=True
)
```

**After:**

```python
subprocess.run(
    ['echo', user_value],
    shell=False,
    capture_output=True,
    text=True,
    check=True
)
```

The updated code reduces the risk of shell command injection by avoiding shell interpretation. The `check=True` option raises an exception if the command exits with a non-zero status.

Input validation and a trusted executable path should also be considered.

### 4.4 Findings After Fix

The follow-up Bandit scan reported three Low-severity findings and no High- or Medium-severity findings.

| Bandit Rule | Severity | Description |
|---|---|---|
| B404 | Low | The `subprocess` module is imported. |
| B607 | Low | A partial executable path is used. |
| B603 | Low | Subprocess execution requires review when untrusted input may be involved. |

These are warnings that require review; they do not automatically prove that the fixed script is exploitable.

### 4.5 Before-and-After Comparison

| Metric | Before Fix | After Fix |
|---|---:|---:|
| High-severity findings | 1 | 0 |
| Medium-severity findings | 0 | 0 |
| Low-severity findings | 1 | 3 |
| Total findings | 2 | 3 |

The High-severity B602 finding was eliminated. The total number of findings increased because additional Low-severity warnings were reported in the fixed script.

Therefore, the scan indicates a reduction in the identified high-risk shell-execution pattern, not a reduction in the total number of warnings.

## 5. Repository of Attack Code and Adversarial/Poisoned Dataset Experiments

**GitHub Repository:** https://github.com/dhananjay369/secure-mnist-ai

The same repository contains the CNN implementation, attack code, defense implementation, and experiment results.

### Relevant Attack and Defense Files

- `attacks/fgsm_attack.py` — FGSM adversarial attack.
- `attacks/poisoning_attack.py` — data poisoning attack implementation.
- `attacks/poisoned_train.py` — training with poisoned data.
- `attacks/evaluate_poisoning.py` — evaluation of the poisoning experiment.
- `attacks/test_defense.py` — comparison of baseline and defended models on FGSM samples.
- `defense/adversarial_training.py` — adversarial-training defense.
- `results/` — experiment metrics and output files.

The repository link above is used for both the CNN implementation and attack code because both are contained in the same repository.

**Dataset note:** The MNIST dataset directory is excluded from GitHub. The dataset must be downloaded or made available locally according to the project setup.

## 6. Performance Metrics with Adversarial and Poisoned Data

### 6.1 FGSM Adversarial Attack

A separate FGSM evaluation used epsilon = 0.2 and 5,000 samples.

| Metric | Result |
|---|---:|
| Clean accuracy in this evaluation | 98.26% |
| Accuracy on adversarial examples | 45.12% |
| Prediction change rate | 53.28% |
| Attack success rate on initially correct clean predictions | 54.08% |

The results show that FGSM perturbations substantially reduced classification accuracy in this evaluation.

The clean accuracy reported here comes from a separate FGSM evaluation run; it is not the baseline metric reported in Section 2.

### 6.2 Data Poisoning Experiment

The poisoning experiment targeted the mapping from digit 7 to digit 1. The recorded configuration used a 5% fraction of the source class and 313 poisoned samples.

| Metric | Baseline Model | Poisoned Model |
|---|---:|---:|
| Clean test accuracy | 98.82% | 98.88% |
| Class-7 accuracy | 98.35% | 98.44% |
| True label 7 predicted as 1 | 0 | 0 |

The intended 7-to-1 targeted misclassification was not observed in the reported clean-test evaluation. No test examples with true label 7 were predicted as 1 in either evaluation.

Therefore, the result should be described as a poisoning attempt whose intended targeted effect was not observed, rather than a successful backdoor attack.

## 7. Blue-Team Implementation and Performance Compared with Baseline

### 7.1 Defense Implementation

The blue-team defense uses adversarial training. The recorded configuration uses:

- Adversarial-training epsilon: 0.2
- Adversarial-training samples: 10,000

Implementation file: `defense/adversarial_training.py`.

The purpose of adversarial training is to improve the model's robustness against adversarial inputs.

### 7.2 Comparison on the Same FGSM Samples

The following results were obtained from the same-sample comparison in `attacks/test_defense.py`.

| Metric | Baseline Model | Defended Model |
|---|---:|---:|
| Clean accuracy | 98.82% | 98.25% |
| FGSM adversarial accuracy | 50.23% | 96.51% |

The defended model improved adversarial accuracy by **46.28 percentage points**:

96.51% - 50.23% = 46.28 percentage points.

Clean accuracy decreased by **0.57 percentage points**:

98.82% - 98.25% = 0.57 percentage points.

### 7.3 Observations

- FGSM substantially reduced the baseline model's accuracy on adversarial samples.
- Adversarial training improved accuracy on the tested FGSM samples.
- The defended model retained slightly lower clean accuracy than the baseline.
- The poisoning experiment did not demonstrate the intended targeted 7-to-1 misclassification in the reported clean-test evaluation.
- These results demonstrate performance on the tested configurations; they do not prove robustness against every possible attack.

## 8. Conclusion and Observations

This project evaluated a CNN for MNIST digit classification using a red-team/blue-team workflow.

The baseline model achieved 98.82% clean test accuracy. The FGSM experiment showed that adversarial perturbations can substantially degrade classification performance. Adversarial training increased accuracy from 50.23% to 96.51% on the same tested FGSM samples, while clean accuracy decreased slightly from 98.82% to 98.25%.

The data poisoning experiment targeted a 7-to-1 misclassification using 313 poisoned samples. However, the intended targeted effect was not observed in the reported clean-test results. This is an important experimental limitation and should not be described as a successful poisoning attack.

Bandit identified a High-severity `shell=True` pattern in the demonstration script. The revised code disabled shell interpretation and removed that High-severity finding, although three Low-severity warnings remained. The scan covered only the two demonstration scripts, so a complete SAST scan of the entire application remains future work.

Overall, the experiments demonstrate the importance of testing both model robustness and code security. Future work should include broader adversarial evaluations, additional poisoning success metrics, review of remaining SAST warnings, and testing with more datasets and model configurations.

## References

1. MNIST Database of Handwritten Digits: http://yann.lecun.com/exdb/mnist/
2. Bandit documentation: https://bandit.readthedocs.io/
3. MITRE CWE-78 — OS Command Injection: https://cwe.mitre.org/data/definitions/78.html
4. Goodfellow, I. J., Shlens, J., and Szegedy, C. "Explaining and Harnessing Adversarial Examples." 2015. https://arxiv.org/abs/1412.6572
5. LINDDUN Privacy Threat Modeling: https://linddun.org/
