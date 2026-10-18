import torch
from defense.input_validation import validate_mnist_input


def check_valid(name, x):
    try:
        validate_mnist_input(x)
        print(f"PASS: {name}")
        return True
    except (TypeError, ValueError):
        print(f"FAIL: {name}")
        return False


def check_invalid(name, x):
    try:
        validate_mnist_input(x)
        print(f"FAIL: {name} was accepted")
        return False
    except (TypeError, ValueError):
        print(f"PASS: {name} was rejected")
        return True


def main():
    results = [
        check_valid(
            "valid MNIST batch",
            torch.rand(4, 1, 28, 28)
        ),
        check_invalid(
            "wrong image shape",
            torch.rand(4, 28, 28)
        ),
        check_invalid(
            "empty batch",
            torch.empty(0, 1, 28, 28)
        ),
        check_invalid(
            "NaN pixel",
            torch.full((1, 1, 28, 28), float("nan"))
        ),
        check_invalid(
            "pixel below zero",
            torch.full((1, 1, 28, 28), -0.1)
        ),
        check_invalid(
            "pixel above one",
            torch.full((1, 1, 28, 28), 1.1)
        ),
        check_invalid(
            "integer input",
            torch.zeros(1, 1, 28, 28, dtype=torch.int64)
        ),
        check_invalid(
            "non-tensor input",
            [[1, 2, 3]]
        )
    ]

    passed = sum(results)
    total = len(results)

    print(f"\nValidation tests passed: {passed}/{total}")

    if passed != total:
        raise SystemExit(1)


if __name__ == "__main__":
    main()