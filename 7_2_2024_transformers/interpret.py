import matplotlib.pyplot as plt
import torch

from data import PAD_TOKEN, padding_mask
from data import CLS_TOKEN, parenthesization_to_tensor


def plot_linear_layer(
    layer,
):
    """
    Plots a heatmap of the weights for a linear layer.

    Parameters:
        layer (nn.Linear): The Linear layer for which the weights are to be visualized.
    """
    # TODO
    weights = layer.weight.data.numpy()
    plt.imshow(weights, cmap="viridis", aspect="auto")
    plt.colorbar()
    plt.title("Heatmap of Linear Layer Weights")
    plt.xlabel("Input Features")
    plt.ylabel("Output Features")
    plt.show()


def incorrect_predictions(model, dataloader):
    """
    Given a model and a dataloader, this function evaluates the model by predicting the labels for each input in the dataloader.
    It keeps track of incorrect predictions and returns a list of inputs that were incorrectly predicted for each label.

    Args:
        model (torch.nn.Module): The model used for prediction.
        dataloader (torch.utils.data.DataLoader): The dataloader containing the input data.

    Returns:
        List[List[List[int]]]: A list of incorrect predictions for each label. The list contains two sublists, one for each label.
            Each sublist contains a list of inputs that were incorrectly predicted for that label.
            Each input is represented as a list of integers.
    """
    model.eval()
    incorrect_predictions = [[], []]

    with torch.no_grad():
        for data in dataloader:
            inputs, labels = data
            outputs = model(inputs, mask=padding_mask(inputs))
            predicted_labels = torch.argmax(outputs, dim=2)
            for input_seq, label, prediction in zip(inputs, labels, predicted_labels):
                predicted_label = prediction[0].item()  # Assume the first token (CLS_TOKEN) gives the prediction
                true_label = label.item()
                if predicted_label != true_label:
                    incorrect_predictions[true_label].append(input_seq.tolist())
    
    return incorrect_predictions


def token_contributions(model, single_input):
    """
    Calculates the contributions of each token in the single_input sequence to each class in the model's
    predicted output. The contribution of a single token is calculated as the difference between the
    model output with the given input and the model output with the single token changed to the other
    parenthesis.

    Args:
        model (torch.nn.Module): The model used for prediction.
        single_input (torch.Tensor): The input sequence for which token contributions are calculated.

    Returns:
        List[float]: A list of contributions of each token to the model's output.
    """
    import torch

def token_contributions(model, single_input):
    """
    Calculates the contributions of each token in the single_input sequence to each class in the model's
    predicted output. The contribution of a single token is calculated as the difference between the
    original prediction and the prediction after masking the token.
    
    Args:
        model (torch.nn.Module): The trained model.
        single_input (torch.Tensor): A tensor representing a single input sequence.
        
    Returns:
        List[float]: A list of contributions of each token to the model's output.
    """
    model.eval()  # Set the model to evaluation mode
    with torch.no_grad():
        original_output = model(single_input.unsqueeze(0), mask=padding_mask(single_input.unsqueeze(0)))
        original_prediction = original_output.squeeze(0).cpu().numpy()
    
    contributions = []
    single_input_list = single_input.tolist()
    
    for i in range(len(single_input_list)):
        # Create a masked version of the input
        masked_input = single_input.clone()
        masked_input[i] = 0  # Masking the token (assuming 0 is the mask token)
        
        with torch.no_grad():
            masked_output = model(masked_input.unsqueeze(0), mask=padding_mask(masked_input.unsqueeze(0)))
            masked_prediction = masked_output.squeeze(0).cpu().numpy()
        
        # Calculate the contribution as the difference in predictions
        contribution = original_prediction - masked_prediction
        contributions.append(contribution)
    
    return contributions


def activations(model, dataloader):
    """
    Returns the frequency of each hidden feature's activation in the feedforward layer of the model
    over all inputs in the dataloader.

    Args:
        model (torch.nn.Module): The model used for prediction.
        dataloader (torch.utils.data.DataLoader): The dataloader containing the input data.

    Returns:
        List[int]: A list of frequencies for each hidden feature in the feedforward layer of the model.
    """
    activation_counts = torch.zeros(model.d_model)  # Assuming d_model is the size of the hidden layer
    model.eval()  # Set model to evaluation mode

    with torch.no_grad():
        for inputs, _ in dataloader:
            outputs = model(inputs)
            
            # Assuming outputs are logits or some form of output from the model
            # You may need to adjust this based on your model's architecture
            activations = torch.sum(outputs, dim=-1)  # Sum along the last dimension
            
            # Ensure activations are flattened correctly
            activations = activations.view(-1, model.d_model)
            
            # Aggregate activations over the batch
            activation_counts += torch.sum(activations, dim=0)  # Sum across batch dimension

    return activation_counts.numpy()
