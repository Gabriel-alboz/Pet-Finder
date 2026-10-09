// Login and retrieve an authentication token for either an adopter or ONG account.
query "auth/login" verb=POST {
  api_group = "Authentication"

  input {
    email email? filters=trim|lower
    text password?
  }

  stack {
    db.get user {
      field_name = "email"
      field_value = $input.email
      output = [
        "id", "name", "email", "password", "role", "account_type"
      ]
    } as $user

    precondition ($user != null) {
      error_type = "accessdenied"
      error = "Invalid Credentials."
    }

    security.check_password {
      text_password = $input.password
      hash_password = $user.password
    } as $pass_result

    precondition ($pass_result) {
      error_type = "accessdenied"
      error = "Invalid Credentials."
    }

    precondition (($user.role == "admin") || ($user.account_type == "ADOTANTE") || ($user.account_type == "ONG")) {
      error_type = "accessdenied"
      error = "Invalid Credentials."
    }

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
        action : "login"
        metadata: $safe_event_metadata
      }
    } as $event_log
  }

  response = {
    authToken   : $authToken
    user_id     : $user.id
    role        : $user.role
    account_type: $user.account_type
    user        : {
      id         : $user.id
      name       : $user.name
      email      : $user.email
      role       : $user.role
      account_type: $user.account_type
    }
  }
  tags = ["xano:quick-start"]
  guid = "y8PnuA7EsZpOrKe-9mBQqntGVhk"
}