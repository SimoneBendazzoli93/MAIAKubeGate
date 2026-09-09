from monai.networks.nets import UNet
from monai.networks.layers import Norm

def get_unet_model(in_channels=4, out_channels=3):
    """
    Create and return a simple UNET model using MONAI.
    
    Args:
        in_channels (int): Number of input channels. Default is 1 for grayscale images.
        out_channels (int): Number of output channels. Default is 1 for binary segmentation.
    
    Returns:
        monai.networks.nets.UNet: The UNET model.
    """
    model = UNet(
        spatial_dims=2,
        in_channels=in_channels,
        out_channels=out_channels,
        channels=(32, 64, 128, 256),
        strides=(2, 2, 2),
        num_res_units=2,
        norm=Norm.BATCH,
    )
    
    return model
