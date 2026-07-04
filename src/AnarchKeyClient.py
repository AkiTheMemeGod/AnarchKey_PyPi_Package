import argparse
import os
from pathlib import Path

import requests as rq

BASE_URL = "https://anarchkey2-0.onrender.com"
INIT_ENDPOINT = "/api/v1/sdk/anarchkey_init"
SECRETS_ENDPOINT = "/api/v1/sdk/secrets"
INIT_FILENAME = ".anarchkey"


class AnarchKeyClient:
    """
    Python SDK for AnarchKey.

    Example
    -------
    from anarchkey import AnarchKeyClient

    client = AnarchKeyClient(api_key="YOUR_ACCESS_TOKEN")
    secret = client.get_api_key("DATABASE_URL")
    print(secret)
    """

    def __init__(
        self,
        api_key: str = "",
        username: str = "",
        password: str = "",
        base_url: str = BASE_URL,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password

        self.init_file = Path.home() / INIT_FILENAME

        try:
            if self.init_file.exists():
                self.token = self.init_file.read_text(encoding="utf-8").strip()
            else:
                self.token = ""
        except Exception:
            self.token = ""

        self.init_token = self._read_init_token()

    def _read_init_token(self):
        try:
            if self.init_file.exists():
                token = self.init_file.read_text(encoding="utf-8").strip()
                return token if token else None
        except Exception:
            pass
        return None

    def get_api_key(self, project_name: str):
        """
        Fetch a secret from AnarchKey.

        Parameters
        ----------
        project_name : str
            Name of the secret.

        Returns
        -------
        str | dict
        """

        if not self.token:
            raise RuntimeError(
                "ERROR! Start your AnarchKey service using:\n"
                "anarchkey init --username YourName --password YourPassword"
            )

        payload = {
            "access_token": self.api_key,
            "secret_name": project_name,
        }

        headers = {
            "Content-Type": "application/json",
        }

        if self.init_token:
            headers["X-AnarchKey-Init"] = self.init_token

        url = self.base_url + SECRETS_ENDPOINT

        response = rq.post(
            url,
            json=payload,
            headers=headers,
        )

        try:
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict) and "api_key" in data:
                return data["api_key"]

            return data

        except rq.HTTPError:
            try:
                return response.json()
            except Exception:
                return response.text


def do_init(
    base_url: str = BASE_URL,
    out_file: Path = None,
    username: str = None,
    password: str = None,
    timeout: int = 10,
):
    """
    Initializes the local SDK by obtaining an init token.
    """

    if out_file is None:
        out_file = Path.home() / INIT_FILENAME

    try:
        if out_file.exists():
            existing = out_file.read_text(encoding="utf-8").strip()

            if existing:
                print(f"Init token already exists at {out_file}")
                return str(existing), False

    except Exception:
        pass

    url = base_url.rstrip("/") + INIT_ENDPOINT

    payload = {}

    if username:
        payload["username"] = username

    if password:
        payload["password"] = password

    try:
        response = rq.post(
            url,
            json=payload,
            timeout=timeout,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to contact {url}: {e}")

    token = None

    try:
        data = response.json()

        if isinstance(data, dict):
            for key in ("token", "secret", "key", "data"):
                if key in data:
                    token = data[key]
                    break

        elif isinstance(data, str):
            token = data.strip()

    except ValueError:
        token = response.text.strip()

    if not token:
        raise RuntimeError("Init endpoint did not return a token")

    try:
        out_file.write_text(str(token), encoding="utf-8")
        os.chmod(out_file, 0o600)
    except Exception as e:
        raise RuntimeError(
            f"Failed to write init token to {out_file}: {e}"
        )

    return str(token), True


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="anarchkey",
        description="AnarchKey CLI",
    )

    sub = parser.add_subparsers(dest="cmd")

    p_init = sub.add_parser(
        "init",
        help="Initialize local token",
    )

    p_init.add_argument(
        "--base-url",
        default=BASE_URL,
        help="Base URL of the AnarchKey service",
    )

    p_init.add_argument(
        "--out-file",
        default=str(Path.home() / INIT_FILENAME),
        help="Path to write the init token",
    )

    p_init.add_argument(
        "--username",
        help="Username to send to the init endpoint",
    )

    p_init.add_argument(
        "--password",
        help="Password to send to the init endpoint",
    )

    args = parser.parse_args(argv)

    if args.cmd == "init":
        try:
            _, created = do_init(
                base_url=args.base_url,
                out_file=Path(args.out_file),
                username=args.username,
                password=args.password,
            )

            if created:
                print(f"Wrote init token to {args.out_file}")

        except Exception as e:
            print(f"Error: {e}")
            return 2

        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())