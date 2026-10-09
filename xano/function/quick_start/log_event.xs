// Creates a record in the event log table.
// Metadata must be sanitized before calling this function so passwords, tokens,
// or other credential material are never written to event logs.
function "Quick Start/log_event" {
  input {
    // Unique identifier for the user who performed the action.
    int user_id
  
    // A description of the action performed by the user (e.g., 'login', 'created_invoice').
    text action
  
    // Additional metadata related to the event; do not include secrets, raw passwords,
    // or authentication tokens.
    json metadata?
  }

  stack {
    // Persist only explicitly approved metadata keys, even if a caller passes a full record.
    var $safe_metadata {
      value = ($input.metadata ?? {})|pick:["account_type"]
    }

    // Add a new user event log entry.
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