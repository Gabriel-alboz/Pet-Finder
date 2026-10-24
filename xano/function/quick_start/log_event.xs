// Creates a record in the event log table
function "Quick Start/log_event" {
  input {
    // Unique identifier for the user who performed the action.
    int user_id
  
    // A description of the action performed by the user (e.g., 'login', 'created_invoice').
    text action
  
    // Only the literal ADOTANTE or ONG account_type may be persisted; other keys are discarded.
    json metadata?
  }

  stack {
    // Rebuild metadata from approved literal values; never persist arbitrary values.
    var $safe_metadata {
      value = {}
    }

    var $candidate_account_type {
      value = $input.metadata|get:"account_type":null
    }

    conditional {
      if ($candidate_account_type == "ADOTANTE") {
        var.update $safe_metadata {
          value = {account_type: "ADOTANTE"}
        }
      }
      elseif ($candidate_account_type == "ONG") {
        var.update $safe_metadata {
          value = {account_type: "ONG"}
        }
      }
    }

    // Add a new user event log entry
    db.add event_log {
      data = {
        created_at: "now"
        user_id   : $input.user_id
        action    : $input.action
        metadata  : $safe_metadata
      }
    } as $new_log_entry
  }

  response = null
  tags = ["xano:quick-start"]
  guid = "LVIY5LiWKI4w840LNyx0-HHORDk"
}
