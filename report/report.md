
# Secure AI Systems: Red and Blue Teaming an MNIST Classifier

**Name:** Dhananjay Kumar
**Roll Number:** CS26MTECH13007

---

## 1. GitHub Repository of CNN Implementation for Image Classification

The CNN implementation for handwritten digit classification using the MNIST dataset is available in the following GitHub repository.

**CNN Implementation Repository:**
https://github.com/dhananjay369/secure-mnist-ai

The project uses a Convolutional Neural Network (CNN) to classify grayscale handwritten digit images into ten classes, from 0 to 9.

### Main Implementation Files

- `src/model.py` — CNN architecture and input validation.
- `src/train.py` — model training.
- `src/evaluate.py` — evaluation on the MNIST test dataset.
- `src/utils.py` — supporting utilities.
- `run_all.py` — project workflow.

The CNN consists of two convolutional layers followed by ReLU activation and max-pooling operations. The extracted features are passed through fully connected layers to produce ten output logits, one for each digit class.

The MNIST dataset is used for training and evaluation. Dataset files are not included in the repository; they must be downloaded or made available locally according to the project setup.

## 2. Performance Metrics of Classification

The baseline CNN was evaluated on the clean MNIST test dataset.

| Metric | Baseline CNN |
|---|---:|
| Clean test accuracy | 98.82% |
| Evaluation loss | 0.03282 |
| Total test images | 10,000 |
| Inference time | 0.8904 seconds |
| Average inference time per image | 0.0890 milliseconds |

The model achieved 98.82% classification accuracy on clean test data. This result serves as the baseline for comparing performance under adversarial attacks and defensive techniques.

The inference time is specific to the recorded execution environment and may vary depending on hardware and system load.

## 3. Threat Model of the Implementation

### 3.1 System Overview

The system accepts handwritten digit images and uses a trained CNN to predict their corresponding digit classes.

The main assets are:

- Training and test images.
- Training labels and their integrity.
- Trained model parameters and saved model files.
- Prediction accuracy and availability.
- Experiment results and evaluation code.

### 3.2 Attacker Model

This project considers two principal attack scenarios.

#### A. Adversarial Example Attacker

The attacker modifies input images to cause the CNN to predict an incorrect class.

The Fast Gradient Sign Method (FGSM) is used to generate adversarial examples. The recorded evaluation uses an epsilon value of 0.2 and evaluates 5,000 samples.

In this experimental setting, the attacker can use model gradients to construct perturbations. The attack demonstrates the potential effect of adversarial inputs on classification accuracy.

#### B. Data Poisoning Attacker

The attacker modifies a portion of the training labels to influence model predictions.

The implemented experiment targets a mapping from digit 7 to digit 1. The recorded configuration uses a 5% fraction of the source class and 313 poisoned samples.

The intended goal is to increase the number of genuine digit-7 images classified as digit 1 after training on the poisoned dataset.

This is a label-flipping experiment. It should not be confused with a trigger-based backdoor attack.

### 3.3 STRIDE Threat Analysis

STRIDE is used to identify potential security threats involving spoofing, tampering, repudiation, information disclosure, denial of service, and elevation of privilege.

| STRIDE Category | Potential Threat | Security Consideration |
|---|---|---|
| Spoofing | An attacker may submit inputs intended to be mistaken for another digit. | Validate inputs and evaluate adversarial robustness. |
| Tampering | Training images, labels, or saved model files may be modified. | Protect datasets, labels, and model files. |
| Repudiation | Missing audit records may make changes difficult to trace. | Maintain appropriate logs and experiment records. |
| Information Disclosure | Stored images, logs, or outputs may expose information in some deployment settings. | Minimize sensitive data collection and restrict access. |
| Denial of Service | Excessive requests may affect system availability. | Apply resource limits and request controls in deployment. |
| Elevation of Privilege | Weak access controls may allow unauthorized changes to models or datasets. | Restrict permissions for model and dataset management. |

These are potential threats identified through threat modeling. They are not claims that every threat was successfully exploited in this project.

### 3.4 LINDDUN Privacy Notes

LINDDUN is a privacy threat-modeling framework used to identify potential privacy risks.

