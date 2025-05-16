from fastapi import Request



def url_key_builder(func, namespace, request: Request, *args, **kwargs) -> str:
    page = request.query_params.get("page", "1")
    limit = request.query_params.get("limit", "10")
    return f"{namespace}:{request.url.path}?page={page}&limit={limit}"

def user_aware_key_builder(func, namespace, request: Request, *args, **kwargs) -> str:
    user_id = getattr(getattr(request.state, "user", None), "id", None)
    base_key = f"{namespace}:{request.url.path}?{request.url.query}"
    if user_id is not None:
        base_key += f":user={user_id}"
    return base_key
