import monai
from monai.transforms import (
    Compose,
    LoadImaged,
    EnsureChannelFirstd,
    Orientationd,
    Spacingd,
    ScaleIntensityd,
    Resized,
    EnsureTyped,
)
from torch.utils.data import DataLoader
import torch

def get_transform():
    """
    Returns the composition of transforms to be applied to the dataset.
    """
    return Compose(
        [
            LoadImaged(keys=["image", "label"]),
            EnsureChannelFirstd(keys=["image", "label"]),
            Orientationd(keys=["image", "label"], axcodes="RAS"),
            Spacingd(keys=["image", "label"], pixdim=(1.0, 1.0, 1.0), mode=("bilinear", "nearest")),
            ScaleIntensityd(keys="image"),
            Resized(keys=["image", "label"], spatial_size=(32, 64, 32), mode=("trilinear", "nearest")),
            EnsureTyped(keys=["image", "label"]),
        ]
    )

def custom_collate(batch):
    """
    Custom collate function to convert MetaTensors to regular tensors and permute dimensions.
    """
    images = []
    labels = []
    for item in batch:
        # Convert to regular tensor and permute dimensions
        images.append(item['image'].as_tensor().permute(3, 0, 1, 2))
        labels.append(item['label'].as_tensor().permute(3, 0, 1, 2))

    return {
        'image': torch.cat(images, dim=0),
        'label': torch.cat(labels, dim=0)
    }

def get_decathlon_dataloader(root_dir, task, section, batch_size, num_workers, shuffle=False):
    """
    Creates and returns a DataLoader for the Decathlon dataset.

    Args:
        root_dir (str): Root directory of the dataset.
        task (str): Task name (e.g., "Task04_Hippocampus").
        section (str): Dataset section ("training" or "validation").
        batch_size (int): Batch size for the DataLoader.
        num_workers (int): Number of worker processes for data loading.
        shuffle (bool): Whether to shuffle the data.

    Returns:
        DataLoader: DataLoader for the specified Decathlon dataset.
    """
    transform = get_transform()
    
    dataset = monai.apps.DecathlonDataset(
        root_dir=root_dir,
        task=task,
        section=section,
        transform=transform,
        download=True,
    )
    
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        collate_fn=custom_collate
    )

# Example usage
if __name__ == "__main__":
    root_dir = './datasets'
    task = "Task04_Hippocampus"
    
    train_loader = get_decathlon_dataloader(root_dir, task, "training", batch_size=4, num_workers=2, shuffle=True)
    val_loader = get_decathlon_dataloader(root_dir, task, "validation", batch_size=4, num_workers=2)
    
    print(f"Number of training batches: {len(train_loader)}")
    print(f"Number of validation batches: {len(val_loader)}")
    
    # Example of accessing a batch
    for batch in train_loader:
        print(f"Batch image shape: {batch['image'].shape}")
        print(f"Batch label shape: {batch['label'].shape}")
        break
