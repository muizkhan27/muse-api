from pathlib import Path

import environ
import pdfkit
from jinja2 import Template

from tenants.utils.constants import PDF_IMAGES, PDF_OPTIONS

env = environ.Env(
  DEBUG=(bool, False)
)
environ.Env.read_env()


def generate_muse_report(muse_affects, tax_rate, name, year):
    report_data = ''

    images = {
        key: 'http://' + env('HOST') + '/static/muse_images/' + filename
        for key, filename in PDF_IMAGES.items()
    }

    top_plans = get_best_tax_plans(muse_affects)
    top_plans.append(format_sum(top_plans))
    front_page_template = Path('templates/pdf_templates/front_pages.html').read_text()
    front_page = Template(front_page_template).render(
        username=name,
        tax_rate=tax_rate,
        images=images,
        top_plans=top_plans,
        tax_year=year
    )
    report_data += front_page

    html = Path('templates/pdf_templates/strategy.html').read_text()
    template = Template(html)
    for category, strategies in muse_affects.items():
        for strategy in strategies:
            image = strategy['Muse Image']
            image_url = 'http://' + env('HOST') + '/static/muse_images/' + image + '.png'
            page = template.render(category=category, strategy=strategy, image_url=image_url)
            report_data += page

    pdfkit.from_string(report_data, 'static/muse_reports/' + name + '_' + year + '.pdf', options=PDF_OPTIONS)


def get_best_tax_plans(muse_affects):
    savings = [
        strategy
        for strategies in muse_affects.values()
        for strategy in strategies
        if isinstance(strategy.get('Est. Savings', None), str)
        and strategy['Est. Savings'].replace(',', '').isdigit()
    ]
    return sorted(savings, key=lambda x: x['Est. Savings'], reverse=True)[:min(len(savings), 7)]


def format_sum(top_plans):
    return format(sum(int(item['Est. Savings'].replace(',', '')) for item in top_plans), ',')
