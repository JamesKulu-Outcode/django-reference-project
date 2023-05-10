from drf_yasg import openapi

manual_parameters = [
    openapi.Parameter(
        "order_by",
        openapi.IN_QUERY, 
        description='sort the list by field',
        type=openapi.TYPE_STRING
        ), 
        openapi.Parameter(
        "keyword",
        openapi.IN_QUERY, 
        description='filter the list by a wildcard',
        type=openapi.TYPE_STRING
        )
    ]

setpassword_request = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=[
                "uid",
                "token",
                "password", 
                "confirm_password",
                ],
        properties={
            "uid": openapi.Schema(type=openapi.TYPE_STRING),
            "token": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
            "confirm_password": openapi.Schema(type=openapi.TYPE_STRING)
        },
)

resetpassword_request = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=[
                "email",
                ],
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING)
        },
)

updatepassword_request = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=[
                "password",
                "new_password",
                ],
        properties={
            "password": openapi.Schema(type=openapi.TYPE_STRING),
            "new_password": openapi.Schema(type=openapi.TYPE_STRING)
        },
)

filecreate_request = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[
                    "file_doc",
                    ],
            properties={
                "file_doc": openapi.Schema(type=openapi.TYPE_FILE),
            },
)