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
from werkzeug.utils import secure_filename
import base64
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

def transform_image_path(imagepath):
    # my_transforms = transforms.Compose([transforms.Resize(255),
    #                                     transforms.CenterCrop(224),
    #                                     transforms.ToTensor(),
    #                                     transforms.Normalize(
    #                                         [0.485, 0.456, 0.406],
    #                                         [0.229, 0.224, 0.225])])
    to_tensor_transform = transforms.ToTensor()
    image = Image.open(imagepath).convert('RGB')
    newsize = (224, 224)
    image = image.resize(newsize)
    image = to_tensor_transform(image)
    return image


def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    y_hat = model(tensor)
    # predicted_idx = str(y_hat.item())
    return str(y_hat.item())

def get_prediction_path(imagepath):
    tensor = transform_image_path(imagepath)
    y_hat = model(tensor)
    # predicted_idx = str(y_hat.item())
    return str(y_hat.item())

@app.route('/', methods=['POST', 'GET'])
def predict():
    # upload_folder = os.path.join('static', 'uploads')
    # app.config['UPLOAD'] = upload_folder

    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        
        estimated_year = get_prediction(image_bytes=img_bytes)
        # print(jsonify({'estimated_year': estimated_year}))
        # filename = secure_filename(file.filename)
        # print('upload_image filename: ' + filename)

        # file.save(os.path.join(app.config['UPLOAD'], filename))
        # img = os.path.join(app.config['UPLOAD'], filename)
        # im = Image.open("test.jpg")
        # data = io.BytesIO(img_bytes)
        # im.save(data, "JPEG")
        # encoded_img_data = base64.b64encode(data.getvalue())
# IMAGE=encoded_img_data.decode('utf-8')
        # image = io.BytesIO(img_bytes).save()
        return render_template('index.html', EST_YEAR = estimated_year, MODEL_SPEAK="'Ah, thank you. What do you think?'")
    else:
        return render_template('index.html', EST_YEAR = '? Year', MODEL_SPEAK = "'Please, I yearn to estimate the dates that photos were taken. Feed my desire!'")

@app.route('/gamePage', methods=['GET'])
def game():
    

    estimated_year_1 = get_prediction_path('static/gamepics/1973.jpg')
    estimated_year_2 = get_prediction_path('static/gamepics/1943.jpg')
    estimated_year_3 = get_prediction_path('static/gamepics/1968.jpg')
    estimated_year_4 = get_prediction_path('static/gamepics/1963Part2.jpg')
    estimated_year_5 = get_prediction_path('static/gamepics/1957.jpg')
    estimated_year_6 = get_prediction_path('static/gamepics/1986.png')
    estimated_year_7 = get_prediction_path('static/gamepics/1974Part2.jpg')
    estimated_year_8 = get_prediction_path('static/gamepics/1983.jpg')

    return render_template('game.html', MODEL_GUESS1=estimated_year_1, MODEL_GUESS2=estimated_year_2, MODEL_GUESS3=estimated_year_3, MODEL_GUESS4=estimated_year_4, MODEL_GUESS5 = estimated_year_5, MODEL_GUESS6= estimated_year_6, MODEL_GUESS7= estimated_year_7, MODEL_GUESS8 = estimated_year_8)

if __name__ == '__main__':
    app.run()