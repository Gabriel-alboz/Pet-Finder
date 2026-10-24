"""Public Home preview and section navigation for Pet Finder."""

import reflex as rx


SECTIONS = {
    "home": "Início",
    "pets": "Pets",
    "ongs": "ONGs cadastradas",
    "quiz": "Quiz de compatibilidade",
    "account": "Configurações da conta",
}


class HomeState(rx.State):
    active_section: str = "home"
    mobile_menu_open: bool = False

    def open_section(self, section: str):
        if section in SECTIONS:
            self.active_section = section
            self.mobile_menu_open = False

    def toggle_mobile_menu(self):
        self.mobile_menu_open = not self.mobile_menu_open


def _nav_item(section: str, icon: str) -> rx.Component:
    return rx.button(
        rx.hstack(
            rx.icon(tag=icon, size=18),
            rx.text(SECTIONS[section], text_align="left"),
            width="100%",
            align="center",
            spacing="3",
        ),
        on_click=HomeState.open_section(section),
        width="100%",
        justify_content="flex-start",
        padding="0.75rem 0.9rem",
        border_radius="0.8rem",
        background=rx.cond(HomeState.active_section == section, "#F5F3FF", "transparent"),
        color=rx.cond(HomeState.active_section == section, "#5B21B6", "#4B5563"),
        font_weight=rx.cond(HomeState.active_section == section, "600", "500"),
        box_shadow="none",
        variant="soft",
        **{"aria-current": rx.cond(HomeState.active_section == section, "page", "false")},
        _hover={"background": "#F5F3FF", "color": "#5B21B6"},
        _focus={"outline": "2px solid #7C3AED", "outline_offset": "2px"},
    )


def _brand() -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.icon(tag="paw-print", size=22, color="#7C3AED"),
            padding="0.65rem",
            border_radius="0.9rem",
            background="linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%)",
        ),
        rx.text("Pet Finder", font_weight="700", font_size="1.15rem", color="#4C1D95"),
        align="center",
        spacing="3",
    )


def _account_footer() -> rx.Component:
    return rx.vstack(
        rx.divider(color="#E5E7EB"),
        rx.hstack(
            rx.center(
                rx.icon(tag="user-round", size=19, color="#5B21B6"),
                width="2.7rem",
                height="2.7rem",
                border_radius="999px",
                background="#EDE9FE",
                flex_shrink="0",
            ),
            rx.vstack(
                rx.text("Visitante", font_weight="600", color="#1F2937", font_size="0.9rem"),
                rx.text("Sessão não conectada", color="#6B7280", font_size="0.75rem"),
                spacing="0",
                align="start",
            ),
            width="100%",
            align="center",
            spacing="3",
        ),
        rx.link(
            rx.button(
                rx.hstack(rx.icon(tag="log-in", size=17), rx.text("Ir para o login"), spacing="2"),
                width="100%",
                variant="soft",
                color="#5B21B6",
                background="#F5F3FF",
                border_radius="0.8rem",
                _focus={"outline": "2px solid #7C3AED", "outline_offset": "2px"},
            ),
            href="/login",
            width="100%",
        ),
        width="100%",
        spacing="3",
        align="stretch",
        margin_top="auto",
    )


def _sidebar(*, mobile: bool = False) -> rx.Component:
    return rx.vstack(
        _brand(),
        rx.vstack(
            rx.text("MENU", color="#9CA3AF", font_size="0.72rem", font_weight="700", letter_spacing="0.08em", padding_x="0.9rem"),
            _nav_item("home", "house"),
            _nav_item("ongs", "building-2"),
            _nav_item("pets", "paw-print"),
            _nav_item("quiz", "clipboard-list"),
            _nav_item("account", "settings-2"),
            width="100%",
            align="stretch",
            spacing="2",
        ),
        _account_footer(),
        width="100%",
        height="100%" if mobile else "100vh",
        padding="1.25rem",
        background="#FFFFFF",
        border_right="1px solid #E5E7EB" if not mobile else "none",
        align="stretch",
        spacing="7",
    )


