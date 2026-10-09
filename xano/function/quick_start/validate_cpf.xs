function "Quick Start/validate_cpf" {
  input {
    text cpf
  }

  stack {
    precondition ("/^([0-9]{11}|[0-9]{3}\\.[0-9]{3}\\.[0-9]{3}-[0-9]{2})$/"|regex_matches:$input.cpf) {
      error_type = "inputerror"
      error = "Invalid registration data."
    }

    var $digits {
      value = "/[^0-9]/"|regex_replace:"":$input.cpf
    }

    precondition (!(("/^(00000000000|11111111111|22222222222|33333333333|44444444444|55555555555|66666666666|77777777777|88888888888|99999999999)$/"|regex_matches:$digits))) {
      error_type = "inputerror"
      error = "Invalid registration data."
    }

    var $first_sum {
      value = (($digits[0]|to_int) * 10) + (($digits[1]|to_int) * 9) + (($digits[2]|to_int) * 8) + (($digits[3]|to_int) * 7) + (($digits[4]|to_int) * 6) + (($digits[5]|to_int) * 5) + (($digits[6]|to_int) * 4) + (($digits[7]|to_int) * 3) + (($digits[8]|to_int) * 2)
    }

    var $first_check {
      value = (($first_sum * 10)|modulus:11)|modulus:10
    }

    precondition (($digits[9]|to_int) == $first_check) {
      error_type = "inputerror"
      error = "Invalid registration data."
    }

    var $second_sum {
      value = (($digits[0]|to_int) * 11) + (($digits[1]|to_int) * 10) + (($digits[2]|to_int) * 9) + (($digits[3]|to_int) * 8) + (($digits[4]|to_int) * 7) + (($digits[5]|to_int) * 6) + (($digits[6]|to_int) * 5) + (($digits[7]|to_int) * 4) + (($digits[8]|to_int) * 3) + (($digits[9]|to_int) * 2)
    }

    var $second_check {
      value = (($second_sum * 10)|modulus:11)|modulus:10
    }

    precondition (($digits[10]|to_int) == $second_check) {
      error_type = "inputerror"
      error = "Invalid registration data."
    }
  }

  response = $digits
}