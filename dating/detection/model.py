import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.optim.lr_scheduler import _LRScheduler
import torch.utils.data as data

import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader

import numpy as np

import os
import random
import time


SEED = 1234

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed(SEED)
torch.backends.cudnn.deterministic = True


class AlexNet(nn.Module):
    def __init__(self, output_dim):
        super().__init__()
        
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, 12, 4, 1), #in_channels, out_channels, kernel_size, stride, padding
            nn.MaxPool2d(2), #kernel_size
            nn.ReLU(inplace = True),
            nn.Conv2d(64, 192, 3, padding = 1),
            nn.MaxPool2d(2),
            nn.ReLU(inplace = True),
            # nn.Conv2d(192, 384, 3, padding = 1),
            # nn.ReLU(inplace = True),
            # nn.Conv2d(192, 256, 3, padding = 1),
            # nn.ReLU(inplace = True),
            nn.Conv2d(192, 256, 3, padding = 1),
            nn.MaxPool2d(2),
            nn.ReLU(inplace = True)
        )
        
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256 * 3 * 3, 4096),
            nn.ReLU(inplace = True),
            nn.Dropout(0.5),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace = True),
            nn.Linear(4096, output_dim),
        )

    def forward(self, x):
        x = self.features(x)
        h = x.view(x.shape[0], -1)
        x = self.classifier(h)
        return x, h


OUTPUT_DIM = 2

model = AlexNet(2)

device = torch.device('cpu')
model = model.to(device)

dir_path = os.path.dirname(os.path.realpath(__file__))

model.load_state_dict(torch.load(
    os.path.join(dir_path, 'best.pt'),
    map_location=device))


class EvaluateDataset(Dataset):
    def __init__(self, image):
        self.image = image
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            ])

    def __len__(self):
        return 1

    def __getitem__(self, idx):
        image = self.transform(self.image)
        return [image, 1]


def predict(iterator):
    model.eval()
    with torch.no_grad():
        for (x, y) in iterator:
            x = x.to(device)

            y_pred, _ = model(x)

            y_prob = F.softmax(y_pred, dim = -1)
            top_pred = y_prob.argmax(1, keepdim = True)

            return y_prob, top_pred


def predict_one(image):
    dataset = EvaluateDataset(image)
    split_data, _ = data.random_split(dataset, [1, 0])
    iterator = data.DataLoader(split_data, batch_size=1)
    prob, pred = predict(iterator)
    return pred[0][0].item(), prob[0].numpy()