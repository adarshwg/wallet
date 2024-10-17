from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str
    message: str


responses = {
    400: {
        "description": "Bad request",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema(),
                "examples": {
                    "example-1": {
                        "value": {
                            "detail": "Bad Request",
                            "message": "Your Request could not be fulfilled"
                        }
                    }
                }
            }
        },
    },
    409: {
        "description": "Username already exists",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema(),
                "examples": {
                    "example-1": {
                        "value": {
                            "detail": "Conflict",
                            "message": "Conflict - Resource already exists!"
                        }
                    }
                }
            }
        },
    },
    401: {
        "description": "Unauthorized access",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema(),
                "examples": {
                    "example-1": {
                        "value": {
                            "detail": "Invalid Credentials",
                            "message": "Unauthorized"
                        }
                    }
                }
            }
        }
    },
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema(),
                "examples": {
                    "example-1": {
                        "value": {
                            "detail": "Forbidden",
                            "message": "Action is forbidden"
                        }
                    }
                }
            }
        }
    },
    404: {
        "description": "Resource not found",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema(),
                "examples": {
                    "example-1": {
                        "value": {
                            "detail": "Resource not found",
                            "message": "Requested resource could not be found!"
                        }
                    }
                }
            }
        }
    },
    500: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema(),
                "examples": {
                    "example-1": {
                        "value": {
                            "detail": "Internal Server Error",
                            "message": "Regret! Internal Server Error"
                        }
                    }
                }
            }
        },
    }
}
