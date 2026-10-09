import reflex as rx


class LoginState(rx.State):
    email: str = ""
    password: str = ""
    remember_me: bool = True
    show_password: bool = False
    is_loading: bool = False
    error_message: str = ""
    info_message: str = ""

    def set_email(self, value):
        self.email = value

    def set_password(self, value):
        self.password = value

    def toggle_password_visibility(self):
        self.show_password = not self.show_password

    def toggle_remember_me(self, value):
        self.remember_me = value

    def handle_submit(self):
        if not self.email or not self.password:
            self.error_message = "Informe seu e-mail e senha para continuar."
            self.info_message = ""
            return

        self.is_loading = True
        self.error_message = ""
        self.info_message = "A integração com o endpoint de autenticação do Xano será habilitada quando o backend estiver conectado."
        self.is_loading = False


def login_page() -> rx.Component:
    return rx.box(
        rx.flex(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.box(
                            rx.text("🐾", font_size="1.7rem"),
                            width="fit-content",
                            height="fit-content",
                            padding="0.65rem",
                            border_radius="0.9rem",
                            background="linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%)",
                            display="flex",
                            align_items="center",
                            justify_content="center",
                        ),
                        rx.text("Pet Finder", font_weight="700", font_size="1.15rem", color="#4C1D95"),
                        align="center",
                        spacing="3",
                    ),
                    rx.heading("Encontre seu novo melhor amigo", size="7", line_height="1.15", color="#1F2937"),
                    rx.text(
                        "Conecte pessoas a animais que precisam de um lar com cuidado, responsabilidade e carinho.",
                        color="#6B7280",
                        font_size="1rem",
                        max_width="28rem",
                    ),
                    rx.box(
                        rx.text("Acesso seguro para adotantes e ONGs", color="#5B21B6", font_weight="600", font_size="0.8rem"),
                        padding_x="0.9rem",
                        padding_y="0.45rem",
                        border_radius="999px",
                        background="rgba(124, 58, 237, 0.08)",
                    ),
                    rx.form(
                        rx.vstack(
                            rx.box(
                                rx.text("E-mail", color="#374151", font_size="0.9rem", font_weight="600", margin_bottom="0.5rem"),
                                rx.hstack(
                                    rx.box(
                                        rx.icon(tag="mail", size=18, color="#7C3AED"),
                                        height="3.15rem",
                                        padding_x="0.9rem",
                                        border="1px solid #D1D5DB",
                                        border_right="none",
                                        border_radius="0.85rem 0 0 0.85rem",
                                        background="#F8F7FC",
                                        display="flex",
                                        align_items="center",
                                        justify_content="center",
                                    ),
                                    rx.input(
                                        placeholder="seu@email.com",
                                        value=LoginState.email,
                                        on_change=LoginState.set_email,
                                        type_="email",
                                        border_radius="0 0.85rem 0.85rem 0",
                                        border_left="none",
                                        height="3.15rem",
                                        width="100%",
                                        background="#FFFFFF",
                                        border="1px solid #D1D5DB",
                                        border_color="#D1D5DB",
                                        color="#1F2937",
                                        box_shadow="none",
                                        padding_left="1rem",
                                        style={
                                            "&:focus-within": {
                                                "border_color": "#7C3AED",
                                                "outline": "2px solid rgba(124, 58, 237, 0.5)",
                                                "outline_offset": "2px",
                                            },
                                            ".rt-TextFieldInput::placeholder": {
                                                "color": "#6B7280",
                                                "opacity": "1",
                                            },
                                        },
                                    ),
                                    spacing="0",
                                    width="100%",
                                    align="center",
                                ),
                                width="100%",
                            ),
                            rx.box(
                                rx.text("Senha", color="#374151", font_size="0.9rem", font_weight="600", margin_bottom="0.5rem"),
                                rx.hstack(
                                    rx.box(
                                        rx.icon(tag="lock", size=18, color="#7C3AED"),
                                        height="3.15rem",
                                        padding_x="0.9rem",
                                        border="1px solid #D1D5DB",
                                        border_right="none",
                                        border_radius="0.85rem 0 0 0.85rem",
                                        background="#F8F7FC",
                                        display="flex",
                                        align_items="center",
                                        justify_content="center",
                                    ),
                                    rx.box(
                                        rx.cond(
                                            LoginState.show_password,
                                            rx.input(
                                                placeholder="Sua senha",
                                                value=LoginState.password,
                                                on_change=LoginState.set_password,
                                                type_="text",
                                                border_radius="0 0.85rem 0.85rem 0",
                                                border_left="none",
                                                height="3.15rem",
                                                width="100%",
                                                background="#FFFFFF",
                                                border="1px solid #D1D5DB",
                                                border_color="#D1D5DB",
                                                color="#1F2937",
                                                box_shadow="none",
                                                padding_left="1rem",
                                                padding_right="3.75rem",
                                                style={
                                                    "&:focus-within": {
                                                        "border_color": "#7C3AED",
                                                        "outline": "2px solid rgba(124, 58, 237, 0.5)",
                                                        "outline_offset": "2px",
                                                    },
                                                    ".rt-TextFieldInput::placeholder": {
                                                        "color": "#6B7280",
                                                        "opacity": "1",
                                                    },
                                                },
                                            ),
                                            rx.input(
                                                placeholder="Sua senha",
                                                value=LoginState.password,
                                                on_change=LoginState.set_password,
                                                type_="password",
                                                border_radius="0 0.85rem 0.85rem 0",
                                                border_left="none",
                                                height="3.15rem",
                                                width="100%",
                                                background="#FFFFFF",
                                                border="1px solid #D1D5DB",
                                                border_color="#D1D5DB",
                                                color="#1F2937",
                                                box_shadow="none",
                                                padding_left="1rem",
                                                padding_right="3.75rem",
                                                style={
                                                    "&:focus-within": {
                                                        "border_color": "#7C3AED",
                                                        "outline": "2px solid rgba(124, 58, 237, 0.5)",
                                                        "outline_offset": "2px",
                                                    },
                                                    ".rt-TextFieldInput::placeholder": {
                                                        "color": "#6B7280",
                                                        "opacity": "1",
                                                    },
                                                },
                                            ),
                                        ),
                                        rx.button(
                                            rx.cond(
                                                LoginState.show_password,
                                                rx.icon(tag="eye-off", size=16, color="#6b7280"),
                                                rx.icon(tag="eye", size=16, color="#6b7280"),
                                            ),
                                            on_click=LoginState.toggle_password_visibility,
                                            variant="soft",
                                            size="2",
                                            border_radius="0.85rem",
                                            position="absolute",
                                            right="0.35rem",
                                            top="50%",
                                            transform="translateY(-50%)",
                                            min_width="2.8rem",
                                            background="#F5F3FF",
                                            color="#5B21B6",
                                        ),
                                        position="relative",
                                        width="100%",
                                    ),
                                    spacing="0",
                                    width="100%",
                                    align="center",
                                ),
                                width="100%",
                            ),
                            rx.hstack(
                                rx.checkbox(
                                    "Mantenha-me conectado",
                                    checked=LoginState.remember_me,
                                    on_change=LoginState.toggle_remember_me,
                                    color="#7C3AED",
                                    size="2",
                                ).set(style=rx.Style({"color": "#374151"})),
                                rx.link("Esqueci minha senha", href="#", color="#7C3AED", font_weight="600"),
                                justify="between",
                                width="100%",
                                align="center",
                            ),
                            rx.cond(
                                LoginState.error_message != "",
                                rx.box(
                                    rx.text(LoginState.error_message, color="#b91c1c", font_size="0.9rem", font_weight="500"),
                                    background="#fef2f2",
                                    border="1px solid #fecaca",
                                    border_radius="0.8rem",
                                    padding="0.8rem 0.9rem",
                                    width="100%",
                                ),
                            ),
                            rx.cond(
                                LoginState.info_message != "",
                                rx.box(
                                    rx.text(LoginState.info_message, color="#5B21B6", font_size="0.85rem", font_weight="500"),
                                    background="#F5F3FF",
                                    border="1px solid #DDD6FE",
                                    border_radius="0.8rem",
                                    padding="0.8rem 0.9rem",
                                    width="100%",
                                ),
                            ),
                            rx.button(
                                "Entrar",
                                on_click=LoginState.handle_submit,
                                width="100%",
                                height="3.2rem",
                                background="linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%)",
                                color="#ffffff",
                                font_weight="700",
                                border_radius="0.9rem",
                                box_shadow="0 12px 30px rgba(124, 58, 237, 0.22)",
                                disabled=LoginState.is_loading,
                                _hover={"background": "linear-gradient(135deg, #6D28D9 0%, #4C1D95 100%)"},
                                _focus={"outline": "3px solid rgba(124, 58, 237, 0.2)", "outline_offset": "2px"},
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        as_="form",
                        on_submit=LoginState.handle_submit,
                        width="100%",
                    ),
                    rx.text(
                        "Ainda não tem conta?",
                        color="#6B7280",
                        font_size="0.95rem",
                    ),
                    rx.flex(
                        rx.link(
                            rx.box(
                                rx.text("Cadastro de adotante", font_weight="600", color="#1F2937"),
                                padding="0.85rem 1rem",
                                border="1px solid #E5E7EB",
                                border_radius="0.8rem",
                                background="#FFFFFF",
                                text_align="center",
                                width="100%",
                            ),
                            href="#",
                            width="100%",
                        ),
                        rx.link(
                            rx.box(
                                rx.text("Cadastro da ONG", font_weight="600", color="#1F2937"),
                                padding="0.85rem 1rem",
                                border="1px solid #E5E7EB",
                                border_radius="0.8rem",
                                background="#FFFFFF",
                                text_align="center",
                                width="100%",
                            ),
                            href="#",
                            width="100%",
                        ),
                        direction="column",
                        spacing="2",
                        width="100%",
                    ),
                    width="100%",
                    spacing="5",
                    align="stretch",
                    padding="0.25rem",
                ),
                width=["100%", "100%", "43%"],
                max_width="560px",
                padding_x=["1.1rem", "1.4rem", "2.2rem"],
                padding_y=["1.5rem", "2rem", "2.4rem"],
                background="#FFFFFF",
                border="1px solid rgba(124, 58, 237, 0.08)",
                border_radius="1.8rem",
                box_shadow="0 24px 50px rgba(91, 33, 182, 0.12)",
            ),
            rx.box(
                rx.vstack(
                    rx.heading("Muito mais que adoção, uma conexão de verdade.", size="6", color="#ffffff", text_align="center"),
                    rx.text(
                        "Encontre seu novo melhor amigo com o Pet Finder! Nosso quiz de compatibilidade ajuda você a descobrir pets que combinam com seu estilo de vida, sua rotina e seu perfil. Porque toda grande amizade começa com uma conexão especial.",
                        color="rgba(255,255,255,0.82)",
                        text_align="center",
                        max_width="26rem",
                    ),
                    rx.box(
                        rx.hstack(
                            rx.box(rx.text("🏠", font_size="1.3rem")),
                            rx.box(rx.text("Lares seguros", color="#ffffff", font_weight="600")),
                            align="center",
                            spacing="2",
                        ),
                        rx.hstack(
                            rx.box(rx.text("❤️", font_size="1.3rem")),
                            rx.box(rx.text("Historias com cuidado", color="#ffffff", font_weight="600")),
                            align="center",
                            spacing="2",
                        ),
                        rx.hstack(
                            rx.box(rx.text("🐱", font_size="1.3rem")),
                            rx.box(rx.text("Conexão com ONGs", color="#ffffff", font_weight="600")),
                            align="center",
                            spacing="2",
                        ),
                        spacing="3",
                        align="stretch",
                    ),
                    spacing="5",
                    align="center",
                ),
                width=["100%", "100%", "43%"],
                max_width="560px",
                background_image="linear-gradient(135deg, rgba(79, 70, 229, 0.82) 0%, rgba(91, 33, 182, 0.8) 45%, rgba(124, 58, 237, 0.75) 100%), url('https://images.unsplash.com/photo-1517849845537-4d257902454a?auto=format&fit=crop&w=1200&q=80')",
                background_size="cover",
                background_position="center",
                border_radius="2rem",
                padding=["1.3rem", "1.7rem", "2.3rem"],
                display="flex",
                align_items="center",
                justify_content="center",
                box_shadow="0 24px 50px rgba(91, 33, 182, 0.2)",
            ),
            direction="row",
            justify="center",
            align="stretch",
            width="100%",
            max_width="1180px",
            spacing="0",
            wrap="wrap",
        ),
        background="radial-gradient(circle at top left, rgba(196,181,253,0.45), transparent 30%), linear-gradient(135deg, #F8F7FC 0%, #F5F3FF 35%, #EEF2FF 100%)",
        min_height="100vh",
        padding_x=["1rem", "2rem", "4rem"],
        padding_y=["1.5rem", "2rem", "3rem"],
        display="flex",
        align_items="center",
        justify_content="center",
    )


def index() -> rx.Component:
    return login_page()


app = rx.App()
app.add_page(index, route="/")
app.add_page(login_page, route="/login")
