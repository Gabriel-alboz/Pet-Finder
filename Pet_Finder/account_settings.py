"""Read-only account previews. No profile state, storage, or network operations."""

from collections.abc import Callable

import reflex as rx

from Pet_Finder.auth import LoginState


def _notice(message: str) -> rx.Component:
    return rx.text(
        message, color="#5B21B6", background="#F5F3FF",
        border="1px solid #DDD6FE", border_radius="0.8rem",
        padding="0.8rem 0.9rem", font_size="0.85rem", line_height="1.6",
        overflow_wrap="anywhere", width="100%", box_sizing="border-box",
    )


def _block(title: str, description: str, *children: rx.Component) -> rx.Component:
    return rx.vstack(
        rx.heading(title, size="4", color="#1F2937"),
        rx.text(description, color="#6B7280", font_size="0.9rem", line_height="1.6"),
        *children,
        width="100%", min_width="0", align="stretch", spacing="4",
        padding=["1rem", "1.5rem"], background="#FFFFFF",
        border="1px solid #E5E7EB", border_radius="1.2rem",
        box_sizing="border-box", overflow_wrap="anywhere",
    )


def _field(key: str, label: str, *, value="", placeholder="Disponível em breve", type_="text") -> rx.Component:
    field_id = f"account-preview-{key}"
    return rx.vstack(
        rx.el.label(label, html_for=field_id, color="#374151", font_size="0.9rem", font_weight="600"),
        rx.input(
            id=field_id, value=value, placeholder=placeholder, type=type_,
            read_only=True, auto_complete=False,
            width="100%", min_width="0", height="3.15rem", padding_x="1rem",
            color="#1F2937", background="#FFFFFF", border="1px solid #D1D5DB",
            border_radius="0.85rem", box_shadow="none",
            style={
                "&:focus-within": {"border_color": "#7C3AED", "outline": "2px solid rgba(124, 58, 237, 0.5)", "outline_offset": "2px"},
                # Radix styles its inner read-only input independently of the root.
                **({
                    "& .rt-TextFieldInput": {"color": "#1F2937", "WebkitTextFillColor": "#1F2937"},
                    "& .rt-TextFieldInput::placeholder": {"color": "#6B7280", "WebkitTextFillColor": "#6B7280", "opacity": "1"},
                } if key == "name" else {}),
            },
        ),
        width="100%", min_width="0", align="stretch", spacing="2",
    )


def _grid(*children: rx.Component) -> rx.Component:
    return rx.grid(
        *children, grid_template_columns=["minmax(0, 1fr)", "minmax(0, 1fr)", "repeat(2, minmax(0, 1fr))"],
        gap="1rem", width="100%", min_width="0",
    )


def _description(key: str, label: str, help_text: str, limit: int) -> rx.Component:
    field_id = f"account-preview-{key}"
    return rx.vstack(
        rx.el.label(label, html_for=field_id, color="#374151", font_size="0.9rem", font_weight="600"),
        rx.text(help_text, id=f"{field_id}-help", color="#6B7280", font_size="0.85rem"),
        rx.text_area(
            id=field_id, value="", read_only=True, max_length=limit, rows="4",
            placeholder="Disponível em breve", resize="vertical", width="100%", min_width="0",
            color="#1F2937", background="#FFFFFF", border="1px solid #D1D5DB",
            border_radius="0.85rem", padding="1rem", box_sizing="border-box",
            aria_describedby=f"{field_id}-help {field_id}-limit",
            style={"&:focus": {"outline": "2px solid rgba(124, 58, 237, 0.5)", "outline_offset": "2px"}},
        ),
        rx.text(f"Limite proposto: {limit:,} caracteres.".replace(",", "."), id=f"{field_id}-limit", color="#6B7280", font_size="0.85rem"),
        width="100%", min_width="0", align="stretch", spacing="2",
    )


def _identity(ngo: bool) -> rx.Component:
    return _grid(
        _field("name", "Nome da ONG" if ngo else "Nome completo", value=LoginState.display_name),
        _field("email", "E-mail", type_="email", placeholder="E-mail não disponível nesta prévia"),
    )


def _contact() -> rx.Component:
    return _grid(
        _field("phone", "Telefone", type_="tel"),
        _field("address", "Endereço"),
        _field("city", "Cidade"),
        _field("uf", "Estado"),
    )


