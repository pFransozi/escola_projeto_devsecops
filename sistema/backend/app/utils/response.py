from flask import jsonify

class APIResponse:
    """Utilitário para formatação de respostas da API."""


    @staticmethod
    def success(message=""
                ,data=None
                ,status_code=200):
        
        """Gera uma resposta de sucesso em formato JSON com dados opcionais."""

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
        
        """Gera uma resposta de erro em formato JSON com mensagem e código HTTP."""

        response = {
            "success":False
            ,"message":message
            ,"data":data
        }

        return jsonify(response), status_code