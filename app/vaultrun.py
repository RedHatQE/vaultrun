from app.login import vault_login
from app.rofi_helper import call_dmenu
from pprint import pprint
from rich import print, pretty


MOUNT_POINT = "apps"
SECRETS_PATH = "mps-qe/managed-services"


def parse_vault_path(client, secret_path=None):
    _path = SECRETS_PATH if not secret_path else f"{SECRETS_PATH}/{secret_path}"
    all_secrets = client.secrets.kv.v2.list_secrets(mount_point=MOUNT_POINT, path=_path)
    _selected = call_dmenu(
        options=all_secrets.get("data", {}).get("keys"), abort=True, prompt=None
    )
    if _selected.endswith("/"):
        all_secrets = client.secrets.kv.v2.list_secrets(
            mount_point=MOUNT_POINT, path=f"{_path}/{_selected}"
        )
        selected = call_dmenu(
            options=all_secrets.get("data", {}).get("keys"), abort=True, prompt=None
        )
        if selected.endswith("/"):
            _secret_path = f"{_selected}/{selected}"
            return parse_vault_path(client=client, secret_path=_secret_path)
        else:
            return f"{_selected}/{selected}"
    else:
        return _selected


def main():
    pretty.install()
    client = vault_login()
    if client and client.is_authenticated():
        user_selection = parse_vault_path(client=client)
        _secret = client.secrets.kv.v2.read_secret_version(
            mount_point=MOUNT_POINT,
            path=f"{SECRETS_PATH}/{user_selection}",
            raise_on_deleted_version=False,
        )["data"]["data"]
        print(_secret)


if __name__ == "__main__":
    main()
