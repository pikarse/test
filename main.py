from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)

# Пути к файлам данных
MARKERS_FILE = 'zmarkers.json'
COMMENTS_FILE = 'comments.json'
ROUTES_FILE = 'routes.json'

def load_data(filename):
    """Загружает данные из JSON файла"""
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(data, filename):
    """Сохраняет данные в JSON файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/api/markers', methods=['GET'])
def get_markers():
    """Получить все метки"""
    markers = load_data(MARKERS_FILE)
    return jsonify(markers)

@app.route('/api/markers', methods=['POST'])
def add_marker():
    """Добавить новую метку"""
    data = request.json
    
    # Валидация данных
    required_fields = ['lat', 'lng', 'comment', 'rating']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Отсутствует обязательное поле: {field}'}), 400
    
    # Создание новой метки
    marker = {
        'id': str(uuid.uuid4()),
        'lat': float(data['lat']),
        'lng': float(data['lng']),
        'comment': data['comment'],
        'rating': int(data['rating']),
        'city': data.get('city', 'Неизвестный город'),
        'timestamp': data.get('timestamp', datetime.now().isoformat()),
        'user_id': data.get('user_id', 'anonymous')
    }
    
    # Загрузка существующих меток и добавление новой
    markers = load_data(MARKERS_FILE)
    markers.append(marker)
    save_data(markers, MARKERS_FILE)
    
    return jsonify(marker), 201

@app.route('/api/markers/<marker_id>/comments', methods=['GET'])
def get_marker_comments(marker_id):
    """Получить комментарии к метке"""
    comments = load_data(COMMENTS_FILE)
    marker_comments = [c for c in comments if c.get('marker_id') == marker_id]
    return jsonify(marker_comments)

@app.route('/api/markers/<marker_id>/comments', methods=['POST'])
def add_comment(marker_id):
    """Добавить комментарий к метке"""
    data = request.json
    
    # Валидация данных
    if 'comment' not in data:
        return jsonify({'error': 'Отсутствует текст комментария'}), 400
    
    # Проверка существования метки
    markers = load_data(MARKERS_FILE)
    marker_exists = any(m['id'] == marker_id for m in markers)
    if not marker_exists:
        return jsonify({'error': 'Метка не найдена'}), 404
    
    # Создание нового комментария
    comment = {
        'id': str(uuid.uuid4()),
        'marker_id': marker_id,
        'comment': data['comment'],
        'rating': data.get('rating', 0),
        'timestamp': data.get('timestamp', datetime.now().isoformat()),
        'user_id': data.get('user_id', 'anonymous')
    }
    
    # Загрузка существующих комментариев и добавление нового
    comments = load_data(COMMENTS_FILE)
    comments.append(comment)
    save_data(comments, COMMENTS_FILE)
    
    return jsonify(comment), 201

@app.route('/api/markers/<marker_id>', methods=['DELETE'])
def delete_marker(marker_id):
    """Удалить метку и все её комментарии"""
    # Загрузка меток
    markers = load_data(MARKERS_FILE)
    markers = [m for m in markers if m['id'] != marker_id]
    save_data(markers, MARKERS_FILE)
    
    # Удаление комментариев к метке
    comments = load_data(COMMENTS_FILE)
    comments = [c for c in comments if c.get('marker_id') != marker_id]
    save_data(comments, COMMENTS_FILE)
    
    return jsonify({'message': 'Метка удалена'}), 200

@app.route('/api/markers/<marker_id>', methods=['PUT'])
def update_marker(marker_id):
    """Обновить метку"""
    data = request.json
    
    markers = load_data(MARKERS_FILE)
    for marker in markers:
        if marker['id'] == marker_id:
            # Обновляем только разрешенные поля
            if 'comment' in data:
                marker['comment'] = data['comment']
            if 'rating' in data:
                marker['rating'] = int(data['rating'])
            marker['updated_at'] = datetime.now().isoformat()
            save_data(markers, MARKERS_FILE)
            return jsonify(marker)
    
    return jsonify({'error': 'Метка не найдена'}), 404

@app.route('/api/cities/<city>/markers', methods=['GET'])
def get_city_markers(city):
    """Получить метки для конкретного города"""
    markers = load_data(MARKERS_FILE)
    city_markers = [m for m in markers if m.get('city', '').lower() == city.lower()]
    return jsonify(city_markers)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Получить статистику"""
    markers = load_data(MARKERS_FILE)
    comments = load_data(COMMENTS_FILE)
    routes = load_data(ROUTES_FILE)
    
    stats = {
        'total_markers': len(markers),
        'total_comments': len(comments),
        'total_routes': len(routes),
        'cities': list(set(m.get('city', '') for m in markers if m.get('city'))),
        'average_rating': sum(m.get('rating', 0) for m in markers) / len(markers) if markers else 0
    }
    
    return jsonify(stats)

