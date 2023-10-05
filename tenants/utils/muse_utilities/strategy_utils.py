import math

from users.models.user import User
from tenants.utils.constants import TAX_INFO_SECTIONS


def get_user_object(name):
    return User.objects.get(name=name)


def get_tax_year(json_data):
    return get_section(json_data, *TAX_INFO_SECTIONS[0]).get('value')


def get_name(json_data):
    return get_section(json_data, '1040', 'firstName').get('value')


def get_taxable_income(json_data):
    return get_section(json_data, '1040', 'section15').get('value')


def find_key(json_obj, search_key):
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if key == search_key:
                return value
            elif 'section' in search_key and is_in_combined_sections(key, search_key) is not None:
                depth = is_in_combined_sections(key, search_key)
                result = find_key(value['rows'][depth], 'a')
                if result is not None:
                    return result
            else:
                result = find_key(value, search_key)
                if result is not None:
                    return result
    elif isinstance(json_obj, list):
        for item in json_obj:
            result = find_key(item, search_key)
            if result is not None:
                return result


def is_in_combined_sections(key, search_key):
    if 'To' in key:
        try:
            section_val = int(search_key.split('section')[1])
        except Exception:
            return None
        section_start, section_end = key.split('section')[1].split('To')
        if section_val in range(int(section_start), int(section_end)):
            return section_val - int(section_start)
        return None
    return None


def get_section(json_data, form, section):
    section_value = None
    documents = json_data['documents']
    for doc in documents:
        if form in doc['type']:
            section_value = find_key(doc, section)
            if 'section' in section and section_value is not None:
                return section_value
            else:
                if section_value is not None:
                    if 'dependents' in section:
                        return section_value
                    elif section_value.get('value', None) is not None:
                        return section_value

    return section_value


def add_est_savings(obj, tax_bracket, value):
    obj.update({'Est. Savings': format(math.ceil(int((tax_bracket/100) * value)), ',')})
    return obj


def count_dependents(dependents):
    count = 0
    for dependent in dependents:
        if dependent.get('i', {}).get('value'):
            count += 1
    return count


def get_amount(tax_info, page, tax_year):
    return float(tax_info[page]['section1A']) if tax_year == '2022' else float(tax_info[page]['section1'])
