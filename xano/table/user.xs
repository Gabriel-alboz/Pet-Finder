// Stores the shared identity for Pet Finder customers and their profile details.
table user {
  auth = true

  schema {
    int id
    timestamp created_at?=now

    text name filters=trim
    email? email filters=trim|lower
    password? password filters=min:8|minAlpha:1|minDigit:1

    // Shared identity classification for the two supported customer account types.
    text account_type? filters=trim

    // Authorization role remains distinct from account_type.
    enum role? {
      values = ["admin", "member"]
    }

    text phone? filters=trim
    text address? filters=trim
    text city? filters=trim
    text uf? filters=trim

    object adopter_profile? {
      schema {
        text cpf? filters=trim
        date birth_date?
      }
    }

    object ngo_profile? {
      schema {
        text cnpj? filters=trim
        text description? filters=trim
      }
    }

    object password_reset? {
      schema {
        password token?
        timestamp? expiration?
        bool used?
      }
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree|unique", field: [{name: "email", op: "asc"}]}
    {type: "btree|unique", field: [{name: "adopter_profile.cpf", op: "asc"}]}
    {type: "btree|unique", field: [{name: "ngo_profile.cnpj", op: "asc"}]}
  ]

  tags = ["xano:quick-start"]
  guid = "kfaBfLnht5KCTWwVApdoUAqaoJE"
}