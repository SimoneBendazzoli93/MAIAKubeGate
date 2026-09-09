import torch
import torch.nn as nn
import torchvision.transforms.functional as TF

class DoubleConv(nn.Module):
    """
    A double convolutional block used in the U-Net architecture.
    
    This module applies two consecutive convolutional layers, each followed by
    batch normalization and ReLU activation.

    Args:
        in_channels (int): Number of input channels.
        out_channels (int): Number of output channels.
    """
    def __init__(self, in_channels, out_channels):
        super(DoubleConv, self).__init__()
        #--- CODE START ---
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, 1, 1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, 3, 1, 1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )
        #--- CODE END ---

    def forward(self, x):
        """
        Forward pass of the DoubleConv module.

        Args:
            x (torch.Tensor): Input tensor.

        Returns:
            torch.Tensor: Output after applying the double convolution.
        """
        #--- CODE START ---
        return self.conv(x)
        #--- CODE END ---

class UNET(nn.Module):
    """
    U-Net architecture for image segmentation tasks.

    This implementation follows the original U-Net paper with some modifications.
    It consists of a contracting path (downsampling) and an expansive path (upsampling),
    with skip connections between the corresponding layers.

    Args:
        in_channels (int): Number of input channels (default: 3 for RGB images).
        out_channels (int): Number of output channels (default: 1 for binary segmentation).
        features (list): List of feature dimensions for each level of the U-Net (default: [64, 128, 256, 512]).
    """
    def __init__(
            self, in_channels=3, out_channels=3, features=[64, 128, 256, 512],
    ):
        super(UNET, self).__init__()
        self.ups = nn.ModuleList()
        self.downs = nn.ModuleList()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        #--- CODE START ---
        # Down part of UNET
        for feature in features:
            self.downs.append(DoubleConv(in_channels, feature))
            in_channels = feature

        # Up part of UNET
        for feature in reversed(features):
            self.ups.append(
                nn.ConvTranspose2d(
                    feature*2, feature, kernel_size=2, stride=2,
                )
            )
            self.ups.append(DoubleConv(feature*2, feature))

        self.bottleneck = DoubleConv(features[-1], features[-1]*2)
        self.final_conv = nn.Conv2d(features[0], out_channels, kernel_size=1)
        #--- CODE END ---

    def forward(self, x):
        """
        Forward pass of the U-Net.

        Args:
            x (torch.Tensor): Input image tensor.

        Returns:
            torch.Tensor: Output segmentation map.
        """
        #--- CODE START ---
        skip_connections = []

        for down in self.downs:
            x = down(x)
            skip_connections.append(x)
            x = self.pool(x)

        x = self.bottleneck(x)
        skip_connections = skip_connections[::-1]

        for idx in range(0, len(self.ups), 2):
            x = self.ups[idx](x)
            skip_connection = skip_connections[idx//2]

            if x.shape != skip_connection.shape:
                x = TF.resize(x, size=skip_connection.shape[2:])

            concat_skip = torch.cat((skip_connection, x), dim=1)
            x = self.ups[idx+1](concat_skip)

        return self.final_conv(x)
        #--- CODE END ---
