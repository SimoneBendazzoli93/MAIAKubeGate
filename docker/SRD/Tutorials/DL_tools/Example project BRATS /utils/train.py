from torch.utils.tensorboard import SummaryWriter
import torch
from monai.inferers import SimpleInferer
from monai.handlers import CheckpointSaver, CheckpointLoader
from monai.transforms import Compose, Activations, AsDiscrete
from monai.data import decollate_batch
from monai.metrics import DiceMetric
from tqdm import tqdm

def train(model, train_loader, loss_fn, optimizer, device, epochs, save_dir, load_path=None, save_interval=1, log_path=None, overfit_batch=False):
    """
    Train the model using a custom training loop with checkpointing.

    Args:
        model (nn.Module): The neural network model.
        train_loader (DataLoader): DataLoader for the training data.
        loss_fn (callable): Loss function.
        optimizer (torch.optim.Optimizer): Optimizer for updating model parameters.
        device (torch.device): Device to run the training on (CPU or GPU).
        epochs (int): Number of epochs to train for.
        save_dir (str): Directory to save checkpoints.
        load_path (str, optional): Path to load a checkpoint from before training.
        save_interval (int): Interval (in epochs) to save checkpoints.
        log_path (str): Path to save TensorBoard logs.
        overfit_batch (bool): If True, overfit to a single batch for debugging.
    """
    writer = SummaryWriter(log_dir=log_path)
    model.to(device)

    # Load checkpoint if specified
    if load_path:
        checkpoint = torch.load(load_path)
        model.load_state_dict(checkpoint['model'])
        optimizer.load_state_dict(checkpoint['optimizer'])

    if overfit_batch:
        batch = next(iter(train_loader))
        inputs = batch["image"].to(device)
        labels = batch["label"].to(device)

    for epoch in range(epochs):
        model.train()
        epoch_loss = 0

        if overfit_batch:
            # Overfit to a single batch
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = loss_fn(outputs.reshape(-1), labels.reshape(-1).float())
            loss.backward()
            optimizer.step()
            epoch_loss = loss.item()
            print(loss.item())
        else:
            # Train on the entire dataset
            for batch_data in tqdm(train_loader):
                inputs, labels = batch_data["image"].to(device), batch_data["label"].to(device)
                optimizer.zero_grad()
                outputs = model(inputs)
                loss = loss_fn(outputs.reshape(-1), labels.reshape(-1).float())
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item()
            epoch_loss /= len(train_loader)

            writer.add_scalar("Loss/train", epoch_loss, epoch)


            # Save checkpoint
            if (epoch + 1) % save_interval == 0:
                torch.save({
                    'model': model.state_dict(),
                    'optimizer': optimizer.state_dict(),
                }, f"{save_dir}/checkpoint_epoch_{epoch + 1}.pth")
                
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {epoch_loss:.4f}")

    writer.close()
    return model
