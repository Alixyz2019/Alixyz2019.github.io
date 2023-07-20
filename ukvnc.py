import requests
import streamlit as st

HMRC_API_URL = 'https://api.service.hmrc.gov.uk/'

def get_organization_details(vat_number):
    try:
        url = f'{HMRC_API_URL}organisations/vat/check-vat-number/lookup/{vat_number}'
        response = requests.get(url)
        data = response.json()

        if 'target' in data and 'vatNumber' in data['target']:
            return data['target']
        else:
            return None
    except (requests.RequestException, ValueError):
        return None

def format_address(address):
    address_lines = []
    for line in ['line1', 'line2', 'line3']:
        if line in address:
            address_lines.append(address[line])
    address_lines.append(address['postcode'])
    address_lines.append(address['countryCode'])
    return ', '.join(address_lines)

def main():

    vat_number = st.text_input('**Enter VAT Number: **')
    if st.button('Validate VAT Number'):
        if vat_number:
            st.text(f'Checking VAT Number: {vat_number}')
            organization_details = get_organization_details(vat_number)
            if organization_details:
                st.success('VAT Number is valid!')
                st.write('**Organization Details:**')
                st.write('**Name:**', organization_details['name'])
                st.write('**VAT Number:**', organization_details['vatNumber'])
                st.write('**Address:**', format_address(organization_details['address']))
            else:
                st.error('VAT Number is invalid!')
        else:
            st.warning('Please enter a VAT Number.')

if __name__ == '__main__':
    main()
