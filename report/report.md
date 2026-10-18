# Secure AI Systems: Red and Blue Teaming an MNIST Classifier

**Name:** Dhananjay Kumar

**Roll Number:** CS26MTECH13007


---

## 1. Model Training and Classification Performance (10%)

### 1.1 GitHub Repository

The CNN implementation for handwritten digit classification using the MNIST dataset is available at:

[Secure MNIST AI Repository](https://github.com/dhananjay369/secure-mnist-ai)

### 1.2 CNN Architecture

The project implements a Convolutional Neural Network (CNN) using PyTorch to classify grayscale handwritten digit images into ten classes, representing digits 0 to 9.

The CNN architecture consists of:

- First convolutional layer with 32 output channels, ReLU activation, and max-pooling.
- Second convolutional layer with 64 output channels, ReLU activation, and max-pooling.
- Flatten layer to convert extracted features into a one-dimensional representation.
- Fully connected layer with 128 neurons.
- ReLU activation and dropout with a probability of 0.2.
- Output layer with 10 logits representing digits 0 to 9.

### 1.3 Main Implementation Files

- `src/model.py` — CNN architecture.
- `src/train.py` — model training.
- `src/evaluate.py` — model evaluation.
- `src/utils.py` — supporting utilities.
- `run_all.py` — project workflow.

The MNIST dataset contains 60,000 training images and 10,000 test images. Dataset files are not included in the GitHub repository.

### 1.4 Baseline Classification Results

The baseline model was evaluated on clean MNIST test images.

| Metric | Baseline CNN |
|---|---:|
| Test dataset size | 10,000 images |
| Clean test accuracy | 98.82% |
| Evaluation loss | 0.03282 |
| Recorded total inference time | Approximately 0.89 seconds |
| Average inference time per image | Approximately 0.089 milliseconds |

The baseline model achieved 98.82% accuracy on clean test data. These results establish the reference point for evaluating adversarial attacks and defensive techniques.

Inference time may vary depending on hardware, software environment, and system load.

---

## 2. Threat Modeling (20%)

### 2.1 System Overview

The system accepts a grayscale handwritten digit image, processes it through a trained CNN, and predicts one of ten digit classes.

The main assets requiring protection are:

- Training images and labels.
- Integrity of the training dataset.
- Trained model parameters and model files.
- Input data and prediction results.
- Availability and reliability of the classification service.
- Experiment results and security evaluation code.

### 2.2 Attacker Model

This project considers two principal attack scenarios.

**A. Adversarial Example Attacker**

The attacker modifies an input image to cause the model to predict an incorrect class.

For the FGSM experiment, the attacker has access to model gradients needed to construct adversarial perturbations. This represents a white-box attack setting.

The attack uses an epsilon value of 0.2 and evaluates 5,000 samples.

The attacker's objective is to reduce classification accuracy without changing the intended semantic content of the image.

**B. Data Poisoning Attacker**

The attacker modifies a portion of the training labels to influence model predictions.

The implemented experiment uses the following configuration:

- Poisoning fraction: 5%.
- Source digit: 7.
- Target digit: 1.
- Random seed: 42.
- Recorded poisoned samples: 313.

The objective is to investigate whether poisoning training labels increases the number of genuine digit-7 images classified as digit 1.

This is a label-flipping experiment, not a trigger-based backdoor attack.

### 2.3 Attacker Capabilities and Assumptions

The experiments assume that the attacker can construct adversarial inputs or modify a portion of training labels, depending on the attack scenario.

The attacker is not assumed to have unrestricted administrative access to the deployed system.

The project evaluates specific attacks under controlled experimental conditions. It does not establish that every possible attack against the model or deployment environment has been tested.

### 2.4 STRIDE Threat Analysis

STRIDE is a threat-modeling framework used to identify six categories of security threats.

| STRIDE Category | Potential Threat | Example in This Project | Possible Mitigation |
|---|---|---|---|
| Spoofing | An attacker pretends to be a trusted source. | Untrusted images or datasets are presented as legitimate inputs. | Verify data sources and restrict access to trusted datasets. |
| Tampering | Data or model parameters are modified. | Training labels are changed during a poisoning experiment. | Verify dataset integrity and protect model files. |
| Repudiation | An action cannot be reliably traced to its source. | Unauthorized dataset or model changes are not recorded. | Maintain audit logs and record dataset and model versions. |
| Information Disclosure | Sensitive information is exposed. | Model artifacts or experiment files are accessed without authorization. | Apply access controls and minimize sensitive data storage. |
| Denial of Service | Legitimate requests cannot be processed. | Excessive or malformed inputs consume system resources. | Validate inputs and apply resource limits. |
| Elevation of Privilege | An attacker gains unauthorized permissions. | An insecure command-execution operation is exploited. | Avoid unsafe shell execution and follow least-privilege principles. |

### 2.5 LINDDUN Privacy Threat Analysis

LINDDUN is a privacy threat-modeling framework that identifies potential privacy risks.

| LINDDUN Category | Potential Privacy Threat | Possible Mitigation |
|---|---|---|
| Linkability | Records or images can be linked across datasets. | Minimize identifiers and separate datasets where appropriate. |
| Identifiability | An individual may be identified from exposed data. | Avoid unnecessary personal data and anonymize data where appropriate. |
| Non-repudiation | Actions can be linked to a particular user. | Limit the collection and retention of identifying logs. |
| Detectability | An attacker can infer whether particular data is present. | Restrict access to datasets and model outputs. |
| Disclosure of Information | Training data or model artifacts reveal sensitive information. | Apply access controls and evaluate model privacy risks. |
| Unawareness | Users do not understand how their data is used. | Document data collection and processing practices. |
| Non-compliance | Data handling violates applicable privacy requirements. | Follow applicable privacy policies and data-protection requirements. |

The MNIST experiments primarily evaluate classification security. The LINDDUN analysis identifies potential privacy risks; it does not establish that a privacy breach occurred in this project.

---

## 3. Static Application Security Testing (SAST) and Fixes (20%)

### 3.1 SAST Tool and Command

Bandit was used to identify potentially insecure Python code patterns.

**Tool:** Bandit

**Scan command:**

`python -m bandit -r src attacks defense security`

The scan examines Python source code for patterns associated with common security weaknesses.

### 3.2 Findings

The recorded scan reported two findings in the intentionally vulnerable demonstration file, `security/sast_before.py`.

| Finding ID | Severity | Description | File |
|---|---|---|---|
| B404 | Low | Importing the subprocess module requires review of how subprocess operations are used. | `security/sast_before.py` |
| B602 | High | Use of `shell=True` can introduce command-injection risk when input is not handled safely. | `security/sast_before.py` |

The B602 finding is associated with CWE-78, which concerns improper neutralization of special elements used in an operating system command.

The B404 finding is a warning about subprocess usage; importing the module alone does not prove that a vulnerability is exploitable.

### 3.3 Vulnerable Code Pattern

The vulnerable demonstration used shell execution with a string containing user-controlled input.

This pattern can be unsafe because shell metacharacters in the input may be interpreted as part of a command.

The demonstration was retained to show the security problem.

### 3.4 Fix Implemented

The fixed demonstration in `security/sast_fixed.py` avoids shell execution and prints the supplied string directly.

The fixed function performs a type check and then prints the input without passing it to a shell command.

### 3.5 Retesting the Fix

The isolated Bandit scan of `security/sast_fixed.py` reported no issues.

The full-project scan still reported the two findings in `security/sast_before.py`, because that file intentionally preserves the vulnerable example.

Therefore, the full-project findings and the isolated fixed-file result must be interpreted separately.

### 3.6 Input Validation as an Additional Defense

The project implements input validation in `defense/input_validation.py`.

The validation checks include:

- Input must be a PyTorch tensor.
- Input shape must be `(N, 1, 28, 28)`.
- The batch must not be empty.
- Input values must use a floating-point data type.
- Input values must be finite; NaN and infinity are rejected.
- Pixel values must lie within the range `[0, 1]`.

The recorded validation tests passed all eight test cases, including valid input, invalid shape, empty batch, NaN, out-of-range pixel values, integer input, and non-tensor input.

Input validation rejects malformed inputs but does not prevent adversarial images that satisfy the expected shape and pixel-range requirements.

---

## 4. Generation of Adversarial Dataset and Data Poisoning (25%)

### 4.1 Attack and Defense Repository

The attack and defense implementation is associated with the following repository:

[Secure MNIST AI Attacks Repository](https://github.com/dhananjay369/secure-mnist-ai-attacks)

The repository should contain the attack-generation and evaluation code required to reproduce the reported experiments. The repository URL and its contents should be verified before final submission.

### 4.2 Fast Gradient Sign Method (FGSM)

FGSM generates adversarial images by perturbing input pixels in the direction determined by the sign of the gradient of the model loss.

The perturbation is controlled by epsilon, which determines its magnitude.

The experiment uses the following configuration:

| Parameter | Value |
|---|---|
| Attack method | FGSM |
| Epsilon | 0.2 |
| Evaluated samples | 5,000 |

The purpose is to measure how much adversarial perturbations reduce classification accuracy compared with clean inputs.

### 4.3 FGSM Attack Results

| Metric | Result |
|---|---:|
| Clean accuracy | 98.26% |
| Adversarial accuracy | 45.12% |
| Prediction change rate | 53.28% |
| Attack success rate on initially correct predictions | 54.08% |

The model's accuracy decreased from 98.26% on clean data to 45.12% on adversarial inputs in this experiment.

The prediction change rate measures the proportion of evaluated predictions that changed after applying the attack.

The attack success rate is calculated among samples that were classified correctly before the attack. It is therefore different from the overall prediction change rate.

### 4.4 Data Poisoning Experiment

The poisoning experiment modifies a portion of training labels to investigate the effect of corrupted training data.

The recorded configuration is:

| Parameter | Value |
|---|---|
| Attack type | Label flipping |
| Poisoning fraction | 5% |
| Source digit | 7 |
| Target digit | 1 |
| Random seed | 42 |
| Recorded poisoned samples | 313 |

The intended objective is to increase the number of genuine digit-7 test images that the trained model classifies as digit 1.

This experiment evaluates label corruption. It does not use a trigger pattern and should not be described as a trigger-based backdoor attack.

### 4.5 Data Poisoning Results

| Metric | Baseline Model | Poisoned Model |
|---|---:|---:|
| Clean accuracy | 98.82% | 98.87% |
| Accuracy on digit 7 | 98.35% | 98.44% |
| Actual digit-7 images predicted as digit 1 | 0 | 8 |
| Number of actual digit-7 test images | 1,028 | 1,028 |

The poisoned model achieved 98.87% clean accuracy compared with 98.82% for the baseline model.

The number of genuine digit-7 test images predicted as digit 1 increased from 0 to 8.

This is a small observed change. The results do not establish a strong or reliably reproducible targeted poisoning effect. Additional controlled runs would be required to determine the consistency and statistical significance of the observed change.

---

## 5. Retesting the Model and Comparing Clean and Adversarial Performance (25%)

### 5.1 Blue-Team Defense

The blue team uses input validation and adversarial training to improve the reliability of the CNN.

**Input validation** checks that model inputs have the expected type, shape, data type, finite values, and pixel range.

**Adversarial training** exposes the model to adversarial examples during training so that it can learn to classify perturbed inputs more reliably.

The recorded adversarial-training configuration uses epsilon = 0.2 and 10,000 adversarial-training samples.

### 5.2 Baseline Versus Defended Model

The following results were recorded using the same evaluation samples for the baseline and defended models.

| Metric | Baseline Model | Defended Model |
|---|---:|---:|
| Clean accuracy | 98.82% | 98.25% |
| FGSM adversarial accuracy | 50.23% | 96.51% |

The comparison shows that adversarial training improved the model's performance against the tested FGSM attack.

### 5.3 Performance Improvement

| Metric | Change |
|---|---:|
| Clean accuracy change | -0.57 percentage points |
| FGSM adversarial accuracy change | +46.28 percentage points |

The defended model's clean accuracy decreased from 98.82% to 98.25%, a reduction of approximately 0.57 percentage points.

FGSM adversarial accuracy increased from 50.23% to 96.51%, an improvement of 46.28 percentage points.

These results indicate improved robustness against the tested FGSM configuration. They do not demonstrate robustness against every adversarial attack or every perturbation strength.

### 5.4 Distinguishing the FGSM Experiments

Two FGSM result sets are reported in this project.

The first experiment evaluated 5,000 samples and reported 98.26% clean accuracy and 45.12% adversarial accuracy.

The second experiment compared the baseline and defended models on the same evaluation samples and reported:

- Baseline clean accuracy: 98.82%.
- Baseline FGSM accuracy: 50.23%.
- Defended clean accuracy: 98.25%.
- Defended FGSM accuracy: 96.51%.

These results come from different recorded evaluation runs and should not be combined into a single comparison.

### 5.5 Overall Baseline and Blue-Team Comparison

| Security Aspect | Baseline | Blue Team |
|---|---|---|
| Clean classification | 98.82% accuracy in the recorded baseline evaluation | 98.25% in the same-sample defense comparison |
| FGSM robustness | 50.23% adversarial accuracy in the same-sample comparison | 96.51% adversarial accuracy |
| Malformed input handling | Depends on input checks | Explicit input validation |
| SAST demonstration | Contains an intentionally vulnerable example | Fixed demonstration avoids shell execution |
| General security | Not guaranteed against attacks | Improved protection against tested conditions, but not complete security |

The experiments show that adversarial training can improve robustness against a specified attack, while input validation and secure coding practices address different classes of security weaknesses.

---

## 6. Conclusion and Observations

This project evaluated a CNN-based MNIST digit classifier through model training, threat modeling, static application security testing, adversarial example generation, data poisoning, and defensive evaluation.

The baseline CNN achieved 98.82% accuracy on clean MNIST test data. The FGSM experiment demonstrated that adversarial perturbations can substantially reduce classification accuracy.

The label-flipping experiment produced a small increase in the number of digit-7 images classified as digit 1. The observed result is limited and does not establish a strong or reliably reproducible targeted poisoning effect.

Threat modeling using STRIDE identified potential threats to data integrity, model security, availability, and access control. LINDDUN was used to identify potential privacy risks that should be considered when handling datasets and model artifacts.

Bandit identified an unsafe shell-execution pattern in the intentionally vulnerable demonstration. The fixed demonstration avoided shell execution and passed its isolated scan. Input validation tests also passed all eight recorded cases.

The blue-team implementation combined input validation with adversarial training. In the same-sample defense comparison, FGSM adversarial accuracy increased from 50.23% to 96.51%, while clean accuracy decreased from 98.82% to 98.25%.

Overall, the results demonstrate that high accuracy on clean data alone is insufficient to establish the security of an AI system. Secure AI development requires evaluation of both model performance and security risks, together with defensive testing and reproducible experiments.

The conclusions are limited to the model, dataset, attack configurations, and experimental environment used in this project. They should not be interpreted as proof of complete security or universal adversarial robustness.