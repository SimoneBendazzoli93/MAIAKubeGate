import torch
import torch.nn as nn

class VGG13(nn.Module):
    """
    VGG13 implementation for the CM2003 course lab, adapted for MNIST.
    
    This class implements a simplified VGG13 architecture, modified to work with
    MNIST input (1 channel, 28x28 images).

    Students should implement the network architecture following these steps:
    1. Create the features section with convolutional and pooling layers.
    2. Implement the adaptive average pooling layer.
    3. Create the classifier section with fully connected layers.
    4. Implement the forward method to define the data flow.

    Args:
        num_classes (int): Number of classes for the final classification layer. Default is 10.
        in_channels (int): Number of input channels. Default is 1 for MNIST.
    """

    def __init__(self, num_classes=10, in_channels=1):
        super(VGG13, self).__init__()
    
        # ---CODE START HERE---
        # Step 1: Implement the features section
        self.features = nn.Sequential(
            # First block
            nn.Conv2d(in_channels, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            # Second block
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            # Third block
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            # Fourth block
            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        # Step 2: Implement the adaptive average pooling layer
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))

        # Step 3: Implement the classifier section
        self.classifier = nn.Sequential(
            nn.Linear(512, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, num_classes)
        )
        # ---CODE END HERE---

    def forward(self, x):
        """
        Define the forward pass of the VGG13 model.

        Args:
            x (torch.Tensor): Input tensor of shape (batch_size, 1, 28, 28)

        Returns:
            torch.Tensor: Output tensor of shape (batch_size, num_classes)
        """
        # ---CODE START HERE---
        # Step 4: Implement the forward method
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        # ---CODE END HERE---

        return x
