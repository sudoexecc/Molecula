import random
import numpy as np

class SimulatedDetector:
    """
    Mocks the behavior of a YOLOv7 model for blood smear analysis.
    Generates deterministic random detections based on image hash/size.
    """
    def __init__(self):
        self.classes = ['RBC', 'WBC', 'Platelets']
        self.wbc_subtypes = [
            'Neutrophil', 'Lymphocyte', 'Monocyte', 
            'Eosinophil', 'Basophil', 'Blast', 
            'Promyelocyte', 'Myelocyte', 'Metamyelocyte', 
            'Band Neutrophil', 'Reactive Lymphocyte'
        ]

    def detect(self, image):
        """
        Generates mock detections for a given image.
        Returns:
            list of dicts: {'bbox': [x1, y1, x2, y2], 'class': str, 'confidence': float, 'subtype': str (optional)}
        """
        width, height = image.size
        # Seed random generator with image dimensions to be deterministic per image size
        # In a real app, we'd use image hash, but size is enough for this demo
        random.seed(width * height)
        
        detections = []
        
        # 1. Generate RBCs (High count)
        num_rbc = random.randint(50, 150)
        for _ in range(num_rbc):
            w = random.randint(30, 60)
            h = w + random.randint(-5, 5)
            x = random.randint(0, width - w)
            y = random.randint(0, height - h)
            detections.append({
                'bbox': [x, y, x+w, y+h],
                'class': 'RBC',
                'confidence': random.uniform(0.7, 0.99)
            })

        # 2. Generate WBCs (Low count, larger size)
        num_wbc = random.randint(2, 8)
        for _ in range(num_wbc):
            w = random.randint(80, 150)
            h = w + random.randint(-10, 10)
            x = random.randint(0, width - w)
            y = random.randint(0, height - h)
            
            # Assign random subtype
            subtype = random.choice(self.wbc_subtypes)
            
            detections.append({
                'bbox': [x, y, x+w, y+h],
                'class': 'WBC',
                'subtype': subtype,
                'confidence': random.uniform(0.85, 0.99)
            })

        # 3. Generate Platelets (Medium count, small size)
        num_platelets = random.randint(10, 30)
        for _ in range(num_platelets):
            w = random.randint(15, 25)
            h = w + random.randint(-3, 3)
            x = random.randint(0, width - w)
            y = random.randint(0, height - h)
            detections.append({
                'bbox': [x, y, x+w, y+h],
                'class': 'Platelets',
                'confidence': random.uniform(0.6, 0.95)
            })
            
        return detections

    def get_disease_flags(self, detections):
        """
        Generates mock disease flags based on counts or random chance.
        """
        counts = {'RBC': 0, 'WBC': 0, 'Platelets': 0}
        wbc_subtypes = {}
        
        for d in detections:
            cls = d['class']
            counts[cls] = counts.get(cls, 0) + 1
            if cls == 'WBC':
                sub = d.get('subtype')
                wbc_subtypes[sub] = wbc_subtypes.get(sub, 0) + 1

        flags = []
        
        # Mock Logic for Flags
        if counts['WBC'] > 6:
            flags.append({
                'title': 'Leukocytosis Pattern',
                'description': 'Elevated WBC count detected. In clinical settings, this may indicate infection or inflammation.',
                'severity': 'warning'
            })
            
        if counts['Platelets'] < 15:
            flags.append({
                'title': 'Thrombocytopenia Pattern',
                'description': 'Low platelet count detected. This simulation suggests further review for clotting issues.',
                'severity': 'warning'
            })
            
        # Random "Rare" Flags for Demo
        if random.random() < 0.2:
             flags.append({
                'title': 'Malaria Parasite Pattern',
                'description': 'Visual anomaly resembling Plasmodium species detected inside RBCs. (PROTOTYPE ONLY)',
                'severity': 'danger'
            })
            
        if 'Blast' in wbc_subtypes:
             flags.append({
                'title': 'Blast Cells Detected',
                'description': 'Presence of immature WBCs (Blasts). This is a critical finding often associated with Leukemia.',
                'severity': 'danger'
            })

        return flags, counts, wbc_subtypes