| LINDDUN Category | Potential Privacy Concern |
|---|---|
| Linkability | Multiple records may be linked to the same user through identifiers or logs. |
| Identifiability | Metadata associated with images may identify an individual. |
| Non-repudiation | Detailed logs may make user actions traceable. |
| Detectability | An observer may infer whether a particular input was processed. |
| Disclosure of Information | Stored inputs, logs, or outputs may expose sensitive information. |
| Unawareness | Users may not know whether their inputs or predictions are stored. |
| Non-compliance | Data collection or retention may violate applicable privacy requirements if not handled appropriately. |

MNIST is a public benchmark dataset. These notes describe possible privacy risks in a deployed system and do not establish that a privacy breach occurred during this experiment.

## 4. SAST Findings and Fixes

### 4.1 Tool and Scan Scope

Bandit was used to perform Static Application Security Testing (SAST) on the Python code.

The latest scan command was:

```bash
python -m bandit -r src attacks defense security
```

The scan covered the following directories:

- `src/`
- `attacks/`
- `defense/`
- `security/`

Bandit reported that 553 lines of Python code were scanned.

The latest scan reported five findings: one High-severity finding and four Low-severity findings. No Medium-severity findings were reported.

### 4.2 Vulnerable Code Before the Fix

The file `security/sast_before.py` contains an intentionally vulnerable demonstration:

```python
import subprocess

def run_demo(user_value):
    return subprocess.run(
        'echo ' + user_value,
        shell=True,
        capture_output=True,
        text=True
    )
```

This implementation constructs a shell command using an input value and executes it with `shell=True`.

If untrusted input is supplied, shell metacharacters may alter the command being executed. This creates a potential command-injection vulnerability.

The relevant findings were:

| Bandit Rule | Severity | Description |
|---|---|---|
| B404 | Low | Import of the subprocess module requires security review. |
| B602 | High | A subprocess call uses `shell=True`, creating a potential command-injection risk. |

The B602 finding is associated with CWE-78, OS Command Injection.

### 4.3 Fix Applied

The revised implementation passes the command and input as separate arguments and disables shell interpretation.

**Revised code in `security/sast_fixed.py`:**

```python
import subprocess

def run_demo(user_value):
    return subprocess.run(
        ['echo', user_value],
        shell=False,
        capture_output=True,
        text=True,
        check=True
    )
```

This change avoids passing the input through a shell command string, reducing the specific command-injection risk present in the vulnerable demonstration.

The following command was used to test the revised function:

```bash
python -c "from security.sast_fixed import run_demo; r=run_demo('hello'); print(r.stdout.strip())"
```

The observed output was:

```text
hello
```

This confirms that the revised function worked for the tested input. It is not a complete proof of security.

### 4.4 Latest Full-Directory Scan Results

The latest Bandit scan reported the following findings.

| Bandit Rule | Severity | Location | Description |
|---|---|---|---|
| B404 | Low | `security/sast_before.py:1` | Subprocess module import. |
| B602 | High | `security/sast_before.py:3` | Subprocess call using `shell=True`. |
| B404 | Low | `security/sast_fixed.py:1` | Subprocess module import. |
| B607 | Low | `security/sast_fixed.py:3` | Partial executable path is used. |
| B603 | Low | `security/sast_fixed.py:3` | Subprocess call requires review. |

**Summary of the latest scan:**

| Severity | Number of Findings |
|---|---:|
| High | 1 |
| Medium | 0 |
| Low | 4 |
| Total | 5 |

The High-severity finding remains in `security/sast_before.py`, which is intentionally retained as the vulnerable before-fix example. Therefore, the full-directory scan does not show that all High-severity findings have been eliminated.

The revised file uses an argument list and `shell=False`, but Bandit still reports Low-severity findings that require contextual review. These findings do not automatically prove that the revised function is exploitable.

### 4.5 Dependency Check

The following command was executed:

```bash
python -m pip check
```

Observed output:

```text
No broken requirements found.
```

This indicates that the installed packages had no broken dependency requirements at the time of the check. It does not establish that all dependencies are free from known security vulnerabilities.

## 5. Repository of Attack Code and Adversarial/Poisoned Dataset Experiments

The attack and defense code is maintained in a separate repository.

