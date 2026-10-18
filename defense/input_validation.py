import torch


def validate_mnist_input(x):
    if not torch.is_tensor(x):
        raise TypeError("Input must be a PyTorch tensor.")

    if x.ndim != 4 or x.shape[1:] != (1, 28, 28):
        raise ValueError("Input must have shape (N, 1, 28, 28).")

    if x.shape[0] == 0:
        raise ValueError("Input batch must not be empty.")

    if not torch.is_floating_point(x):
        raise TypeError("Input must use a floating-point dtype.")

    if not torch.isfinite(x).all().item():
        raise ValueError("Input contains NaN or Inf values.")

    if (x < 0).any().item() or (x > 1).any().item():
        raise ValueError("Pixel values must be in the range [0, 1].")

    return x