# API для маршрутов
@app.route('/api/routes', methods=['GET'])
def get_routes():
    """Получить все маршруты"""
    routes = load_data(ROUTES_FILE)
    return jsonify(routes)

@app.route('/api/routes', methods=['POST'])
def create_route():
    """Создать новый маршрут"""
    data = request.json
    
    # Валидация данных
    if 'coordinates' not in data:
        return jsonify({'error': 'Отсутствуют координаты маршрута'}), 400
    
    route = {
        'id': str(uuid.uuid4()),
        'coordinates': data['coordinates'],
        'user_id': data.get('user_id', 'anonymous'),
        'created_at': data.get('created_at', datetime.now().isoformat())
    }
    
    routes = load_data(ROUTES_FILE)
    routes.append(route)
    save_data(routes, ROUTES_FILE)
    
    return jsonify(route), 201

@app.route('/api/routes/<route_id>', methods=['GET'])
def get_route(route_id):
    """Получить конкретный маршрут"""
    routes = load_data(ROUTES_FILE)
    route = next((r for r in routes if r['id'] == route_id), None)
    
    if not route:
        return jsonify({'error': 'Маршрут не найден'}), 404
    
    return jsonify(route)

@app.route('/api/routes/<route_id>', methods=['DELETE'])
def delete_route(route_id):
    """Удалить маршрут"""
    routes = load_data(ROUTES_FILE)
    routes = [r for r in routes if r['id'] != route_id]
    save_data(routes, ROUTES_FILE)
    
    return jsonify({'message': 'Маршрут удален'}), 200

@app.route('/api/comments/<comment_id>', methods=['PUT'])
def update_comment(comment_id):
    """Обновить комментарий"""
    data = request.json
    
    comments = load_data(COMMENTS_FILE)
    for comment in comments:
        if comment['id'] == comment_id:
            # Обновляем только разрешенные поля
            if 'comment' in data:
                comment['comment'] = data['comment']
            if 'rating' in data:
                comment['rating'] = int(data['rating'])
            comment['updated_at'] = datetime.now().isoformat()
            save_data(comments, COMMENTS_FILE)
            return jsonify(comment)
    
    return jsonify({'error': 'Комментарий не найден'}), 404

@app.route('/api/comments/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """Удалить комментарий"""
    comments = load_data(COMMENTS_FILE)
    comments = [c for c in comments if c['id'] != comment_id]
    save_data(comments, COMMENTS_FILE)
    
    return jsonify({'message': 'Комментарий удален'}), 200

@app.route('/')
def health_check():
    """Проверка здоровья сервиса"""
    return jsonify({'status': 'ok', 'service': 'russia-map-backend'})

if __name__ == '__main__':
    # Создаем файлы данных, если они не существуют
    for filename in [MARKERS_FILE, COMMENTS_FILE, ROUTES_FILE]:
        if not os.path.exists(filename):
            save_data([], filename)
    
    # Получаем порт из переменной окружения или используем 5000
    port = int(os.environ.get('PORT', 5000))
    
    app.run(host='0.0.0.0', port=port, debug=False) 
