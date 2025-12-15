from flask import Flask, request, jsonify
from data import restaurants, users, reviews

app = Flask(__name__)

# 로그인
@app.route("/login", methods=["POST"])
def login():
    user_id = request.json.get("user_id")
    if user_id not in users:
        users[user_id] = {"taste": []}
    return jsonify({"message": "로그인 성공", "user_id": user_id})


# 맛 선호도 설정
@app.route("/taste", methods=["POST"])
def set_taste():
    user_id = request.json.get("user_id")
    taste = request.json.get("taste")

    if user_id not in users:
        return jsonify({"error": "사용자 없음"}), 400

    users[user_id]["taste"] = taste
    return jsonify({"message": "맛 선호도 저장 완료"})


# 맛집 추천
@app.route("/recommend", methods=["GET"])
def recommend():
    user_id = request.args.get("user_id")

    if user_id not in users:
        return jsonify({"error": "사용자 없음"}), 400

    user_taste = users[user_id]["taste"]
    result = []

    for r in restaurants:
        if any(t in r["taste"] for t in user_taste):
            result.append(r)

    return jsonify(result)


# 리뷰 작성
@app.route("/review", methods=["POST"])
def add_review():
    review = {
        "user": request.json.get("user"),
        "restaurant": request.json.get("restaurant"),
        "content": request.json.get("content")
    }
    reviews.append(review)
    return jsonify({"message": "리뷰 등록 완료"})


# 리뷰 조회
@app.route("/reviews", methods=["GET"])
def get_reviews():
    restaurant = request.args.get("restaurant")
    result = [r for r in reviews if r["restaurant"] == restaurant]
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
