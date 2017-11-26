from flask import Flask, jsonify, request, render_template

app = Flask(__name__) # __name__ gives the file a unique name for Flask

stores = [{
    'name': 'My Store',
    'items': [{'name':'my item', 'price': 15.99 }]
}]

# from server perspective:
# POST recieve data, and use it
# GET send data back only

#post /store data: {name :}
#get /store/<name> data: {name :}
#get /store
#post /store/<name> data: {name :}


# ===============================
# Tell app what requests to understand using decorators (ex. @app.route('/'))
# Going to a page always sends a GET, so default is always a get request. otherwise we have to specify methods=['POST', 'GET', ...]
@app.route('/') 
def home():
  return render_template('index.html') 

# ===============================
#post /store data: {name :}
@app.route('/store' , methods=['POST'])
def create_store():
  # request is the request(from browser) that was made to this endpoint
  request_data = request.get_json()
  new_store = {
    'name':request_data['name'],
    'items':[]
  }
  stores.append(new_store)
  return jsonify(new_store) # return just so browser knows we returned a new store
  #pass

# ===============================
#get /store/<name> data: {name :}
@app.route('/store/<string:name>')
def get_store(name):
  for store in stores:
    if store['name'] == name:
          return jsonify(store)
  return jsonify ({'message': 'store not found'})
  #pass

# ===============================
#get /store
@app.route('/store')
def get_stores():
  #return jsonify(stores)
  return jsonify({'stores': stores})
  #pass

# ===============================
#post /store/<name> data: {name :}
@app.route('/store/<string:name>/item' , methods=['POST'])
def create_item_in_store(name):
  request_data = request.get_json()
  for store in stores:
    if store['name'] == name:
        # update if store exists
        new_item = {
            'name': request_data['name'],
            'price': request_data['price']
        }
        store['items'].append(new_item)
        return jsonify(new_item) #return for browser
  return jsonify ({'message' :'store not found'})
  #pass

# ===============================
#get /store/<name>/item data: {name :}
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
  for store in stores:
    if store['name'] == name:
        return jsonify( {'items':store['items'] } )
  return jsonify ({'message':'store not found'})

  #pass

app.run(port=5000) # area on the computer where your app will be recieveing requests (data) 
