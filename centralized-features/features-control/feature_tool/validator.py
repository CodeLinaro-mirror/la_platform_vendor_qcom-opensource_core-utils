# Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause-Clear

import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from common_utils import QtiFeatureUtils, QtiFeatureLogger, QtiFeatureConstants
from dataclasses import dataclass

class ValidationError(Exception):
    pass

class ValidationTypeMatchError(ValidationError):
    pass

class IOperator(ABC):
    """ Abstract operator interface"""

    @abstractmethod
    def symbol(self) -> str:
        """
        Get the operator symbol
        Returns:
            The operator symbol
        """

    @abstractmethod
    def arity(self) -> int:
        """
        Get the number of operands taken
        Returns:
            The number of operands taken
        """

    @abstractmethod
    def evaluate(self, *operands: Any) -> bool:
        """
        Evaluate the operator with the given operands
        Input:
            *operands: The operands to evaluate (1 for unary, 2 for binary)
        Returns:
            The result of the operation
        """

class EqualOperator(IOperator):
    """ Equal('==') operator"""
    def symbol(self) -> str:
        return "=="

    def arity(self) -> int:
        return 2

    def evaluate(self, *operands: Any) -> bool:
        if len(operands) != self.arity():
            raise ValidationError(f"Equal operator requires exactly {self.arity()} operands, but got {len(operands)}")

        return operands[0] == operands[1]

class NotEqualOperator(IOperator):
    """ Not('!=') operator"""
    def symbol(self) -> str:
        return "!="

    def arity(self) -> int:
        return 2

    def evaluate(self, *operands: Any) -> bool:
        if len(operands) != self.arity():
            raise ValidationError(f"Not equal requires exactly {self.arity()} operands, but got {len(operands)}")

        return operands[0] != operands[1]

class GreaterThanOrEqualOperator(IOperator):
    """ '>=' operator"""
    def symbol(self) -> str:
        return ">="

    def arity(self) -> int:
        return 2

    def evaluate(self, *operands: Any) -> bool:
        if len(operands) != self.arity():
            raise ValidationError(f"Greater than or equal operator requires exactly {self.arity()} operands, but got {len(operands)}")

        return operands[0] >= operands[1]

class LessThanOrEqualOperator(IOperator):
    """ '<=' operator"""
    def symbol(self) -> str:
        return "<="

    def arity(self) -> int:
        return 2

    def evaluate(self, *operands: Any) -> bool:
        if len(operands) != self.arity():
            raise ValidationError(f"Less than or equal operator requires exactly {self.arity()} operands, but got {len(operands)}")

        return operands[0] <= operands[1]

class GreaterThanOperator(IOperator):
    """ '>' operator"""
    def symbol(self) -> str:
        return ">"

    def arity(self) -> int:
        return 2

    def evaluate(self, *operands: Any) -> bool:
        if len(operands) != self.arity():
            raise ValidationError(f"Greater than operator requires exactly {self.arity()} operands, but got {len(operands)}")

        return operands[0] > operands[1]

class LessThanOperator(IOperator):
    """ '<' operator"""
    def symbol(self) -> str:
        return "<"

    def arity(self) -> int:
        return 2

    def evaluate(self, *operands: Any) -> bool:
        if len(operands) != self.arity():
            raise ValidationError(f"Less than operator requires exactly {self.arity()} operands, but got {len(operands)}")

        return operands[0] < operands[1]

class AndOperator(IOperator):
    """ And('&&') operator"""
    def symbol(self) -> str:
        return "&&"

    def arity(self) -> int:
        return 2

    def evaluate(self, *operands: Any) -> bool:
        if len(operands) != self.arity():
            raise ValidationError(f"And operator requires exactly {self.arity()} operands, but got {len(operands)}")

        return bool(operands[0]) and bool(operands[1])

class OrOperator(IOperator):
    """ Or('||') operator"""
    def symbol(self) -> str:
        return "||"

    def arity(self) -> int:
        return 2

    def evaluate(self, *operands: Any) -> bool:
        if len(operands) != self.arity():
            raise ValidationError(f"Or operator requires exactly {self.arity()} operands, but got {len(operands)}")

        return bool(operands[0]) or bool(operands[1])

