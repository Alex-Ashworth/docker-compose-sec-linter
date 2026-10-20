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
    auth_url = "https://auth.docker.io/token"
    payload = {"service": registry, "scope": f"repository:{repo}/{image}:pull"}
    auth = requests.get(auth_url, params=payload)
    token = auth.json()["token"]
    auth_head = {"Authorization": f"Bearer {token}"}

    if registry == "docker.io":
        registry = "https://registry-1.docker.io/v2/"
    if digest is not None:
        tag = digest

    req = requests.head(f"{registry}{repo}/{image}/manifests/{tag}", headers=auth_head)
    print(req.status_code)

    return req.status_code
