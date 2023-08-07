from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
import jwt


def authenticate_token(view_func):
    def wrapper(request, *args, **kwargs):
        token = args[0].headers["Authorization"].split("Bearer ")[1]
        print("args and kwargs",args[0].headers["Authorization"].split("Bearer ")[1],type(args))
        # print("request body in decorator ###########-",request.headers)
        # token = args.headers["Authorization"].split("Bearer ")[1]
        # print('token is: ', token)
        # token = False
        # return JsonResponse({'error': 'Token has expired.'}, status=401)
        if token:
            try:
                decoded_token = jwt.decode(token, 'secret', algorithms=['HS256'])

                expiration_timestamp = decoded_token.get('exp')
                if expiration_timestamp:
                    expiration_datetime = datetime.utcfromtimestamp(expiration_timestamp)
                    if datetime.utcnow() > expiration_datetime:
                        return JsonResponse({'error': 'Token has expired.'}, status=401)

                request.decoded_token = decoded_token  # for further processing if needed

            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token has expired.'}, status=401)

            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token.'}, status=401)

        else:
            return JsonResponse({'error': 'Token not found in the request headers.'}, status=401)

        return view_func(request, *args, **kwargs)

    return wrapper



def authenticate_admin(view_func):
    def wrapper(request, *args, **kwargs):
        print('############################     ', args[0].headers["Authorization"])
        token = args[0].headers["Authorization"].split("Bearer ")[1]
        decoded_token = jwt.decode(token, 'secret', algorithms=['HS256'])
        role = decoded_token["role"]
        if role != "admin":
            return JsonResponse({'error': 'Admin not logged in.'}, status=401)

        return view_func(request, *args, **kwargs)

    return wrapper


