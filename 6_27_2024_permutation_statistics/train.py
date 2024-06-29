import torch
import matplotlib.pyplot as plt


def train_one_epoch(training_loader, model, loss_fn, optimizer):
    """
    Trains the model for one epoch using the given training data loader, model, loss function, and optimizer.

    Args:
        training_loader (torch.utils.data.DataLoader): The data loader for the training data.
        model (torch.nn.Module): The model to be trained.
        loss_fn (torch.nn.loss._Loss): The loss function used to compute the loss.
        optimizer (torch.optim.Optimizer): The optimizer used to update the model parameters.

    Returns:
        float: The total loss computed over the entire epoch.
    """
    total_loss = 0

    for data in training_loader:
        inputs, labels = data
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = loss_fn(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    return total_loss


def evaluate_model(model, test_dataset):
    """
    Evaluates the model using the provided test dataset and returns the confusion matrix.

    Args:
        model (torch.nn.Module): The model to be evaluated.
        test_dataset (torch.utils.data.Dataset): The dataset used for evaluation.

    Returns:
        ConfusionMatrix: A k by k confusion matrix where rows represent true labels and columns represent predicted labels.
    """
    model.eval()
    num_classes = model.layers[-1].weight.shape[0]

    with torch.no_grad():
        confusion_matrix = [[0 for _ in range(num_classes)] for _ in range(num_classes)]
        for data in test_dataset:
            input, label = data
            output = model(input)
            confusion_matrix[label][torch.argmax(output)] += 1
        return ConfusionMatrix(confusion_matrix)


class ConfusionMatrix:
    def __init__(self, confusion_matrix):
        self.confusion_matrix = confusion_matrix

    def __str__(self):
        return str(self.confusion_matrix)

    def print_accuracy(self):
        """
        Prints out the accuracy within each of the prediction classes and the overall accuracy.
        """
        confusion_matrix = self.confusion_matrix
        num_classes = len(confusion_matrix)
        for i in range(num_classes):
            if sum(confusion_matrix[i]) == 0:
                print(f"No examples for class {i}")
                continue
            print(
                f"Accuracy for class {i} = {100 * confusion_matrix[i][i] / sum(confusion_matrix[i])}%"
            )

        total_correct = sum([confusion_matrix[i][i] for i in range(num_classes)])
        total = sum([sum(confusion_matrix[i]) for i in range(num_classes)])
        print(f"Overall accuracy = {100 * total_correct / total}%")

    def plot(self, title="Confusion Matrix"):
        """
        Plots the confusion matrix as a heatmap.
        """
        confusion_matrix = self.confusion_matrix
        plt.imshow(confusion_matrix, cmap="Blues")
        plt.xticks(range(len(confusion_matrix)), range(len(confusion_matrix)))
        plt.yticks(range(len(confusion_matrix)), range(len(confusion_matrix)))
        plt.xlabel("Predicted label")
        plt.ylabel("True label")
        for i in range(len(confusion_matrix)):
            for j in range(len(confusion_matrix)):
                plt.text(j, i, confusion_matrix[i][j], ha="center", va="center")
        plt.title(title)
        plt.show()