def _empty_state(
    title: str,
    description: str,
    icon: str,
    action: str = "",
    action_section: str = "home",
) -> rx.Component:
    return rx.vstack(
        rx.center(
            rx.icon(tag=icon, size=27, color="#7C3AED"),
            width="3.5rem",
            height="3.5rem",
            border_radius="1rem",
            background="#F5F3FF",
        ),
        rx.heading(title, size="4", color="#1F2937", text_align="center"),
        rx.text(description, color="#6B7280", text_align="center", max_width="32rem", line_height="1.6"),
        rx.cond(
            action != "",
            rx.button(
                action,
                on_click=HomeState.open_section(action_section),
                color="#5B21B6",
                background="#F5F3FF",
                border_radius="0.8rem",
                _hover={"background": "#EDE9FE"},
                _focus={"outline": "2px solid #7C3AED", "outline_offset": "2px"},
            ),
        ),
        width="100%",
        align="center",
        justify="center",
        spacing="3",
        padding=["1.25rem", "1.75rem", "2.25rem"],
        background="#FFFFFF",
        border="1px solid #E5E7EB",
        border_radius="1.2rem",
        box_shadow="0 12px 30px rgba(91, 33, 182, 0.06)",
    )


def _section_heading(title: str, description: str) -> rx.Component:
    return rx.vstack(
        rx.heading(title, size="7", line_height="1.15", color="#1F2937"),
        rx.text(description, color="#6B7280", font_size="1rem", line_height="1.6"),
        width="100%",
        align="start",
        spacing="2",
    )


