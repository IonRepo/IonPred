import torch

# Checking if pytorch can run in GPU, else CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def train(model, criterion, train_loader, optimizer):
    """Train the model using the provided optimizer and criterion on the training dataset.

    Args:
        model (torch.nn.Module): The model to train.
        optimizer (torch.optim.Optimizer): The optimizer to use for updating model parameters.
        criterion (torch.nn.Module): The loss function to use.
        train_loader (torch.utils.data.DataLoader): The training dataset loader.

    Returns:
        float: The average training loss.
    """
    
    model.train()
    train_loss = 0
    all_predictions   = []
    all_ground_truths = []
    for data in train_loader:  # Iterate in batches over the training dataset
        # Perform a single forward pass
        out = model(data.x, data.edge_index, data.edge_attr, data.batch).to(device)
        
        # Compute the loss
        loss = criterion(out, data.y)
        
        # Accumulate the training loss
        train_loss += loss.item()

        # Append predictions and ground truths to lists
        all_predictions.append(out.detach())
        all_ground_truths.append(data.y.detach())
        
        # Derive gradients
        loss.backward()
        
        # Update parameters based on gradients
        optimizer.step()
        
        # Clear gradients
        optimizer.zero_grad()
    
    # Compute the average training loss
    avg_train_loss = train_loss/ len(train_loader)
    
    # Concatenate predictions and ground truths into single arrays
    all_predictions = torch.cat(all_predictions)
    all_ground_truths = torch.cat(all_ground_truths)
    
    return avg_train_loss, all_predictions.cpu().numpy(), all_ground_truths.cpu().numpy()


def test(model, criterion, test_loader):
    """Evaluate the performance of a given model on a test dataset.

    Args:
        model (torch.nn.Module): The model to evaluate.
        criterion (torch.nn.Module): The loss function to use.
        test_loader (torch.utils.data.DataLoader): The test dataset loader.

    Returns:
        float: The average loss on the test dataset.
    """
    
    model.eval()
    test_loss = 0
    all_predictions   = []
    all_ground_truths = []
    with torch.no_grad():
        for data in test_loader:  # Iteratea in batches over the train/test dataset
            # Perform a single forward pass
            out = model(data.x, data.edge_index, data.edge_attr, data.batch).to(device)
            
            # Compute the loss
            loss = criterion(out, data.y)
            
            # Accumulate the training loss
            test_loss += loss.item()

            # Append predictions and ground truths to lists
            all_predictions.append(out.detach())
            all_ground_truths.append(data.y.detach())
    
    # Compute the average test loss
    avg_test_loss = test_loss/ len(test_loader)
    
    # Concatenate predictions and ground truths into single arrays
    all_predictions = torch.cat(all_predictions)
    all_ground_truths = torch.cat(all_ground_truths)
    
    return avg_test_loss, all_predictions.cpu().numpy(), all_ground_truths.cpu().numpy()
