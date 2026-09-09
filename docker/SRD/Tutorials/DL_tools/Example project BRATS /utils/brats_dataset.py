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
    NormalizeIntensityd,
)
from torch.utils.data import Dataset, DataLoader
import torch
import random

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
            Resized(keys=["image", "label"], spatial_size=(120, 120, 155), mode=("trilinear", "nearest")),
            EnsureTyped(keys=["image", "label"]),
            NormalizeIntensityd(
                keys="image",
                subtrahend=[0.0287, 0.0388, 0.0384, 0.0322],
                divisor=[0.0751, 0.0954, 0.0951, 0.0858],
                channel_wise=True
            ),
        ]
    )

class BRATSSliceDataset(Dataset):
    def __init__(self, decathlon_dataset, sample_num_slices=10, val=False):
        self.dataset = decathlon_dataset
        self.sample_num_slices = sample_num_slices
        self.val = val

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        sample = self.dataset[idx]
        # random indices for slices 
        if not self.val:
            indices = torch.randint(0, sample['image'].shape[-1], (self.sample_num_slices,))
        else:
            indices = torch.arange(sample['image'].shape[-1])
        

        return {'image': sample['image'][..., indices], 'label': 1*(sample['label'][..., indices]>=1)}

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

def get_brats_dataloader(root_dir, section, batch_size, num_workers, shuffle=False, num_slices=50):
    """
    Creates and returns a DataLoader for the BRATS dataset.

    Args:
        root_dir (str): Root directory of the dataset.
        section (str): Dataset section ("training" or "validation").
        batch_size (int): Batch size for the DataLoader.
        num_workers (int): Number of worker processes for data loading.
        shuffle (bool): Whether to shuffle the data.

    Returns:
        DataLoader: DataLoader for the specified BRATS dataset.
    """
    transform = get_transform()
    

    decathlon_dataset = monai.apps.DecathlonDataset(
        root_dir=root_dir,
        task="Task01_BrainTumour",
        transform=transform,
        section=section,
        download=True,
        cache_rate=0.0,  # Disable caching to avoid loading into memory
        num_workers=num_workers,
    )
    
    brats_slice_dataset = BRATSSliceDataset(decathlon_dataset, num_slices, val=True if section == "validation" else False)
    
    return DataLoader(
        brats_slice_dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        collate_fn=custom_collate
    )

def main():
    root_dir = "../datasets"  # Update this to your dataset directory
    batch_size = 4
    num_workers = 2

    print("Loading training data...")
    train_dataloader = get_brats_dataloader(root_dir, "training", batch_size, num_workers, shuffle=True)
    

    # Rest of the function remains the same
    print("\nLoading a batch from the training dataloader...")
    batch = next(iter(train_dataloader))
    image, label = batch['image'], batch['label']

    print(f"Batch image shape: {image.shape}")
    print(f"Batch label shape: {label.shape}")

    print(f"\nImage min value: {image.min():.2f}")
    print(f"Image max value: {image.max():.2f}")
    print(f"Image mean value: {image.mean():.2f}")
    print(f"Image std value: {image.std():.2f}")

    print(f"\nUnique label values: {torch.unique(label)}")

if __name__ == "__main__":
    main()