def _home_content() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.text("Bem-vindo ao Pet Finder", color="#5B21B6", font_weight="600", font_size="0.9rem"),
            rx.heading("Seu próximo melhor amigo pode estar mais perto do que você imagina.", size="7", line_height="1.15", color="#1F2937", max_width="54rem"),
            rx.text("Descubra animais e organizações que fazem a adoção responsável acontecer.", color="#6B7280", font_size="1rem", max_width="42rem", line_height="1.6"),
            width="100%",
            align="start",
            spacing="3",
        ),
        rx.hstack(
            rx.icon(tag="search", size=18, color="#9CA3AF"),
            rx.input(
                placeholder="A busca será ativada quando o catálogo estiver conectado ao Xano",
                disabled=True,
                width="100%",
                height="3.15rem",
                background="#FFFFFF",
                border="1px solid #D1D5DB",
                border_radius="0.85rem",
                color="#6B7280",
                aria_label="Busca indisponível até a conexão do catálogo",
            ),
            width="100%",
            max_width="52rem",
            padding_left="1rem",
            background="#FFFFFF",
            border="1px solid #D1D5DB",
            border_radius="0.85rem",
            align="center",
            spacing="3",
        ),
        rx.box(
            rx.flex(
                rx.vstack(
                    rx.text("ADOÇÃO RESPONSÁVEL", color="#EDE9FE", font_weight="700", font_size="0.75rem", letter_spacing="0.09em"),
                    rx.heading("Um novo amigo está esperando por você.", size="6", line_height="1.15", color="#FFFFFF", max_width="35rem"),
                    rx.text("Descubra animais que combinam com seu estilo de vida e transforme uma adoção em uma conexão para a vida toda.", color="rgba(255,255,255,0.86)", max_width="34rem", line_height="1.6"),
                    rx.flex(
                        rx.button(
                            rx.hstack(rx.text("Encontrar meu match"), rx.icon(tag="arrow-right", size=17), spacing="2"),
                            on_click=HomeState.open_section("quiz"),
                            background="#FFFFFF",
                            color="#5B21B6",
                            font_weight="700",
                            border_radius="0.9rem",
                            height="3.1rem",
                            _hover={"background": "#F5F3FF"},
                            _focus={"outline": "3px solid rgba(255,255,255,0.45)", "outline_offset": "2px"},
                        ),
                        rx.button(
                            "Explorar pets",
                            on_click=HomeState.open_section("pets"),
                            variant="soft",
                            color="#FFFFFF",
                            background="rgba(255,255,255,0.14)",
                            border="1px solid rgba(255,255,255,0.35)",
                            border_radius="0.9rem",
                            height="3.1rem",
                            _hover={"background": "rgba(255,255,255,0.22)"},
                            _focus={"outline": "3px solid rgba(255,255,255,0.45)", "outline_offset": "2px"},
                        ),
                        wrap="wrap",
                        spacing="3",
                        width="100%",
                    ),
                    align="start",
                    spacing="4",
                    width="100%",
                ),
                rx.center(
                    rx.icon(tag="paw-print", size=64, color="rgba(255,255,255,0.9)"),
                    width=["4.5rem", "6rem", "8rem"],
                    height=["4.5rem", "6rem", "8rem"],
                    border_radius="999px",
                    background="rgba(255,255,255,0.12)",
                    border="1px solid rgba(255,255,255,0.25)",
                    flex_shrink="0",
                    display=["none", "flex", "flex"],
                ),
                width="100%",
                align="center",
                justify="between",
                wrap="wrap",
                spacing="5",
            ),
            width="100%",
            padding=["1.4rem", "1.8rem", "2.4rem"],
            border_radius="1.8rem",
            background="linear-gradient(135deg, #6D28D9 0%, #5B21B6 55%, #4C1D95 100%)",
            box_shadow="0 24px 50px rgba(91, 33, 182, 0.2)",
        ),
        rx.hstack(
            rx.vstack(
                rx.hstack(rx.heading("Pets esperando por um lar", size="5", color="#1F2937"), rx.spacer(), rx.button("Ver catálogo", on_click=HomeState.open_section("pets"), variant="ghost", color="#7C3AED"), width="100%", align="center"),
                rx.text("Conheça os animais disponíveis para adoção.", color="#6B7280"),
                _empty_state("O catálogo está sendo preparado", "Assim que houver um endpoint de pets conectado, os animais disponíveis aparecerão aqui.", "paw-print"),
                width="100%", align="stretch", spacing="3",
            ),
            width="100%",
            align="stretch",
        ),
        rx.flex(
            rx.box(
                rx.vstack(
                    rx.hstack(rx.icon(tag="heart", size=19, color="#7C3AED"), rx.heading("Combina com você", size="4", color="#1F2937"), spacing="2"),
                    rx.text("Veja os animais com afinidade com seu perfil.", color="#6B7280", line_height="1.5"),
                    rx.text("O quiz e os resultados ainda não estão conectados.", color="#5B21B6", font_size="0.85rem", font_weight="600"),
                    rx.button("Conhecer o quiz", on_click=HomeState.open_section("quiz"), variant="soft", color="#5B21B6", background="#F5F3FF", border_radius="0.8rem", align_self="start"),
                    width="100%", align="start", spacing="3",
                ),
                padding="1.25rem", background="#FFFFFF", border="1px solid #E5E7EB", border_radius="1.2rem", width=["100%", "100%", "calc(50% - 0.5rem)"],
            ),
            rx.box(
                rx.vstack(
                    rx.hstack(rx.icon(tag="building-2", size=19, color="#7C3AED"), rx.heading("ONGs em destaque", size="4", color="#1F2937"), spacing="2"),
                    rx.text("Conheça as organizações que tornam a adoção possível.", color="#6B7280", line_height="1.5"),
                    rx.text("A listagem de organizações ainda não está conectada.", color="#5B21B6", font_size="0.85rem", font_weight="600"),
                    rx.button("Ver ONGs", on_click=HomeState.open_section("ongs"), variant="soft", color="#5B21B6", background="#F5F3FF", border_radius="0.8rem", align_self="start"),
                    width="100%", align="start", spacing="3",
                ),
                padding="1.25rem", background="#FFFFFF", border="1px solid #E5E7EB", border_radius="1.2rem", width=["100%", "100%", "calc(50% - 0.5rem)"],
            ),
            wrap="wrap",
            spacing="4",
            width="100%",
        ),
        width="100%",
        align="stretch",
        spacing="6",
    )


