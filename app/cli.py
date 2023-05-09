import click as click
import urllib3
import yaml
from hvac import Client as hvacClient
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

MOUNT_PATH = "apps"
VAULT_PATH = "/mps-qe/managed-services"


@click.command()
@click.option(
    "-a",
    "--action",
    help="""\b
        add - to add or update a secret.
        read - read a secret.
        """,
    required=True,
    default="read",
    type=click.Choice(["add", "read"]),
    show_default=True,
)
@click.option(
    "-t",
    "--token",
    help="Vault token",
    required=False,
    envvar="VAULT_TOKEN",
    show_default=True,
)
@click.option(
    "-n", "--secret-name", help="secret_dict name", required=True, show_default=True
)
@click.argument(
    "yaml-path",
    required=False,
    type=click.File(),
)
def main(action, token, secret_name, yaml_path):
    vault_client = get_vault_client(token=token)
    if action == "add":
        add_secret(
            secret_name=secret_name, vault_client=vault_client, yaml_path=yaml_path
        )
    if action == "read":
        read_secret(secret_name=secret_name, vault_client=vault_client)


def add_secret(secret_name, vault_client, yaml_path):
    click.echo(f"Add / update secret {secret_name} in vault.")
    vault_client.secrets.kv.v2.create_or_update_secret(
        mount_point=MOUNT_PATH,
        path=f"{VAULT_PATH}/{secret_name}",
        secret=yaml.safe_load(yaml_path.read()),
    )


def read_secret(secret_name, vault_client):
    click.echo(
        yaml.dump(
            vault_client.secrets.kv.v2.read_secret_version(
                mount_point=MOUNT_PATH, path=f"{VAULT_PATH}/{secret_name}"
            )["data"]["data"]
        )
    )


def get_vault_client(token):
    assert (
        token
    ), "Token is mandatory. Either pass it or set 'VAULT_TOKEN' environment variable"
    vault_client = hvacClient(
        url="https://vault.corp.redhat.com:8200", verify=False, token=token
    )
    assert vault_client.is_authenticated(), "Failed to authenticate to vault."

    return vault_client


if __name__ == "__main__":
    main()
