from torch import nn, load, rand, random
import torchvision
import io
import numpy as np


class Generator(nn.Module):
    def __init__(self, latent_dim, img_shape):
        super(Generator, self).__init__()
        self.img_shape = img_shape

        def normBlock(in_feat, out_feat, normalize=True):
            layers = [nn.Linear(in_feat, out_feat)]
            if normalize:
                layers.append(nn.BatchNorm1d(out_feat, 0.8))
            layers.append(nn.LeakyReLU(0.1, inplace=True))
            return layers

        self.model = nn.Sequential(
            *normBlock(latent_dim, 1024, normalize=False),
            *normBlock(1024, 2048, normalize=False),
            nn.Linear(2048, int(np.prod(img_shape))),
            nn.Tanh(),
        )

    def forward(self, z):
        img = self.model(z)
        img = img.view(-1, *self.img_shape)
        return img

def create_mnist_image_from_noise(model, generator):
    noise = (rand(1, 128, generator=generator) - 0.5) / 0.5
    output = model.forward(noise)[0][0]
    image = torchvision.transforms.ToPILImage()(output.unsqueeze(0))
    return_image = io.BytesIO()
    image.save(return_image, "JPEG")
    return_image.seek(0)
    return return_image.read()

def load_generator_from_file(filename: str = "web_app/models/generator.pth") -> Generator:
    return load(filename)