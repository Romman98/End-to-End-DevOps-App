from flask import Flask, request, Response, jsonify
from connDB import queryFunc, checkEntry, DATABASE_INIT
from prometheus_client import Counter, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNTER = Counter('names_requests_total','Total requests to the app',['endpoint','method'])

DATABASE_INIT()

@app.before_request
def before_request():
    REQUEST_COUNTER.labels(endpoint=request.path, method=request.method).inc()

@app.route('/')
def index():
    return "I am working!"

@app.route('/review/new',methods=["POST"])
def new_review():
    data = request.json
    name = data.get("name")
    rating = data.get("rating")
    print(name,rating)
    if not checkEntry(name):
        output=queryFunc(f"INSERT INTO Reviews (name,rating) values ('{name}','{rating}')")
        return Response("Data Inserted Successfully",status=200)
    return Response("Data already exists")

@app.route('/review')
def get_reviews():
    data = queryFunc("SELECT * from Reviews")
    return jsonify({'results': data})

@app.route ('/review/query')
def get_review():
    name_param = request.args.get("name")
    rating_param = request.args.get("rating")
    
    if name_param:
        data = queryFunc(f"SELECT * from Reviews where name='{name_param}'")
    elif rating_param:
        data = queryFunc(f"SELECT * from Reviews where rating='{rating_param}'")
    else:
        data = "Incorrect input. Please filter on 'name' or 'rating'."
        
    return jsonify({"Result": data})

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
