   # Note: Twillio limitations will only send texts to area codes (603), (801)

andrew = {
  'first_name': 'Andrew',
  'last_name': 'Tidd',
  'full': lambda x: self.first_name + ' ' + self.last_name,
  'email': 'andrew@sendmi.com',
  'phone': '617-555-0185',
  'password': 'federals',
  'businesses': ['accordionConnection']
} #Developer

brad = {
  'first_name': 'Bradley',
  'last_name': 'Wilkes',
  'email': 'brad@fake.com',
  'phone': '(801)456-7890',
  'password': 'password',
  'businesses': [],
  'country': 'United States'
} #Developer

jeffrey = {
  'first_name': 'Jeffrey',
  'last_name': 'Reading',
  'email': 'jeffrey@sendmi.com',
  'phone': '(801) 380-7425',
  'password': 'sendmijeff',
  'businesses': ['abacusCorporation']
} #Developer

nintendo = {
  'find_name': 'Nintendo of America',
  'find_option': 1,
  'ein': '66787665',
  'name': 'Nintendo of America',
  'line1': '4600 150th Avenue Northeast',
  'city': 'Redmond',
  'country': 'United States',
  'state': 'Washington',
  'postal_code': '98052',
  'phone': '(425) 882-2040',
  'website': 'http://www.nintendo.com/corp/'
}

accordionConnection = {
  'find_name': 'Accordion Connection, LLC',
  'find_option': 1,
  'ein': '548585',
  'name': 'Accordion Connection, LLC',
  'line1': '136 New Hampshire 106',
  'city': 'Gilmanton',
  'country': 'United States',
  'state': 'New Hampshire',
  'postal_code': '03237',
  'phone': '(603) 267-8600',
  'website': 'http://accordionconnection.com/'
}

abacusCorporation = {
  'find_name': 'Abacus Corporation',
  'find_option': 1,
  'ein': '98765432',
  'name': 'Abacus Corporation',
  'line1': ' 610 Gusryan Street',
  'city': 'Baltimore',
  'country': 'United States',
  'state': 'Maryland',
  'postal-code': '21224',
  'phone': '(410) 633-1900',
  'website': 'http://abacuscorporation.biz/about-abacus'
}

lili = {
  'first_name': 'Lili',
  'last_name': 'Ana',
  'email': 'lili@dummy.com',
  'phone': '(202) 498-1279',
  'password': 'asdfasdf',
  'businesses': []
}

nicol = {
  'first_name': 'Nicol',
  'last_name': 'Bolas',
  'full': lambda x: nicol.first_name + ' ' + nicol.last_name,
  'email': 'nbolas@example.com',
  'phone': '(202) 487-6542',
  'password': 'asdfasdf',
  'businesses': ['multiverse']
}

# Used to test reset password funcionality
# test_authentication.py:TestForgotPassword.test_success
alone1 = {
  'first_name': 'Stand',
  'last_name': 'Alone1',
  'full': lambda x: alone1.first_name + ' ' + alone1.last_name,
  'email': 'alone1@example.com',
  'phone': '(202) 487-1234',
  'password': 'asdfasdf',
  'businesses': []
}

# test_employees.py:TestDetails.test_profile
alone2 = {
  'first_name': 'Stand',
  'last_name': 'Alone2',
  'full': lambda x: alone2.first_name + ' ' + alone2.last_name,
  'email': 'alone2@example.com',
  'phone': '(202) 487-1235',
  'password': 'asdfasdf',
  'businesses': []
}

# test_employees.py:TestDetails.test_verify_permissions
alone3 = {
  'first_name': 'Stand',
  'last_name': 'Alone3',
  'full': lambda x: alone3.first_name + ' ' + alone3.last_name,
  'email': 'alone3@example.com',
  'phone': '(202) 487-1236',
  'password': 'asdfasdf',
  'businesses': []
}

# test_profile.py:TestPS.test_change_password
alone4 = {
  'first_name': 'Stand',
  'last_name': 'Alone4',
  'full': lambda x: alone4.first_name + ' ' + alone4.last_name,
  'email': 'alone4@example.com',
  'phone': '(202) 487-1237',
  'password': 'asdfasdf',
  'businesses': []
}

# test_profile.py:TestPS.test_update_email
alone5 = {
  'first_name': 'Stand',
  'last_name': 'Alone5',
  'full': lambda x: alone5.first_name + ' ' + alone5.last_name,
  'email': 'alone5@example.com',
  'phone': '(202) 487-1238',
  'password': 'asdfasdf',
  'businesses': []
}

# test_menu.py:TestDefaultBehavior.test_employee_buttons
# Must have NO permissions
alone6 = {
  'first_name': 'Stand',
  'last_name': 'Alone6',
  'full': lambda x: alone6.first_name + ' ' + alone6.last_name,
  'email': 'alone6@example.com',
  'phone': '(202) 487-1239',
  'password': 'asdfasdf',
  'businesses': []
}

################### Profiles for create/delete business tests #################

