import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from torch.autograd import Variable
from PIL import Image
import requests
from numpy import dot
from numpy.linalg import norm
import numpy as np
from tempfile import TemporaryFile

# Tải mô hình được đào tạo trước
model = models.resnet18(pretrained=True)
# Sử dụng đối tượng mô hình để chọn lớp mong muốn
layer = model._modules.get("avgpool")

model.eval()
# biến đổi hình ảnh
scaler = transforms.Resize((224, 224))
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
to_tensor = transforms.ToTensor()


def get_vector(image_name):
    # 1. Load ảnh bằng thư viện Pillow
    img = Image.open(image_name)
    # 2.Tạo Biến PyTorch với hình ảnh đã chuyển đổi
    t_img = Variable(normalize(to_tensor(scaler(img))).unsqueeze(0))
    # 3. Tạo một vectơ số 0 sẽ chứa vectơ đặc trưng
    #    Lớp 'avgpool' có kích thước đầu ra là 512
    my_embedding = torch.zeros(512)

    # 4.  Xác định chức năng sẽ sao chép đầu ra của một lớp
    def copy_data(m, i, o):
        my_embedding.copy_(o.data.reshape(o.data.size(1)))

    # 5. Đính kèm chức năng đó vào lớp đã chọn
    h = layer.register_forward_hook(copy_data)
    # 6. Chạy mô hình trên hình ảnh đã chuyển đổi
    model(t_img)
    # 7. Tách chức năng sao chép khỏi lớp
    h.remove()
    # 8. Trả về vector đặc trưng
    X = my_embedding.numpy().astype("float64")
    return X


# for loop
# lấy tất cả jpg trong folder -> get_vector -> save npy folder
jpg_folder = "D:/harris/anh_lichsu/"
npy_folder = "D:/harris/npy_lichsu"

import os
from glob import glob

filename_list = glob(os.path.join(jpg_folder, "*.jpg"))

for filename in filename_list:
    print(filename)  # abc.jpg + npy
    vector = get_vector(filename)
    new_name = os.path.join("D:/harris/npy_lichsu", filename.replace("jpg", "") + "npy")
    with open(new_name, "wb") as f:
        print("ahihi")
        print(new_name)
        np.save(f, vector)
