"""Registration page and server-side form state."""

import re
from datetime import datetime

import reflex as rx

from Pet_Finder.services.xano import XanoSignupError, create_account


BRAZIL_UFS = {
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
    "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
    "RS", "RO", "RR", "SC", "SP", "SE", "TO",
}


def _digits(value: str) -> str:
    return re.sub(r"\D", "", value)


def _format_birth_date(value: str) -> str:
    digits = _digits(value)[:8]
    if len(digits) <= 2:
        return f"{digits}/" if len(digits) == 2 else digits
    if len(digits) <= 4:
        day, month = digits[:2], digits[2:]
        return f"{day}/{month}/" if len(digits) == 4 else f"{day}/{month}"
    return f"{digits[:2]}/{digits[2:4]}/{digits[4:]}"


def _valid_cpf(value: str) -> bool:
    cpf = _digits(value)
    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False
    for length in (9, 10):
        weight = length + 1
        check = (sum(int(cpf[i]) * (weight - i) for i in range(length)) * 10) % 11
        if check == 10:
            check = 0
        if check != int(cpf[length]):
            return False
    return True


def _valid_cnpj(value: str) -> bool:
    cnpj = _digits(value)
    if len(cnpj) != 14 or len(set(cnpj)) == 1:
        return False
    for length, weights in ((12, (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)),
                            (13, (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2))):
        remainder = sum(int(cnpj[i]) * weights[i] for i in range(length)) % 11
        check = 0 if remainder < 2 else 11 - remainder
        if check != int(cnpj[length]):
            return False
    return True


