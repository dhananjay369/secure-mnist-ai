**# Secure AI Systems: Red and Blue Teaming an MNIST Classifier**

**\*\*Name:\*\*** Dhananjay Kumar

**\*\*Roll Number:\*\*** CS26MTECH13007

\---

**## 1. GitHub Repository of CNN Implementation for Image Classification**

The CNN implementation for handwritten digit classification using the MNIST dataset is available in the following GitHub repository.

**\*\*CNN Implementation Repository:\*\***

[https://github.com/dhananjay369/secure-mnist-ai](https://github.com/dhananjay369/secure-mnist-ai)

The project uses a Convolutional Neural Network (CNN) to classify grayscale handwritten digit images into ten classes, from 0 to 9.

**### Main Implementation Files**

\- `src/model.py` — CNN architecture and input validation.

\- `src/train.py` — model training.

\- `src/evaluate.py` — evaluation on the MNIST test dataset.

\- `src/utils.py` — supporting utilities.

\- `run_all.py` — project workflow.

The CNN consists of two convolutional layers followed by ReLU activation and max-pooling operations. The extracted features are passed through fully connected layers to produce ten output logits, one for each digit class.

The MNIST dataset is used for training and evaluation. Dataset files are not included in the repository; they must be downloaded or made available locally according to the project setup.

**## 2. Performance Metrics of Classification**

The baseline CNN was evaluated on the clean MNIST test dataset.

| Metric | Baseline CNN |
|---|---:|
| Clean test accuracy | 98.82% |
| Evaluation loss | 0.03282 |
| Total test images | 10,000 |
| Inference time | Approximately 0.89 seconds |
| Average inference time per image | Approximately 0.089 milliseconds |

The model achieved 98.82% classification accuracy on clean test data. This result serves as the baseline for comparing performance under adversarial attacks and defensive techniques.

The inference time is specific to the recorded execution environment and may vary depending on hardware and system load.

**## 3. Threat Model of the Implementation**

**### 3.1 System Overview**

The system accepts handwritten digit images and uses a trained CNN to predict their corresponding digit classes.

The main assets are:

\- Training and test images.

\- Training labels and their integrity.

\- Trained model parameters and saved model files.

\- Prediction accuracy and availability.

\- Experiment results and evaluation code.

**### 3.2 Attacker Model**

This project considers two principal attack scenarios.

**#### A. Adversarial Example Attacker**

The attacker modifies input images to cause the CNN to predict an incorrect class.

The Fast Gradient Sign Method (FGSM) is used to generate adversarial examples. The recorded evaluation uses an epsilon value of 0.2 and evaluates 5,000 samples.

In this experimental setting, the attacker can use model gradients to construct perturbations. The attack demonstrates the potential effect of adversarial inputs on classification accuracy.

**#### B. Data Poisoning Attacker**

The attacker modifies a portion of the training labels to influence model predictions.

The implemented experiment targets a mapping from digit 7 to digit 1. The recorded configuration uses a 5% poisoning fraction and 313 poisoned samples.

The intended goal is to increase the number of genuine digit-7 images classified as digit 1 after training on the poisoned dataset.

This is a label-flipping experiment. It should not be confused with a trigger-based backdoor attack.

**### 3.3 STRIDE Threat Analysis**

STRIDE is a threat-modeling framework used to identify six categories of security threats.

| STRIDE Category | Potential Threat | Example in This Project | Possible Mitigation |
|---|---|---|---|
| Spoofing | An attacker pretends to be a trusted source. | Untrusted images or datasets are presented as legitimate inputs. | Verify data sources and restrict access to trusted datasets. |
| Tampering | Data or model parameters are modified. | Training labels are changed to perform a poisoning attack. | Verify dataset integrity and protect model files. |
| Repudiation | An attacker denies performing an action. | Unauthorized changes cannot be traced to their source. | Maintain audit logs and record dataset versions. |
| Information Disclosure | Sensitive information is exposed. | Model artifacts or experiment files are accessed without authorization. | Apply access controls and avoid storing sensitive data unnecessarily. |
| Denial of Service | Legitimate requests cannot be processed. | Repeated malformed inputs consume system resources. | Validate inputs and apply resource limits. |
| Elevation of Privilege | An attacker obtains unauthorized permissions. | An insecure command-execution operation is exploited. | Avoid unsafe shell execution and follow least-privilege principles. |

**### 3.4 LINDDUN Privacy Threat Analysis**

LINDDUN is a privacy threat-modeling framework. It identifies Linkability, Identifiability, Non-repudiation, Detectability, Disclosure of information, Unawareness, and Non-compliance.

| LINDDUN Category | Potential Privacy Threat | Possible Mitigation |
|---|---|---|
| Linkability | Records or images can be linked across datasets. | Minimize identifiers and separate datasets where appropriate. |
| Identifiability | An individual may be identified from exposed data. | Avoid using personal data unnecessarily and anonymize where applicable. |
| Non-repudiation | Actions or predictions can be linked to a specific user. | Limit the collection and retention of identifying logs. |
| Detectability | An attacker can infer whether certain data is present. | Restrict access to datasets and model outputs. |
| Disclosure of Information | Training data or model artifacts reveal sensitive information. | Apply access controls and evaluate model privacy risks. |
| Unawareness | Users do not know how their data is used. | Clearly document data collection and processing. |
| Non-compliance | Data handling violates applicable privacy requirements. | Follow applicable privacy policies and data-protection requirements. |

The project uses the MNIST handwritten digit dataset. The privacy threats above are potential risks in an AI system and do not establish that personal information has actually been exposed in this experiment.

**## 4. SAST Findings and Fixes**

Static Application Security Testing (SAST) was performed using Bandit to identify potentially insecure Python code patterns.

**### 4.1 Tool Used**

\- Tool: Bandit

\- Scan command: `python -m bandit -r src attacks defense security`

\- Purpose: Identify potentially insecure Python operations and security weaknesses.

**### 4.2 Findings**

The latest scan reported two findings in the intentionally vulnerable demonstration file, `security/sast_before.py`.

| Finding | Severity | Description | Fix |
|---|---|---|---|
| B404 | Low | Use of the subprocess module. | Review subprocess usage and avoid unnecessary command execution. |
| B602 | High | Use of `shell=True`, which can lead to command injection when input is unsafe. | Avoid shell-based command execution for untrusted input. |

The High-severity finding relates to CWE-78, which concerns improper neutralization of special elements used in an OS command.

**### 4.3 Fix Implemented**

The fixed demonstration in `security/sast_fixed.py` avoids shell execution and prints the supplied string directly.

```python
def run_demo(user_value):
    if not isinstance(user_value, str):
        raise TypeError("Input must be a string")

    print(user_value)
```

The isolated Bandit scan of `security/sast_fixed.py` reported no issues.

The intentionally vulnerable file is retained to demonstrate the original security problem. Therefore, the two findings in the full project scan refer to that demonstration file, not to the fixed function.

**### 4.4 Input Validation**

The project also implements input validation in `defense/input_validation.py`.

The validation checks include:

\- Input must be a PyTorch tensor.

\- Input shape must be `(N, 1, 28, 28)`.

\- The batch must not be empty.

\- Input values must use a floating-point data type.

\- Input values must be finite; NaN and infinity are rejected.

\- Pixel values must lie within the range `[0, 1]`.

The validation tests passed all eight recorded cases, including valid input, invalid shape, empty batch, NaN values, out-of-range values, integer input, and non-tensor input.

Input validation prevents malformed data from entering the model. It does not prevent adversarial examples that satisfy all the validation rules.

**## 5. GitHub Repository of Attack and Defense Implementation**

**\*\*Attack and Defense Repository:\*\***

[https://github.com/dhananjay369/secure-mnist-ai-attacks](https://github.com/dhananjay369/secure-mnist-ai-attacks)

This repository contains the attack and defense implementation used for the experiments.

The project evaluates adversarial examples generated using FGSM, label-flipping data poisoning, input validation, and adversarial training.

**### Main Experimental Components**

\- FGSM attack implementation.

\- Data poisoning and poisoned-model training.

\- Poisoning evaluation.

\- Adversarial training defense.

\- Baseline and defended model comparison.

\- Input validation tests.

The experiments compare model accuracy on clean inputs, adversarial inputs, and data-poisoning scenarios.

**## 6. Performance Metrics with Adversarial and Poisoned Data**

**### 6.1 FGSM Adversarial Attack**

The FGSM attack generates adversarial images by perturbing input pixels using the gradient of the model loss.

The recorded experiment uses epsilon = 0.2 and evaluates 5,000 samples.

| Metric | Result |
|---|---:|
| Clean accuracy | 98.26% |
| Accuracy on adversarial images | 45.12% |
| Prediction change rate | 53.28% |
| Attack success rate on initially correct predictions | 54.08% |

The model's accuracy decreased substantially when evaluated on adversarial images. This indicates that a classifier performing well on clean data can still be vulnerable to carefully constructed perturbations.

The attack success rate is calculated over predictions that were correct before the attack. It is not the same as the overall prediction change rate.

**### 6.2 Data Poisoning Attack**

The poisoning experiment changes a portion of training labels to investigate whether the model's predictions are affected.

The recorded configuration uses a 5% poisoning fraction, digit 7 as the source class, digit 1 as the target class, and random seed 42. The poisoning process records 313 poisoned samples.

| Metric | Baseline Model | Poisoned Model |
|---|---:|---:|
| Clean accuracy | 98.82% | 98.87% |
| Accuracy on digit 7 | 98.35% | 98.44% |
| Actual digit-7 images predicted as digit 1 | 0 | 8 |
| Number of actual digit-7 test images | 1,028 | 1,028 |

The poisoned model achieved 98.87% clean accuracy, compared with 98.82% for the baseline model. The number of digit-7 images classified as digit 1 increased from 0 to 8.

These results show a small change in the targeted misclassification count. They do not establish a strong or reliable targeted poisoning effect. Additional controlled experiments and repeated runs would be needed to determine the consistency of the effect.

**## 7. Blue-Team Implementation and Comparison with Baseline**

The blue team implements defensive techniques to improve the reliability of the CNN against malicious or malformed inputs.

The main defenses are input validation and adversarial training.

**### 7.1 Input Validation Defense**

Input validation checks that incoming images have the expected tensor type, shape, data type, finite values, and pixel range.

The validation tests passed all eight recorded test cases.

This defense helps reject malformed inputs before model inference. However, a valid-range adversarial image can still pass these checks.

**### 7.2 Adversarial Training Defense**

Adversarial training exposes the model to adversarial examples during training. The objective is to improve its ability to classify perturbed inputs correctly.

The recorded configuration uses epsilon = 0.2 and 10,000 adversarial-training samples.

The following results were obtained using the same clean and adversarial evaluation samples for the baseline and defended models.

| Metric | Baseline Model | Defended Model |
|---|---:|---:|
| Clean accuracy | 98.82% | 98.25% |
| FGSM adversarial accuracy | 50.23% | 96.51% |

**### 7.3 Comparison and Observations**

\- Clean accuracy decreased by approximately 0.57 percentage points after adversarial training.

\- FGSM adversarial accuracy increased from 50.23% to 96.51%.

\- The improvement in FGSM adversarial accuracy was 46.28 percentage points.

\- The results indicate that adversarial training substantially improved robustness against the tested FGSM attack at epsilon = 0.2.

\- These results do not guarantee robustness against all adversarial attacks, perturbation strengths, or distribution shifts.

**### 7.4 Baseline Versus Blue-Team Summary**

| Evaluation Aspect | Baseline | Blue Team |
|---|---|---|
| Clean image classification | High accuracy | Slightly lower accuracy |
| FGSM robustness | Vulnerable to tested perturbations | Substantially improved for the tested attack |
| Malformed input handling | Depends on input checks | Explicit input validation |
| General security | No guarantee against attacks | Improved protection, but not complete security |

The experiments show that defensive techniques can improve robustness, but the effectiveness of each defense must be measured against clearly defined attack conditions.

**## 8. Conclusion and Observations**

This project evaluated the security of a CNN-based MNIST digit classifier through red-team attacks and blue-team defenses.

The baseline CNN achieved 98.82% accuracy on clean test images. However, the FGSM experiment showed that adversarial perturbations can significantly reduce classification accuracy.

The data-poisoning experiment resulted in a small increase in the number of digit-7 images classified as digit 1. The observed effect was limited, so further controlled experiments are needed before concluding that the poisoning attack reliably achieves its intended goal.

The blue-team implementation introduced input validation and adversarial training. Input validation rejected malformed inputs, while adversarial training improved FGSM accuracy from 50.23% to 96.51% in the same-sample comparison. The defended model's clean accuracy decreased slightly from 98.82% to 98.25%.

SAST identified an unsafe shell-execution pattern in the intentionally vulnerable demonstration. The fixed demonstration avoided shell execution and passed its isolated Bandit scan.

Overall, the experiments demonstrate that clean-data accuracy alone is insufficient to establish the security of an AI system. A more secure implementation should combine input validation, secure coding practices, dataset-integrity controls, adversarial evaluation, and ongoing testing against multiple attack types.

The results are limited to the tested MNIST dataset, model, attack configurations, and experimental environment. They should not be interpreted as proof of complete robustness or security.

