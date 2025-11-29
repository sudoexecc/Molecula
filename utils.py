from PIL import Image, ImageDraw, ImageFont
import random

def draw_detections(image, detections):
    """
    Draws bounding boxes and labels on the image.
    """
    draw = ImageDraw.Draw(image)
    
    # Colors for classes
    colors = {
        'RBC': '#ff4b4b',      # Red
        'WBC': '#9d00ff',      # Purple
        'Platelets': '#ffa600' # Orange
    }
    
    try:
        # Try to load a font, fallback to default
        font = ImageFont.truetype("arial.ttf", 15)
    except IOError:
        font = ImageFont.load_default()

    for det in detections:
        bbox = det['bbox']
        cls = det['class']
        conf = det['confidence']
        color = colors.get(cls, '#ffffff')
        
        # Draw Box
        draw.rectangle(bbox, outline=color, width=2)
        
        # Draw Label
        label = f"{cls}"
        if cls == 'WBC':
            label += f" ({det['subtype']})"
            
        # Draw label background
        text_bbox = draw.textbbox((bbox[0], bbox[1]-15), label, font=font)
        draw.rectangle(text_bbox, fill=color)
        draw.text((bbox[0], bbox[1]-15), label, fill="white", font=font)
        
    return image

def crop_wbcs(image, detections):
    """
    Returns a list of cropped WBC images with their subtype labels.
    """
    crops = []
    for det in detections:
        if det['class'] == 'WBC':
            bbox = det['bbox']
            # Crop: (left, upper, right, lower)
            crop = image.crop((bbox[0], bbox[1], bbox[2], bbox[3]))
            crops.append({'image': crop, 'subtype': det['subtype']})
    return crops
