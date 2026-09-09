import torch
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

class GradCAM:
    """
    Gradient-weighted Class Activation Mapping (Grad-CAM) implementation.
    
    This class implements the Grad-CAM technique for visualizing the regions of input 
    that are important for predictions from CNN-based models.
    """

    def __init__(self, model, target_layer):
        """
        Initialize the GradCAM object.

        Args:
            model (torch.nn.Module): The model to analyze.
            target_layer (torch.nn.Module): The target layer to generate CAM for.
        """
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        
        # Register hooks to capture activations and gradients
        target_layer.register_forward_hook(self.save_activation)
        target_layer.register_backward_hook(self.save_gradient)
    
    def save_activation(self, module, input, output):
        """Save the activations of the target layer."""
        self.activations = output.detach()
    
    def save_gradient(self, module, grad_input, grad_output):
        """Save the gradients of the target layer."""
        self.gradients = grad_output[0].detach()
    
    def generate_cam(self, input_image, target_class):
        """
        Generate the Class Activation Map (CAM) for the target class.

        Args:
            input_image (torch.Tensor): Input image tensor.
            target_class (int): Index of the target class.

        Returns:
            torch.Tensor: The generated heatmap.
        """
        # Forward pass
        output = self.model(input_image)
        
        # Clear gradients
        self.model.zero_grad()
        
        # Compute the mean of the target class output
        target_output = output[:, target_class].mean()
        
        # Backward pass to compute gradients
        target_output.backward()
        
        # Generate CAM
        pooled_gradients = torch.mean(self.gradients, dim=[0, 2, 3])
        for i in range(self.activations.shape[1]):
            self.activations[:, i, :, :] *= pooled_gradients[i]
        
        heatmap = torch.mean(self.activations, dim=1).squeeze()
        heatmap = torch.relu(heatmap)  # Apply ReLU to focus on features that have a positive influence on the class of interest
        heatmap /= torch.max(heatmap)  # Normalize the heatmap
        
        return heatmap


def apply_cam(image, label, cam, class_idx, prediction):
    """
    Apply the generated CAM to the original image and visualize the results.

    Args:
        image (torch.Tensor): Original input image.
        label (torch.Tensor): Ground truth label.
        cam (torch.Tensor): Generated Class Activation Map.
        class_idx (int): Index of the class being visualized.
        prediction (torch.Tensor): Model's prediction.
    """
    # Convert tensors to numpy arrays
    cam = cam.cpu().numpy()
    image = image.squeeze().cpu().numpy()
    label = label.squeeze().cpu().long().numpy()
    prediction = prediction.squeeze().cpu().numpy()

    # Create a custom colormap for the heatmap
    colors = ['navy', 'blue', 'cyan', 'yellow', 'red']
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list('custom', colors, N=n_bins)

    plt.figure(figsize=(20, 5))

    plt.subplot(1, 4, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(1, 4, 2)
    plt.imshow(label == class_idx, cmap='gray')
    plt.title(f'Label for Class {class_idx}')
    plt.axis('off')
    
    plt.subplot(1, 4, 3)
    plt.imshow(prediction == class_idx, cmap='gray')
    plt.title(f'Prediction for Class {class_idx}')
    plt.axis('off')
    
    plt.subplot(1, 4, 4)
    plt.imshow(image, cmap='gray')
    heatmap = plt.imshow(cam, cmap=cmap, alpha=0.7)
    plt.colorbar(heatmap, fraction=0.046, pad=0.04)
    plt.title(f'Attention Map for Class {class_idx}')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()
