"""Static XanoScript contracts and offline checks, not a Xano runtime emulator."""

import ast
import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = ROOT / "xano/api/authentication/account/profile_GET.xs"


def block(source, marker):
    """Extract a balanced XS block, ignoring braces inside quoted strings."""
    start = source.index("{", source.index(marker))
    depth = 0
    quote = None
    escaped = False
    for index in range(start, len(source)):
        char = source[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        elif char in ('"', "'"):
            quote = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return source[start + 1:index]
    raise AssertionError("Unclosed block")


def arithmetic(expression, digits=(), variables=None):
    """Check the arithmetic actually declared in XS using synthetic digits."""
    expression = re.sub(
        r"\(\(\$digits\|get:(\d+)\)\|to_int\)",
        lambda match: str(int(digits[int(match[1])])), expression,
    )
    for name, value in (variables or {}).items():
        expression = expression.replace("$" + name, str(value))
    tree = ast.parse(expression, mode="eval")
    allowed = (ast.Expression, ast.BinOp, ast.Constant, ast.Add, ast.Sub, ast.Mult, ast.Mod)
    if any(not isinstance(node, allowed) for node in ast.walk(tree)):
        raise AssertionError("Unexpected arithmetic expression")
    return eval(compile(tree, "<XS arithmetic only>", "eval"), {"__builtins__": {}}, {})


class AccountProfileContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = ENDPOINT.read_text(encoding="utf-8")
        cls.code = re.sub(r"(?m)^\s*//[^\n]*", "", cls.source)

    def test_authentication_ownership_and_no_client_identity(self):
        self.assertIn('query "account/profile" verb=GET', self.code)
        self.assertIn('api_group = "Authentication"', self.code)
        self.assertIn('auth = "user"', self.code)
        self.assertFalse(block(self.code, "input").strip())
        query = block(self.code, "db.get user")
        self.assertIn('field_name = "id"', query)
        self.assertIn("field_value = $auth.id", query)
        self.assertNotIn("$input", self.code)
        self.assertEqual(self.code.count("db.get user"), 1)

    def test_missing_user_and_unknown_type_fail_before_profile_access(self):
        missing = self.code.index("precondition ($user != null)")
        classified = self.code.index('precondition ($user.account_type === "ADOTANTE" || $user.account_type === "ONG")')
        self.assertLess(missing, classified)
        self.assertLess(classified, self.code.index("var $profile"))
        self.assertIn('error_type = "notfound"', self.code)
        self.assertIn('error_type = "accessdenied"', self.code)
        errors = re.findall(r'error = "([^"]*)"', self.code)
        self.assertEqual(errors, ["Perfil indisponivel.", "Perfil indisponivel."])

    def test_common_response_and_db_allowlists_exclude_credentials(self):
        response = block(self.code, "response =")
        fields = set(re.findall(r"(?m)^\s+(\w+):", response))
        expected = {"data", "id", "name", "email", "account_type", "phone", "address", "city", "uf", "adopter_profile", "ngo_profile"}
        self.assertEqual(fields, expected)
        output = json.loads(re.search(r"output = (\[[^\n]+\])", self.code)[1])
        self.assertEqual(set(output), expected - {"data"})
        self.assertNotRegex(self.code, r"\b(password|password_reset|authToken|role|birth_date)\b")
        self.assertNotRegex(response, r"\$user\.(adopter_profile|ngo_profile)")

    def test_mutually_exclusive_filtered_profiles(self):
        self.assertIn("var $adopter_profile { value = null }", self.code)
        self.assertIn("var $ngo_profile { value = null }", self.code)
        adopter = block(self.code, "var.update $adopter_profile")
        self.assertEqual(set(re.findall(r"(?m)^\s+(\w+):", adopter)), {
            "cpf_masked", "about_me", "adoption_preferences", "consents", "discoverable_by_ngos", "allow_ngo_contact",
        })
        self.assertIn("value = {cnpj_masked: $document_masked, description: $description}", block(self.code, "var.update $ngo_profile"))
        self.assertNotIn("$profile", adopter)
        self.assertNotIn("$profile", block(self.code, "var.update $ngo_profile"))

    def test_absent_and_legacy_json_are_type_guarded_without_decoding(self):
        for value in ("$user.adopter_profile", "$user.ngo_profile", "$preferences_candidate", "$consents_candidate"):
            self.assertIn(f"({value}|is_object) && !({value}|is_array)", self.code)
        for name in ("profile", "preferences", "consents"):
            self.assertIn(f"var ${name} {{ value = {{}} }}", self.code)
        self.assertNotIn("json_decode", self.code)
        self.assertIn('var $about_me { value = "" }', self.code)
        self.assertIn('var $description { value = "" }', self.code)
        for field in ("phone", "address", "city", "uf"):
            self.assertIn(f'($user.{field}|first_notnull:"")', self.code)

    def test_future_fields_are_reconstructed_and_consent_is_strict(self):
        defaults = block(self.code, "var $safe_preferences")
        for field in ("species", "sizes", "age_ranges"):
            self.assertIn(f"{field}: []", defaults)
            self.assertIn(f"if (${field}_candidate|is_array)", self.code)
            self.assertIn(f"var.update $safe_preferences.{field}", self.code)
        self.assertEqual(self.code.count('|filter:($$|is_text)|map:($$|trim)'), 3)
        self.assertEqual(self.code.count("|unique|slice:0:20"), 3)
        for field in ("preferred_city", "preferred_uf", "description"):
            self.assertIn(f'{field}: ""', defaults)
        self.assertIn("preferred_sex: null", defaults)
        self.assertIn("($discoverable_candidate === true)", self.code)
        self.assertIn("($contact_candidate === true)", self.code)
        self.assertNotIn("to_bool", self.code)
        for size in (1000, 2000):
            self.assertIn(f"|substr:0:{size}", self.code)

    def test_invalid_document_types_format_and_repetition_remain_null(self):
        self.assertIn("var $document_masked { value = null }", self.code)
        type_guard = block(self.code, "if ($document|is_text)")
        self.assertIn("regex_matches:$document", type_guard)
        valid_format = block(self.code, "if ($document_format_valid)")
        self.assertIn('"/[^0-9]/"|regex_replace:"":$document', valid_format)
        self.assertIn("if (($digits|unique|count) > 1)", valid_format)
        self.assertIn("[0-9]{11}", type_guard)
        self.assertIn("[0-9]{14}", type_guard)
        self.assertEqual(self.code.count("var.update $document_masked"), 2)
        for name in ("cpf", "cnpj"):
            self.assertIn(f"== ${name}_check1", valid_format)
            self.assertIn(f"== ${name}_check2", valid_format)

    def test_mask_literals_and_substrings_expose_only_two_digits(self):
        values = re.findall(r"var.update \$document_masked \{ value = (.*?) \}", self.code)
        self.assertEqual(len(values), 2)
        for expression in values:
            self.assertIn('($document_digits|substr:-2:2)', expression)
            literal = re.match(r'"([^"]+)" ~ ', expression)[1]
            self.assertFalse(any(char.isdigit() for char in literal))
            self.assertIn("*", literal)
            for ending in ("00", "09", "81", "99"):
                self.assertEqual(sum(char.isdigit() for char in literal + ending), 2)

    def test_document_checksum_expressions_with_synthetic_bases(self):
        def value(name):
            return re.search(r"value = (.*?)\s*$", block(self.code, "var $" + name).strip())[1]

        # Generated arithmetic fixtures only; no production documents or records.
        for prefix in ("123456789", "987654321", "112223330001", "543210980001"):
            cpf = len(prefix) == 9
            kind = "cpf" if cpf else "cnpj"
            digits = prefix + "00"
            weights1 = list(range(10, 1, -1)) if cpf else [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            weights2 = list(range(11, 1, -1)) if cpf else [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            sum1 = arithmetic(value(kind + "_sum1"), digits)
            self.assertEqual(sum1, sum(int(digits[i]) * w for i, w in enumerate(weights1)))
            check1 = ((sum1 * 10) % 11) % 10 if cpf else (0 if sum1 % 11 < 2 else 11 - sum1 % 11)
            digits = prefix + str(check1) + "0"
            sum2 = arithmetic(value(kind + "_sum2"), digits)
            self.assertEqual(sum2, sum(int(digits[i]) * w for i, w in enumerate(weights2)))
            if cpf:
                self.assertEqual(arithmetic(value("cpf_check1"), variables={"cpf_sum1": sum1}), check1)
                self.assertEqual(arithmetic(value("cpf_check2"), variables={"cpf_sum2": sum2}), ((sum2 * 10) % 11) % 10)
            else:
                for index in (1, 2):
                    self.assertIn(f"if ($cnpj_rem{index} >= 2)", self.code)
                    self.assertIn(f"value = 11 - $cnpj_rem{index}", self.code)

    def test_no_effectful_operation_or_shared_cache(self):
        operations = re.findall(r"(?m)^\s*([a-z]+\.[a-z_]+)\s+", self.code)
        self.assertEqual(set(operations), {"util.set_header", "db.get", "var.update"})
        self.assertNotRegex(self.code, r"\b(function\.run|api\.|debug\.|storage\.|security\.)")
        self.assertIn('value = "Cache-Control: private, no-store"', self.code)
        self.assertIn('value = "Vary: Authorization"', self.code)
        self.assertNotIn("$env", self.code)

    def test_separate_snapshot_hashes_and_no_records(self):
        snapshots = list((ROOT / "backups/xano-definitions").glob("*-account-profile/manifest.json"))
        self.assertTrue(snapshots)
        manifest_path = max(snapshots)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertFalse(manifest["records_included"])
        self.assertFalse(manifest["credentials_included"])
        self.assertFalse(manifest["account_profile_published"])
        self.assertEqual(manifest["workspace_id"], 151970)
        self.assertEqual(manifest["branch"], "v1")
        for resource in manifest["resources"]:
            data = (manifest_path.parent / resource["filename"]).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), resource["sha256"])
            if "local_file" in resource:
                original = (ROOT / resource["local_file"]).read_bytes()
                self.assertEqual(hashlib.sha256(original).hexdigest(), resource["local_sha256"])


if __name__ == "__main__":
    unittest.main()
