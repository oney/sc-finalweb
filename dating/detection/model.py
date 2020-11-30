import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as data
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader
import numpy as np
import os
import random


SEED = 1234

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed(SEED)
torch.backends.cudnn.deterministic = True


class AlexNet(nn.Module):
    '''
    PyTorch neural network model
    '''
    def __init__(self, output_dim):
        '''
        The class initializer

        **Parameters**

            output_dim: *int*
                Dimension of output (classes of targets)

        '''
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv2d(3, 64, 12, 4, 1),
            # in_channels, out_channels, kernel_size, stride, padding
            # in_channels: color channels
            # out_channels: the number of filters
            # kernel_size: scanning kernel size
            # stride: stride when scanning
            # padding: added padding
            # output 2D size calculation: https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html#torch.nn.Conv2d

            nn.MaxPool2d(2),  # kernel_size
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 192, 3, padding=1),
            nn.MaxPool2d(2),
            nn.ReLU(inplace=True),
            # nn.Conv2d(192, 384, 3, padding = 1),
            # nn.ReLU(inplace = True),
            # nn.Conv2d(192, 256, 3, padding = 1),
            # nn.ReLU(inplace = True),
            nn.Conv2d(192, 256, 3, padding=1),
            nn.MaxPool2d(2),
            nn.ReLU(inplace=True)
        )

        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256 * 3 * 3, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, output_dim),
        )

    def forward(self, x):
        '''
        Forward computation of the CNN

        **Parameters**

            x: *<torch.Tensor[batch size, color channels, width, height]>*
                A batch of tensor inputs

        **Returns**

            x: *<torch.Tensor[batch size, output dim]>*
                A batch of tensor prediction

            h: *<torch.Tensor[batch size, output dim]>*
                A batch of tensor Conv2d output

        '''
        x = self.features(x)
        h = x.view(x.shape[0], -1)
        x = self.classifier(h)
        return x, h


model = AlexNet(2)
device = torch.device('cpu')
model = model.to(device)
dir_path = os.path.dirname(os.path.realpath(__file__))
# Load trained model
model.load_state_dict(torch.load(
    os.path.join(dir_path, 'best.pt'),
    map_location=device))


class EvaluateDataset(Dataset):
    '''
    Dataset for evaluation
    '''
    def __init__(self, image):
        '''
        The class initializer

        **Parameters**

            image: *numpy.ndarray[width, height, color channels]*
                Numpy array of an image

        '''
        self.image = image
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            ])

    def __len__(self):
        '''
        Return size of the dataset

        **Returns**
            len: size of the dataset

        '''
        return 1

    def __getitem__(self, idx):
        '''
        Return an item (image tensor and label) of dataset by idx

        **Parameters**

            idx: *int*
                The index of getting item

        **Returns**

            item: *<list, (torch.Tensor[color channels, width, height], int)>*
                Image tensor and label (0 or 1) in a list

        '''
        image = self.transform(self.image)
        return [image, 1]


def predict(iterator):
    '''
    Predict a batch of images

    **Parameters**

        iterator: *torch.utils.data.dataloader.DataLoader*
            A batch of images

    **Returns**

        probability: *<torch.Tensor[batch size, float]>*
            A batch of probability of each prediction

        prediction: *<torch.Tensor[batch size, int]>*
            A batch of prediction (0 or 1)

    '''
    model.eval()
    # No need to track gradients in evaluation
    with torch.no_grad():
        for (x, _) in iterator:
            x = x.to(device)
            y_pred, _ = model(x)
            y_prob = F.softmax(y_pred, dim=-1)
            # Get the label of the highest probability
            top_pred = y_prob.argmax(1, keepdim=True)

            return y_prob, top_pred


def predict_one(image):
    '''
    Predict an image

    **Parameters**

        image: *numpy.ndarray[width, height, color channels]*
            Numpy array of an image

    **Returns**

        prediction: *int*
            Prediction (0 or 1)

        probability: *<numpy.ndarray[float]>*
            Probability of each prediction

    '''
    dataset = EvaluateDataset(image)
    # Generate subset dataset from dataset for prediction
    split_data, _ = data.random_split(dataset, [1, 0])
    iterator = data.DataLoader(split_data, batch_size=1)
    prob, pred = predict(iterator)
    # Extract the prediction and probability from the batch
    return pred[0][0].item(), prob[0].numpy()
