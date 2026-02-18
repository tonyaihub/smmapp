import requests
import base64
import config

def publish_to_wp(title, content, meta_desc, images, status='publish'):
    auth = base64.b64encode(f"{config.WORDPRESS_USER}:{config.WORDPRESS_PASS}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/json'
    }
    data = {
        'title': title,
        'content': content + ''.join([f'<img src="{img}" alt="{title}">' for img in images]),
        'status': status,  # 'draft' for review
        'excerpt': meta_desc
    }
    response = requests.post(f"{config.WORDPRESS_URL}/posts", headers=headers, json=data)
    return response.json()