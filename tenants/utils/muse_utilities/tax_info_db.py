from tenants.utils.constants import (DB_TAX_INFO, TAX_INFO_SECTIONS,
                                     TAX_INFO_SECTIONS_22)
from users.models.user import User
from users.models.user_tax_info import UserTaxInfo

from .strategy_utils import count_dependents, get_section, get_user_object


def user_exists(name):
    return User.objects.filter(name=name).exists()


def user_tax_info_exists(name, tax_year):
    return UserTaxInfo.objects.filter(user=get_user_object(name), tax_year=tax_year).exists()


def get_section_value(json_data, doc_type, section_name):
    section = get_section(json_data, doc_type, section_name)
    if section is not None:
        if section.get('value') is not None:
            return section.get('value')
    return 0


def save_tax_data_in_db(json_data, tax_year, name):
    User.objects.get_or_create(name=name)

    sections = TAX_INFO_SECTIONS_22 if tax_year == '2022' else TAX_INFO_SECTIONS[2:]
    for section in sections:
        doc_type, section_name = section
        DB_TAX_INFO[doc_type][section_name] = get_section_value(json_data, doc_type, section_name)

    virtual_currency_section = 'digitalAssetsYes' if tax_year == '2022' else 'virtualCurrencyYes'
    virtual_currency = get_section(json_data, '1040', virtual_currency_section)
    if virtual_currency is not None:
        virtual_currency = virtual_currency.get('value') == 'true'
    no_of_dependents = count_dependents(get_section(json_data, *TAX_INFO_SECTIONS[1])['rows'])
    DB_TAX_INFO['1040']['virtual_currency'] = virtual_currency
    DB_TAX_INFO['1040']['dependents'] = no_of_dependents
    UserTaxInfo.objects.create(tax_year=tax_year, tax_info=DB_TAX_INFO, user=get_user_object(name))
