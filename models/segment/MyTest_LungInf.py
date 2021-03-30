import torch
import torch.nn.functional as F
import numpy as np
import os
import argparse
from scipy import misc
from Code.model_lung_infection.InfNet_Res2Net import Inf_Net as Network
from Code.utils.dataloader_LungInf import test_dataset
import matplotlib.pyplot as plt
from skimage import measure,draw
from PIL import Image

def show_label(label,name):
    img = misc.toimage(label,cmin=0.0,cmax=1.0)
    img =img.convert('RGBA')
    x, y = img.size
    for i in range(x):
        for j in range(y):
            color = img.getpixel((i, j))
            Mean = np.mean(list(color[:-1]))
            if Mean < 100:
                color = (255, 97, 0, 0)
            elif Mean < 200:
                color = (255, 97, 0, 200)
            else:
                color = (0, 0, 128, 200)
            img.putpixel((i, j), color)

    img.save(name)
    return img

def inference(image_root):
    parser = argparse.ArgumentParser()
    parser.add_argument('--testsize', type=int, default=352, help='testing size')
    parser.add_argument('--data_path', type=str, default='./Dataset/TestingSet/LungInfection-Test/',
                        help='Path to test data')
    parser.add_argument('--pth_path', type=str, default='./Snapshots/save_weights/Inf-Net/Inf-Net-100.pth',
                        help='Path to weights file. If `semi-sup`, edit it to `Inf-Net/Inf-Net-100.pth`')
    parser.add_argument('--save_path', type=str, default='./Results/Lung infection segmentation/Inf-Net/Labels/',
                        help='Path to save the predictions. if `semi-sup`, edit it to `Inf-Net`')
    parser.add_argument('--save_path_append', type=str, default='./Results/Lung infection segmentation/Inf-Net/Append_result/',
                        help='Path to save the predictions. if `semi-sup`, edit it to `Inf-Net`')
    parser.add_argument('--save_path_mask', type=str, default='./Results/Lung infection segmentation/Inf-Net/Mask/',
                        help='Path to save the predictions. if `semi-sup`, edit it to `Inf-Net`')
    opt = parser.parse_args()
    model = Network()
    # model = torch.nn.DataParallel(model, device_ids=[0, 1]) # uncomment it if you have multiply GPUs.
    model.load_state_dict(torch.load(opt.pth_path, map_location={'cuda:1':'cuda:0'}))
    model.cuda()
    model.eval()

     # gt_root = '{}/GT/'.format(opt.data_path)
    test_loader = test_dataset(image_root, opt.testsize)
    os.makedirs(opt.save_path, exist_ok=True)

    image, name = test_loader.load_data()
    image = image.cuda()

    lateral_map_5, lateral_map_4, lateral_map_3, lateral_map_2, lateral_edge = model(image)

    res = lateral_map_2
    # res = F.upsample(res, size=(ori_size[1],ori_size[0]), mode='bilinear', align_corners=False)
    res = res.sigmoid().data.cpu().numpy().squeeze()
    res = (res - res.min()) / (res.max() - res.min() + 1e-8)
    print(name)
    misc.imsave(opt.save_path + name, res)
    icon = show_label(res,opt.save_path_mask + name)
    img = Image.open(image_root)
    img = img.convert("RGBA")
    img_w, img_h = img.size
    icon = icon.resize((img_w,img_h ), Image.ANTIALIAS)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    layer.paste(icon, (0, 0))
    out = Image.composite(layer, img, layer)
    out.save(opt.save_path_append + name)
    print('Test Done!')



if __name__ == "__main__":
    image_root = "test.jpg"
    inference(image_root)
