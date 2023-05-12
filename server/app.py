import io
import json
import torch
from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request, render_template
import os 
from PIL import Image
import torch.nn as nn
import math

app = Flask(__name__)

class MyCNN(nn.Module):

    def __init__(self, input_size, output_size):
        super(MyCNN, self).__init__()

        self.input_size = input_size 

        self.conv1 = nn.Conv2d(in_channels=3, out_channels=8, kernel_size=(5,5), stride=3)
        self.conv2 = nn.Conv2d(in_channels=8, out_channels=16, kernel_size=(3,3), stride=1)

        self.relu = nn.ReLU() 
#         72*72*16 approx 83,000
        cnn_out_size =  int((((math.sqrt(input_size) - 5 )//3 + 1 - 3 + 1)**2) * 16)    
        self.lin1 = nn.Linear(cnn_out_size, 2500)
        self.lin2 = nn.Linear(2500, 1)

    def forward(self, x):
        x = x.view(-1, 3, 224, 224)   # This reshapes the input to work with the batches

        x = self.conv1(x)
        x = self.relu(x)
        x = self.conv2(x)
        x = self.relu(x)

        x = x.flatten(start_dim=1) 
        
        x = self.lin1(x)  
        x = self.relu(x)
        x = self.lin2(x)  
#         out = self.relu(out)
#         out = self.lin3(out)  
        # get integer year estimates
#         out = out.round()
        return x
    
    #.round()
# imagenet_class_index = json.load(open('<PATH/TO/.json/FILE>/imagenet_class_index.json'))
weights_path = '../models/fullmodelbestsofar.pt'
model = MyCNN(50176, 1)    

if(os.path.exists(weights_path)):
    model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))
    print("Loaded pretrained date estimator")
else:
    print(f"No weights found at: {weights_path}")
    exit()

def transform_image(image_bytes):
    # my_transforms = transforms.Compose([transforms.Resize(255),
    #                                     transforms.CenterCrop(224),
    #                                     transforms.ToTensor(),
    #                                     transforms.Normalize(
    #                                         [0.485, 0.456, 0.406],
    #                                         [0.229, 0.224, 0.225])])
    to_tensor_transform = transforms.ToTensor()
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    newsize = (224, 224)
    image = image.resize(newsize)
    image = to_tensor_transform(image)
    return image


def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    y_hat = model(tensor)
    # predicted_idx = str(y_hat.item())
    return str(y_hat.item())


@app.route('/', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        estimated_year = get_prediction(image_bytes=img_bytes)
        print(jsonify({'estimated_year': estimated_year}))
        return jsonify({'estimated_year': estimated_year})
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()