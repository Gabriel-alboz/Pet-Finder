"""Server-side client for the versioned Pet Finder Xano API contract."""

import os
from urllib.parse import urljoin

import httpx


class XanoSignupError(Exception):
    """A user-safe registration failure."""


async def create_account(payload: dict[str, str]) -> None:
    """Create an account through the Xano signup endpoint.

    The returned Xano token is deliberately discarded: this app does not yet
    have a session lifecycle or secure token storage mechanism.
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
