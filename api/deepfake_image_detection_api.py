import uvicorn
import tensorflow as tf
from fastapi import FastAPI, File, UploadFile 
from keras.preprocessing import image
from io import BytesIO
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.config.set_visible_devices([], 'GPU')

from PIL  import Image
import numpy as np

model=tf.keras.models.load_model('imagesdeepfake.h5',) 
class_names=['real','fake']
def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image

app = FastAPI()
@app.post("/predict")
async def predict_api(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png",'webp')
    if not extension:
        return "Image must be jpg or png format!"
 
    img = tf.image.decode_image(await file.read(), channels=3) 
  
    img = tf.image. resize(img, [128,128])
    
    img=image.image_utils.img_to_array(img)
    img=np.expand_dims(img,axis=0)
   
    prediction=model.predict(img)[0]
    predictionclass=class_names[prediction.argmax()]
    if predictionclass =='fake':
        predicted_class='machine generated'
    else:
        predicted_class='this image file is not fake and it is real' 
    result_dict = {'predicted_class': predicted_class}


   

    return result_dict
    @app.post('/')
    async def main(request: Request): 
        return await request.json()

        
            
    

    return {predictionclass}