class RegistrationState(rx.State):
    account_type: str = "ADOTANTE"
    adopter_name: str = ""
    adopter_email: str = ""
    adopter_phone: str = ""
    adopter_cpf: str = ""
    adopter_birth_date: str = ""
    adopter_address: str = ""
    adopter_city: str = ""
    adopter_uf: str = ""
    adopter_password: str = ""
    adopter_password_confirmation: str = ""
    ngo_name: str = ""
    ngo_email: str = ""
    ngo_phone: str = ""
    ngo_cnpj: str = ""
    ngo_address: str = ""
    ngo_city: str = ""
    ngo_uf: str = ""
    ngo_description: str = ""
    ngo_password: str = ""
    ngo_password_confirmation: str = ""
    show_password: bool = False
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""

    def set_adopter_name(self, value: str): self.adopter_name = value
    def set_adopter_email(self, value: str): self.adopter_email = value
    def set_adopter_phone(self, value: str): self.adopter_phone = value
    def set_adopter_cpf(self, value: str): self.adopter_cpf = value
    def set_adopter_birth_date(self, value: str): self.adopter_birth_date = _format_birth_date(value)
    def set_adopter_address(self, value: str): self.adopter_address = value
    def set_adopter_city(self, value: str): self.adopter_city = value
    def set_adopter_uf(self, value: str): self.adopter_uf = value
    def set_adopter_password(self, value: str): self.adopter_password = value
    def set_adopter_password_confirmation(self, value: str): self.adopter_password_confirmation = value
    def set_ngo_name(self, value: str): self.ngo_name = value
    def set_ngo_email(self, value: str): self.ngo_email = value
    def set_ngo_phone(self, value: str): self.ngo_phone = value
    def set_ngo_cnpj(self, value: str): self.ngo_cnpj = value
    def set_ngo_address(self, value: str): self.ngo_address = value
    def set_ngo_city(self, value: str): self.ngo_city = value
    def set_ngo_uf(self, value: str): self.ngo_uf = value
    def set_ngo_description(self, value: str): self.ngo_description = value
    def set_ngo_password(self, value: str): self.ngo_password = value
    def set_ngo_password_confirmation(self, value: str): self.ngo_password_confirmation = value

    def set_account_type(self, value: str | list[str]):
        if isinstance(value, list):
            value = value[0] if value else ""
        if value in {"ADOTANTE", "ONG"}:
            self.account_type = value
            self.error_message = ""
            self.success_message = ""

    def toggle_password_visibility(self):
        self.show_password = not self.show_password

    async def submit(self):
        if self.is_loading:
            return
        self.error_message = ""
        self.success_message = ""

        if self.account_type == "ADOTANTE":
            name = self.adopter_name.strip()
            email = self.adopter_email.strip().lower()
            password = self.adopter_password
            confirmation = self.adopter_password_confirmation
            phone = _digits(self.adopter_phone)
            cpf = _digits(self.adopter_cpf)
            address = self.adopter_address.strip()
            city = self.adopter_city.strip()
            uf = self.adopter_uf.strip().upper()
            birth_date = self.adopter_birth_date.strip().rstrip("/")
            if not all((name, email, password, confirmation, phone, cpf, address, city, uf, birth_date)):
                self.error_message = "Preencha todos os campos obrigatórios."
                return
            if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
                self.error_message = "Informe um e-mail válido."
                return
            if not _valid_cpf(cpf):
                self.error_message = "Informe um CPF válido."
                return
            if not 10 <= len(phone) <= 11:
                self.error_message = "Informe um telefone brasileiro válido com DDD."
                return
            if uf not in BRAZIL_UFS:
                self.error_message = "Selecione uma UF válida."
                return
            try:
                birth_date_iso = datetime.strptime(birth_date, "%d/%m/%Y").date().isoformat()
            except ValueError:
                self.error_message = "Informe uma data válida no formato dia/mês/ano."
                return
            if len(password) < 8 or not re.search(r"[A-Za-zÀ-ÿ]", password) or not re.search(r"\d", password):
                self.error_message = "A senha deve ter ao menos 8 caracteres, uma letra e um número."
                return
            if password != confirmation:
                self.error_message = "As senhas informadas não são iguais."
                return
            payload = {
                "account_type": "ADOTANTE", "name": name, "email": email,
                "password": password, "phone": phone, "cpf": cpf,
                "birth_date": birth_date_iso, "address": address, "city": city, "uf": uf,
            }
        else:
            name = self.ngo_name.strip()
            email = self.ngo_email.strip().lower()
            password = self.ngo_password
            confirmation = self.ngo_password_confirmation
            phone = _digits(self.ngo_phone)
            cnpj = _digits(self.ngo_cnpj)
            address = self.ngo_address.strip()
            city = self.ngo_city.strip()
            uf = self.ngo_uf.strip().upper()
            description = self.ngo_description.strip()
            if not all((name, email, password, confirmation, phone, cnpj, address, city, uf, description)):
                self.error_message = "Preencha todos os campos obrigatórios."
                return
            if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
                self.error_message = "Informe um e-mail válido."
                return
            if not _valid_cnpj(cnpj):
                self.error_message = "Informe um CNPJ válido."
                return
            if not 10 <= len(phone) <= 11:
                self.error_message = "Informe um telefone brasileiro válido com DDD."
                return
            if uf not in BRAZIL_UFS:
                self.error_message = "Selecione uma UF válida."
                return
            if len(password) < 8 or not re.search(r"[A-Za-zÀ-ÿ]", password) or not re.search(r"\d", password):
                self.error_message = "A senha deve ter ao menos 8 caracteres, uma letra e um número."
                return
            if password != confirmation:
                self.error_message = "As senhas informadas não são iguais."
                return
            payload = {
                "account_type": "ONG", "name": name, "email": email,
                "password": password, "phone": phone, "cnpj": cnpj,
                "address": address, "city": city, "uf": uf,
                "description": description,
            }

        self.is_loading = True
        try:
            await create_account(payload)
        except XanoSignupError as exc:
            self.error_message = str(exc)
        except Exception:
            self.error_message = "Não foi possível concluir o cadastro agora. Tente novamente mais tarde."
        else:
            self.success_message = "Cadastro concluído. Agora você já pode entrar com seu e-mail e senha."
            self.adopter_password = ""
            self.adopter_password_confirmation = ""
            self.ngo_password = ""
            self.ngo_password_confirmation = ""
        finally:
            self.is_loading = False


