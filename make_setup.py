import datetime

EASYSMART_VERSION = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
with open('setup_exp.py', 'r', encoding='utf-8') as f:
    setup_exp = f.read()
    setup_exp = setup_exp.replace('$EASYSMART_VERSION$', EASYSMART_VERSION)
with open('setup.py', 'w', encoding='utf-8') as f:
    f.write(setup_exp)
