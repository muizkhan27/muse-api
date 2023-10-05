TAX_INFO_SECTIONS = [
        ('1040', 'year'),
        ('1040', 'dependents'),
        ('1040', 'section1'),
        ('1040', 'section34'),
        ('1040', 'section37'),
        ('Schedule1', 'section21'),
        ('ScheduleA', 'section8A'),
        ('ScheduleC', 'section26'),
        ('ScheduleC', 'section31'),
        ('ScheduleD', 'section7'),
        ('ScheduleD', 'section15'),
        ('ScheduleE', 'section3')

    ]

TAX_INFO_SECTIONS_22 = [
        ('1040', 'section1A'),
        ('1040', 'section34'),
        ('1040', 'section37'),
        ('Schedule1', 'section21'),
        ('ScheduleA', 'section8A'),
        ('ScheduleC', 'section26'),
        ('ScheduleC', 'section31'),
        ('ScheduleD', 'section7'),
        ('ScheduleD', 'section15'),
        ('ScheduleE', 'section3')

    ]

DB_TAX_INFO = {
        '1040': {},
        'Schedule1': {},
        'ScheduleA': {},
        'ScheduleC': {},
        'ScheduleD': {},
        'ScheduleE': {}
    }

FILING_STATUSES = {
        'filingStatusSingle': 'single',
        'filingStatusMarried': 'married_joint',
        'filingStatusMfs': 'married_separate',
        'filingStatusHoh': 'head_of_household'
    }

FILING_STATUSES_22 = {
        'filingStatusSingle': 'single',
        'filingStatusMarried': 'married_joint',
        'filingStatusMFS': 'married_separate',
        'filingStatusHOH': 'head_of_household'
    }

PDF_OPTIONS = {
        'page-size': 'A4',
        'margin-top': '0.5in',
        'margin-right': '0.5in',
        'margin-bottom': '0.5in',
        'margin-left': '0.5in',
        "enable-local-file-access": ""
    }

PDF_IMAGES = {
        'logo': 'logo.png',
        'disclaimer': 'toc_disclaimer.png',
        'top_savings': 'toc_top_savings.png',
        'strategy': 'toc_strategy.png',
        'overview': 'strategy_overview.png'
    }
