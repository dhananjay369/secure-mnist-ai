# Secure AI Systems: Red and Blue Teaming an MNIST Classifier

**Name:** Dhananjay Kumar (Team Member1)

**Roll Number:** CS26MTECH13007


**Name:** Satyam Singh (Team Member2)

**Roll Number:** CS26MTECH13005

---

## 1. Introduction

Artificial Intelligence and Machine Learning systems can be vulnerable to attacks that manipulate their inputs, corrupt training data, or compromise model integrity. High accuracy on clean data does not guarantee that a model will behave correctly under malicious conditions.

The objective of this project is to develop a Convolutional Neural Network (CNN) for handwritten digit classification using the MNIST dataset, evaluate its performance, identify security risks, conduct red-team attacks, and implement blue-team defenses.

The project applies STRIDE threat modeling, LINDDUN privacy analysis, the OWASP Machine Learning Security Top 10, and Static Application Security Testing (SAST).

The experiments include the Fast Gradient Sign Method (FGSM) adversarial attack and label-flipping data poisoning. The defensive implementation uses adversarial training and input validation.

## 2. Project Repositories

### 2.1 CNN Implementation

**GitHub repository:**

https://github.com/dhananjay369/secure-mnist-ai

The repository contains the CNN implementation, training and evaluation code, and associated project artifacts.

### 2.2 Red-Team and Blue-Team Implementation

**GitHub repository:**

https://github.com/dhananjay369/secure-mnist-ai-attacks

This repository is associated with attack generation, label-flipping poisoning, FGSM evaluation, and adversarial defense experiments.

## 3. Model Training and Classification Performance (10%)

### 3.1 Dataset

The project uses the MNIST handwritten digit dataset, which contains grayscale images of handwritten digits from 0 to 9.

| Dataset property | Value |
|---|---|
| Training images | 60,000 |
| Test images | 10,000 |
| Image dimensions | 28 × 28 pixels |
| Number of classes | 10 |
| Input channels | 1 |
| Framework | PyTorch |

The pixel values are normalized to the range [0, 1] for model processing.

### 3.2 CNN Architecture

The model uses a Convolutional Neural Network implemented in PyTorch.

The architecture consists of:

1. A convolutional layer with 32 output channels, followed by ReLU activation and max-pooling.
2. A convolutional layer with 64 output channels, followed by ReLU activation and max-pooling.
3. A flatten layer that converts the extracted features into a one-dimensional representation.
4. A fully connected layer with 128 neurons and ReLU activation.
5. A dropout layer with probability 0.2.
6. An output layer with 10 logits corresponding to digits 0 through 9.

The model learns spatial features from handwritten digit images and uses these features to predict the corresponding digit class.

### 3.3 Main Source Files

| File | Purpose |
|---|---|
| `src/model.py` | CNN architecture |
| `src/train.py` | Model training |
| `src/evaluate.py` | Evaluation on clean test data |
| `src/utils.py` | Supporting utilities |
| `attacks/fgsm_attack.py` | FGSM attack experiment |
| `attacks/poisoning_attack.py` | Data poisoning experiment |
| `attacks/evaluate_poisoning.py` | Evaluation of the poisoned model |
| `attacks/test_defense.py` | Baseline and defense comparison |
| `defense/adversarial_training.py` | Adversarial training |
| `defense/input_validation.py` | Input validation |
| `security/sast_before.py` | Intentionally vulnerable SAST example |
| `security/sast_fixed.py` | Fixed SAST demonstration |

### 3.4 Baseline Performance Metrics

The baseline model was evaluated on the clean MNIST test dataset.

| Metric | Baseline result |
|---|---:|
| Test dataset size | 10,000 images |
| Correct predictions | 9,882 |
| Incorrect predictions | 118 |
| Test accuracy | 98.82% |
| Evaluation loss | 0.03282 |
| Recorded total inference time | Approximately 0.89 seconds |
| Average inference time per image | Approximately 0.089 milliseconds |

The accuracy is calculated as:

Accuracy = (Number of correct predictions / Total number of test images) × 100

Accuracy = (9,882 / 10,000) × 100 = 98.82%

The model achieved high accuracy on clean images, establishing the baseline for the security experiments.

Inference time depends on the hardware, software environment, and system load.

### 3.5 Confusion Matrix

The confusion matrix compares the actual digit classes with the classes predicted by the baseline CNN.