def _security() -> rx.Component:
    return _block(
        "Segurança da conta", "Cuide dos seus dados de acesso.",
        rx.text("Alteração de senha e atualização de e-mail estarão disponíveis em uma próxima etapa, com validação de segurança.", color="#6B7280"),
        rx.text("A sessão atual é temporária. Você pode precisar entrar novamente após recarregar a página ou reiniciar o aplicativo. Sair encerra o acesso neste aplicativo.", color="#6B7280"),
        rx.button(
            "Sair", on_click=LoginState.logout, background="#7C3AED", color="#FFFFFF",
            border_radius="0.8rem", _hover={"background": "#6D28D9"}, align_self="start",
        ),
    )


def _adopter_blocks() -> list[rx.Component]:
    return [
        _block("Meus dados", "Somente o nome da sessão está disponível. O e-mail permanece somente leitura.", _identity(False), _contact()),
        _block("Sobre mim", "Sua apresentação pessoal.", _description("about", "Apresentação pessoal", "Conte um pouco sobre você e sua experiência com animais.", 1000)),
        _block(
            "Pet que procuro", "Prévia das preferências de adoção. As opções e a seleção de múltiplas preferências serão definidas futuramente.",
            _grid(*[
                _field(key, label)
                for key, label in (
                    ("species", "Espécie"), ("size", "Porte"), ("age", "Faixa etária"),
                    ("sex", "Sexo (opcional)"), ("interest-city", "Cidade de interesse"),
                    ("interest-uf", "Estado de interesse"),
                )
            ]),
            _description("desired-pet", "Descrição livre do pet desejado", "Descreva as características que você procura em um companheiro.", 1000),
        ),
        _block(
            "Privacidade e visibilidade", "Futuramente, você poderá escolher se ONGs podem encontrar seu perfil e iniciar contato.",
            *[
                rx.checkbox(label, checked=False, disabled=True, color_scheme="purple", size="2", aria_describedby="account-preview-privacy-info")
                for label in ("Permitir que ONGs encontrem meu perfil.", "Permitir que ONGs iniciem contato comigo.")
            ],
            rx.box(_notice("Recurso em desenvolvimento. Suas preferências ainda não são compartilhadas com ONGs."), id="account-preview-privacy-info"),
            rx.text("A futura visibilidade exigirá consentimento explícito e revogável. Documentos, credenciais e endereço privado não farão parte da descoberta de perfis.", color="#6B7280", font_size="0.85rem"),
        ),
        _security(),
    ]


def _ngo_blocks() -> list[rx.Component]:
    return [
        _block("Dados da organização", "Somente o nome da sessão está disponível. O e-mail permanece somente leitura.", _identity(True)),
        _block("Sobre a ONG", "Sua apresentação institucional.", _description("ngo-description", "Descrição institucional", "Apresente sua organização, sua missão e o trabalho realizado com os animais.", 2000)),
        _block("Localização e contato", "Telefone e endereço não são publicados automaticamente. A futura divulgação dependerá de definição explícita dos dados públicos.", _contact()),
        _block(
            "Meus pets", "Cadastre e gerencie os animais disponíveis para adoção pela sua organização.",
            _notice("Funcionalidade em desenvolvimento."),
            rx.button("Cadastrar pet — indisponível", disabled=True, variant="soft", color_scheme="purple", align_self="start", white_space="normal", max_width="100%", height="auto", padding="0.8rem 0.9rem"),
        ),
        _security(),
    ]


def _preview(ngo: bool, heading: Callable[[str, str], rx.Component]) -> rx.Component:
    return rx.vstack(
        heading(
            "Configurações da organização" if ngo else "Configurações da conta",
            "Gerencie as informações da sua ONG e prepare seu perfil para divulgar animais disponíveis para adoção." if ngo else "Gerencie suas informações e suas preferências de adoção.",
        ),
        _notice("Prévia de interface: os campos são somente leitura. Edição e salvamento ainda não estão disponíveis; nenhum dado é enviado por esta prévia."),
        *(_ngo_blocks() if ngo else _adopter_blocks()),
        width="100%", min_width="0", align="stretch", spacing="5", overflow_wrap="anywhere",
    )


def account_settings(heading: Callable[[str, str], rx.Component]) -> rx.Component:
    """Use only authenticated classification; unknown/invalid sessions show no data."""
    return rx.cond(
        LoginState.can_view_home,
        rx.cond(
            LoginState.account_type == "ADOTANTE", _preview(False, heading),
            rx.cond(LoginState.account_type == "ONG", _preview(True, heading), rx.fragment()),
        ),
        rx.fragment(),
    )
