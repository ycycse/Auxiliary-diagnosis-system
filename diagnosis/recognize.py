from models.recognize.code.model import *
import torch
from PIL import Image
from torchvision import transforms
from torch.autograd import Variable
import h5py
import numpy as np
import os

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print('Loadinging model...\n')
model = CovidNet(bna=True, bnd=True, hidden_size=1024, emmbedding_size=128).to(device)

model.load_state_dict(
    torch.load('models/recognize/code/saved/cont/best_checkpoint.pth', map_location=str(device))['state_dict'])
model.eval()


def recognize(img_root):
    print(img_root)
    img = Image.open(img_root).convert('RGB')
    site = 'ucsd'
    trans = transforms.Compose(
        [transforms.Resize([224, 224]),
         transforms.ToTensor(),
         transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
    pred, prob = predict(img, site, trans)
    print(pred, prob)
    return pred


def predict(img, site, trans):
    d = ['阴性', '阳性']
    input = trans(img)
    img = input.unsqueeze(0)

    input = Variable(img.to(device))
    score, features = model(input, site)
    probability = torch.nn.functional.softmax(score, dim=1)
    max_value, index = torch.max(probability, 1)

    return d[index.item()], probability
