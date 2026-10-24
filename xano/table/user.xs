// Stores user information and allows the user to authenticate  against
table user {
  auth = true

  schema {
    int id
    timestamp created_at?=now
    text name filters=trim
    email? email filters=trim|lower
    password? password filters=min:8|minAlpha:1|minDigit:1
  
    // The role of the user within their company (e.g., 'admin', 'member').
    enum role? {
      values = ["admin", "member"]
    }
  
    object password_reset? {
      schema {
        password token?
        timestamp? expiration?
        bool used?
      }
    }
  
    // Tipo de conta do usuário (ADOTANTE ou ONG).
    text account_type? filters=trim
  
    // Número de telefone do usuário.
    text phone? filters=trim
  
    // Endereço completo do usuário.
    text address? filters=trim
  
    // Cidade do endereço do usuário.
    text city? filters=trim
  
    // Sigla do estado brasileiro (UF).
    text uf? filters=trim
  
    // Objeto para armazenar detalhes de perfil específicos para contas de adotantes.
    json adopter_profile?
  
    // Objeto para armazenar detalhes de perfil específicos para contas de ONGs.
    json ngo_profile?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree|unique", field: [{name: "email", op: "asc"}]}
  ]

  tags = ["xano:quick-start"]
  guid = "kfaBfLnht5KCTWwVApdoUAqaoJE"
}