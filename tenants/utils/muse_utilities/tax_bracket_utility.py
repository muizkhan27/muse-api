import json

from tenants.utils.constants import FILING_STATUSES, FILING_STATUSES_22

from .strategy_utils import get_section, get_tax_year, get_taxable_income


def get_tax_bracket(json_data, tax_year):
    taxable_income = int(get_taxable_income(json_data))
    year = get_tax_year(json_data)
    filing_status = get_filing_status(json_data, tax_year)
    with open('tenants/resources/tax_brackets.json') as file:
        data = json.load(file)
        brackets = data[year][filing_status]
        for bracket in brackets:
            try:
                range1 = taxable_income in range(bracket['income_range']['start'], bracket['income_range']['end'])
            except Exception:
                range1 = taxable_income > bracket['income_range']['start'] and bracket['income_range']['end'] == 'inf'
            if range1:
                return bracket['bracket']


def get_filing_status(json_data, tax_year):
    filing_statuses = FILING_STATUSES_22 if tax_year == '2022' else FILING_STATUSES
    for key, value in filing_statuses.items():
        if get_section(json_data, '1040', key).get('value') == 'true':
            return value
