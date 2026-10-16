import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from src.model import MNISTCNN, load_weights
from src.utils import device, validate_mnist_input
from attacks.fgsm_attack import fgsm


dev = device()

test_ds = datasets.MNIST(
    "datasets",
    train=False,
    download=True,
    transform=transforms.ToTensor()
)

loader = DataLoader(
    test_ds,
    batch_size=256,
    shuffle=False
)

baseline = MNISTCNN().to(dev)
load_weights(baseline, "models/baseline_model.pt", dev)
baseline.eval()

defended = MNISTCNN().to(dev)
load_weights(defended, "models/defended_model.pt", dev)
defended.eval()

epsilon = 0.20

baseline_clean_correct = 0
baseline_adv_correct = 0
defended_clean_correct = 0
defended_adv_correct = 0
total = 0

for x, y in loader:
    x = x.to(dev)
    y = y.to(dev)

    validate_mnist_input(x)

    # Generate ONE set of adversarial examples
    # using the baseline model.
    x_adv = fgsm(baseline, x, y, epsilon)

    with torch.no_grad():
        baseline_clean_pred = baseline(x).argmax(1)
        baseline_adv_pred = baseline(x_adv).argmax(1)

        defended_clean_pred = defended(x).argmax(1)
        defended_adv_pred = defended(x_adv).argmax(1)

    baseline_clean_correct += (
        baseline_clean_pred == y
    ).sum().item()

    baseline_adv_correct += (
        baseline_adv_pred == y
    ).sum().item()

    defended_clean_correct += (
        defended_clean_pred == y
    ).sum().item()

    defended_adv_correct += (
        defended_adv_pred == y
    ).sum().item()

    total += y.size(0)


baseline_clean_accuracy = baseline_clean_correct / total
baseline_adv_accuracy = baseline_adv_correct / total

defended_clean_accuracy = defended_clean_correct / total
defended_adv_accuracy = defended_adv_correct / total

print()
print("Same FGSM adversarial samples")
print("--------------------------------")
print("Baseline clean accuracy:",
      baseline_clean_accuracy)

print("Baseline FGSM accuracy:",
      baseline_adv_accuracy)

print("Defended clean accuracy:",
      defended_clean_accuracy)

print("Defended FGSM accuracy:",
      defended_adv_accuracy)