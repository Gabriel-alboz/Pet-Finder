"""Transient authentication held exclusively in the Reflex backend state.

There is no persistent login cookie or refresh flow. Missing server state fails
closed. Clearing this state does not revoke an already issued Xano token.
"""

import time
from typing import Any

import reflex as rx

from Pet_Finder.services.xano import (
    XanoAuthError,
    XanoSessionExpired,
    authenticate,
    get_current_user,
)


class LoginState(rx.State):
    show_password: bool = False
    is_loading: bool = False
    error_message: str = ""
    info_message: str = ""

    # Backend-only vars: no setters, client storage, or frontend serialization.
    _auth_token: str = ""
    _expires_at: float = 0.0
    _user_id: int = 0
    _user_name: str = ""
    _account_type: str = ""
    _home_verified: bool = False

    def _has_valid_session(self) -> bool:
        return bool(
            self._auth_token and self._user_id > 0
            and self._account_type in ("ADOTANTE", "ONG")
            and time.time() < self._expires_at
        )

    def _clear_session(self):
        self._auth_token = ""
        self._expires_at = 0.0
        self._user_id = 0
        self._user_name = ""
        self._account_type = ""
        self._home_verified = False

    @rx.var(cache=False)
    def can_view_home(self) -> bool:
        return self._home_verified and self._has_valid_session()

    @rx.var(cache=False)
    def display_name(self) -> str:
        return self._user_name if self.can_view_home else ""

    @rx.var(cache=False)
    def account_type(self) -> str:
        return self._account_type if self.can_view_home else ""

    @rx.event
    def toggle_password_visibility(self):
        self.show_password = not self.show_password

    @rx.event
    async def handle_submit(self, form_data: dict[str, Any]):
        # Credentials are submitted once by the form, never stored in State vars.
        email = form_data.get("email", "")
        password = form_data.pop("password", "")
        form_data.clear()
        if self.is_loading:
            return
        self._clear_session()
        self.error_message = ""
        self.info_message = ""
        if (
            not isinstance(email, str) or not isinstance(password, str)
            or not email.strip() or not password
        ):
            self.error_message = "Informe seu e-mail e senha para continuar."
            return

        self.is_loading = True
        yield
        try:
            session = await authenticate(email, password)
            self._auth_token = session.token
            self._expires_at = session.expires_at
            self._user_id = session.user.user_id
            self._user_name = session.user.name
            self._account_type = session.user.account_type
            if not self._has_valid_session():
                raise XanoSessionExpired("Sua sessão expirou. Entre novamente.")
            self._home_verified = True
        except XanoAuthError as exc:
            self._clear_session()
            self.error_message = str(exc)
        except Exception:
            self._clear_session()
            self.error_message = "Não foi possível entrar agora. Tente novamente mais tarde."
        finally:
            password = ""
            self.is_loading = False
        if self.can_view_home:
            yield rx.redirect("/home")

    @rx.event
    async def require_auth(self):
        self._home_verified = False
        if not self._has_valid_session():
            self._clear_session()
            self.error_message = "Entre com seu e-mail e senha para continuar."
            yield rx.redirect("/login")
            return
        yield
        try:
            user = await get_current_user(self._auth_token)
            if user.user_id != self._user_id:
                raise XanoSessionExpired("Sua sessão não é válida. Entre novamente.")
            self._account_type = user.account_type
            self._user_name = user.name
            if not self._has_valid_session():
                raise XanoSessionExpired("Sua sessão expirou. Entre novamente.")
            self._home_verified = True
        except XanoAuthError as exc:
            self._clear_session()
            self.error_message = str(exc)
        except Exception:
            self._clear_session()
            self.error_message = "Não foi possível validar sua sessão. Entre novamente."
        if not self.can_view_home:
            yield rx.redirect("/login")

    @rx.event
    def logout(self):
        self._clear_session()
        self.error_message = ""
        self.info_message = ""
        self.show_password = False
        return rx.redirect("/login")
