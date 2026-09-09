import torch
import torch.nn as nn


class ResNetBlock(nn.Module):
    """
    ResNet block implementation for the CM2003 course lab.
    
    This class implements a single ResNet block as described in the paper:
    "Deep Residual Learning for Image Recognition" by He et al.

    Students should implement the block architecture following these steps:
    1. Create the convolutional layers with batch normalization.
    2. Implement the skip connection (identity_downsample).
    3. Implement the forward method to define the data flow.

    Args:
        in_channels (int): Number of input channels.
        out_channels (int): Number of output channels.
        stride (int): Stride for the first convolutional layer. Default is 1.
    """

    def __init__(self, in_channels, out_channels, stride=1):
        super(ResNetBlock, self).__init__()
        self.expansion = 4
        self.stride = stride

        #--CODE START--
        # Step 1: Implement the convolutional layers with batch normalization
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, padding=0, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        self.conv3 = nn.Conv2d(out_channels, out_channels * self.expansion, kernel_size=1, stride=1, padding=0, bias=False)
        self.bn3 = nn.BatchNorm2d(out_channels * self.expansion)

        # Step 2: Implement the skip connection
        self.identity_downsample = None
        if stride != 1 or in_channels != out_channels * self.expansion:
            self.identity_downsample = nn.Sequential(
                nn.Conv2d(in_channels, out_channels * self.expansion, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels * self.expansion)
            )

        self.relu = nn.ReLU(inplace=True)
        #--CODE END--

    def forward(self, x):
        #--CODE START--
        # Step 3: Implement the forward method
        identity = x
        out = None
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)

        if self.identity_downsample is not None:
            identity = self.identity_downsample(x)

        out += identity
        out = self.relu(out)
        #--CODE END--

        return out

class ResNet50(nn.Module):
    """
    ResNet-50 implementation for the CM2003 course lab.
    
    This class implements the ResNet-50 architecture as described in the paper:
    "Deep Residual Learning for Image Recognition" by He et al.

    Args:
        num_classes (int): Number of classes for the final classification layer. Default is 1000.
        in_channels (int): Number of input channels. Default is 3.
    """

    def __init__(self, num_classes=1000, in_channels=3):
        super(ResNet50, self).__init__()
        
        self.in_channels = 64
        self.conv1 = nn.Conv2d(in_channels, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        # ResNet layers
        self.layer1 = self._make_layer(64, 3, stride=1)
        self.layer2 = self._make_layer(128, 4, stride=2)
        self.layer3 = self._make_layer(256, 6, stride=2)
        self.layer4 = self._make_layer(512, 3, stride=2)

        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 * 4, num_classes)

    def _make_layer(self, out_channels, blocks, stride):
        layers = []
        layers.append(ResNetBlock(self.in_channels, out_channels, stride))
        self.in_channels = out_channels * 4
        for _ in range(1, blocks):
            layers.append(ResNetBlock(self.in_channels, out_channels))
        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)

        return x