class NotOperator(IOperator):
    """ Not('!') operator"""
    def symbol(self) -> str:
        return "!"

    def arity(self) -> int:
        return 1

    def evaluate(self, *operands: Any) -> bool:
        if len(operands) != self.arity():
            raise ValidationError(f"Not operator requires exactly {self.arity()} operands, but got {len(operands)}")

        return not bool(operands[0])

class Node(ABC):
    "Base Node for all AST nodes produced by parsing a depends_on expression"
    @abstractmethod
    def evaluate(self, cxt: Any) -> Any:
        pass

class LiteralNode(Node):
    """
    Literal operation node, represents a literal value (e.g., boolean, integer, or string).

    Fields:
        value: literal value
    """
    def __init__(self, value: Any):
        self.value = value

    def evaluate(self, cxt: Any) -> Any:
        """
        Directly return literal value
        """
        return self.value

class IdentifierNode(Node):
    """
    Identifier operation node

    Fields:
        name: feature name string
    """
    def __init__(self, name: str):
        self.name = name

    def evaluate(self, cxt: Any) -> Any:
        """
        Evaluates the value of the feature name defined in the cxt
        """
        if self.name not in cxt:
            raise ValidationError(f"unknown feature '{self.name}' referenced in depends_on expression.")
        else:
            return cxt[self.name][QtiFeatureConstants.FEATURE_VALUE_KEY]

class UnaryNode(Node):
    """
    Unary operation node: (<operator> <expr>)

    Fields:
        operator: The unary operator  (e.g., '!').
        expr: The sub-expression node.
    """
    def __init__(self, operator: IOperator, expr: Node):
        self.operator = operator
        self.expr_node = expr

    def evaluate(self, cxt: Any) -> Any:
        """
        Recursively evaluates sub-expressions and applies operator to the results.
        """
        result = self.expr_node.evaluate(cxt)
        if not isinstance(result, bool):
            raise ValidationTypeMatchError("type mismatch")
        return self.operator.evaluate(result)

class BinaryNode(Node):
    """
    Binary operation node: (<left_expr> <operator> <right_expr>)

    Fields:
        operator: The binary operator  (e.g., '&&', '||', '==', '!=', '>', '>=', '<=','<').
        left_expr: The left sub-expression node.
        right_expr: The right sub-expression node.
    """

    def __init__(self, left_expr: Node, operator: IOperator, right_expr: Node):
        self.left_expr_node = left_expr
        self.operator = operator
        self.right_expr_node = right_expr

    def evaluate(self, cxt: Any) -> Any:
        """
        Recursively evaluates the left and right sub-expressions
        and applies operator to the results.
        """
        left_result = self.left_expr_node.evaluate(cxt)
        right_result = self.right_expr_node.evaluate(cxt)

        if type(left_result) is not type(right_result):
            raise ValidationTypeMatchError("type mismatch")
        return self.operator.evaluate(left_result, right_result)

@dataclass(frozen=True)
class Token:
    type: str   # 'LPAREN', 'RPAREN', 'OPERATOR', 'IDENTIFIER', 'BOOL', 'NUMBER', 'STRING', 'EOF'
    value: str
    pos: int    # position in source string

