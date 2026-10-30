"""Offline account preview contracts; HTTP is forbidden throughout rendering."""

import ast
import json
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from Pet_Finder import account_settings as settings
from Pet_Finder.auth import LoginState
from Pet_Finder.home import HomeState, _section_heading, home_page
from Pet_Finder.services.xano import AuthenticatedSession, AuthenticatedUser
from test_home_navigation import texts, walk


class AccountPreviewTests(unittest.TestCase):
    def test_name_is_reactive_read_only_and_visible_in_inner_radix_input(self):
        for ngo in (False, True):
            with patch("httpx.AsyncClient", side_effect=AssertionError("HTTP forbidden")):
                identity = settings._identity(ngo)
            name = identity.children[0].children[1]
            value = name.value
            dependencies = value._get_all_var_data().field_dependencies
            self.assertIn("display_name", dependencies[LoginState.get_full_name()])
            props = name.render()["props"]
            self.assertTrue(any(p.startswith("value:") and "display_name_rx_state_" in p for p in props))
            self.assertFalse(any(p.startswith("defaultValue:") for p in props))
            self.assertIn("readOnly:true", props)
            self.assertFalse(name.event_triggers)
            inner = name.style["& .rt-TextFieldInput"]
            self.assertEqual(str(inner["color"]), '"#1F2937"')
            self.assertEqual(str(inner["WebkitTextFillColor"]), '"#1F2937"')
            self.assertIn("Nome da ONG" if ngo else "Nome completo", texts(identity))
            # The fix must not change the blank email or other preview fields.
            self.assertNotIn("& .rt-TextFieldInput", identity.children[1].children[1].style)

    def render_account(self, account_type, valid=True):
        authority = SimpleNamespace(
            account_type=account_type, can_view_home=valid,
            display_name="Nome seguro da sessão", logout=LoginState.logout,
        )
        with patch.object(settings, "LoginState", authority), patch(
            "httpx.AsyncClient", side_effect=AssertionError("HTTP forbidden")
        ):
            return settings.account_settings(_section_heading)

    def test_adopter_sections_and_ngo_separation(self):
        content = texts(self.render_account("ADOTANTE"))
        for expected in (
            "Configurações da conta", "Gerencie suas informações e suas preferências de adoção.",
            "Meus dados", "Sobre mim", "Pet que procuro", "Privacidade e visibilidade", "Segurança da conta",
        ):
            self.assertIn(expected, content)
        for forbidden in ("Configurações da organização", "Sobre a ONG", "Meus pets"):
            self.assertNotIn(forbidden, content)

    def test_ngo_sections_and_adopter_separation(self):
        content = texts(self.render_account("ONG"))
        for expected in (
            "Configurações da organização", "Dados da organização", "Sobre a ONG",
            "Localização e contato", "Meus pets", "Segurança da conta",
        ):
            self.assertIn(expected, content)
        for forbidden in ("Sobre mim", "Pet que procuro", "Privacidade e visibilidade"):
            self.assertNotIn(forbidden, content)

    def test_invalid_session_or_unrecognized_type_has_no_profile(self):
        for account_type, valid in (("ADOTANTE", False), ("ONG", False), ("", True), ("admin", True), ("member", True)):
            self.assertEqual(texts(self.render_account(account_type, valid)), [])

    def test_fields_read_only_empty_except_safe_name_without_submit(self):
        for ngo in (False, True):
            with patch("httpx.AsyncClient", side_effect=AssertionError("HTTP forbidden")):
                preview = settings._preview(ngo, _section_heading)
            fields = [c for c in walk(preview) if str(c.tag) in ("TextField.Root", "TextArea")]
            self.assertEqual(len(fields), 7 if ngo else 14)
            ids = []
            for field in fields:
                props = field.render()["props"]
                self.assertIn("readOnly:true", props)
                self.assertFalse(field.event_triggers)
                field_id = str(field.id)
                ids.append(field_id)
                if "preview-name" in field_id:
                    self.assertIn("display_name", str(field.value))
                else:
                    self.assertIn(str(field.value), ('""', '(isNotNullOrUndefined("") ? "" : "")'))
            self.assertEqual(len(ids), len(set(ids)))
            labels = [c for c in walk(preview) if str(c.tag) == "label"]
            self.assertEqual(len(labels), len(fields))
            rendered = json.dumps(preview.render())
            for forbidden in ("onSubmit", "Dados atualizados", "Salvar", "password_reset", "_auth_token"):
                self.assertNotIn(forbidden, rendered)
            self.assertIn("somente leitura", " ".join(texts(preview)))
            for component in walk(preview):
                if component.event_triggers:
                    self.assertEqual(set(component.event_triggers), {"on_click"})
                    self.assertIn("logout", str(component.event_triggers))

    def test_description_limits_and_consent_unavailable(self):
        adopter = settings._preview(False, _section_heading)
        ngo = settings._preview(True, _section_heading)
        areas = [c for c in walk(adopter) if str(c.tag) == "TextArea"]
        self.assertEqual([str(c.max_length) for c in areas], ["1000", "1000"])
        self.assertEqual([str(c.max_length) for c in walk(ngo) if str(c.tag) == "TextArea"], ["2000"])
        checks = [c for c in walk(adopter) if str(c.tag) == "Checkbox"]
        self.assertEqual(len(checks), 2)
        for check in checks:
            self.assertEqual(str(check.checked), "false")
            self.assertEqual(str(check.disabled), "true")
            self.assertFalse(check.event_triggers)
        self.assertIn("Recurso em desenvolvimento. Suas preferências ainda não são compartilhadas com ONGs.", texts(adopter))
        pet_button = [c for c in walk(ngo) if "Button" in str(c.tag) and any("Cadastrar pet" in t for t in texts(c))][0]
        self.assertEqual(str(pet_button.disabled), "true")
        self.assertFalse(pet_button.event_triggers)

    def test_responsive_grid_and_vertical_textarea_resizing(self):
        for ngo in (False, True):
            preview = settings._preview(ngo, _section_heading)
            grids = [c for c in walk(preview) if str(c.tag) == "Grid"]
            self.assertTrue(grids)
            for grid in grids:
                css = str(grid.style)
                self.assertIn("minmax(0, 1fr)", css)
                self.assertIn("repeat(2, minmax(0, 1fr))", css)
                self.assertIn("48em", " ".join(grid.render()["props"]))
            for area in (c for c in walk(preview) if str(c.tag) == "TextArea"):
                self.assertEqual(str(area.resize), '"vertical"')

    def test_routes_and_auth_guard_unchanged_and_no_new_state_or_network(self):
        root = Path(__file__).resolve().parents[1]
        app_tree = ast.parse((root / "pet_finder/Pet_Finder.py").read_text(encoding="utf-8"))
        pages = [node for node in ast.walk(app_tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "add_page"]
        routes = {kw.value.value: page for page in pages for kw in page.keywords if kw.arg == "route"}
        self.assertEqual(set(routes), {"/", "/login", "/register", "/home"})
        self.assertTrue(any(kw.arg == "on_load" and ast.unparse(kw.value) == "LoginState.require_auth" for kw in routes["/home"].keywords))
        self.assertIn("can_view_home", json.dumps(home_page().render()))
        module = ast.parse((root / "pet_finder/account_settings.py").read_text(encoding="utf-8"))
        self.assertFalse(any(isinstance(node, (ast.ClassDef, ast.AsyncFunctionDef)) for node in ast.walk(module)))
        imports = [ast.unparse(node) for node in ast.walk(module) if isinstance(node, (ast.Import, ast.ImportFrom))]
        self.assertFalse(any("httpx" in node or "services" in node for node in imports))


class AccountNavigationTests(unittest.IsolatedAsyncioTestCase):
    async def test_authenticated_names_follow_valid_session_changes_and_logout(self):
        for account_type, name in (("ADOTANTE", "Nome adotante offline"), ("ONG", "Nome organização offline")):
            auth = LoginState(_reflex_internal_init=True)
            session = AuthenticatedSession(
                token="offline-name-fixture", expires_at=time.time() + 3600,
                user=AuthenticatedUser(user_id=7, name=name, account_type=account_type),
            )
            with patch("Pet_Finder.auth.authenticate", new=AsyncMock(return_value=session)) as authenticate, patch(
                "httpx.AsyncClient", side_effect=AssertionError("HTTP forbidden")
            ):
                async for _ in auth.handle_submit({"email": "offline@example.test", "password": "offline-fixture"}):
                    pass
                authenticate.assert_awaited_once()
                self.assertEqual(auth.display_name, name)
                self.assertEqual(auth.account_type, account_type)
                self.assertEqual(auth.dict()[LoginState.get_full_name()]["display_name_rx_state_"], name)
                # Revalidation already updates the same private name in production.
                renamed = AuthenticatedUser(user_id=7, name=name + " atualizado", account_type=account_type)
                with patch("Pet_Finder.auth.get_current_user", new=AsyncMock(return_value=renamed)) as me:
                    async for _ in auth.require_auth():
                        pass
                    me.assert_awaited_once_with("offline-name-fixture")
                self.assertEqual(auth.display_name, renamed.name)
                self.assertEqual(auth.dict()[LoginState.get_full_name()]["display_name_rx_state_"], renamed.name)
                auth.logout()
                self.assertEqual(auth.display_name, "")
                self.assertEqual(auth._user_name, "")
                self.assertEqual(auth.dict()[LoginState.get_full_name()]["display_name_rx_state_"], "")

    async def test_name_hidden_for_absent_expired_unverified_or_unknown_session(self):
        for failure in ("absent", "expired", "unverified", "unknown"):
            auth = LoginState(_reflex_internal_init=True)
            auth._auth_token = "offline-name-fixture"
            auth._user_id = 7
            auth._user_name = "Nome que deve ficar privado"
            auth._account_type = "ADOTANTE"
            auth._expires_at = time.time() + 3600
            auth._home_verified = True
            if failure == "absent":
                auth._auth_token = ""
            elif failure == "expired":
                auth._expires_at = time.time() - 1
            elif failure == "unverified":
                auth._home_verified = False
            else:
                auth._account_type = "admin"
            with patch("httpx.AsyncClient", side_effect=AssertionError("HTTP forbidden")):
                self.assertEqual(auth.display_name, "")
                self.assertEqual(auth.dict()[LoginState.get_full_name()]["display_name_rx_state_"], "")
                authority = SimpleNamespace(can_view_home=auth.can_view_home, account_type=auth.account_type, display_name=auth.display_name, logout=LoginState.logout)
                with patch.object(settings, "LoginState", authority):
                    self.assertEqual(texts(settings.account_settings(_section_heading)), [])

    async def test_both_types_open_account_close_mobile_and_logout_blocks(self):
        for account_type in ("ADOTANTE", "ONG"):
            auth = LoginState(_reflex_internal_init=True)
            auth._auth_token = "offline-fixture"
            auth._user_id = 7
            auth._user_name = "Conta local"
            auth._account_type = account_type
            auth._expires_at = time.time() + 3600
            auth._home_verified = True
            home = HomeState(_reflex_internal_init=True)
            home.mobile_menu_open = True
            with patch.object(HomeState, "get_state", new=AsyncMock(return_value=auth)), patch("httpx.AsyncClient", side_effect=AssertionError("HTTP forbidden")):
                self.assertIsNone(await home.open_section("account"))
                self.assertEqual(home.active_section, "account")
                self.assertFalse(home.mobile_menu_open)
                self.assertTrue(auth.can_view_home)
                auth.logout()
                self.assertFalse(auth.can_view_home)
                self.assertIn("/login", str(await home.open_section("account")))


if __name__ == "__main__":
    unittest.main()