# test_business.py:TestDetails.test_required_fields
boss = {
  'first_name': 'Boss',
  'last_name': 'Mcbossface',
  'full': lambda x: boss.first_name + ' ' + boss.last_name,
  'email': 'boss@example.com',
  'phone': '(202) 555-4846',
  'password': 'asdfasdf',
  'businesses': []
}

# test_business.py:TestPrefilled.test_required_fields
faker = {
  'first_name': 'Faker',
  'last_name': 'Mctester',
  'full': lambda x: faker.first_name + ' ' + faker.last_name,
  'email': 'faker@example.com',
  'phone': '(202) 555-8877',
  'password': 'asdfasdf',
  'businesses': []
}

# test_business.py:TestPrefilled.test_success_skip
tester = {
  'first_name': 'Tester',
  'last_name': 'McTester',
  'full': lambda x: tester.first_name + ' ' + tester.last_name,
  'email': 'tester@example.com',
  'phone': '(202) 555-9988',
  'password': 'asdfasdf',
  'businesses': []
}

# test_business.py:TestPrefilled.test_success_participate
fire = {
  'first_name': 'Firefox',
  'last_name': 'Boss',
  'full': lambda x: fire.first_name + ' ' + fire.last_name,
  'email': 'fire@example.com',
  'phone': '(202) 555-1000',
  'password': 'asdfasdf',
  'businesses': []
}

patrick = {
  'first_name': 'Patrick',
  'last_name': 'Star',
  'full': lambda x: patrick.first_name + ' ' + patrick.last_name,
  'email': 'patrick@example.com',
  'phone': '(202) 222-0000',
  'password': 'asdfasdf',
  'businesses': []
}

krabs = {
  'first_name': 'Eugene',
  'last_name': 'Krabs',
  'full': lambda x: krabs.first_name + ' ' + krabs.last_name,
  'email': 'krabs@example.com',
  'phone': '(202) 222-4234',
  'password': 'asdfasdf',
  'businesses': []
}

squid = {
  'first_name': 'Squidward',
  'last_name': 'Tentacles',
  'full': lambda x: squid.first_name + ' ' + squid.last_name,
  'email': 'squid@example.com',
  'phone': '(202) 222-4235',
  'password': 'asdfasdf',
  'businesses': []
}

# Has following Active Employees:
  #Lili Ana (lili@dummy.com, Manage Bus. perm)
  #Sandy Cheeks (scheeks@example.com, no perms)
  #Irene's Test accounts (no perms)
  # Nicol Bolas (nbolas@example.com, owner/admin)
# Has following Invited Employee:
  #Jane Doe (mime@example.com, for reinvite test)
# Has following Removed Employee:
  # Zuriel Conseco
# Has following Terminated Employee:
  # Aaron Hernandez
multiverse = {
  'find_name': 'Multiverse',
  'find_option': 1,
  'ein': '4896434',
  'hr': 'nbolas@example.com',
  'name': 'Multiverse',
  'line1': '17 Whiteladies Road',
  'city': 'Avon',
  'country': 'United States',
  'state': 'New York',
  'postal_code': '14414',
  'phone': '(202) 548-4023',
  'website': 'http://multiverse-music.com/'
}

# employee of multiverse, no permissions
# employee of Dunkin' Donuts, no permissions
# has recipients setup for test_recipient.py
# has account balance
cheeks = {
  'first_name': 'Sandy',
  'last_name': 'Cheeks',
  'email': 'scheeks@example.com',
  'phone': '(202) 786-4237',
  'password': 'asdfasdf',
  'businesses': []
}


booth = {
  'first-name': 'Jeremy',
  'last_name': 'Booth',
  'email': 'jwbooth@example.com',
  'phone': '(202) 789-1248',
  'password': 'eighty-seven',
  'businesses': []
} #Employer with no buisnesses


test = {
  'first-name': 'Test',
  'last-name': 'Account',
  'email': 'testaccount@example.com',
  'phone': '(202) 578-4687',
  'password': 'asdfasdf',
  'businesses': []
}
# Employee of Multiverse. Use for password/language tests?

education = {
  'first-name': 'Test',
  'last-name': 'Account',
  'email': 'testaccount@example.com',
  'phone': '(202) 578-4687',
  'password': 'testing123',
  'businesses': []
}
# used for education

def get_credentials(name):
  if name is not None:
    return eval(name)

# different states...

# employers
  # no businesses                 Jeremy Booth
  # one business                  Nicol (multi, Nintendo if remove business fails)
  # multiple businesses           Nicol (have to add 1)
  # owner of 1 bus, employee of 1 Nicol (invite nicol to be

  # 1 employee (self)
  # multiple employees            Nicol (multi)

# employees
  # no businesses                 Lili
  # one business                  Nicol (multi, Nintendo if remove business fails), Alejandro (multi)
  # multiple businesses           Sandy (multi, Dunkin Donuts), test

  # no personal accounts          Jeremy, Lili
  # existing personal accounts    Nicol, Sandy

  # no account balance            Nicol,Jeremy,Lili, test
  # account balance               Sandy, Alejandro