class Parser:
    """
    Expression Parser
    The expression must be fully parenthesized, and every operation has the form:
      - unary expression: (<op> <expr>)
      - binary expression: (<expr> <op> <expr>)
    Parentheses must be balanced.
    """
    def __init__(self, tokens: List[Token], operators: Dict[str, IOperator], feature_dict: Dict, depend_on_expr: str):
        self.tokens = tokens
        self.operators = operators
        self.pos = 0
        self.feature_dict = feature_dict
        self.depend_feature_names:List[str] = []
        self.depend_on_expr = depend_on_expr

    def cur(self) -> Token:
        if self.pos >= len(self.tokens):
            return Token(type='EOF', value='', pos=-1)
        return self.tokens[self.pos]

    def consume(self, token_type: str, token_value: str = None) -> Token:
        cur_token = self.cur()
        if cur_token.type != token_type:
            raise ValidationError(f"depends_on invalid expression '{self.depend_on_expr}'")
        if token_value is not None and cur_token.value != token_value:
            raise ValidationError(f"depends_on invalid expression '{self.depend_on_expr}'")
        self.pos += 1
        return cur_token

    def parse(self) -> Node:
        """
        The expression is parsed recursively as follows:
        - Decompose the current expression into its left sub-expression, operator, and right sub-expression.
        - Apply the same parsing procedure recursively to the left and right sub-expressions until an operand is reached (e.g., a literal value or an identifier).
        """
        cur_token = self.cur()
        if cur_token.type == 'LPAREN':
            self.consume('LPAREN', "(")
            cur_token = self.cur()
            if cur_token.type == 'OPERATOR' and cur_token.value == '!':
                self.consume('OPERATOR', '!')
                # unary: ( <op> <expr> )
                not_operator = self.operators[cur_token.value]
                inner_expr = self.parse()  # expression of unary
                self.consume('RPAREN', ")")
                return UnaryNode(not_operator, inner_expr)
            else:
                # binary: ( <expr> <op> <expr> )
                left_expr = self.parse()    # left expression
                op_token = self.consume('OPERATOR') # second token should be an operator type
                if op_token.value not in self.operators or op_token.value == "!":
                    raise ValidationError(f"Unknown/invalid binary operator '{op_token.value}' at pos {op_token.pos} in depends_on expression {self.depend_on_expr}.")
                binary_operator = self.operators[op_token.value]
                right_expr = self.parse()  # right expression
                self.consume('RPAREN', ")")
                return BinaryNode(left_expr, binary_operator, right_expr)
        elif cur_token.type == 'IDENTIFIER':
            self.consume("IDENTIFIER")
            if cur_token.value not in self.feature_dict:
                raise ValidationError(f"unknown feature '{cur_token.value}' referenced in depends_on expression '{self.depend_on_expr}'.")
            if cur_token.value not in self.depend_feature_names:
                self.depend_feature_names.append(cur_token.value)
            return IdentifierNode(cur_token.value)
        elif cur_token.type == 'BOOL':
            self.consume("BOOL")
            return LiteralNode(cur_token.value.lower() == "true")
        elif cur_token.type == 'STRING':
            self.consume("STRING")
            raw = cur_token.value
            if len(raw) >= 2 and raw[0] in ('"', "'") and raw[-1] == raw[0]:
                raw = raw[1:-1]
            return LiteralNode(raw)
        elif cur_token.type == 'NUMBER':
            self.consume("NUMBER")
            return LiteralNode(float(cur_token.value) if "." in cur_token.value else int(cur_token.value))
        else:
            raise ValidationError(f"depends_on invalid expression '{self.depend_on_expr}'")

# ── Schema validation types and helpers ──────────────────────────────────────

@dataclass
class ValidationIssue:
    level:   str    # "ERROR" or "WARNING"
    path:    str    # dotted path, e.g. "features.fastmmi.feature_fastmmi.feature_value"
    message: str

    def __str__(self):
        return f"[{self.level}] {self.path}: {self.message}"


@dataclass
class DispatchContext:
    """Immutable context bundle passed to every rule handler.

    Centralises all per-dispatch state so handler signatures stay stable
    when new context fields are added in the future.

    feature_name — name of the enclosing feature (key in _context["all_features"]).
                   Handlers that need the full feature data look it up via
                   validator._context["all_features"][ctx.feature_name].
    """
    value:        Any
    path:         str
    level:        str           # uppercased severity from rule_def ("ERROR" / "WARNING")
    message:      Optional[str]    # custom message override from rule_def; None if absent
    feature_name: Optional[str] = None

