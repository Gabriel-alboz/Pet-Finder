// Signup and retrieve an authentication token
query "auth/signup" verb=POST {
  api_group = "Authentication"

  input {
    // Tipo de conta: ADOTANTE ou ONG
    text account_type? filters=trim
  
    // Nome completo do adotante ou razao social da ONG
    text name? filters=trim
  
    // Endereço de e-mail do usuario
    email email? filters=trim|lower
  
    // Senha de acesso com no minimo 8 caracteres
    text password?
  
    // Telefone com DDD (10 ou 11 digitos)
    text phone? filters=trim
  
    // Endereço completo
    text address? filters=trim
  
    // Cidade de residencia ou sede
    text city? filters=trim
  
    // Sigla do estado (UF) em 2 letras
    text uf? filters=trim|upper
  
    // CPF do adotante (apenas se ADOTANTE)
    text cpf? filters=trim
  
    // Data de nascimento do adotante (apenas se ADOTANTE)
    date birth_date?
  
    // CNPJ da ONG (apenas se ONG)
    text cnpj? filters=trim
  
    // Descriçao da ONG e suas atividades (apenas se ONG)
    text description? filters=trim
  }

  stack {
    // Validate account type is ADOTANTE or ONG
    precondition ($input.account_type == "ADOTANTE" || $input.account_type == "ONG") {
      error_type = "inputerror"
      error = "Tipo de conta inválido. Deve ser ADOTANTE ou ONG."
    }
  
    // Validate that name is provided
    precondition ($input.name != null && ($input.name|strlen) > 0) {
      error_type = "inputerror"
      error = "O nome é obrigatório."
    }
  
    // Validate that email is provided
    precondition ($input.email != null && ($input.email|strlen) > 0) {
      error_type = "inputerror"
      error = "O e-mail é obrigatório."
    }
  
    // Validate password minimum length
    precondition ($input.password != null && ($input.password|strlen) >= 8) {
      error_type = "inputerror"
      error = "A senha deve conter pelo menos 8 caracteres."
    }
  
    // Validate password contains letters and numbers
    precondition (("/[a-zA-Z]/"|regex_matches:$input.password) && ("/[0-9]/"|regex_matches:$input.password)) {
      error_type = "inputerror"
      error = "A senha deve conter letras e números."
    }
  
    // Extract digits from phone number
    var $phone_digits {
      value = "/[^0-9]/"|regex_replace:"":$input.phone
    }
  
    // Validate phone number length (10 or 11 digits)
    precondition (($phone_digits|strlen) == 10 || ($phone_digits|strlen) == 11) {
      error_type = "inputerror"
      error = "Telefone deve conter 10 ou 11 dígitos com DDD."
    }
  
    // Validate that address is provided
    precondition ($input.address != null && ($input.address|strlen) > 0) {
      error_type = "inputerror"
      error = "O endereço é obrigatório."
    }
  
    // Validate that city is provided
    precondition ($input.city != null && ($input.city|strlen) > 0) {
      error_type = "inputerror"
      error = "A cidade é obrigatória."
    }
  
    // Define list of 27 valid Brazilian state codes (UF)
    var $valid_ufs {
      value = [
        "AC"
        "AL"
        "AP"
        "AM"
        "BA"
        "CE"
        "DF"
        "ES"
        "GO"
        "MA"
        "MT"
        "MS"
        "MG"
        "PA"
        "PB"
        "PR"
        "PE"
        "PI"
        "RJ"
        "RN"
        "RS"
        "RO"
        "RR"
        "SC"
        "SP"
        "SE"
        "TO"
      ]
    }
  
    // Validate UF matches one of the 27 Brazilian states
    precondition ($valid_ufs|some:$$ == $input.uf) {
      error_type = "inputerror"
      error = "UF inválida. Informe uma das 27 siglas de estados brasileiros."
    }
  
    // Check if a user record with that email exists
    db.get user {
      field_name = "email"
      field_value = $input.email
    } as $existing_email_user
  
    // Verify that the email being used to sign up is unique
    precondition ($existing_email_user == null) {
      error_type = "accessdenied"
      error = "An account with this email already exists."
    }
  
    // Initialize adopter profile container
    var $adopter_profile {
      value = null
    }
  
    // Initialize NGO profile container
    var $ngo_profile {
      value = null
    }
  
    // Perform specific validations based on account type
    conditional {
      if ($input.account_type == "ADOTANTE") {
        // Validate CPF is provided
        precondition ($input.cpf != null && ($input.cpf|strlen) > 0) {
          error_type = "inputerror"
          error = "O CPF é obrigatório para contas de adotante."
        }
      
        // Normalize CPF to numeric digits
        var $cpf_clean {
          value = "/[^0-9]/"|regex_replace:"":$input.cpf
        }
      
        // Validate CPF length
        precondition (($cpf_clean|strlen) == 11) {
          error_type = "inputerror"
          error = "CPF inválido. Deve conter 11 dígitos."
        }
      
        // Split CPF into array of digits
        var $cpf_digits {
          value = $cpf_clean|split:""
        }
      
        // Check for CPF with all identical digits
        precondition (($cpf_digits|unique|count) > 1) {
          error_type = "inputerror"
          error = "CPF inválido."
        }
      
        // Extract individual digits for CPF validation
        var $cpf_d1 {
          value = ($cpf_digits|get:0)|to_int
        }
      
        var $cpf_d2 {
          value = ($cpf_digits|get:1)|to_int
        }
      
        var $cpf_d3 {
          value = ($cpf_digits|get:2)|to_int
        }
      
        var $cpf_d4 {
          value = ($cpf_digits|get:3)|to_int
        }
      
        var $cpf_d5 {
          value = ($cpf_digits|get:4)|to_int
        }
      
        var $cpf_d6 {
          value = ($cpf_digits|get:5)|to_int
        }
      
        var $cpf_d7 {
          value = ($cpf_digits|get:6)|to_int
        }
      
        var $cpf_d8 {
          value = ($cpf_digits|get:7)|to_int
        }
      
        var $cpf_d9 {
          value = ($cpf_digits|get:8)|to_int
        }
      
        var $cpf_d10 {
          value = ($cpf_digits|get:9)|to_int
        }
      
        var $cpf_d11 {
          value = ($cpf_digits|get:10)|to_int
        }
      
        // Calculate sum for first CPF verification digit
        var $cpf_sum1 {
          value = ($cpf_d1 * 10) + ($cpf_d2 * 9) + ($cpf_d3 * 8) + ($cpf_d4 * 7) + ($cpf_d5 * 6) + ($cpf_d6 * 5) + ($cpf_d7 * 4) + ($cpf_d8 * 3) + ($cpf_d9 * 2)
        }
      
        // Calculate remainder for first verification digit
        var $cpf_rem1 {
          value = ($cpf_sum1 * 10) % 11
        }
      
        // Adjust remainder if equal to 10
        conditional {
          if ($cpf_rem1 == 10) {
            var.update $cpf_rem1 {
              value = 0
            }
          }
        }
      
        // Calculate sum for second CPF verification digit
        var $cpf_sum2 {
          value = ($cpf_d1 * 11) + ($cpf_d2 * 10) + ($cpf_d3 * 9) + ($cpf_d4 * 8) + ($cpf_d5 * 7) + ($cpf_d6 * 6) + ($cpf_d7 * 5) + ($cpf_d8 * 4) + ($cpf_d9 * 3) + ($cpf_d10 * 2)
        }
      
        // Calculate remainder for second verification digit
        var $cpf_rem2 {
          value = ($cpf_sum2 * 10) % 11
        }
      
        // Adjust remainder if equal to 10
        conditional {
          if ($cpf_rem2 == 10) {
            var.update $cpf_rem2 {
              value = 0
            }
          }
        }
      
        // Verify both CPF check digits match
        precondition ($cpf_d10 == $cpf_rem1 && $cpf_d11 == $cpf_rem2) {
          error_type = "inputerror"
          error = "CPF inválido."
        }
      
        // Validate birth date is provided
        precondition ($input.birth_date != null) {
          error_type = "inputerror"
          error = "Data de nascimento é obrigatória para adotantes."
        }
      
        // Validate birth date is in the past
        precondition (($input.birth_date|to_timestamp) < ("now"|to_timestamp)) {
          error_type = "inputerror"
          error = "Data de nascimento deve ser uma data no passado."
        }
      
        // Query database to check if CPF is already registered
        db.query user {
          where = $db.user.adopter_profile @> {cpf: $cpf_clean}
          return = {type: "single"}
        } as $existing_cpf_user
      
        // Reject if CPF is already registered
        precondition ($existing_cpf_user == null) {
          error_type = "inputerror"
          error = "Não foi possível concluir o cadastro com os dados informados."
        }
      
        // Populate adopter profile object
        var.update $adopter_profile {
          value = {cpf: $cpf_clean, birth_date: $input.birth_date}
        }
      }
    
      else {
        // Validate CNPJ is provided
        precondition ($input.cnpj != null && ($input.cnpj|strlen) > 0) {
          error_type = "inputerror"
          error = "O CNPJ é obrigatório para contas de ONG."
        }
      
        // Normalize CNPJ to numeric digits
        var $cnpj_clean {
          value = "/[^0-9]/"|regex_replace:"":$input.cnpj
        }
      
        // Validate CNPJ length
        precondition (($cnpj_clean|strlen) == 14) {
          error_type = "inputerror"
          error = "CNPJ inválido. Deve conter 14 dígitos."
        }
      
        // Split CNPJ into array of digits
        var $cnpj_digits {
          value = $cnpj_clean|split:""
        }
      
        // Check for CNPJ with all identical digits
        precondition (($cnpj_digits|unique|count) > 1) {
          error_type = "inputerror"
          error = "CNPJ inválido."
        }
      
        // Extract individual digits for CNPJ validation
        var $c1 {
          value = ($cnpj_digits|get:0)|to_int
        }
      
        var $c2 {
          value = ($cnpj_digits|get:1)|to_int
        }
      
        var $c3 {
          value = ($cnpj_digits|get:2)|to_int
        }
      
        var $c4 {
          value = ($cnpj_digits|get:3)|to_int
        }
      
        var $c5 {
          value = ($cnpj_digits|get:4)|to_int
        }
      
        var $c6 {
          value = ($cnpj_digits|get:5)|to_int
        }
      
        var $c7 {
          value = ($cnpj_digits|get:6)|to_int
        }
      
        var $c8 {
          value = ($cnpj_digits|get:7)|to_int
        }
      
        var $c9 {
          value = ($cnpj_digits|get:8)|to_int
        }
      
        var $c10 {
          value = ($cnpj_digits|get:9)|to_int
        }
      
        var $c11 {
          value = ($cnpj_digits|get:10)|to_int
        }
      
        var $c12 {
          value = ($cnpj_digits|get:11)|to_int
        }
      
        var $c13 {
          value = ($cnpj_digits|get:12)|to_int
        }
      
        var $c14 {
          value = ($cnpj_digits|get:13)|to_int
        }
      
        // Calculate sum for first CNPJ verification digit
        var $cnpj_sum1 {
          value = ($c1 * 5) + ($c2 * 4) + ($c3 * 3) + ($c4 * 2) + ($c5 * 9) + ($c6 * 8) + ($c7 * 7) + ($c8 * 6) + ($c9 * 5) + ($c10 * 4) + ($c11 * 3) + ($c12 * 2)
        }
      
        // Calculate remainder for first verification digit
        var $cnpj_rem1 {
          value = $cnpj_sum1 % 11
        }
      
        // Determine expected 13th digit
        var $expected_c13 {
          value = 0
        }
      
        conditional {
          if ($cnpj_rem1 >= 2) {
            var.update $expected_c13 {
              value = 11 - $cnpj_rem1
            }
          }
        }
      
        // Calculate sum for second CNPJ verification digit
        var $cnpj_sum2 {
          value = ($c1 * 6) + ($c2 * 5) + ($c3 * 4) + ($c4 * 3) + ($c5 * 2) + ($c6 * 9) + ($c7 * 8) + ($c8 * 7) + ($c9 * 6) + ($c10 * 5) + ($c11 * 4) + ($c12 * 3) + ($c13 * 2)
        }
      
        // Calculate remainder for second verification digit
        var $cnpj_rem2 {
          value = $cnpj_sum2 % 11
        }
      
        // Determine expected 14th digit
        var $expected_c14 {
          value = 0
        }
      
        conditional {
          if ($cnpj_rem2 >= 2) {
            var.update $expected_c14 {
              value = 11 - $cnpj_rem2
            }
          }
        }
      
        // Verify both CNPJ check digits match
        precondition ($c13 == $expected_c13 && $c14 == $expected_c14) {
          error_type = "inputerror"
          error = "CNPJ inválido."
        }
      
        // Validate NGO description is provided
        precondition ($input.description != null && ($input.description|strlen) > 0) {
          error_type = "inputerror"
          error = "A descrição da ONG é obrigatória."
        }
      
        // Query database to check if CNPJ is already registered
        db.query user {
          where = $db.user.ngo_profile @> {cnpj: $cnpj_clean}
          return = {type: "single"}
        } as $existing_cnpj_user
      
        // Reject if CNPJ is already registered
        precondition ($existing_cnpj_user == null) {
          error_type = "inputerror"
          error = "Não foi possível concluir o cadastro com os dados informados."
        }
      
        // Populate NGO profile object
        var.update $ngo_profile {
          value = {cnpj: $cnpj_clean, description: $input.description}
        }
      }
    }
  
    // Create a new user record in the database
    db.add user {
      data = {
        created_at     : "now"
        name           : $input.name
        email          : $input.email
        password       : $input.password
        role           : "member"
        account_type   : $input.account_type
        phone          : $phone_digits
        address        : $input.address
        city           : $input.city
        uf             : $input.uf
        adopter_profile: $adopter_profile
        ngo_profile    : $ngo_profile
      }
    } as $user
  
    // Create an authentication token for the new user
    security.create_auth_token {
      table = "user"
      extras = {}
      expiration = 86400
      id = $user.id
    } as $authToken
  
    // Create an event log for signup
    function.run "Quick Start/log_event" {
      input = {
        user_id : $user.id
        action  : "signup"
        metadata: {
        user_id     : $user.id
        account_type: $user.account_type
        action      : "signup"
      }
      }
    } as $event_log
  }

  response = {
    authToken   : $authToken
    user_id     : $user.id
    account_type: $user.account_type
    user        : ```
      {
        id             : $user.id
        name           : $user.name
        email          : $user.email
        account_type   : $user.account_type
        phone          : $user.phone
        address        : $user.address
        city           : $user.city
        uf             : $user.uf
        adopter_profile: $user.adopter_profile
        ngo_profile    : $user.ngo_profile
      }
      ```
  }

  tags = ["xano:quick-start"]
  guid = "K5iU4tg0bkAPoi_zDXocvJ2Wzg0"
}