
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets, transforms

# 1. Choose CPU or CUDA if supported
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)
print("Using:", device)

# 2. Prepare image preprocessing
transform = transforms.ToTensor()

# 3. Download the training and test datasets
train_data = datasets.CIFAR10(
    root="data",
    train=True,
    download=True,
    transform=transform
)

test_data = datasets.CIFAR10(
    root="data",
    train=False,
    download=True,
    transform=transform
)

# CIFAR-10 class IDs: cat = 3, dog = 5