class SchemaValidator:
    """
    Schema-driven validator.  All rules are read from a schema YAML file.

    Schema block keys:
      unknown_fields: allow | warning | error   (default: allow, absent = allow)
                      or object form: {policy: warning|error, message: "<custom text>"}
      fields:         fixed keys with required/type/rules
      dynamic_fields: list of {pattern, type?, schema?, rules?, min_count?, level?}
                      first-match-wins; enforces minimum match count when min_count is set
      rules:          object-level cross-field rules (e.g. at_least_one_of)

    Key resolution order:
      1. fields         — exact name match
      2. dynamic_fields — first fullmatch regex + optional min_count tracking
      3. unknown_fields policy — allow | warning | error
    """

    def __init__(self, schema: dict):
        self._schema: dict = schema
        self._issues: List[ValidationIssue] = []
        self._context: dict = {}

    def validate_central(self, central_feature_dict: dict) -> List[ValidationIssue]:
        self._issues = []
        feature_dict = QtiFeatureUtils.get_all_feature_nodes(central_feature_dict)
        self._context["all_features"] = feature_dict
        self._validate_object(central_feature_dict, schema_name="root", path="")
        return self._issues

    # ── object-level validation ───────────────────────────────────────────────
    def _validate_object(self, data: Any, schema_name: str, path: str,
                         feature_name: Optional[str] = None):
        block = self._schema.get(schema_name)
        if block is None:
            return   # no schema defined for this name — skip silently

        if not isinstance(data, dict):
            self._add("ERROR", path,
                      f"Expected a mapping, got {self._py_type_name(data)}")
            return

        fixed_fields     = block.get("fields", {})
        dynamic_fields   = block.get("dynamic_fields", [])
        object_rules     = block.get("rules", [])
        dyn_match_counts = [0] * len(dynamic_fields)

        # ── fixed field validation ────────────────────────────────────────────
        for field_name, field_spec in fixed_fields.items():
            fpath = f"{path}.{field_name}" if path else field_name
            if field_name not in data:
                if field_spec.get("required", False):
                    self._add("ERROR", fpath,
                              f"Required field '{field_name}' is missing")
                continue
            self._apply_spec(field_spec, data[field_name], fpath, data, feature_name)

        # ── dynamic key dispatch ──────────────────────────────────────────────
        all_features = self._context.get("all_features", {})
        for key in data:
            if key in fixed_fields:
                continue
            fpath, val = (f"{path}.{key}" if path else key), data[key]
            dyn_idx, dyn_entry = self._match_dynamic(key, dynamic_fields)
            if dyn_entry is not None:
                dyn_match_counts[dyn_idx] += 1
                # Promote feature_name only when not already inside a feature and
                # the key is a known feature name. Use a local variable so each
                # feature in the same group gets its own name without polluting
                # subsequent iterations.
                child_feature_name = key if (feature_name is None and isinstance(val, dict) and key in all_features) else feature_name
                self._apply_spec(dyn_entry, val, fpath, data, child_feature_name)
            elif "unknown_fields" in block:
                unknown_fields   = block.get("unknown_fields")
                self._check_unknown_field(key, fpath, unknown_fields)

        # ── min_count / max_count enforcement for dynamic_fields ─────────────
        for i, entry in enumerate(dynamic_fields):
            self._check_count_constraint(dyn_match_counts[i], entry, path)

        # ── object-level rules ────────────────────────────────────────────────
        for rule_def in object_rules:
            self._dispatch(rule_def, data, path,
                           feature_name=feature_name)

    def _check_count_constraint(self, count: int, entry: dict, path: str) -> None:
        """Check min_count / max_count constraints for a dynamic_fields entry.

        Emits an issue when *count* falls outside the declared [min_count, max_count]
        range.  Either bound is optional; omitting it means "no constraint".
        Both bounds use the entry's 'level' key for severity (default: error).

        Can be called from any context that tracks how many keys matched a pattern —
        currently used by dynamic_fields post-processing in _validate_object, but
        reusable wherever count-range enforcement is needed.
        """
        level   = entry.get("level", "error").upper()
        pattern = entry.get("pattern", "")

        min_count = entry.get("min_count")
        if min_count is not None and count < min_count:
            self._add(level, path,
                      f"Expected at least {min_count} field(s) matching "
                      f"pattern '{pattern}', found {count}")

        max_count = entry.get("max_count")
        if max_count is not None and count > max_count:
            self._add(level, path,
                      f"Expected at most {max_count} field(s) matching "
                      f"pattern '{pattern}', found {count}")

    def _check_type(self, value: Any, type_name: str, path: str) -> bool:
        """Type-check value against a YAML type name. Emits ERROR and returns False on mismatch.
        """
        if not isinstance(type_name, str):
            return True   # non-string type_name means feature_datatype itself is malformed;
                          # that error is already reported by the feature_datatype field check
        exp_py = self.YAML_TO_PY.get(type_name)
        if exp_py is None:
            return True   # unknown type name — skip check

        # Python's bool is a subclass of int, so isinstance(True, int) == True.
        # Without this guard, a YAML `true` would silently pass an `integer` type check.
        # Must come before the generic isinstance check below.
        if exp_py is int and isinstance(value, bool):
            self._add("ERROR", path, f"Expected {type_name}, got boolean")
            return False

        if not isinstance(value, exp_py):
            self._add("ERROR", path,
                      f"Expected {type_name}, got {self._py_type_name(value)}")
            return False
        return True

    def _apply_spec(self, spec: dict, val: Any, fpath: str, data: dict,
                    feature_name: Optional[str] = None):
        """Apply a field spec dict (type, schema, rules) to a value.

        Used for fixed_fields, pattern_fields entries, and additional_fields dict
        form — they all share the same structure.  If the type check fails,
        schema validation and rule dispatch are both skipped.

        spec keys (all optional):
          type:   YAML type name — checked first; on failure, rest is skipped
          schema: named schema block — validated via _validate_object
          rules:  list of rule defs — dispatched via _dispatch
        """
        exp_type = spec.get("type")
        if exp_type and not self._check_type(val, exp_type, fpath):
            return
        sub_schema = spec.get("schema")
        if sub_schema:
            self._validate_object(val, schema_name=sub_schema, path=fpath,
                                  feature_name=feature_name)
        for rule_def in spec.get("rules", []):
            self._dispatch(rule_def, val, fpath,
                           feature_name=feature_name)

    def _check_unknown_field(self, key: str, fpath: str, unknown_fields: Any):
        """Emit a diagnostic for a key that matched no fixed or dynamic field.

        unknown_fields is the raw value of the 'unknown_fields' key in the schema block.
        Supported forms:
          - string → "allow" | "warning" | "warn" | "error"
          - dict   → {policy: "warning"|"error", message: "<custom text>"}
        The default message is "Unknown field '<key>'" when no custom message is provided.
        """
        message = f"Unknown field '{key}'"
        if isinstance(unknown_fields, dict):
            policy  = unknown_fields.get("policy", "allow")
            message = unknown_fields.get("message") or message
        else:
            policy  = unknown_fields
        if policy == "allow":
            return
        level = "WARNING" if policy in ("warning", "warn") else "ERROR"
        self._add(level, fpath, message)

    def _match_dynamic(self, key: str, entries: list) -> Tuple[int, Optional[dict]]:
        """Return (index, entry) of the first pattern entry matching key, or (-1, None)."""
        for i, entry in enumerate(entries):
            try:
                if re.fullmatch(entry.get("pattern", ".*"), key):
                    return i, entry
            except re.error as exc:
                QtiFeatureLogger.warning(
                    f"Schema dynamic_fields: invalid regex pattern "
                    f"'{entry.get('pattern', '')}': {exc}"
                )
        return -1, None

    # ── rule dispatcher ───────────────────────────────────────────────────────

    def _dispatch(self, rule_def: dict, value: Any, path: str,
                  feature_name: Optional[str] = None):
        rule_type = rule_def.get("rule")
        handler   = self.RULE_HANDLERS.get(rule_type)
        if handler is None:
            self._add("WARNING", path,
                      f"Schema references unknown rule type '{rule_type}'")
            return
        ctx = DispatchContext(
            value        = value,
            path         = path,
            level        = rule_def.get("level", "error").upper(),
            message      = rule_def.get("message"),
            feature_name = feature_name,
        )
        handler(self, rule_def, ctx)

    def _add(self, level: str, path: str, message: str):
        self._issues.append(ValidationIssue(level.upper(), path, message))

    # ── rule handlers ─────────────────────────────────────────────────────────
    # Each handler signature:
    #   (self, rule_def, ctx: DispatchContext)

    def _h_non_empty(self, rule, ctx: DispatchContext):
        if isinstance(ctx.value, str) and not ctx.value.strip():
            self._add(ctx.level, ctx.path,
                      ctx.message or "Value must not be empty or whitespace-only")

    def _h_enum(self, rule, ctx: DispatchContext):
        allowed = rule.get("values", [])
        if ctx.value not in allowed:
            self._add(ctx.level, ctx.path,
                      ctx.message or f"'{ctx.value}' is not allowed. "
                                     f"Must be one of: {allowed}")

    def _h_list_items_enum(self, rule, ctx: DispatchContext):
        if not isinstance(ctx.value, list):
            return
        allowed = rule.get("values", [])
        for item in ctx.value:
            if item not in allowed:
                self._add(ctx.level, ctx.path,
                          ctx.message or f"Item '{item}' is not in the allowed list: "
                                         f"{allowed}")

    def _h_list_items_type(self, rule, ctx: DispatchContext):
        if not isinstance(ctx.value, list):
            return
        item_type_name = rule.get("item_type", "string")
        expected_py    = self.YAML_TO_PY.get(item_type_name)
        if expected_py is None:
            return
        for i, item in enumerate(ctx.value):
            if expected_py is int and isinstance(item, bool):
                self._add(ctx.level, f"{ctx.path}[{i}]",
                          ctx.message or f"Expected {item_type_name}, got boolean")
            elif not isinstance(item, expected_py):
                self._add(ctx.level, f"{ctx.path}[{i}]",
                          ctx.message or f"Expected {item_type_name}, "
                                         f"got {self._py_type_name(item)}")

    def _h_exclusive_item(self, rule, ctx: DispatchContext):
        if not isinstance(ctx.value, list):
            return
        sentinel = rule.get("item")
        if sentinel in ctx.value and len(ctx.value) > 1:
            self._add(ctx.level, ctx.path,
                      ctx.message or f"'{sentinel}' must be the only item when present, "
                                     f"but the list has {len(ctx.value)} items")

    def _h_type_matches_field(self, rule, ctx: DispatchContext):
        """Cross-field rule: validate that value's type matches the type named by another field.

        Looks up ref_field in the enclosing feature's data dict via
        _context["all_features"][ctx.feature_name].  Covers both same-level
        (feature_value ↔ feature_datatype) and nested
        (soc_override.value ↔ feature_datatype) cases uniformly.
        """
        ref_field = rule.get("field")
        if not ctx.feature_name:
            return
        feature_data = self._context["all_features"].get(ctx.feature_name)
        if feature_data and ref_field in feature_data:
            self._check_type(ctx.value, feature_data[ref_field], ctx.path)

    def _h_list_items_schema(self, rule, ctx: DispatchContext):
        """Validate each item in a list against a named sub-schema."""
        if not isinstance(ctx.value, list):
            return
        item_schema = rule.get("item_schema")
        for i, item in enumerate(ctx.value):
            self._validate_object(item, schema_name=item_schema,
                                  path=f"{ctx.path}[{i}]",
                                  feature_name=ctx.feature_name)

    def _h_apply_schema(self, rule, ctx: DispatchContext):
        """Validate a value against a named schema block."""
        schema_name = rule.get("schema")
        if schema_name:
            self._validate_object(ctx.value, schema_name=schema_name, path=ctx.path,
                                  feature_name=ctx.feature_name)

    def _h_at_least_one_of(self, rule, ctx: DispatchContext):
        """Object-level: at least one of the listed fields must be present."""
        fields  = rule.get("fields", [])
        present = [f for f in fields if f in ctx.value] if isinstance(ctx.value, dict) else []
        if not present:
            self._add(ctx.level, ctx.path,
                      ctx.message or f"At least one of {fields} must be present")

    def _h_min_items(self, rule, ctx: DispatchContext):
        """List rule: list must contain at least `count` items."""
        if not isinstance(ctx.value, list):
            return
        count = rule.get("count", 1)
        if len(ctx.value) < count:
            self._add(ctx.level, ctx.path,
                      ctx.message or f"List must have at least {count} item(s), got {len(ctx.value)}")

    # ── YAML type name ↔ Python type ─────────────────────────────────────────

    YAML_TO_PY = {
        "string":  str,
        "boolean": bool,
        "integer": int,
        "list":    list,
        "mapping": dict,
        "float":   float,
    }

    @staticmethod
    def _py_type_name(value: Any) -> str:
        """Return a human-readable YAML type name for a Python value."""
        if isinstance(value, bool):  return "boolean"   # must be before int
        if isinstance(value, float): return "float"
        if isinstance(value, str):   return "string"
        if isinstance(value, list):  return "list"
        if isinstance(value, int):   return "integer"
        if isinstance(value, dict):  return "mapping"
        return type(value).__name__

    # ── handler registry ──────────────────────────────────────────────────────
    # To add a new rule type: add a handler method above, then add it here.

    RULE_HANDLERS = {
        "non_empty":                   _h_non_empty,
        "enum":                        _h_enum,
        "list_items_enum":             _h_list_items_enum,
        "list_items_type":             _h_list_items_type,
        "exclusive_item":              _h_exclusive_item,
        "type_matches_field":          _h_type_matches_field,
        "list_items_schema":           _h_list_items_schema,
        "apply_schema":                _h_apply_schema,
        "at_least_one_of":             _h_at_least_one_of,
        "min_items":                   _h_min_items,
    }

