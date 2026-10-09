// Return the authenticated user's safe account profile without exposing secrets.
query "auth/me" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = [
        "id", "created_at", "name", "email", "role", "account_type"
      ]
    } as $user

    var $safe_event_metadata {
      value = {
        account_type: $user.account_type
      }
    }

    function.run "Quick Start/log_event" {
      input = {
        user_id : $user.id
        action  : "get_auth_user"
        metadata: $safe_event_metadata
      }
    } as $event_log
  }

  response = {
    id           : $user.id
    created_at   : $user.created_at
    name         : $user.name
    email        : $user.email
    role         : $user.role
    account_type : $user.account_type
  }
  tags = ["xano:quick-start"]
  guid = "yzGqKb3r5Tr0lDkdR-lpZubmz_s"
}