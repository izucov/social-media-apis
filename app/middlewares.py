import json


class AddUsernameMiddleware:
    """
    Middleware to add a "username" key to the request body if the request is being made to "/api/auth".
    This is needed because the "username" field is required by the RegisterSerializer.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is being made to "/api/auth"
        if request.path == "/api/auth":
            try:
                # Parse the request body as JSON
                data = json.loads(request.body.decode("utf-8"))

                # Check if the request body has an "email" field
                if "email" in data:
                    # Add a "username" key with the same value as "email"
                    email_addr = data["email"].lower()
                    data["username"] = email_addr
                    data["email"] = email_addr

                    # Update the request body with the modified data
                    request._body = json.dumps(data).encode("utf-8")
            except json.JSONDecodeError:
                # Handle JSON decoding error if necessary
                pass

        response = self.get_response(request)

        return response