class QtiFeatureValidator:

    _TOKEN_RE = re.compile(
        r"""
        \s*(?:
            (?P<LPAREN>\() |
            (?P<RPAREN>\)) |
            (?P<OPERATOR>[=!<>|&]+) |  # any operator
            (?P<BOOL>true|false) |
            (?P<NUMBER>-?\d+(?:\.\d+)?) |
            (?P<STRING>"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*') |
            (?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)
        )
        """,
        re.VERBOSE
    )

    def __init__(self):
        self.operators: Dict[str, IOperator] = self.default_operator_registry()

    def tokenize(self, depends_on_expr: str) -> List[Token]:
        """
        Tokenize expression using the TOKEN_RE regex.
        Input:
            depends_on_expr: depends_on expression of feature
        Return:
            List of token
        """
        if not (depends_on_expr.startswith('(') and depends_on_expr.endswith(')')):
            raise ValidationError(f"depends_on expression '{depends_on_expr}' must be enclosed in parentheses")
        tokens: List[Token] = []
        balance = 0  # for Parenthesis balance check
        last_end = 0
        for match in self._TOKEN_RE.finditer(depends_on_expr):
            # The regex pattern starts with \s*, so each match consumes its own
            # leading whitespace.  Any gap between last_end and match.start()
            # therefore contains at least one character the regex could not
            # consume — that character is invalid.
            if match.start() != last_end:
                gap = depends_on_expr[last_end:match.start()]
                invalid_pos = last_end + len(gap) - len(gap.lstrip())
                raise ValidationError(
                    f"invalid character at position {invalid_pos}: "
                    f"'{depends_on_expr[invalid_pos]}' in depends_on expression '{depends_on_expr}'"
                )
            last_end = match.end()
            token_type = match.lastgroup
            token_value = match.group(token_type)
            pos = match.start()

            # Parenthesis balance check
            if token_type == 'LPAREN':
                balance += 1
            elif token_type == 'RPAREN':
                balance -= 1
                if balance < 0:
                    raise ValidationError(f"unbalanced parentheses in depends_on expression '{depends_on_expr}'")

            if token_type:  # Skip whitespace
                tokens.append(Token(token_type, token_value, pos))

        # parentheses must be balanced(balance == 0)
        if balance != 0:
            raise ValidationError(f"unbalanced parentheses in depends_on expression '{depends_on_expr}'")
        return tokens

    def default_operator_registry(self) -> Dict[str, IOperator]:
        ops: List[IOperator] = [
                EqualOperator(),
                NotEqualOperator(),
                GreaterThanOrEqualOperator(),
                LessThanOrEqualOperator(),
                GreaterThanOperator(),
                LessThanOperator(),
                OrOperator(),
                NotOperator(),
                AndOperator()
            ]
        return {op.symbol(): op for op in ops}

    def format_feature_value(self, val: Any) -> str:
        """Format a feature value for display:
        - bool   -> lowercase true/false  (e.g. true)
        - str    -> double-quoted string  (e.g. "hello")
        - others -> plain str conversion  (e.g. 42)
        """
        if isinstance(val, bool):
            return str(val).lower()
        if isinstance(val, str):
            return f'"{val}"'
        return str(val)

    def evaluate_depends_on(self, depends_on_expr: str, feature_dict: Dict) -> Tuple[bool, str]:
        try:
            tokens = self.tokenize(depends_on_expr.strip())
            parser = Parser(tokens, self.operators, feature_dict, depends_on_expr)
            expr_node = parser.parse()
            if parser.cur().type != 'EOF':
                raise ValidationError(f"depends_on invalid expression '{depends_on_expr}'")
            result = expr_node.evaluate(feature_dict)
            error = ""
            if result is not True:
                actual_value = "{" + ", ".join(
                        f"{name} : {self.format_feature_value(feature_dict[name][QtiFeatureConstants.FEATURE_VALUE_KEY])}"
                        for name in parser.depend_feature_names
                    ) + "}"
                error = f"depends_on expression '{depends_on_expr}' evaluated to False, but expected True. Actual values: {actual_value}"
            return result, error
        except ValidationTypeMatchError as e:
            return False, (f"{e} in depends_on expression '{depends_on_expr}'")
        except ValidationError as e:
            return False, str(e)

    def validate_dependency(self, feature_dict: Dict) -> int:
        """
        Iterate over all features and validate each feature’s depends_on expression, 
        reporting all features that fail validation along with the corresponding reasons.
        """
        ret = 0
        for feature_name, feature in feature_dict.items():
            if 'depends_on' not in feature:
                continue
            depends_on = feature['depends_on']
            if not isinstance(depends_on, str):
                QtiFeatureLogger.error(f"[Validator] Feature '{feature_name}': depends_on expression '{depends_on}' must be a string")
                ret = -1
                continue
            depends_on = depends_on.strip()
            if len(depends_on) == 0:
                continue
            result, error = self.evaluate_depends_on(depends_on, feature_dict)
            if not result:
                ret = -1
                QtiFeatureLogger.error(f"[Validator] Feature '{feature_name}': {error}")
        return ret

    def validate_schema(self, central_feature_dict: Dict, schema_dict: Dict) -> int:
        if not schema_dict:
            return 0
        sv = SchemaValidator(schema_dict)
        issues = sv.validate_central(central_feature_dict)

        ret = 0
        for issue in issues:
            if issue.level == "ERROR":
                QtiFeatureLogger.error(f"[Validator] {issue}")
                ret = -1
            else:
                QtiFeatureLogger.warning(f"[Validator] {issue}")
        return ret

    def validate(self, central_feature_dict: Dict, schema_dict: Dict) -> int:
        """
        Input :
            central_feature_dict:  produced by the Stitch + Parser stage
            schema_dict: in-memory schema definition used by validation stage

        Return:
            0: validation completed successfully
            -1: validation failed
        """
        ret = self.validate_schema(central_feature_dict, schema_dict)
        if ret != 0:
            QtiFeatureLogger.error("[Validator] Schema validation: FAILED")
            return ret
        QtiFeatureLogger.info("[Validator] Schema validation: SUCCEEDED")
        feature_dict = QtiFeatureUtils.get_all_feature_nodes(central_feature_dict)
        ret = self.validate_dependency(feature_dict)
        if ret != 0:
            QtiFeatureLogger.error("[Validator] Dependency validation: FAILED")
            return ret
        else:
            QtiFeatureLogger.info("[Validator] Dependency validation: SUCCEEDED")
        return 0
