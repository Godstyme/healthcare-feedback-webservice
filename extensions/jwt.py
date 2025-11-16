from flask_jwt_extended import JWTManager
from models.token_blocklist import TokenBlocklist

jwt = JWTManager()

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    return token is not None
