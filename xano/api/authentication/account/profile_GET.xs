// LOCAL ONLY: not published. No audit, mutations, HTTP calls or helper functions.
query "account/profile" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    util.set_header {
      value = "Cache-Control: private, no-store"
      duplicates = "replace"
    }
    util.set_header {
      value = "Vary: Authorization"
      duplicates = "add"
    }

    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "name", "email", "account_type", "phone", "address", "city", "uf", "adopter_profile", "ngo_profile"]
    } as $user

    precondition ($user != null) {
      error_type = "notfound"
      error = "Perfil indisponivel."
    }
    precondition ($user.account_type === "ADOTANTE" || $user.account_type === "ONG") {
      error_type = "accessdenied"
      error = "Perfil indisponivel."
    }

    // Treat malformed JSON as absent in memory only. Never decode legacy strings.
    var $profile { value = {} }
    conditional {
      if ($user.account_type === "ADOTANTE") {
        conditional {
          if (($user.adopter_profile|is_object) && !($user.adopter_profile|is_array)) {
            var.update $profile { value = $user.adopter_profile }
          }
        }
      }
      else {
        conditional {
          if (($user.ngo_profile|is_object) && !($user.ngo_profile|is_array)) {
            var.update $profile { value = $user.ngo_profile }
          }
        }
      }
    }

    var $document { value = null }
    var $document_format_valid { value = false }
    var $document_masked { value = null }
    conditional {
      if ($user.account_type === "ADOTANTE") {
        var.update $document { value = $profile|get:"cpf":null }
      }
      else {
        var.update $document { value = $profile|get:"cnpj":null }
      }
    }
    conditional {
      if ($document|is_text) {
        var.update $document { value = $document|trim }
        conditional {
          if ($user.account_type === "ADOTANTE") {
            var.update $document_format_valid {
              value = "/^([0-9]{11}|[0-9]{3}\\.[0-9]{3}\\.[0-9]{3}-[0-9]{2})$/"|regex_matches:$document
            }
          }
          else {
            var.update $document_format_valid {
              value = "/^([0-9]{14}|[0-9]{2}\\.[0-9]{3}\\.[0-9]{3}\\/[0-9]{4}-[0-9]{2})$/"|regex_matches:$document
            }
          }
        }
      }
    }

    conditional {
      if ($document_format_valid) {
        var $document_digits { value = "/[^0-9]/"|regex_replace:"":$document }
        var $digits { value = $document_digits|split:"" }
        conditional {
          if (($digits|unique|count) > 1) {
            conditional {
              if ($user.account_type === "ADOTANTE") {
                var $cpf_sum1 { value = ((($digits|get:0)|to_int) * 10) + ((($digits|get:1)|to_int) * 9) + ((($digits|get:2)|to_int) * 8) + ((($digits|get:3)|to_int) * 7) + ((($digits|get:4)|to_int) * 6) + ((($digits|get:5)|to_int) * 5) + ((($digits|get:6)|to_int) * 4) + ((($digits|get:7)|to_int) * 3) + ((($digits|get:8)|to_int) * 2) }
                var $cpf_sum2 { value = ((($digits|get:0)|to_int) * 11) + ((($digits|get:1)|to_int) * 10) + ((($digits|get:2)|to_int) * 9) + ((($digits|get:3)|to_int) * 8) + ((($digits|get:4)|to_int) * 7) + ((($digits|get:5)|to_int) * 6) + ((($digits|get:6)|to_int) * 5) + ((($digits|get:7)|to_int) * 4) + ((($digits|get:8)|to_int) * 3) + ((($digits|get:9)|to_int) * 2) }
                var $cpf_check1 { value = (($cpf_sum1 * 10) % 11) % 10 }
                var $cpf_check2 { value = (($cpf_sum2 * 10) % 11) % 10 }
                conditional {
                  if ((($digits|get:9)|to_int) == $cpf_check1 && (($digits|get:10)|to_int) == $cpf_check2) {
                    var.update $document_masked { value = "***.***.***-" ~ ($document_digits|substr:-2:2) }
                  }
                }
              }
              else {
                var $cnpj_sum1 { value = ((($digits|get:0)|to_int) * 5) + ((($digits|get:1)|to_int) * 4) + ((($digits|get:2)|to_int) * 3) + ((($digits|get:3)|to_int) * 2) + ((($digits|get:4)|to_int) * 9) + ((($digits|get:5)|to_int) * 8) + ((($digits|get:6)|to_int) * 7) + ((($digits|get:7)|to_int) * 6) + ((($digits|get:8)|to_int) * 5) + ((($digits|get:9)|to_int) * 4) + ((($digits|get:10)|to_int) * 3) + ((($digits|get:11)|to_int) * 2) }
                var $cnpj_sum2 { value = ((($digits|get:0)|to_int) * 6) + ((($digits|get:1)|to_int) * 5) + ((($digits|get:2)|to_int) * 4) + ((($digits|get:3)|to_int) * 3) + ((($digits|get:4)|to_int) * 2) + ((($digits|get:5)|to_int) * 9) + ((($digits|get:6)|to_int) * 8) + ((($digits|get:7)|to_int) * 7) + ((($digits|get:8)|to_int) * 6) + ((($digits|get:9)|to_int) * 5) + ((($digits|get:10)|to_int) * 4) + ((($digits|get:11)|to_int) * 3) + ((($digits|get:12)|to_int) * 2) }
                var $cnpj_rem1 { value = $cnpj_sum1 % 11 }
                var $cnpj_rem2 { value = $cnpj_sum2 % 11 }
                var $cnpj_check1 { value = 0 }
                var $cnpj_check2 { value = 0 }
                conditional {
                  if ($cnpj_rem1 >= 2) {
                    var.update $cnpj_check1 { value = 11 - $cnpj_rem1 }
                  }
                }
                conditional {
                  if ($cnpj_rem2 >= 2) {
                    var.update $cnpj_check2 { value = 11 - $cnpj_rem2 }
                  }
                }
                conditional {
                  if ((($digits|get:12)|to_int) == $cnpj_check1 && (($digits|get:13)|to_int) == $cnpj_check2) {
                    var.update $document_masked { value = "**.***.***/****-" ~ ($document_digits|substr:-2:2) }
                  }
                }
              }
            }
          }
        }
      }
    }

    // Reconstruct each JSON level; never return a stored object directly.
    var $adopter_profile { value = null }
    var $ngo_profile { value = null }
    conditional {
      if ($user.account_type === "ADOTANTE") {
        var $about_me { value = "" }
        var $about_candidate { value = $profile|get:"about_me":null }
        conditional {
          if ($about_candidate|is_text) {
            var.update $about_me { value = $about_candidate|trim|substr:0:1000 }
          }
        }
        var $preferences { value = {} }
        var $preferences_candidate { value = $profile|get:"adoption_preferences":null }
        conditional {
          if (($preferences_candidate|is_object) && !($preferences_candidate|is_array)) {
            var.update $preferences { value = $preferences_candidate }
          }
        }
        var $safe_preferences {
          value = {
            species: []
            sizes: []
            age_ranges: []
            preferred_sex: null
            preferred_city: ""
            preferred_uf: ""
            description: ""
          }
        }
        var $species_candidate { value = $preferences|get:"species":null }
        conditional {
          if ($species_candidate|is_array) {
            var.update $safe_preferences.species {
              value = $species_candidate|filter:($$|is_text)|map:($$|trim)|filter:(($$|strlen) > 0 && ($$|strlen) <= 50)|unique|slice:0:20
            }
          }
        }
        var $sizes_candidate { value = $preferences|get:"sizes":null }
        conditional {
          if ($sizes_candidate|is_array) {
            var.update $safe_preferences.sizes {
              value = $sizes_candidate|filter:($$|is_text)|map:($$|trim)|filter:(($$|strlen) > 0 && ($$|strlen) <= 50)|unique|slice:0:20
            }
          }
        }
        var $age_ranges_candidate { value = $preferences|get:"age_ranges":null }
        conditional {
          if ($age_ranges_candidate|is_array) {
            var.update $safe_preferences.age_ranges {
              value = $age_ranges_candidate|filter:($$|is_text)|map:($$|trim)|filter:(($$|strlen) > 0 && ($$|strlen) <= 50)|unique|slice:0:20
            }
          }
        }
        var $preferred_sex_candidate { value = $preferences|get:"preferred_sex":null }
        conditional {
          if ($preferred_sex_candidate|is_text) {
            var.update $safe_preferences.preferred_sex { value = $preferred_sex_candidate|trim|substr:0:50 }
          }
        }
        var $preferred_city_candidate { value = $preferences|get:"preferred_city":null }
        conditional {
          if ($preferred_city_candidate|is_text) {
            var.update $safe_preferences.preferred_city { value = $preferred_city_candidate|trim|substr:0:120 }
          }
        }
        var $description_candidate { value = $preferences|get:"description":null }
        conditional {
          if ($description_candidate|is_text) {
            var.update $safe_preferences.description { value = $description_candidate|trim|substr:0:1000 }
          }
        }
        var $uf_candidate { value = $preferences|get:"preferred_uf":null }
        var $valid_ufs { value = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"] }
        conditional {
          if ($uf_candidate|is_text) {
            var $normalized_uf { value = $uf_candidate|trim|to_upper }
            conditional {
              if ($valid_ufs|some:$$ === $normalized_uf) {
                var.update $safe_preferences.preferred_uf { value = $normalized_uf }
              }
            }
          }
        }
        var $consents { value = {} }
        var $consents_candidate { value = $profile|get:"consents":null }
        conditional {
          if (($consents_candidate|is_object) && !($consents_candidate|is_array)) {
            var.update $consents { value = $consents_candidate }
          }
        }
        var $discoverable_candidate { value = $consents|get:"discoverable_by_ngos":null }
        var $contact_candidate { value = $consents|get:"allow_ngo_contact":null }
        var.update $adopter_profile {
          value = {
            cpf_masked: $document_masked
            about_me: $about_me
            adoption_preferences: $safe_preferences
            consents: {
              discoverable_by_ngos: ($discoverable_candidate === true)
              allow_ngo_contact: ($contact_candidate === true)
            }
          }
        }
      }
      else {
        var $description { value = "" }
        var $ngo_description_candidate { value = $profile|get:"description":null }
        conditional {
          if ($ngo_description_candidate|is_text) {
            var.update $description { value = $ngo_description_candidate|trim|substr:0:2000 }
          }
        }
        var.update $ngo_profile {
          value = {cnpj_masked: $document_masked, description: $description}
        }
      }
    }
  }

  response = {
    data: {
      id: $user.id
      name: $user.name
      email: $user.email
      account_type: $user.account_type
      phone: ($user.phone|first_notnull:"")
      address: ($user.address|first_notnull:"")
      city: ($user.city|first_notnull:"")
      uf: ($user.uf|first_notnull:"")
      adopter_profile: $adopter_profile
      ngo_profile: $ngo_profile
    }
  }
}
