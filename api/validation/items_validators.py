from api.database.models import Product
from api.validation.base_rules import Rule, RequiredRule, RequiredIfRule, NullableRule, StringRule, IntegerRule, \
    ExistsInRule, GreaterThanRule
from api.validation.base_validators import Validator


class CreateItemValidator(Validator):
    def rules(self) -> dict[str, list[Rule]]:
        return {
            'product_id': [
                RequiredIfRule(self.schema.product_name is None),
                IntegerRule(),
                ExistsInRule(Product, 'id')
            ],
            'product_name': [
                RequiredIfRule(self.schema.product_id is None),
                StringRule(),
                ExistsInRule(Product, 'name')
            ],
            'quantity': [
                NullableRule(),
                IntegerRule(),
                GreaterThanRule(0)
            ],
        }


class UpdateItemValidator(Validator):
    def rules(self) -> dict[str, list[Rule]]:
        return {
            'quantity': [
                RequiredRule(),
                GreaterThanRule(0)
            ]
        }
