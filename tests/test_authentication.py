"""Offline contract/security tests. All HTTP calls use MockTransport."""

import json
import os
import time
import unittest
from unittest.mock import AsyncMock, patch

import httpx

from Pet_Finder.auth import LoginState
from Pet_Finder.home import HomeState
from Pet_Finder.services import xano


REAL_ASYNC_CLIENT = httpx.AsyncClient
TEST_TOKEN = "offline-test-token"


def profile(account_type="ADOTANTE", user_id=7):
    return {"id": user_id, "name": "Conta de teste", "account_type": account_type, "role": "member"}


def session(account_type="ADOTANTE"):
    return xano.AuthenticatedSession(
        TEST_TOKEN, time.time() + 3600,
        xano.AuthenticatedUser(7, "Conta de teste", account_type),
    )


async def collect(events):
    return [event async for event in events]


class XanoContractTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        env = patch.dict(os.environ, {"XANO_API_BASE_URL": "https://xano.example/api:auth:v1"})
        env.start()
        self.addCleanup(env.stop)

    def transport(self, handler):
        mock_transport = httpx.MockTransport(handler)
        return patch.object(
            xano.httpx, "AsyncClient",
            side_effect=lambda **kwargs: REAL_ASYNC_CLIENT(transport=mock_transport, **kwargs),
        )

    async def test_login_and_me_for_both_account_types(self):
        for account_type in ("ADOTANTE", "ONG"):
            with self.subTest(account_type=account_type):
                requests = []

                def handle(request):
                    requests.append(request)
                    if request.method == "POST":
                        self.assertEqual(request.url.path, "/api:auth:v1/auth/login")
                        self.assertEqual(json.loads(request.content), {"email": "person@example.test", "password": "  synthetic password  "})
                        return httpx.Response(200, json={"authToken": TEST_TOKEN, "user_id": "7"})
                    self.assertEqual(request.url.path, "/api:auth:v1/auth/me")
                    self.assertEqual(request.headers["Authorization"], "Bearer " + TEST_TOKEN)
                    body = profile(account_type)
                    body.update(role="admin", email="ignored@example.test", password="discard-this")
                    return httpx.Response(200, json=body)

                before = time.time()
                with self.transport(handle):
                    result = await xano.authenticate(" Person@Example.Test ", "  synthetic password  ")
                self.assertEqual(result.user.account_type, account_type)
                self.assertEqual(result.user.user_id, 7)
                self.assertEqual(len(requests), 2)
                self.assertGreaterEqual(result.expires_at, before + 86400)
                self.assertLessEqual(result.expires_at, time.time() + 86400)
                self.assertNotIn(TEST_TOKEN, repr(result))
                self.assertFalse(hasattr(result.user, "role"))
                self.assertFalse(hasattr(result.user, "email"))

    async def test_invalid_credentials_do_not_call_me_or_reveal_body(self):
        for status in (400, 401, 403):
            calls = []

            def handle(request):
                calls.append(request)
                return httpx.Response(status, json={"message": "unsafe-response-marker"})

            with self.transport(handle), self.assertRaises(xano.XanoCredentialsError) as error:
                await xano.authenticate("person@example.test", "synthetic")
            self.assertEqual(len(calls), 1)
            self.assertNotIn("unsafe-response-marker", str(error.exception))

    async def test_unavailable_rate_limit_and_redirect_do_not_forward_credentials(self):
        for status in (302, 429, 500, 503):
            calls = []

            def handle(request):
                calls.append(request)
                return httpx.Response(status, headers={"Location": "https://other.example/"})

            with self.transport(handle), self.assertRaises(xano.XanoServiceUnavailable):
                await xano.authenticate("person@example.test", "synthetic")
            self.assertEqual(len(calls), 1)

    async def test_timeout_and_network_errors_have_safe_messages(self):
        for failure in (httpx.ReadTimeout, httpx.ConnectError):
            def handle(request):
                raise failure("unsafe-exception-marker", request=request)

            with self.transport(handle), self.assertRaises(xano.XanoServiceUnavailable) as error:
                await xano.authenticate("person@example.test", "synthetic")
            self.assertNotIn("unsafe-exception-marker", str(error.exception))

    async def test_malformed_login_responses_fail_closed(self):
        bodies = [[], {}, {"authToken": "", "user_id": 7},
                  {"authToken": TEST_TOKEN, "user_id": True},
                  {"authToken": TEST_TOKEN, "user_id": 1.5},
                  {"authToken": "bad\r\ntoken", "user_id": 7}]
        for body in bodies:
            with self.transport(lambda request: httpx.Response(200, json=body)):
                with self.assertRaises(xano.XanoServiceUnavailable):
                    await xano.authenticate("person@example.test", "synthetic")
        with self.transport(lambda request: httpx.Response(200, text="not json")):
            with self.assertRaises(xano.XanoServiceUnavailable):
                await xano.authenticate("person@example.test", "synthetic")

    async def test_me_rejects_invalid_tokens(self):
        for status in (401, 403):
            with self.transport(lambda request: httpx.Response(status)):
                with self.assertRaises(xano.XanoSessionExpired):
                    await xano.get_current_user(TEST_TOKEN)

    async def test_me_never_infers_type_from_role(self):
        for value in (None, "member", "admin", "adotante", {}, ["ONG"]):
            body = profile(value)
            body["role"] = "admin"
            with self.transport(lambda request: httpx.Response(200, json=body)):
                with self.assertRaises(xano.XanoUnclassifiedAccount):
                    await xano.get_current_user(TEST_TOKEN)

    async def test_me_identity_must_match_login(self):
        def handle(request):
            return httpx.Response(200, json={"authToken": TEST_TOKEN, "user_id": 7} if request.method == "POST" else profile(user_id=8))

        with self.transport(handle), self.assertRaises(xano.XanoServiceUnavailable):
            await xano.authenticate("person@example.test", "synthetic")

    async def test_missing_or_insecure_configuration_sends_nothing(self):
        for base in ("", "http://xano.example", "https://user:password@xano.example", "https://xano.example/?secret=value"):
            with patch.dict(os.environ, {"XANO_API_BASE_URL": base}), patch.object(xano.httpx, "AsyncClient") as client:
                with self.assertRaises(xano.XanoServiceUnavailable):
                    await xano.authenticate("person@example.test", "synthetic")
                client.assert_not_called()

    async def test_signup_client_preserved_and_does_not_establish_session(self):
        for account_type in ("ADOTANTE", "ONG"):
            payload = {"account_type": account_type, "email": "person@example.test", "password": "synthetic"}

            def handle(request):
                self.assertEqual(request.method, "POST")
                self.assertEqual(request.url.path, "/api:auth:v1/auth/signup")
                self.assertEqual(json.loads(request.content), payload)
                return httpx.Response(200, json={"authToken": TEST_TOKEN, "user_id": 7})

            with self.transport(handle):
                self.assertIsNone(await xano.create_account(payload))


class LoginStateTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state = LoginState(_reflex_internal_init=True)

    async def login(self, account_type="ADOTANTE"):
        data = {"email": "person@example.test", "password": "synthetic"}
        with patch("Pet_Finder.auth.authenticate", new=AsyncMock(return_value=session(account_type))):
            return await collect(self.state.handle_submit(data))

    async def test_success_redirects_without_serializing_token_or_password(self):
        for account_type in ("ADOTANTE", "ONG"):
            events = await self.login(account_type)
            self.assertTrue(self.state.can_view_home)
            self.assertEqual(self.state.account_type, account_type)
            self.assertIn("/home", str(events[-1]))
            serialized = json.dumps(self.state.dict(), default=str)
            self.assertNotIn(TEST_TOKEN, serialized)
            self.assertNotIn("synthetic", serialized)
            self.assertNotIn("_auth_token", self.state.base_vars)
            self.assertNotIn("password", self.state.base_vars)

    async def test_missing_credentials_do_not_call_xano(self):
        with patch("Pet_Finder.auth.authenticate", new=AsyncMock()) as authenticate:
            await collect(self.state.handle_submit({"email": "", "password": ""}))
            authenticate.assert_not_awaited()
        self.assertFalse(self.state.can_view_home)

    async def test_private_authority_and_computed_identity_have_no_client_setters(self):
        for name in ("_auth_token", "_expires_at", "_user_id", "_account_type", "_home_verified", "can_view_home", "account_type"):
            self.assertNotIn("set_" + name, LoginState.event_handlers)
            with self.assertRaises(AttributeError):
                LoginState.setvar(name, "forged")
        self.assertNotIn("_clear_session", LoginState.event_handlers)

    async def test_login_password_is_a_real_password_input_not_a_css_property(self):
        from Pet_Finder.Pet_Finder import login_page

        def walk(component):
            yield component
            for child in component.children:
                yield from walk(child)

        inputs = [c for c in walk(login_page()) if "TextField" in str(c.tag)]
        password = next(c for c in inputs if str(getattr(c, "name", "")) == '"password"')
        props = password.render()["props"]
        self.assertTrue(any(p.startswith("type:") and '"password"' in p for p in props))
        self.assertFalse(any(p.startswith("css:") and '["type"]' in p for p in props))

    async def test_busy_submission_is_not_duplicated(self):
        with patch("Pet_Finder.auth.authenticate", new=AsyncMock(return_value=session())) as authenticate:
            first = self.state.handle_submit({"email": "person@example.test", "password": "synthetic"})
            await anext(first)
            await collect(self.state.handle_submit({"email": "person@example.test", "password": "synthetic"}))
            await collect(first)
            authenticate.assert_awaited_once()

    async def test_form_account_type_cannot_override_backend_classification(self):
        with patch("Pet_Finder.auth.authenticate", new=AsyncMock(return_value=session("ADOTANTE"))):
            await collect(self.state.handle_submit({"email": "person@example.test", "password": "synthetic", "account_type": "ONG", "role": "admin"}))
        self.assertEqual(self.state.account_type, "ADOTANTE")

    async def test_failed_login_clears_session_and_sensitive_payload(self):
        await self.login()
        data = {"email": "person@example.test", "password": "synthetic"}
        with patch("Pet_Finder.auth.authenticate", new=AsyncMock(side_effect=xano.XanoCredentialsError("E-mail ou senha inválidos."))):
            await collect(self.state.handle_submit(data))
        self.assertEqual(data, {})
        self.assertEqual(self.state._auth_token, "")
        self.assertFalse(self.state.can_view_home)
        self.assertFalse(self.state.is_loading)

    async def test_unexpected_exception_does_not_reach_ui(self):
        with patch("Pet_Finder.auth.authenticate", new=AsyncMock(side_effect=RuntimeError("unsafe-exception-marker"))):
            await collect(self.state.handle_submit({"email": "person@example.test", "password": "synthetic"}))
        self.assertNotIn("unsafe-exception-marker", self.state.error_message)
        self.assertFalse(self.state.can_view_home)

    async def test_anonymous_direct_home_redirects_without_http(self):
        with patch("Pet_Finder.auth.get_current_user", new=AsyncMock()) as me:
            events = await collect(self.state.require_auth())
            me.assert_not_awaited()
        self.assertIn("/login", str(events[-1]))
        self.assertFalse(self.state.can_view_home)

    async def test_expiration_blocks_home_without_http(self):
        await self.login()
        self.state._expires_at = time.time() - 1
        self.assertFalse(self.state.can_view_home)
        with patch("Pet_Finder.auth.get_current_user", new=AsyncMock()) as me:
            await collect(self.state.require_auth())
            me.assert_not_awaited()
        self.assertEqual(self.state._auth_token, "")

    async def test_reload_guard_revalidates_identity_and_backend_account_type(self):
        await self.login()
        with patch("Pet_Finder.auth.get_current_user", new=AsyncMock(return_value=session("ONG").user)) as me:
            await collect(self.state.require_auth())
            me.assert_awaited_once_with(TEST_TOKEN)
        self.assertTrue(self.state.can_view_home)
        self.assertEqual(self.state.account_type, "ONG")

    async def test_guard_fails_closed_on_network_error_expiry_or_identity_change(self):
        failures = [xano.XanoServiceUnavailable("Serviço indisponível."), xano.XanoSessionExpired("Sessão expirada.")]
        for failure in failures:
            await self.login()
            with patch("Pet_Finder.auth.get_current_user", new=AsyncMock(side_effect=failure)):
                events = await collect(self.state.require_auth())
            self.assertFalse(self.state.can_view_home)
            self.assertEqual(self.state._auth_token, "")
            self.assertIn("/login", str(events[-1]))
        await self.login()
        with patch("Pet_Finder.auth.get_current_user", new=AsyncMock(return_value=xano.AuthenticatedUser(8, "Outra conta de teste", "ONG"))):
            await collect(self.state.require_auth())
        self.assertFalse(self.state.can_view_home)

    async def test_logout_clears_local_session_without_remote_calls(self):
        await self.login()
        with patch("Pet_Finder.auth.get_current_user", new=AsyncMock()) as me:
            event = self.state.logout()
            me.assert_not_awaited()
        self.assertFalse(self.state.can_view_home)
        self.assertEqual(self.state._auth_token, "")
        self.assertEqual(self.state.display_name, "")
        self.assertIn("/login", str(event))

    async def test_home_navigation_checks_private_session(self):
        home = HomeState(_reflex_internal_init=True)
        with patch.object(HomeState, "get_state", new=AsyncMock(return_value=self.state)):
            event = await home.open_section("pets")
            self.assertEqual(home.active_section, "home")
            self.assertIn("/login", str(event))
            await self.login()
            await home.open_section("pets")
            self.assertEqual(home.active_section, "pets")
            self.state._expires_at = time.time() - 1
            event = await home.toggle_mobile_menu()
            self.assertIn("/login", str(event))


if __name__ == "__main__":
    unittest.main()
