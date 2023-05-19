import os
import torch
from torchvision.transforms import transforms
from nn.model import MNISTNet
from dotenv import load_dotenv

load_dotenv()

MODEL_PATH = os.getenv('MODEL_PATH')


class MNISTModel:

    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Loading model for device {self.device}")
        self.model = MNISTNet()
        self.model.load_state_dict(torch.load(MODEL_PATH))
        self.model = self.model.eval()
        self.model = self.model.to(self.device)

    def predict(self, image_data):
        preprocessed_image_data = self._preprocess(image_data)
        prediction = self._predict(preprocessed_image_data)
        return prediction

    def _preprocess(self, image_data):
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Grayscale(),
            transforms.Resize(28),
            transforms.CenterCrop(28),
            transforms.Normalize((0.1307,), (0.3081,)),
        ])
        tensor = transform(image_data)
        return torch.unsqueeze(tensor, dim=0)

    def _predict(self, image_data):
        with torch.inference_mode():
            data = image_data.to(self.device)
            output = self.model(data)
            pred = output.argmax(dim=1, keepdim=True)
            return pred.item()


