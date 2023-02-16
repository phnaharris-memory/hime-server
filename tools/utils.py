import pathlib
from fastapi import UploadFile
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from torch.autograd import Variable
from PIL import Image

import shutil
import numpy as np
from numpy import dot
from numpy.linalg import norm
from bs4 import BeautifulSoup


class Embedded:
    def __init__(self) -> None:

        self.model = models.resnet18(pretrained=True)
        self.layer = self.model._modules.get("avgpool")

        self.model.eval()
        self.scaler = transforms.Resize((224, 224))
        self.normalize = transforms.Normalize(
            mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
        )
        self.to_tensor = transforms.ToTensor()

    def get_vector(self, image_name):
        print("image_name ne")
        print(image_name)
        # img = Image.open(image_name)
        img = Image.open(image_name)
        print("img ne")
        print(img)
        t_img = Variable(self.normalize(self.to_tensor(self.scaler(img))).unsqueeze(0))
        my_embedding = torch.zeros(512)

        def copy_data(m, i, o):
            my_embedding.copy_(o.data.reshape(o.data.size(1)))

        h = self.layer.register_forward_hook(copy_data)
        self.model(t_img)
        h.remove()
        X = my_embedding.numpy().astype("float64")
        return X


def cosine_similarity(vec_a, vec_b):
    return dot(vec_a, vec_b) / (norm(vec_a) * norm(vec_b))


def parse_text_from_html(html_str):
    soup = BeautifulSoup(html_str, features="html.parser")
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines()[1:])
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "\n".join(chunk for chunk in chunks if chunk)
    return text


def load_vector_from_path_db(PATH):
    print("load_vector_from_path_db")
    print(PATH)
    # return np.load(PATH, dtype=np.float64)
    return np.load(PATH)


def save_upload_file(upload_file: UploadFile, destination: pathlib.Path) -> None:
    with destination.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