def _section_content() -> rx.Component:
    return rx.cond(
        HomeState.active_section == "home",
        _home_content(),
        rx.cond(
            HomeState.active_section == "pets",
            rx.vstack(
                _section_heading("Encontre seu novo melhor amigo", "Explore os pets disponíveis e conheça suas histórias."),
                _empty_state("Ainda não há catálogo conectado", "O projeto ainda não possui tabela nem endpoint confirmado para listar pets. Nenhum animal fictício será exibido.", "paw-print"),
                width="100%", align="stretch", spacing="5",
            ),
            rx.cond(
                HomeState.active_section == "ongs",
                rx.vstack(
                    _section_heading("ONGs cadastradas", "Conheça as organizações que trabalham para transformar a vida dos animais."),
                    _empty_state("A listagem de ONGs ainda não está disponível", "O Xano não possui um endpoint de organizações no snapshot local. Os dados institucionais serão exibidos quando houver um contrato confirmado.", "building-2"),
                    width="100%", align="stretch", spacing="5",
                ),
                rx.cond(
                    HomeState.active_section == "quiz",
                    rx.vstack(
                        _section_heading("Quiz de compatibilidade", "Descubra quais animais podem combinar com sua rotina e suas preferências."),
                        _empty_state("O quiz ainda não está disponível", "Ainda não existem perguntas, regras de compatibilidade ou endpoints de persistência definidos para esta experiência.", "clipboard-list", "Voltar ao início"),
                        width="100%", align="stretch", spacing="5",
                    ),
                    rx.vstack(
                        _section_heading("Configurações da conta", "Consulte e atualize as informações da sua conta."),
                        _empty_state("Sua sessão não está conectada", "O login atual ainda não estabelece uma sessão verificável. Acesse o login para continuar; nenhum perfil será inventado ou alterado.", "user-round"),
                        rx.link(rx.button("Ir para o login", background="#7C3AED", color="#FFFFFF", border_radius="0.8rem", _hover={"background": "#6D28D9"}), href="/login", align_self="start"),
                        width="100%", align="stretch", spacing="5",
                    ),
                ),
            ),
        ),
    )


def home_page() -> rx.Component:
    return rx.flex(
        rx.box(_sidebar(), width="16rem", min_width="16rem", display=["none", "none", "block"]),
        rx.vstack(
            rx.flex(
                _brand(),
                rx.button(
                    rx.icon(tag=rx.cond(HomeState.mobile_menu_open, "x", "menu"), size=21),
                    on_click=HomeState.toggle_mobile_menu,
                    variant="soft", color="#5B21B6", background="#F5F3FF", border_radius="0.8rem",
                    aria_label=rx.cond(HomeState.mobile_menu_open, "Fechar menu", "Abrir menu"),
                    _focus={"outline": "2px solid #7C3AED", "outline_offset": "2px"},
                ),
                display=["flex", "flex", "none"],
                width="100%",
                justify="between",
                align="center",
                padding="0.9rem 1rem",
                background="#FFFFFF",
                border_bottom="1px solid #E5E7EB",
            ),
            rx.cond(
                HomeState.mobile_menu_open,
                rx.box(_sidebar(mobile=True), display=["block", "block", "none"], width="100%", background="#FFFFFF", border_bottom="1px solid #E5E7EB"),
            ),
            rx.box(
                _section_content(),
                width="100%",
                max_width="1180px",
                margin_x="auto",
                padding_x=["1rem", "1.5rem", "2.5rem"],
                padding_y=["1.5rem", "2rem", "2.75rem"],
            ),
            width="100%",
            min_height="100vh",
            align="stretch",
            spacing="0",
        ),
        width="100%",
        min_height="100vh",
        align="stretch",
        background="radial-gradient(circle at top left, rgba(196,181,253,0.18), transparent 30%), linear-gradient(135deg, #F8F7FC 0%, #F5F3FF 35%, #EEF2FF 100%)",
    )
