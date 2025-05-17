from flask import jsonify

class APIResponse:

    @staticmethod
    def success(message=""
                ,data=None
                ,status_code=200):
        response = {
            "success":True
            ,"message": message
            ,"data":data
        }

        return jsonify(response), status_code
    

    @staticmethod
    def error(message="Ocorreu um erro"
              , data=None
              , status_code=400):
        response = {
            "success":False
            ,"message":message
            ,"data":data
        }

        return jsonify(response), status_code