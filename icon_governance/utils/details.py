import requests


def get_details(details_endpoint):
    try:
        r = requests.get(details_endpoint)
        out = {}

        if r.status_code == 200:
            r = r.json()
            out.update(r["representative"]["logo"])
            out.update(r["representative"]["media"])

            out.update(r["server"])
            out.pop("location")

            out["server_country"] = r["server"]["location"]["city"]
            out["server_city"] = r["server"]["location"]["country"]

    except Exception:
        return None

    return out