**Attack and Defense Repository:**
https://github.com/dhananjay369/secure-mnist-ai-attacks

**CNN Implementation Repository:**
https://github.com/dhananjay369/secure-mnist-ai

The attack repository contains the code used for generating and evaluating attacks, training with poisoned data, and testing defensive mechanisms.

### Main Attack and Defense Files

- `attacks/fgsm_attack.py` — FGSM adversarial attack.
- `attacks/poisoning_attack.py` — data poisoning attack.
- `attacks/poisoned_train.py` — training with poisoned data.
- `attacks/evaluate_poisoning.py` — evaluation of poisoning results.
- `attacks/test_defense.py` — comparison of baseline and defended models on FGSM examples.
- `attacks/test_input_validation.py` — input-validation tests.
- `defense/adversarial_training.py` — adversarial-training defense.
- `defense/input_validation.py` — input-validation defense.

The MNIST dataset must be downloaded or made available locally before running the experiments. The repository links above identify the projects; the files and their paths should be checked against the current repository contents.

## 6. Performance Metrics with Adversarial and Poisoned Data

### 6.1 FGSM Adversarial Attack

The FGSM evaluation used epsilon = 0.2 and 5,000 samples.

| Metric | Result |
|---|---:|
| Clean accuracy in this evaluation | 98.26% |
| Accuracy on adversarial examples | 45.12% |
| Prediction change rate | 53.28% |
| Attack success rate on initially correct clean predictions | 54.08% |

The results show that the FGSM perturbations substantially reduced classification accuracy in this evaluation.

The prediction change rate is the fraction of evaluated samples whose predictions changed after perturbation. The attack success rate on initially correct clean predictions measures the fraction of initially correct predictions that became incorrect under the attack.

The clean accuracy in this table comes from a separate FGSM evaluation run and should not be confused with the baseline accuracy reported in Section 2.

### 6.2 Data Poisoning Experiment

The data poisoning experiment targeted the mapping from digit 7 to digit 1. The recorded configuration used a 5% fraction of the source class and 313 poisoned samples.

The latest evaluation reported the following results.

| Metric | Baseline Model | Poisoned Model |
|---|---:|---:|
| Clean test accuracy | 98.82% | 98.87% |
| Class-7 accuracy | 98.35% | 98.44% |
| Actual digit-7 samples predicted as digit 1 | 0 | 8 |
| Total actual digit-7 test samples | 1,028 | 1,028 |

The poisoned model classified 8 out of 1,028 actual digit-7 test samples as digit 1, compared with zero such predictions by the baseline model. This is approximately 0.78% of the tested digit-7 samples.

The observed result is consistent with the intended targeted effect, but it does not independently establish that poisoning caused the misclassifications. Repeated runs, controlled comparisons, and additional evaluation are needed to assess the reliability and cause of this change.

The experiment uses label flipping. It does not establish the behavior of a trigger-based backdoor attack.

## 7. Blue-Team Implementation and Performance Compared with Baseline

Two defensive controls are considered: adversarial training and input validation.

### 7.1 Defense 1: Adversarial Training

Adversarial training attempts to improve robustness by training the model using adversarial examples.

**Implementation file:** `defense/adversarial_training.py`

The recorded configuration uses:

- Adversarial-training epsilon: 0.2.
- Adversarial-training samples: 10,000.

The goal is to reduce the model's sensitivity to the tested adversarial perturbations.

### 7.2 Baseline and Defended Model Comparison

The following results were obtained using the same FGSM samples in the comparison script.

| Metric | Baseline Model | Defended Model |
|---|---:|---:|
| Clean accuracy | 98.82% | 98.25% |
| FGSM adversarial accuracy | 50.23% | 96.51% |

The improvement in FGSM adversarial accuracy was:

96.51% - 50.23% = **46.28 percentage points**.

The change in clean accuracy was:

98.25% - 98.82% = **-0.57 percentage points**.

The defended model showed substantially higher accuracy on the tested FGSM examples, with a small reduction in clean accuracy.

These results apply to the tested attack configuration. They do not prove robustness against all adversarial attacks, perturbation strengths, or distribution shifts.

### 7.3 Observations from Adversarial Training

