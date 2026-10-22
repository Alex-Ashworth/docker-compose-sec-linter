import requests
from compose_linter.parsing import parse_image


# url = "https://auth.docker.io/token"
# scope = "repository:library/nginx:pull"
# service = "registry.docker.io"
# payload = {"service": service, "scope": scope}
# target = scope.split(":")
# tag = "latest"
# r = requests.get(url, params=payload)
# data = r.json()
# token = data["token"]
# headers = {"Authorization": f"Bearer {token}"}
# # print(token)
def check_registry(image_entry: str):
    registry, repo, image, tag, digest = parse_image(image_entry)

    print(f"{registry}/{repo}/{image}/manifests/{tag}")
    print("***BEFORE")
    auth_url = "https://auth.docker.io/token"
    payload = {
        "service": f"registry.{registry}",
        "scope": f"repository:{repo}/{image}:pull",
    }
    auth = requests.get(auth_url, params=payload)
    token = auth.json()["token"]
    auth_head = {"Authorization": f"Bearer {token}"}

    if registry == "docker.io":
        registry = "https://registry-1.docker.io/v2"
    if digest is not None:
        tag = digest

    print(f"{registry}/{repo}/{image}/manifests/{tag}")
    req = requests.head(f"{registry}/{repo}/{image}/manifests/{tag}", headers=auth_head)
    match req.status_code:
        case 200:
            print()
        case 400:
            print()
        case 401:
            print()
        case 403:
            print()
        case 404:
            print()
        case x if x in range(500, 601):
            print()

    return req.status_code
