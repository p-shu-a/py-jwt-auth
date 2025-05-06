from api.app import api

@api.get("/health")
def health_check():
    return {"status": "The wizards have landed...status okay"}
