import csv
import torch
from torch.utils.data import Dataset, DataLoader, random_split
import torch.nn.functional as F
from torch import nn

device = "cpu"

def parenthesization_to_tensor(parenthesization):
    """
    Convert a parenthesization string to a pytorch tensor representation.

    Args:
        parenthesization (str): The parenthesization string to convert.

    Returns:
        torch.Tensor: The tensor representation of the parenthesization.
        The tensor has shape (4*n), where 2*n is the length of the parenthesization string.
        Each element in the tensor is either 0 or 1, representing whether the corresponding
        parenthesization character is "(" or ")".
    """
    list = []
    for i, c in enumerate(parenthesization):
        if c == "(":
            list.append(1)
            list.append(0)
        else:
            list.append(0)
            list.append(1)
    return torch.tensor(list)

class ParenthesizationDataset(Dataset):
    def __init__(self, n):
        #parenthesization_to_tensor("(())")
        self.data = []
        filename = f"data/parenthesizations_{n}.csv"
        with open(filename, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                self.data.append((parenthesization_to_tensor(row["parenthesization"]), int(row["valid"])))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

class ParenthesizationModel(nn.Module):
    def __init__(self, n):
        super().__init__()
        self.fc = nn.Linear(2*2*n, 2)

    def forward(self, x):
        return self.fc(x)