def _field(label: str, value, setter, placeholder: str, *, type_: str = "text") -> rx.Component:
    return rx.box(
        rx.text(label, color="#374151", font_size="0.9rem", font_weight="600", margin_bottom="0.5rem"),
        rx.input(
            value=value, on_change=setter, placeholder=placeholder, type_=type_,
            width="100%", height="3.15rem", padding_x="1rem", color="#1F2937",
            background="#FFFFFF", border="1px solid #D1D5DB", border_radius="0.85rem",
            box_shadow="none",
            style={"&:focus-within": {"border_color": "#7C3AED", "outline": "2px solid rgba(124, 58, 237, 0.5)", "outline_offset": "2px"}},
        ),
        width="100%",
    )


def _password_field(label: str, value, setter, placeholder: str) -> rx.Component:
    return rx.box(
        rx.text(label, color="#374151", font_size="0.9rem", font_weight="600", margin_bottom="0.5rem"),
        rx.box(
            rx.input(
                value=value, on_change=setter, placeholder=placeholder,
                type_=rx.cond(RegistrationState.show_password, "text", "password"),
                width="100%", height="3.15rem", padding_x="1rem", padding_right="3.75rem", color="#1F2937",
                background="#FFFFFF", border="1px solid #D1D5DB", border_radius="0.85rem",
            ),
            rx.button(
                rx.cond(
                    RegistrationState.show_password,
                    rx.icon(tag="eye-off", size=16, color="#6b7280"),
                    rx.icon(tag="eye", size=16, color="#6b7280"),
                ),
                on_click=RegistrationState.toggle_password_visibility,
                type="button", variant="soft", size="2", border_radius="0.85rem",
                position="absolute", right="0.35rem", top="50%", transform="translateY(-50%)",
                min_width="2.8rem", background="#F5F3FF", color="#5B21B6",
                **{"aria-label": rx.cond(RegistrationState.show_password, "Ocultar senhas", "Mostrar senhas")},
            ),
            position="relative", width="100%",
        ),
        width="100%",
    )


def _fields() -> rx.Component:
    adopter_fields = rx.vstack(
        _field("Nome completo *", RegistrationState.adopter_name, RegistrationState.set_adopter_name, "Seu nome"),
        _field("E-mail *", RegistrationState.adopter_email, RegistrationState.set_adopter_email, "seu@email.com", type_="email"),
        _field("Telefone com DDD *", RegistrationState.adopter_phone, RegistrationState.set_adopter_phone, "(11) 99999-9999", type_="tel"),
        _field("CPF *", RegistrationState.adopter_cpf, RegistrationState.set_adopter_cpf, "000.000.000-00"),
        _field("Data de nascimento *", RegistrationState.adopter_birth_date, RegistrationState.set_adopter_birth_date, "DD/MM/AAAA", type_="text"),
        _field("Endereço *", RegistrationState.adopter_address, RegistrationState.set_adopter_address, "Rua, número e complemento"),
        rx.hstack(
            _field("Cidade *", RegistrationState.adopter_city, RegistrationState.set_adopter_city, "Sua cidade"),
            _field("UF *", RegistrationState.adopter_uf, RegistrationState.set_adopter_uf, "SP"),
            width="100%", spacing="3", align="start",
        ),
        _password_field("Senha *", RegistrationState.adopter_password, RegistrationState.set_adopter_password, "Mínimo de 8 caracteres"),
        _password_field("Confirme a senha *", RegistrationState.adopter_password_confirmation, RegistrationState.set_adopter_password_confirmation, "Digite a senha novamente"),
        width="100%", spacing="4",
    )
    ngo_fields = rx.vstack(
        _field("Nome da organização *", RegistrationState.ngo_name, RegistrationState.set_ngo_name, "Nome da ONG"),
        _field("E-mail de contato *", RegistrationState.ngo_email, RegistrationState.set_ngo_email, "contato@ong.org.br", type_="email"),
        _field("Telefone com DDD *", RegistrationState.ngo_phone, RegistrationState.set_ngo_phone, "(11) 99999-9999", type_="tel"),
        _field("CNPJ *", RegistrationState.ngo_cnpj, RegistrationState.set_ngo_cnpj, "00.000.000/0000-00"),
        _field("Endereço *", RegistrationState.ngo_address, RegistrationState.set_ngo_address, "Rua, número e complemento"),
        rx.hstack(
            _field("Cidade *", RegistrationState.ngo_city, RegistrationState.set_ngo_city, "Sua cidade"),
            _field("UF *", RegistrationState.ngo_uf, RegistrationState.set_ngo_uf, "SP"),
            width="100%", spacing="3", align="start",
        ),
        _field("Sobre a organização *", RegistrationState.ngo_description, RegistrationState.set_ngo_description, "Conte brevemente sobre o trabalho da ONG"),
        _password_field("Senha *", RegistrationState.ngo_password, RegistrationState.set_ngo_password, "Mínimo de 8 caracteres"),
        _password_field("Confirme a senha *", RegistrationState.ngo_password_confirmation, RegistrationState.set_ngo_password_confirmation, "Digite a senha novamente"),
        width="100%", spacing="4",
    )
    return rx.cond(RegistrationState.account_type == "ADOTANTE", adopter_fields, ngo_fields)


