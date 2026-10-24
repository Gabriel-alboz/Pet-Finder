"""Server-side client for the versioned Pet Finder Xano API contract."""

import os
import time
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlsplit

import httpx


AUTH_TOKEN_TTL_SECONDS = 86400


class XanoAuthError(Exception):
    """An authentication failure whose message is safe for the UI."""


class XanoCredentialsError(XanoAuthError):
    """The supplied credentials were rejected."""


class XanoSessionExpired(XanoAuthError):
    """Xano rejected an authenticated request."""


class XanoServiceUnavailable(XanoAuthError):
    """Authentication could not be completed safely."""


class XanoUnclassifiedAccount(XanoAuthError):
    """The backend has not assigned a supported account type."""


@dataclass(frozen=True)
class AuthenticatedUser:
    user_id: int
    name: str
    account_type: str


@dataclass(frozen=True)
class AuthenticatedSession:
    token: str = field(repr=False)
    expires_at: float
    user: AuthenticatedUser


def _auth_base_url() -> str:
    base = os.getenv("XANO_API_BASE_URL", "").strip()
    parsed = urlsplit(base)
    if (
        parsed.scheme != "https" or not parsed.hostname
        or parsed.username or parsed.password or parsed.query or parsed.fragment
    ):
        raise XanoServiceUnavailable(
            "O serviço de acesso ainda não está configurado. Tente novamente mais tarde."
        )
    return base.rstrip("/") + "/"


def _identity(value: object) -> int:
    if isinstance(value, str) and value.isascii() and value.isdecimal():
        value = int(value)
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise XanoServiceUnavailable("O serviço retornou uma resposta inesperada.")
    return value


async def _auth_json(
    client: httpx.AsyncClient,
    method: str,
    endpoint: str,
    *,
    payload: dict[str, str] | None = None,
    token: str = "",
) -> dict:
    # Never log the payload, headers, response body, or raw HTTP exceptions.
    try:
        response = await client.request(
            method, endpoint, json=payload,
            headers={"Authorization": f"Bearer {token}"} if token else {},
        )
    except httpx.TimeoutException:
        raise XanoServiceUnavailable(
            "O serviço demorou para responder. Tente novamente."
        ) from None
    except httpx.RequestError:
        raise XanoServiceUnavailable(
            "Não foi possível conectar ao serviço de acesso. Tente novamente."
        ) from None

    if endpoint == "auth/login" and response.status_code in (400, 401, 403):
        raise XanoCredentialsError("E-mail ou senha inválidos.")
    if endpoint == "auth/me" and response.status_code in (401, 403):
        raise XanoSessionExpired("Sua sessão expirou. Entre novamente.")
    if response.status_code == 429:
        raise XanoServiceUnavailable("Muitas tentativas. Aguarde um pouco e tente novamente.")
    if not response.is_success:
        raise XanoServiceUnavailable("O serviço de acesso está indisponível. Tente novamente.")
    try:
        body = response.json()
    except ValueError:
        raise XanoServiceUnavailable("O serviço retornou uma resposta inesperada.") from None
    if not isinstance(body, dict):
        raise XanoServiceUnavailable("O serviço retornou uma resposta inesperada.")
    return body


async def _current_user(client: httpx.AsyncClient, token: str) -> AuthenticatedUser:
    body = await _auth_json(client, "GET", "auth/me", token=token)
    account_type = body.get("account_type")
    if account_type not in ("ADOTANTE", "ONG"):
        raise XanoUnclassifiedAccount(
            "Sua conta ainda não possui um tipo válido. Entre em contato com o suporte."
        )
    name = body.get("name")
    if not isinstance(name, str) or not name.strip():
        raise XanoServiceUnavailable("O serviço retornou uma resposta inesperada.")
    # Do not retain role, email, documents, or unexpected response fields.
    return AuthenticatedUser(_identity(body.get("id")), name, account_type)


async def authenticate(email: str, password: str) -> AuthenticatedSession:
    """Authenticate and verify the user's identity before establishing a session."""
    issued_at = time.time()
    async with httpx.AsyncClient(
        base_url=_auth_base_url(), timeout=httpx.Timeout(10.0), follow_redirects=False,
    ) as client:
        body = await _auth_json(
            client, "POST", "auth/login",
            payload={"email": email.strip().lower(), "password": password},
        )
        token = body.get("authToken")
        if (
            not isinstance(token, str) or not token or token != token.strip()
            or "\r" in token or "\n" in token
        ):
            raise XanoServiceUnavailable("O serviço retornou uma resposta inesperada.")
        user_id = _identity(body.get("user_id"))
        user = await _current_user(client, token)
        if user.user_id != user_id:
            raise XanoServiceUnavailable("O serviço retornou uma resposta inesperada.")
        return AuthenticatedSession(token, issued_at + AUTH_TOKEN_TTL_SECONDS, user)


async def get_current_user(token: str) -> AuthenticatedUser:
    """Validate a server-held token with Xano; never accept a browser-held token."""
    if not token:
        raise XanoSessionExpired("Sua sessão expirou. Entre novamente.")
    async with httpx.AsyncClient(
        base_url=_auth_base_url(), timeout=httpx.Timeout(10.0), follow_redirects=False,
    ) as client:
        return await _current_user(client, token)


class XanoSignupError(Exception):
    """A user-safe registration failure."""


async def create_account(payload: dict[str, str]) -> None:
    """Create an account through the Xano signup endpoint.

    The returned signup token is deliberately discarded. Registration does not
    establish a session; users continue through the separate login flow.
    """
    base_url = os.getenv("XANO_API_BASE_URL", "").strip()
    if not base_url:
        raise XanoSignupError(
            "O cadastro ainda não está conectado ao ambiente do Xano. Tente novamente mais tarde."
        )

    url = urljoin(base_url.rstrip("/") + "/", "auth/signup")
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
            response = await client.post(url, json=payload)
    except httpx.TimeoutException as exc:
        raise XanoSignupError(
            "O serviço demorou para responder. Verifique sua conexão e tente novamente."
        ) from exc
    except httpx.RequestError as exc:
        raise XanoSignupError(
            "Não foi possível conectar ao serviço de cadastro. Tente novamente."
        ) from exc

    if response.is_success:
        try:
            body = response.json()
        except ValueError as exc:
            raise XanoSignupError(
                "O serviço retornou uma resposta inesperada. Tente novamente mais tarde."
            ) from exc
        if not isinstance(body, dict) or not body.get("user_id"):
            raise XanoSignupError(
                "O serviço retornou uma resposta inesperada. Tente novamente mais tarde."
            )
        return

    # Keep duplicate-account feedback generic so the UI does not disclose
    # whether a particular email or document is registered.
    if response.status_code in (400, 409, 422):
        raise XanoSignupError(
            "Não foi possível concluir o cadastro. Confira os dados informados ou tente outro e-mail/documento."
        )
    raise XanoSignupError(
        "O cadastro não pôde ser concluído agora. Tente novamente mais tarde."
    )
