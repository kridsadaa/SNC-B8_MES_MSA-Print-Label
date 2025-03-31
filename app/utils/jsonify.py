from flask import jsonify


def jsonifySuccess(message, data=None, code=200):
    data = data or []
    
    response = jsonify({
        "status": "success",
        "message": message,
        "data": data
    })
    response.status_code = code
    
    return response

    
def jsonifyError(message, data, code=500): 
    data = data or []
    
    response = jsonify({
        "status": "error",
        "message": message,
        "data": data
    })
    response.status_code = code
    
    return response

    
def jsonifyContentType(message="Content-Type must be application/json", data=[], code=415): 
    data = data or []
    
    response = jsonify({
        "status": "error",
        "message": message,
        "data": data
    })
    response.status_code = code
    
    return response

 


