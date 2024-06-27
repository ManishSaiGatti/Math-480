import torch
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
    # TODO: Use https://pytorch.org/tutorials/beginner/introyt/trainingyt.html#the-training-loop as a reference.
    model.train()
    # running_loss = 0.0
    # last_loss = 0.0

    # for i, data in enumerate(training_loader):
    #     inputs, labels = data
    #     inputs = inputs.float()
    #     optimizer.zero_grad()
    #     outputs = model(inputs)
    #     loss = loss_fn(outputs, labels)
    #     loss.backward()
    #     optimizer.step()
    #     running_loss += loss.item()
    #     if i % 1000 == 999:
    #         last_loss = running_loss / 1000
    #         print(f"[{i + 1}] loss: {last_loss:.3f}")
    #         running_loss = 0.0
    # return last_loss

    total_loss = 0.0

    for batch in training_loader:
        inputs, labels = batch
        inputs = inputs.float()

        optimizer.zero_grad()
        outputs = model(inputs.float())
        loss = loss_fn(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    return total_loss / len(training_loader)

def evaluate_model(model, test_dataset):
    """
    Evaluates the model using the provided test dataset and returns the confusion matrix.

    Args:
        model (torch.nn.Module): The model to be evaluated.
        test_dataset (torch.utils.data.Dataset): The dataset used for evaluation.

    Returns:
        list: A 2x2 confusion matrix where rows represent true labels and columns represent predicted labels.
    """
    model.eval()

    with torch.no_grad():
        confusion_matrix = [[0, 0], [0, 0]]
        # TODO
        for data, target in test_dataset:
            data = data.float()
            output = model(data.unsqueeze_(0))
            _, predicted = torch.max(output, 1)
            confusion_matrix[target][predicted] += 1
    return confusion_matrix
