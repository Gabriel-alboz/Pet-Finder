"""Local section navigation and demonstrative UI; no live backend requests."""

import json
import time
import unittest
from unittest.mock import AsyncMock, patch

from Pet_Finder.auth import LoginState
from Pet_Finder.home import (
    HomeState,
    _chats_content,
    _home_layout,
    _sidebar,
    home_page,
)


def walk(component):
    yield component
    for child in component.children:
        yield from walk(child)


def texts(component):
    """Decode rendered literal text, independently of JS unicode escaping."""
    found = []

    def visit(value):
        if isinstance(value, dict):
            if value.get("cond_state") in ("true", "false"):
                branch = "true_value" if value["cond_state"] == "true" else "false_value"
                visit(value[branch])
                return
            content = value.get("contents")
            if isinstance(content, str):
                try:
                    found.append(json.loads(content))
                except (ValueError, TypeError):
                    pass
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(component.render())
    return found


class ChatsNavigationTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.auth = LoginState(_reflex_internal_init=True)
        self.home = HomeState(_reflex_internal_init=True)

    def authorize(self, account_type):
        self.auth._auth_token = "offline-chat-fixture"
        self.auth._user_id = 7
        self.auth._user_name = "Conta de teste local"
        self.auth._account_type = account_type
        self.auth._expires_at = time.time() + 3600
        self.auth._home_verified = True

    async def navigate(self, section):
        with patch.object(HomeState, "get_state", new=AsyncMock(return_value=self.auth)):
            with patch("httpx.AsyncClient", side_effect=AssertionError("HTTP forbidden")):
                return await self.home.open_section(section)

    async def test_both_profiles_open_chats_close_mobile_and_return_home(self):
        for account_type in ("ADOTANTE", "ONG"):
            with self.subTest(account_type=account_type):
                self.authorize(account_type)
                self.home.mobile_menu_open = True
                self.assertIsNone(await self.navigate("chats"))
                self.assertEqual(self.home.active_section, "chats")
                self.assertFalse(self.home.mobile_menu_open)
                await self.navigate("home")
                self.assertEqual(self.home.active_section, "home")

    async def test_anonymous_expired_unverified_and_unclassified_are_blocked(self):
        for failure in ("anonymous", "expired", "unverified", "unclassified"):
            with self.subTest(failure=failure):
                self.authorize("ADOTANTE")
                if failure == "anonymous":
                    self.auth._clear_session()
                elif failure == "expired":
                    self.auth._expires_at = time.time() - 1
                elif failure == "unverified":
                    self.auth._home_verified = False
                else:
                    self.auth._account_type = ""
                self.home.active_section = "home"
                event = await self.navigate("chats")
                self.assertIn("/login", str(event))
                self.assertEqual(self.home.active_section, "home")
                self.assertFalse(self.auth.can_view_home)

    async def test_logout_prevents_reopening_chats(self):
        self.authorize("ONG")
        await self.navigate("chats")
        self.auth.logout()
        event = await self.navigate("chats")
        self.assertIn("/login", str(event))
        self.assertEqual(self.auth._auth_token, "")

    async def test_existing_sections_remain_accessible(self):
        self.authorize("ADOTANTE")
        for section in ("ongs", "pets", "quiz", "account", "home"):
            await self.navigate(section)
            self.assertEqual(self.home.active_section, section)


class ChatsComponentsTests(unittest.TestCase):
    def test_preview_has_requested_copy_without_message_entry_or_network(self):
        with patch("httpx.AsyncClient", side_effect=AssertionError("HTTP forbidden")):
            preview = _chats_content()
            rendered_text = texts(preview)
        for expected in (
            "Chats",
            "Converse com ONGs e adotantes e acompanhe suas conversas.",
            "Você ainda não possui conversas.",
            "Quando iniciar uma conversa, ela aparecerá aqui.",
            "Interface demonstrativa: o chat ainda não está conectado ao backend.",
        ):
            self.assertIn(expected, rendered_text)
        self.assertFalse(any("TextField" in str(c.tag) or "TextArea" in str(c.tag) for c in walk(preview)))
        self.assertTrue(any(c.render().get("name") == "LucideMessagesSquare" for c in walk(preview)))

    def test_shared_sidebar_exposes_chats_with_selection_and_hover_on_both_layouts(self):
        for mobile in (False, True):
            sidebar = _sidebar(mobile=mobile)
            buttons = [c for c in walk(sidebar) if "Button" in str(c.tag) and "Chats" in texts(c)]
            self.assertEqual(len(buttons), 1)
            props = " ".join(buttons[0].render()["props"])
            self.assertIn("open_section", props)
            self.assertIn('"chats"', props)
            self.assertIn("aria-current", props)
            self.assertIn("&:hover", props)
            self.assertIn("&:focus", props)

    def test_home_keeps_auth_gate_and_responsive_menu_controls(self):
        page = json.dumps(home_page().render())
        layout = json.dumps(_home_layout().render())
        self.assertIn("can_view_home", page)
        self.assertIn("toggle_mobile_menu", layout)
        self.assertIn("mobile_menu_open", layout)
        self.assertIn("min-width: 48em", layout)
        self.assertIn("16rem", layout)

if __name__ == "__main__":
    unittest.main()
