import torch
from monai.metrics import DiceMetric
from torch.utils.tensorboard import SummaryWriter
from monai.inferers import SimpleInferer
from monai.transforms import Compose, Activations, AsDiscrete
from monai.data import decollate_batch
from torch.utils.data import DataLoader, TensorDataset

def evaluate(model: torch.nn.Module, 
             data_loader: torch.utils.data.DataLoader, 
             device: torch.device,
             log_dir: str = None):
    model.eval()
    model.to(device)
    
    # Define MONAI metrics
    dice_metric = DiceMetric(include_background=False, reduction="mean")
    
    # Create MONAI inferer
    inferer = SimpleInferer()
    
    # Post-processing transforms
    post_trans = Compose([Activations(sigmoid=True), AsDiscrete(threshold=0.5)])
    
    # Initialize TensorBoard writer if log_dir is provided
    writer = SummaryWriter(log_dir) if log_dir else None
    
    with torch.no_grad():
        for batch_idx, batch_data in enumerate(data_loader):
            inputs, labels = batch_data["image"].to(device), batch_data["label"].to(device)
            outputs = inferer(inputs, model)
            outputs = [post_trans(i) for i in decollate_batch(outputs)]
            dice_metric(y_pred=outputs, y=labels)
    
    # Aggregate and print results
    mean_dice = dice_metric.aggregate().item()
    print(f"Mean Dice: {mean_dice:.4f}")
    
    # Log to TensorBoard if writer is initialized
    if writer:
        writer.add_scalar('Mean Dice', mean_dice)
        writer.close()
    
    # Reset the metric for the next evaluation
    dice_metric.reset()

def main():
    # Create a simple model
    model = torch.nn.Sequential(
        torch.nn.Conv2d(1, 1, kernel_size=3, padding=1),
        torch.nn.ReLU(),
        torch.nn.Conv2d(1, 1, kernel_size=3, padding=1)
    )
    
    # Create a simple dataset and dataloader
    data = torch.randn(10, 1, 64, 64)  # 10 samples of 1x64x64 images
    labels = torch.randint(0, 2, (10, 1, 64, 64))  # Binary labels
    dataset = TensorDataset(data, labels)
    data_loader = DataLoader(dataset, batch_size=2)
    
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Move model to device
    model.to(device)
    
    # Run evaluation
    evaluate(model, data_loader, device, log_dir="./logs")

if __name__ == "__main__":
    main()