- FGSM substantially reduced baseline accuracy on adversarial examples.
- Adversarial training improved accuracy on the tested FGSM examples.
- The defended model retained slightly lower clean accuracy than the baseline.
- Additional attacks and evaluation settings are needed to assess broader robustness.

### 7.4 Defense 2: Input Validation

An additional defensive control was implemented to reject malformed MNIST inputs before classification.

**Implementation files:**

- `defense/input_validation.py`
- `src/model.py`
- `attacks/test_input_validation.py`

The validation function checks that:

- The input is a PyTorch tensor.
- The input shape is `(N, 1, 28, 28)`.
- The batch is not empty.
- The input has a floating-point data type.
- Pixel values are finite and do not contain NaN or Inf.
- Pixel values lie within the permitted range `[0, 1]`.

The validation function is integrated into `MNISTCNN.forward()`, so the checks run before feature extraction and classification.

**Unit test results**

Eight input-validation test cases were executed.

| Test Case | Expected Behavior | Result |
|---|---|---|
| Valid MNIST batch | Accept input | Passed |
| Incorrect image shape | Reject input | Passed |
| Empty batch | Reject input | Passed |
| NaN pixel | Reject input | Passed |
| Pixel below zero | Reject input | Passed |
| Pixel above one | Reject input | Passed |
| Integer input | Reject input | Passed |
| Non-tensor input | Reject input | Passed |

**Total: 8/8 unit tests passed.**

**Integration test results**

A valid input tensor with shape `(1, 1, 28, 28)` produced an output tensor with shape `(1, 10)`, corresponding to the ten MNIST digit classes.

An input tensor with shape `(1, 28, 28)` was rejected with a `ValueError` before classification.

These tests confirm the expected behavior for the tested valid and malformed inputs.

**Limitation:** Input validation does not guarantee adversarial robustness. An adversarial image can have the correct shape, finite values, and pixel values within `[0, 1]`. Therefore, input validation complements adversarial training rather than replacing it.

## 8. Conclusion and Observations

This project evaluated a CNN for MNIST handwritten digit classification through a red-team/blue-team workflow.

The baseline CNN achieved 98.82% accuracy on clean test data, with an evaluation loss of approximately 0.03282.

The FGSM experiment demonstrated that adversarial perturbations can substantially reduce classification performance. In the same-sample comparison, adversarial training increased FGSM accuracy from 50.23% to 96.51%, an improvement of 46.28 percentage points. Clean accuracy decreased from 98.82% to 98.25%.

The data poisoning experiment targeted digit-7-to-digit-1 misclassification using 313 poisoned samples. The latest evaluation observed eight such misclassifications among 1,028 actual digit-7 samples in the poisoned model, compared with zero in the baseline model. Further controlled experiments and repeated runs are needed to establish the reliability and cause of this observation.

Input validation was added as a complementary defensive control. All eight unit tests passed, and integration tests confirmed that a valid input produced ten class logits while a malformed image shape was rejected.

Bandit identified a High-severity `shell=True` pattern in the intentionally vulnerable demonstration file. The revised demonstration uses `shell=False` and an argument list, and its functional test returned the expected output. However, the latest full-directory scan still reported one High-severity and four Low-severity findings because the intentionally vulnerable before-fix file remains in the scanned directories.

The dependency check reported no broken requirements.

Overall, the project demonstrates CNN classification, adversarial attack evaluation, a label-flipping poisoning experiment, adversarial training, input validation, and static code analysis. The results are limited to the tested configurations. Future work should include repeated poisoning experiments, evaluation against additional attacks, review of remaining SAST warnings, and broader robustness testing.

## References

1. **MNIST Database of Handwritten Digits**
   http://yann.lecun.com/exdb/mnist/

2. **Bandit Documentation**
   https://bandit.readthedocs.io/

3. **MITRE CWE-78: OS Command Injection**
   https://cwe.mitre.org/data/definitions/78.html

4. Goodfellow, I. J., Shlens, J., and Szegedy, C. *Explaining and Harnessing Adversarial Examples*. 2015.
   https://arxiv.org/abs/1412.6572

5. **LINDDUN Privacy Threat Modeling**
   https://linddun.org/