def registration_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(rx.text("🐾", font_size="1.7rem"), padding="0.65rem", border_radius="0.9rem", background="linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%)"),
                rx.text("Pet Finder", font_weight="700", font_size="1.15rem", color="#4C1D95"),
                spacing="3", align="center",
            ),
            rx.heading("Crie sua conta", size="7", line_height="1.15", color="#1F2937"),
            rx.text("Aproximamos pessoas, ONGs e animais que precisam de um novo lar.", color="#6B7280", font_size="1rem"),
            rx.text("Seu perfil", color="#374151", font_size="0.9rem", font_weight="600", width="100%"),
            rx.segmented_control.root(
                rx.segmented_control.item("Quero adotar", value="ADOTANTE"),
                rx.segmented_control.item("Sou uma ONG", value="ONG"),
                value=RegistrationState.account_type,
                on_change=RegistrationState.set_account_type,
                width="100%",
            ),
            rx.cond(
                RegistrationState.account_type == "ONG",
                rx.text("O cadastro cria uma conta para a organização conforme os dados aceitos pelo Xano.", color="#6B7280", font_size="0.85rem"),
                rx.text("Crie seu perfil para iniciar sua jornada de adoção responsável.", color="#6B7280", font_size="0.85rem"),
            ),
            _fields(),
            rx.button(
                rx.cond(RegistrationState.is_loading, "Criando conta...", "Criar conta"),
                on_click=RegistrationState.submit, width="100%", height="3.2rem",
                background="linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%)", color="#ffffff",
                font_weight="700", border_radius="0.9rem",
                box_shadow="0 12px 30px rgba(124, 58, 237, 0.22)",
                disabled=RegistrationState.is_loading,
            ),
            rx.cond(
                RegistrationState.error_message != "",
                rx.box(rx.text(RegistrationState.error_message, color="#b91c1c", font_size="0.9rem", role="alert"), background="#fef2f2", border="1px solid #fecaca", border_radius="0.8rem", padding="0.8rem 0.9rem", width="100%"),
            ),
            rx.cond(
                RegistrationState.success_message != "",
                rx.box(rx.text(RegistrationState.success_message, color="#5B21B6", font_size="0.9rem", role="status"), background="#F5F3FF", border="1px solid #DDD6FE", border_radius="0.8rem", padding="0.8rem 0.9rem", width="100%"),
            ),
            rx.text("Já tem uma conta? ", rx.link("Acesse o login", href="/login", color="#7C3AED", font_weight="600"), color="#6B7280"),
            width="100%", max_width="560px", align="stretch", spacing="4",
        ),
        width="100%", min_height="100vh", display="flex", align_items="center", justify_content="center",
        padding_x=["1rem", "2rem", "4rem"], padding_y=["1.5rem", "2rem", "3rem"],
        background="radial-gradient(circle at top left, rgba(196,181,253,0.45), transparent 30%), linear-gradient(135deg, #F8F7FC 0%, #F5F3FF 35%, #EEF2FF 100%)",
    )
