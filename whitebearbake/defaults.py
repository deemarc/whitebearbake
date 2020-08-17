""" Config defaults """

FLASK_ENV = "development"
SQLALCHEMY_DATABASE_URI = 'postgresql://capstone_usr:mypass@localhost:5432/capstone_dev'
# APISPEC_SPEC = {
  
# }
APISPEC = {
  "version":"1.0.0",
  "openapi_version":"3.0.2",
  "title": "WhiteBearBake API",
  "description": "API for dessert recipe",
  "host": "localhost:5000",  # overrides localhost:500
  "basePath": "/api",  # base bash for blueprint registration
  "schemes": [
    "http",
    "https"
  ],
  "components": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "in": "header",
            }
        }
    }
}

# }
# TEMPLATE = {
#   "swagger": "2.0",
#   "info": {
    
#     "contact": {
#       "responsibleOrganization": "Deemarc B.",
#       "responsibleDeveloper": "Deemarc B.",
#       "email": "notgviven@hahaha.com",
#       "url": "www.me.com",
#     },
#     "version": "0.0.1"
#   },
#   "host": "localhost:5000",  # overrides localhost:500
#   "basePath": "/api",  # base bash for blueprint registration
#   "schemes": [
#     "http",
#     "https"
#   ],
#     "components": {
#         "securitySchemes": {
#             "BearerAuth": {
#                 "type": "http",
#                 "scheme": "bearer",
#                 "bearerFormat": "JWT",
#                 "in": "header",
#             }
#         }
#     }
# }