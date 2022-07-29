# -*- coding: utf-8 -*-
import os
import argparse
import tifffile as tiff
import matplotlib.pyplot as plt
from PIL import Image
import torch
import torchvision.transforms as transforms
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

parser = argparse.ArgumentParser(description='mvtec3d')
parser.add_argument('--obj', type=str, default='cookie')
args = parser.parse_args()

xyz_dir = f'/data/dataset/jikuya/mvtec3d/{args.obj}/train/good/xyz'
rgb_dir = f'/data/dataset/jikuya/mvtec3d/{args.obj}/train/good/rgb'
output_dir = f'outputs/{args.obj}'
os.makedirs(output_dir, exist_ok=True)

transform = transforms.Compose([
    #transforms.Resize((224, 224)),
    transforms.ToTensor()
])

sorted_xyz_dir = sorted(os.listdir(xyz_dir))
for file_name in sorted_xyz_dir:
    #print(os.path.isfile(f'{xyz_dir}/{file_name}'))
    xyz_img = tiff.imread(f'{xyz_dir}/{file_name}')
    rgb_img = Image.open(f'{rgb_dir}/{os.path.splitext(file_name)[0]}.png')
    xyz_img_tensor = torch.tensor(xyz_img).permute(2, 0, 1).unsqueeze(dim=0)
    rgb_img_tensor = transform(rgb_img).unsqueeze(dim=0)
    xyz_img = torch.nn.functional.interpolate(xyz_img_tensor, size=(224, 224),mode='nearest').squeeze()
    rgb_img = torch.nn.functional.interpolate(rgb_img_tensor, size=(224, 224),mode='nearest').squeeze()
    print(xyz_img.shape, rgb_img.shape)
    rgb = rgb_img.permute(1,2,0).view(-1,3)
    print(rgb_img.shape)

    #描画エリアの作成
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    x = xyz_img[0].view(-1)
    y = xyz_img[1].view(-1)
    z = xyz_img[2].view(-1)
    x = x[z>0.5]
    y = y[z>0.5]
    rgb = rgb[z>0.5]
    z = z[z>0.5]
    
    print(x.shape, rgb.shape)
    #散布図の作成
    ax.scatter(x[z<0.75],y[z<0.75],-1*z[z<0.75],s=1,c=rgb[z<0.75])
    
    #描画
    #plt.show()
    def plt_graph3d(angle):
        ax.view_init(30, -2*angle)

    ani = animation.FuncAnimation(fig, func=plt_graph3d, frames=100, interval=120)
    ani.save(os.path.join(output_dir, f'{os.path.splitext(file_name)[0]}.gif'), writer="pillow")

    print(f'finished : {output_dir} {os.path.splitext(file_name)[0]}.gif')

    break