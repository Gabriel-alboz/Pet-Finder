// Pull all event logs for the authenticated user
query "logs/user/my_events" verb=GET {
  api_group = "Event Logs"
  auth = "user"

  input {
  }

  stack {
    // Retrieve event logs for the authenticated user
    db.query event_log {
      where = $db.event_log.user_id == $auth.id
      return = {type: "list"}
    } as $user_events
  }

  response = $user_events|map:{
    id: $$.id,
    created_at: $$.created_at,
    user_id: $$.user_id,
    action: $$.action,
    metadata: {},
  }
  tags = ["xano:quick-start"]
  guid = "cIkiQvBrdxT2rujpoNt-xWZMzAA"
}