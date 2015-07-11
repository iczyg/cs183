from datetime import datetime
db = DAL("sqlite://storage.sqlite")

#------------------------------------------------------------------------------------
# GETS ENTERED USER'S FIRST AND LAST NAME
#------------------------------------------------------------------------------------
def get_name():
                if auth.user: return auth.user.first_name + " " + auth.user.last_name
                else:         return 'None'
#------------------------------------------------------------------------------------
# GET ENTERED USER'S EMAILED
#------------------------------------------------------------------------------------
def get_email():
                if auth.user: return auth.user.email
                else:         return 'None'

#------------------------------------------------------------------------------------
# Questions Generated For Customer's To Hold Auctions
# cost = /month; usage = KWH
#------------------------------------------------------------------------------------
db.define_table('questions',
   Field('User', default = get_name,
                 writable = False),
   Field('Email', default = get_email,
                  writable = False),
   Field('Address'),
   Field('City', 'string'),
   Field('State', 'string'),
   Field('Zip_Code', 'integer'),
   Field('Roof_Type', requires=IS_IN_SET ( ['Inclined',
                                       'Very Inclined',
                                       'Flat', 'Ground' ],
                                     zero = T('Please Select One') ) ),
   Field('Direction_of_Roof', requires=IS_IN_SET ( ['North',
                                            'South',
                                            'East',
                                            'West',
                                            'NorthWest',
                                            'NorthEast',
                                            'SouthWest',
                                            'SouthEast'],
                                          zero = T('Please Select One') ) ),
   Field('Sun_Direction', requires=IS_IN_SET ( ['Little Amount',
                                      'Fair Amount',
                                      'Strong Amount' ],
                                    zero = T('Please Select One') ) ),
   Field('Cost_Per_Month', 'double'),
   Field('Average_Usage_KWH', 'double'),
   Field('Comments', 'text'),
   Field('Respond', 'boolean', readable = False),
   )
db.questions.id.readable = False

#------------------------------------------------------------------------------------
# For Contractor's Response to Customer's Interests
# Needs a boolean to indicate whether the auction was responded or not.
# It also needs a boolean to indicate if the response(bid) was approved.
#------------------------------------------------------------------------------------
db.define_table('reply',
   Field('Company', default = get_name,
                    writable = False),
   Field('Email', default = get_email,
                  writable = False),
   Field('Address'),
   Field('City', 'string'),
   Field('State', 'string'),
   Field('Zip_Code', 'integer'),
   Field('Price', 'double'),
   Field('Approve', 'boolean', readable = False),
   Field('Disapprove', 'boolean', readable = False),
   )
db.reply.id.readable = False

#------------------------------------------------------------------------------------
# For Determining Two Distinct Logins
#------------------------------------------------------------------------------------
db.define_table('login',
   Field('Customer', 'boolean'),
   Field('Contractor', 'boolean')
   )
db.login.id.readable = False

#------------------------------------------------------------------------------------
# If User Is A Contractor He Will Need To Enlist His Company
#------------------------------------------------------------------------------------
db.define_table('company',
   Field('Company', 'string')
   )
db.company.id.readable = False
