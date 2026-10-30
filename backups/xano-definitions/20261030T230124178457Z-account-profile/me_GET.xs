// Get the user record belonging to the authentication token
query "auth/me" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    // Get the user record based on the auth ID
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "created_at", "name", "email", "role", "account_type"]
    } as $user
  
    // Classify only from the authenticated record; preserve unclassified accounts.
    var $account_type {
      value = null
    }
  
    var $safe_event_metadata {
      value = {}
    }
  
    conditional {
      if ($user.account_type == "ADOTANTE") {
        var.update $account_type {
          value = "ADOTANTE"
        }
      
        var.update $safe_event_metadata {
          value = {account_type: "ADOTANTE"}
        }
      }
    
      elseif ($user.account_type == "ONG") {
        var.update $account_type {
          value = "ONG"
        }
      
        var.update $safe_event_metadata {
          value = {account_type: "ONG"}
        }
      }
    }
  
    // Create an event log for get user record
    function.run "Quick Start/log_event" {
      input = {
        user_id : $user.id
        action  : "get_auth_user"
        metadata: $safe_event_metadata
      }
    } as $event_log
  }

  response = {
    id          : $user.id
    created_at  : $user.created_at
    name        : $user.name
    email       : $user.email
    role        : $user.role
    account_type: $account_type
  }

  tags = ["xano:quick-start"]
}