![Baseline MNIST Confusion Matrix](https://raw.githubusercontent.com/dhananjay369/secure-mnist-ai/main/results/baseline_confusion_matrix.png)

Rows represent the true digit classes, while columns represent the predicted digit classes. Values along the main diagonal represent correct predictions. Values outside the diagonal represent misclassifications.

The diagonal entries sum to 9,882 correct predictions out of 10,000 test images, corresponding to 98.82% accuracy.

The confusion matrix shows that the model correctly classifies most test images, although a small number of images are assigned to incorrect digit classes.

## 4. Threat Modeling (20%)

### 4.1 System Overview

The application receives a 28 × 28 grayscale image, processes it through the trained CNN, and returns a predicted digit from 0 to 9.

The main assets requiring protection are:

- Integrity of the training data and labels.
- Integrity and confidentiality of model files.
- Correctness of model predictions.
- Availability of the classification application.
- Security of dependencies and training code.
- Integrity of experimental results.

### 4.2 Attacker Model

This project considers two main attackers.

#### A. Adversarial Example Attacker

The attacker modifies the pixel values of an input image to cause the model to predict an incorrect digit.

For the FGSM experiment, the attacker has access to the model gradients. This represents a white-box attack.

The attack uses epsilon = 0.2 and evaluates 5,000 samples in the recorded experiment.

The attacker's objective is to reduce classification accuracy by introducing adversarial perturbations.

#### B. Data Poisoning Attacker

The attacker modifies a portion of the training labels to influence the model's behavior.

The experiment uses the following configuration:

| Parameter | Value |
|---|---|
| Attack type | Label flipping |
| Poisoning fraction | 5% |
| Source digit | 7 |
| Target digit | 1 |
| Random seed | 42 |
| Recorded poisoned samples | 313 |

The objective is to investigate whether training with incorrectly labeled samples increases the number of genuine digit-7 images classified as digit 1.

This experiment is a label-flipping attack. It is not a trigger-based backdoor attack.

### 4.3 Attacker Capabilities and Limitations

The attacker is assumed to have the ability to craft input images or manipulate a portion of the training labels, depending on the attack scenario.

The experiments do not assume unrestricted administrative access to the application.

The results evaluate specific attacks under controlled conditions. They do not prove that the model is secure against every possible attack.

### 4.4 STRIDE Threat Analysis

STRIDE identifies six categories of security threats.

| STRIDE category | Potential threat | Example in the MNIST application | Mitigation |
|---|---|---|---|
| Spoofing | An attacker pretends to be a trusted source. | An untrusted dataset is presented as an approved training dataset. | Verify dataset provenance and restrict access. |
| Tampering | Data or model parameters are modified. | Training labels are changed to poison the model. | Validate labels, protect model files, and track dataset versions. |
| Repudiation | Actions cannot be traced reliably. | Unauthorized changes to training data are not recorded. | Maintain audit logs and experiment records. |
| Information Disclosure | Sensitive information is exposed. | Model artifacts or data files are accessed without authorization. | Restrict access and minimize sensitive data storage. |
| Denial of Service | The system becomes unavailable. | Excessive or malformed inputs consume resources. | Validate inputs and apply resource limits. |
| Elevation of Privilege | An attacker gains unauthorized permissions. | Unsafe command execution is exploited. | Avoid unsafe shell execution and follow least privilege. |

### 4.5 Mapping to the OWASP Machine Learning Security Top 10

The OWASP Machine Learning Security Top 10 identifies risks specific to machine learning systems. The following mapping identifies the risks relevant to the implemented experiments and the potential risks that were not tested.

| OWASP ML risk | Description | Relevance to this project | Mitigation or limitation |
|---|---|---|---|
| ML01:2023 Input Manipulation Attack | Malicious inputs cause incorrect model behavior. | Directly tested using FGSM adversarial examples. | Adversarial training and input validation. |
| ML02:2023 Data Poisoning Attack | Training data is manipulated to influence model behavior. | Directly tested using label flipping. | Data validation, label verification, and controlled dataset access. |
| ML03:2023 Model Inversion Attack | Model outputs may reveal information about training data. | Not tested. | Assess privacy leakage and limit unnecessary access to model outputs. |
| ML04:2023 Membership Inference | An attacker attempts to determine whether a sample was in the training set. | Not tested. | Evaluate membership inference risk and avoid unnecessary exposure of model information. |
| ML05:2023 Model Theft | An attacker attempts to replicate or extract a model. | Not tested. | Restrict model access and monitor excessive querying. |
| ML06:2023 AI Supply Chain Attacks | Dependencies, datasets, or model components are compromised. | Relevant to the security of project dependencies and downloaded datasets. | Verify sources, pin dependencies, and scan packages. |
| ML07:2023 Transfer Learning Attack | Attacks exploit risks associated with transferred model knowledge. | Not directly applicable to the current model because the project trains a CNN from scratch. | Review pretrained components if transfer learning is introduced. |
| ML08:2023 Model Skewing | Training or input distributions are manipulated to bias behavior. | Related to the potential impact of corrupted training labels; not separately evaluated. | Monitor data distributions and evaluate performance across classes. |
| ML09:2023 Output Integrity Attack | An attacker manipulates or undermines the integrity of model outputs. | Relevant to adversarial misclassification and incorrect predictions. | Test prediction robustness and protect the inference pipeline. |
| ML10:2023 Model Poisoning | The model itself or its parameters are maliciously altered. | Direct model-parameter poisoning was not tested. | Protect model artifacts, control training access, and verify model integrity. |

The implemented attacks directly evaluate input manipulation and data poisoning. The remaining entries identify relevant or potential risks; they should not be interpreted as attacks successfully performed in this project.

The mapping follows the OWASP Machine Learning Security Top 10 project. The OWASP list is a separate ML security taxonomy, not the OWASP Top 10 for Large Language Model applications.

Reference: https://owasp.org/projects/machine-learning-security-top-ten

### 4.6 LINDDUN Privacy Threat Analysis

LINDDUN is used to identify privacy threats that may apply to a real-world version of the application.

| LINDDUN category | Potential privacy threat | Possible mitigation |
|---|---|---|
| Linkability | Records may be linked across datasets or sessions. | Minimize identifiers and separate datasets where appropriate. |
| Identifiability | Data may reveal information about an individual. | Avoid unnecessary personal information and assess anonymization. |
| Non-repudiation | Logs may link actions to specific users. | Limit the collection and retention of identifying logs. |
| Detectability | An attacker may infer whether particular information is present. | Restrict access to datasets and sensitive model outputs. |
| Disclosure of Information | Training data or model artifacts may expose sensitive information. | Apply access controls and assess privacy leakage. |
| Unawareness | Users may not understand how their data is processed. | Document data collection and processing practices. |
| Non-compliance | Data handling may violate applicable requirements. | Follow applicable privacy policies and data-protection obligations. |

The MNIST dataset contains handwritten digits rather than a comprehensive set of personal records. However, a real-world system could process personal images or other sensitive data.

The LINDDUN analysis identifies potential risks. It does not establish that a privacy breach occurred during these experiments.

## 5. Static Application Security Testing (SAST) and Fixes (20%)

### 5.1 SAST Tool

Bandit was used to scan Python code for potentially insecure patterns.

**Scan command:**

`python -m bandit -r src attacks defense security`

Bandit is a static analysis tool that identifies suspicious coding patterns. Its findings require interpretation and do not automatically prove that a vulnerability is exploitable.

### 5.2 Findings

The recorded scan identified two findings in the intentionally vulnerable demonstration file, `security/sast_before.py`.

| Finding | Severity | Description | Associated weakness |
|---|---|---|---|
| B404 | Low | Subprocess module usage requires review. | Subprocess security considerations |
| B602 | High | Shell execution with `shell=True` can introduce command-injection risk when input is not handled safely. | CWE-78 |

B404 is a warning associated with subprocess usage. Importing the module alone does not prove that the code is vulnerable.

B602 identifies a potentially dangerous shell-execution pattern. If attacker-controlled input is interpreted by the shell, an attacker may be able to alter the executed command.

### 5.3 Vulnerable Pattern and Fix

The vulnerable demonstration used shell execution with a string containing user-controlled input.

The fix in `security/sast_fixed.py` removes the unsafe shell-execution pattern. The fixed demonstration validates that the input is a string and prints it directly instead of passing it to a shell command.

This avoids the specific command-injection pattern in the demonstration.

### 5.4 Retesting the Fix

The isolated Bandit scan of `security/sast_fixed.py` reported no issues.

The full-project scan still reported findings in `security/sast_before.py`, because that file intentionally retains the vulnerable example for demonstration.

Therefore, the isolated result for the fixed file and the full-project result are different and must be interpreted separately.

### 5.5 Input Validation

The project implements input validation in `defense/input_validation.py`.

The validation checks include:

- Input must be a PyTorch tensor.
- Input shape must be `(N, 1, 28, 28)`.
- The batch must not be empty.
- Input values must use a floating-point data type.
- Input values must be finite; NaN and infinity are rejected.
- Pixel values must be within the range [0, 1].

The recorded validation tests passed eight test cases covering valid input, invalid shape, empty batch, NaN, out-of-range values, integer input, and non-tensor input.

Input validation protects against malformed inputs. It does not prevent every adversarial image because a malicious image may still satisfy all expected shape and pixel-range requirements.

## 6. Red-Team Attack 1: FGSM Adversarial Examples (25%)

### 6.1 Attack Description

The Fast Gradient Sign Method (FGSM) creates adversarial examples by perturbing input pixels in the direction determined by the sign of the gradient of the model loss.

The perturbation magnitude is controlled by epsilon.

The FGSM experiment uses epsilon = 0.2 and evaluates 5,000 samples.

### 6.2 OWASP Risk Mapping

This attack exercises:

- **ML01:2023 Input Manipulation Attack:** The attacker deliberately modifies the model input to cause incorrect predictions.
- **ML09:2023 Output Integrity Attack:** The attack can undermine the integrity of the classification result.

FGSM was selected because it is a simple, established gradient-based attack that can demonstrate how a model with high clean accuracy may perform poorly on adversarial inputs.

### 6.3 FGSM Results

| Metric | Result |
|---|---:|
| Clean accuracy | 98.26% |
| Adversarial accuracy | 45.12% |
| Prediction change rate | 53.28% |
| Attack success rate on initially correct predictions | 54.08% |
| Epsilon | 0.2 |
| Evaluated samples | 5,000 |

The accuracy decreased from 98.26% on clean images to 45.12% on adversarial images in this recorded experiment.

The prediction change rate measures the proportion of predictions that changed after perturbation.

The attack success rate is measured among samples that were initially classified correctly. It is therefore different from the overall prediction change rate.

These results demonstrate vulnerability to the tested FGSM configuration, not universal vulnerability to all adversarial attacks.

## 7. Red-Team Attack 2: Data Poisoning (25%)

### 7.1 Attack Description

The data poisoning experiment changes a portion of training labels to investigate whether corrupted training data affects model predictions.

The experiment uses the following parameters:

| Parameter | Value |
|---|---|
| Attack type | Label flipping |
| Poisoning fraction | 5% |
| Source digit | 7 |
| Target digit | 1 |
| Random seed | 42 |
| Recorded poisoned samples | 313 |

The intended objective is to increase the number of genuine digit-7 images classified as digit 1.

### 7.2 OWASP Risk Mapping

This attack exercises **ML02:2023 Data Poisoning Attack** because training labels are deliberately manipulated before training.

The experiment is relevant to ML08, Model Skewing, as a potential consequence of biased or corrupted training data. However, a separate model-skewing attack was not implemented.

This experiment is not a trigger-based backdoor attack because it does not introduce a trigger pattern into the images.

### 7.3 Data Poisoning Results

| Metric | Baseline Model | Poisoned Model |
|---|---:|---:|
| Clean accuracy | 98.82% | 98.87% |
| Accuracy on digit 7 | 98.35% | 98.44% |
| Actual digit-7 images predicted as digit 1 | 0 | 8 |
| Number of actual digit-7 test images | 1,028 | 1,028 |

The poisoned model achieved 98.87% clean accuracy compared with 98.82% for the baseline model.

The number of genuine digit-7 images classified as digit 1 increased from 0 to 8.

The observed change is small. The results do not establish a strong or reliably reproducible targeted poisoning effect. Additional controlled experiments would be needed to assess its consistency and statistical significance.

### 7.4 Red-Team Summary

| Attack | OWASP ML risk | Observed result |
|---|---|---|
| FGSM | ML01: Input Manipulation Attack | Adversarial accuracy decreased substantially. |
| Label flipping | ML02: Data Poisoning Attack | A small increase in digit-7-to-digit-1 errors was observed. |

The two attacks evaluate different security weaknesses. FGSM manipulates inputs during inference, while label flipping corrupts labels in the training dataset.

## 8. Blue-Team Defense and Performance Comparison (25%)

### 8.1 Defense Strategy

The blue-team implementation uses two defensive measures.

**1. Adversarial Training**

Adversarial training exposes the model to adversarial examples during training. The aim is to improve its ability to classify perturbed inputs.

The recorded configuration uses epsilon = 0.2 and 10,000 adversarial-training samples.

**2. Input Validation**

Input validation checks the data type, shape, batch size, finite values, and pixel range before model processing.

Input validation prevents malformed input from reaching the model, while adversarial training aims to improve robustness against valid but adversarially perturbed images.

These defenses address different problems and should not be treated as interchangeable.

### 8.2 Baseline Versus Defended Model

The following results were recorded using the same evaluation samples for the baseline and defended models.

| Metric | Baseline Model | Defended Model |
|---|---:|---:|
| Clean accuracy | 98.82% | 98.25% |
| FGSM adversarial accuracy | 50.23% | 96.51% |

### 8.3 Performance Improvement

| Metric | Change |
|---|---:|
| Clean accuracy | -0.57 percentage points |
| FGSM adversarial accuracy | +46.28 percentage points |

The defended model's clean accuracy decreased from 98.82% to 98.25%, a reduction of approximately 0.57 percentage points.

FGSM adversarial accuracy increased from 50.23% to 96.51%, an improvement of 46.28 percentage points.

The results indicate that adversarial training substantially improved the model's performance against the tested FGSM configuration, with a small reduction in clean accuracy.

### 8.4 Distinguishing the Two FGSM Experiments

Two FGSM result sets are reported.

The first experiment evaluated 5,000 samples and reported 98.26% clean accuracy and 45.12% adversarial accuracy.

The second experiment compared baseline and defended models on the same evaluation samples and reported:

- Baseline clean accuracy: 98.82%.
- Baseline FGSM accuracy: 50.23%.
- Defended clean accuracy: 98.25%.
- Defended FGSM accuracy: 96.51%.

These results come from different recorded evaluation runs and should not be combined as if they were one experiment.

### 8.5 Overall Security Comparison

| Security aspect | Baseline | Blue-team implementation |
|---|---|---|
| Clean classification | 98.82% in the recorded baseline evaluation | 98.25% in the same-sample defense comparison |
| FGSM robustness | 50.23% adversarial accuracy in the same-sample comparison | 96.51% adversarial accuracy |
| Malformed input handling | Depends on the input checks applied | Explicit input validation |
| SAST demonstration | Contains an intentionally vulnerable example | Fixed demonstration avoids shell execution |
| General security | Not guaranteed against attacks | Improved protection against tested conditions, but not complete security |

The results demonstrate that adversarial training can improve robustness against a specific attack. They do not prove that the defended model is robust against all attacks, perturbation strengths, or poisoning strategies.

## 9. Conclusion and Observations

This project evaluated a CNN-based MNIST classifier through model training, threat modeling, static application security testing, adversarial example generation, data poisoning, and defensive evaluation.

The baseline CNN achieved 98.82% accuracy on clean MNIST test data. The confusion matrix confirms that 9,882 of the 10,000 test images were classified correctly.

The FGSM experiment showed that adversarial perturbations can substantially reduce classification accuracy. In the separate 5,000-sample experiment, adversarial accuracy was 45.12%, compared with 98.26% clean accuracy.

The label-flipping experiment produced a small increase in digit-7 images classified as digit 1. The result is limited and does not establish a strong or reliably reproducible targeted poisoning effect.

STRIDE threat modeling identified potential threats to data integrity, model security, availability, and access control. The OWASP Machine Learning Security Top 10 mapping connected the implemented attacks to input manipulation and data poisoning, while identifying additional risks that were not tested. LINDDUN was used to discuss potential privacy risks in a real-world version of the application.

Bandit identified an unsafe shell-execution pattern in the intentionally vulnerable demonstration. The fixed demonstration avoided shell execution and passed its isolated scan. Input validation tests also passed the eight recorded test cases.

The blue-team implementation combined input validation with adversarial training. In the same-sample defense comparison, FGSM adversarial accuracy increased from 50.23% to 96.51%, while clean accuracy decreased from 98.82% to 98.25%.

The project demonstrates that high accuracy on clean data alone is insufficient to establish the security of an AI system. Secure AI development requires threat modeling, testing against multiple attacks, secure coding practices, data integrity controls, and evaluation of defensive measures.

The results are limited to the model, dataset, attack configurations, and experimental environment used in this project. They should not be interpreted as proof of complete security or universal adversarial robustness.

## 10. References

1. OWASP Machine Learning Security Top 10: https://owasp.org/projects/machine-learning-security-top-ten
2. OWASP Machine Learning Security Top 10 project documentation: https://owasp.github.io/www-project-machine-learning-security-top-10/
3. PyTorch documentation: https://pytorch.org/docs/stable/index.html
4. Bandit documentation: https://bandit.readthedocs.io/
5. CNN implementation repository: https://github.com/dhananjay369/secure-mnist-ai
6. Attack and defense repository: https://github.com/dhananjay369/secure-mnist-ai-attacks