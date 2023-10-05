import json
import math

from users.models.user_tax_info import UserTaxInfo

from .strategy_utils import add_est_savings, get_user_object, get_amount


def get_life_strategies(tax_info, tax_bracket, tax_year):
    strategies = []

    with open('tenants/resources/musetax_rules.json') as file:
        data = json.load(file)

        if float(tax_info['ScheduleA']['section8A']) > 0:
            a37 = data['Life']['A37']
            a39 = data['Life']['A39']
            a37['Est. Savings'] = 'varies'
            a39['Est. Savings'] = 'varies'
            strategies.extend([a37, a39])

        if get_amount(tax_info, '1040', tax_year) > 50000:
            a26 = add_est_savings(data['Life']['A26'], tax_bracket, 3850)
            strategies.append(a26)

        if float(tax_info['Schedule1']['section21']) > 0:
            a19 = add_est_savings(data['Life']['A19'], tax_bracket, 5250)
            strategies.append(a19)

        if float(tax_info['1040']['section34']) > 0:
            a35 = data['Life']['A35']
            a35['Est. Savings'] = 'varies'
            strategies.append(a35)

        if float(tax_info['1040']['section37']) > 0:
            a38 = data['Life']['A38']
            a38['Est. Savings'] = 'varies'
            strategies.append(a38)

        if float(tax_info['1040']['dependents']) > 0:
            a33 = data['Life']['A33']
            a33['Est. Savings'] = 'varies'
            a24 = data['Life']['A24']
            a24['Est. Savings'] = format(math.ceil(5000 * (tax_bracket/100 + 0.0765)), ',')
            strategies.extend([a24, a33])
            if float(tax_info['ScheduleD']['section7']) > 0 \
                    or float(tax_info['ScheduleD']['section15']) > 0:
                a25 = add_est_savings(data['Life']['A25'], 17000, 20)
                strategies.append(a25)

    return strategies


def get_retirement_strategies(tax_info, tax_bracket, tax_year):

    with open('tenants/resources/musetax_rules.json') as file:
        data = json.load(file)

        if get_amount(tax_info, '1040', tax_year) > 50000:
            a27 = add_est_savings(data['Retirement']['A27'], tax_bracket, 22500)
            a30 = add_est_savings(data['Retirement']['A30'], tax_bracket, 6500)
            return [a27, a30]

    return []


def get_investment_strategies(tax_info, tax_bracket):
    strategies = []

    with open('tenants/resources/musetax_rules.json') as file:
        data = json.load(file)

        if float(tax_info['ScheduleE']['section3']) > 10000:
            a11 = data['Investments']['A11']
            a11.update({'Est. Savings': 'varies'})
            strategies.append(a11)

        if float(tax_info['ScheduleD']['section7']) > 0 \
                or float(tax_info['ScheduleD']['section15']) > 0 \
                or tax_info['1040']['virtual_currency']:
            a14 = add_est_savings(data['Investments']['A14'], tax_bracket, 3000)
            strategies.append(a14)

        if float(tax_info['ScheduleA']['section8A']) > 0:
            a17 = add_est_savings(data['Investments']['A17'], tax_bracket, 2100)
            strategies.append(a17)

    return strategies


def get_business_strategies(tax_info, tax_bracket):
    strategies = []

    with open('tenants/resources/musetax_rules.json') as file:
        data = json.load(file)

        if float(tax_info['ScheduleC']['section26']) > 0:
            a1 = add_est_savings(data['Business']['A1'], tax_bracket, 1000)
            strategies.append(a1)

        if float(tax_info['ScheduleC']['section31']) > 50000:
            a2 = data['Business']['A2']
            a2['Est. Savings'] = format(3060, ',')
            strategies.append(a2)

        if float(tax_info['ScheduleC']['section31']) > 25000:
            a3 = add_est_savings(data['Business']['A3'], tax_bracket, 25000)
            strategies.append(a3)

        if float(tax_info['ScheduleC']['section31']) > 0:
            a4 = add_est_savings(data['Business']['A4'], tax_bracket, 47500)
            strategies.append(a4)

            if float(tax_info['1040']['dependents']) > 0:
                a5 = data['Business']['A5']
                a5['Est. Savings'] = format(math.ceil(tax_bracket/100 * 13850), ',')
                strategies.append(a5)

    return strategies


def get_strategies_plan(tax_info, tax_bracket, name, tax_year):
    plan = {'Life': get_life_strategies(tax_info, tax_bracket, tax_year),
            'Business': get_business_strategies(tax_info, tax_bracket),
            'Investments': get_investment_strategies(tax_info, tax_bracket),
            'Retirement': get_retirement_strategies(tax_info, tax_bracket, tax_year)}
    user_info = UserTaxInfo.objects.get(user=get_user_object(name), tax_year=tax_year)
    user_info.tax_plan = plan
    user_info.save()
    return plan
