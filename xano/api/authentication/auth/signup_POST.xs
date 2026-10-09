// Create an account for adopter or ONG and return a session token.
query "auth/signup" verb=POST {
  api_group = "Authentication"

  input {
    text account_type? filters=trim
    text name?
    email email? filters=trim|lower
    text password?
    text phone?
    text address?
    text city?
    text uf?
    text cpf?
    date birth_date?
    text cnpj?
    text description?
  }

  stack {
    precondition ($input.account_type != null) {
      error_type = "accessdenied"
      error = "Account type is required."
    }

    precondition (($input.account_type == "ADOTANTE") || ($input.account_type == "ONG")) {
      error_type = "accessdenied"
      error = "Account type must be ADOTANTE or ONG."
    }

    precondition ($input.email != null) {
      error_type = "accessdenied"
      error = "Email is required."
    }

    precondition ($input.password != null) {
      error_type = "accessdenied"
      error = "Password is required."
    }

    // Shared global uniqueness for the login identity.
    db.get user {
      field_name = "email"
      field_value = $input.email
    } as $user_by_email

    precondition ($user_by_email == null) {
      error_type = "accessdenied"
      error = "An account with this email already exists."
    }

    conditional {
      if ($input.account_type == "ADOTANTE") {
        precondition ($input.name != null) {
          error_type = "accessdenied"
          error = "Full name is required for adopter accounts."
        }
        precondition ($input.cpf != null) {
          error_type = "accessdenied"
          error = "CPF is required for adopter accounts."
        }
        precondition ($input.birth_date != null) {
          error_type = "accessdenied"
          error = "Birth date is required for adopter accounts."
        }
        precondition ($input.phone != null) {
          error_type = "accessdenied"
          error = "Phone is required for adopter accounts."
        }
        precondition ($input.address != null) {
          error_type = "accessdenied"
          error = "Address is required for adopter accounts."
        }
        precondition ($input.city != null) {
          error_type = "accessdenied"
          error = "City is required for adopter accounts."
        }
        precondition ($input.uf != null) {
          error_type = "accessdenied"
          error = "UF is required for adopter accounts."
        }

        db.get user {
          field_name = "adopter_profile.cpf"
          field_value = $input.cpf
        } as $user_by_cpf

        precondition ($user_by_cpf == null) {
          error_type = "accessdenied"
          error = "This CPF is already registered to another adopter account."
        }
      }
      elseif ($input.account_type == "ONG") {
        precondition ($input.name != null) {
          error_type = "accessdenied"
          error = "Organization name is required for ONG accounts."
        }
        precondition ($input.cnpj != null) {
          error_type = "accessdenied"
          error = "CNPJ is required for ONG accounts."
        }
        precondition ($input.phone != null) {
          error_type = "accessdenied"
          error = "Phone is required for ONG accounts."
        }
        precondition ($input.address != null) {
          error_type = "accessdenied"
          error = "Address is required for ONG accounts."
        }
        precondition ($input.city != null) {
          error_type = "accessdenied"
          error = "City is required for ONG accounts."
        }
        precondition ($input.uf != null) {
          error_type = "accessdenied"
          error = "UF is required for ONG accounts."
        }
        precondition ($input.description != null) {
          error_type = "accessdenied"
          error = "Description is required for ONG accounts."
        }

        db.get user {
          field_name = "ngo_profile.cnpj"
          field_value = $input.cnpj
        } as $user_by_cnpj

        precondition ($user_by_cnpj == null) {
          error_type = "accessdenied"
          error = "This CNPJ is already registered to another ONG account."
        }
      }
    }

    db.add user {
      data = {
        created_at    : "now"
        name          : $input.name
        email         : $input.email
        password      : $input.password
        role          : "member"
        account_type  : $input.account_type
        phone         : $input.phone
        address       : $input.address
        city          : $input.city
        uf            : $input.uf
        adopter_profile: {
          cpf       : $input.cpf
          birth_date: $input.birth_date
        }
        ngo_profile   : {
          cnpj      : $input.cnpj
          description: $input.description
        }
      }
    } as $user

    security.create_auth_token {
      table = "user"
      extras = {}
      expiration = 86400
      id = $user.id
    } as $authToken

    var $safe_event_metadata {
      value = {
        account_type: $user.account_type
      }
    }

    function.run "Quick Start/log_event" {
      input = {
        user_id: $user.id
        action : "signup"
        metadata: $safe_event_metadata
      }
    } as $event_log
  }

  response = {
    authToken   : $authToken
    user_id     : $user.id
    account_type: $user.account_type
    user        : {
      id         : $user.id
      name       : $user.name
      email      : $user.email
      account_type: $user.account_type
      phone      : $user.phone
      address    : $user.address
      city       : $user.city
      uf         : $user.uf
      adopter_profile: $user.adopter_profile
      ngo_profile: $user.ngo_profile
    }
  }
  tags = ["xano:quick-start"]
  guid = "K5iU4tg0bkAPoi_zDXocvJ2Wzg0"
}