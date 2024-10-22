from flask import Flask, jsonify, make_response
import redis
import json

app = Flask(__name__)

# Cấu hình kết nối Redis
redis_host = 'localhost'  # Thay bằng host của Redis nếu khác
redis_port = 6379         # Thay bằng port của Redis nếu khác

# Kết nối đến Redis
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)

# Hàm giả định để lấy tất cả người dùng từ cơ sở dữ liệu
def get_all_users_from_db():
    # Đây là dữ liệu mẫu thay cho việc truy vấn cơ sở dữ liệu
    return [
        {"id": 1, "name": "User 1"},
        {"id": 2, "name": "User 2"},
        {"id": 3, "name": "User 3"}
    ]

# Route API để lấy tất cả người dùng và cache vào Redis
@app.route('/users/', methods=['GET'])
def get_users():
    try:
        # Kiểm tra xem dữ liệu có tồn tại trong Redis không
        cached_users = redis_client.get('all_users')
        
        if cached_users:
            # Nếu dữ liệu đã có trong Redis, trả về dữ liệu từ cache
            users = json.loads(cached_users)  # Chuyển từ chuỗi JSON sang danh sách Python
            return make_response(jsonify(users), 200)
        
        # Nếu dữ liệu không có trong Redis, lấy từ cơ sở dữ liệu
        users = get_all_users_from_db()
        
        # Lưu danh sách người dùng vào Redis với key 'all_users'
        redis_client.set('all_users', json.dumps(users))
        
        # Trả về dữ liệu người dùng từ cơ sở dữ liệu và lưu vào Redis
        return make_response(jsonify(users), 200)
    
    except redis.ConnectionError as e:
        # Xử lý lỗi kết nối Redis
        return jsonify({"error": "Unable to connect to Redis", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
