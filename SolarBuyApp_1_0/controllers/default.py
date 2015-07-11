#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
import random

#-----------------------------------------------------------------------
# Public page for all users before logging in
#-----------------------------------------------------------------------
def index():
    session.counter = (session.counter or 0) + 1
    response.flash = T("Welcome to Solar Buy Saving")
    return dict( counter=session.counter)

#-----------------------------------------------------------------------
# User will login and then be asked whether he or she is a customer
#      or a contractor. So they can be directed to their corresponding
#      account interface.
#-----------------------------------------------------------------------
@auth.requires_login()
def login():
    response.flash = T("Choose Either As A Customer Or A Contractor")
    form = SQLFORM(db.login)
    if form.process().accepted:
        r = random.getrandbits(60)
        form.vars.random_id = r
        redirect(URL('default', 'company', args = [form.vars.id, r]))
    return dict(form=form)

#-----------------------------------------------------------------------
# Customer's main account interface
#-----------------------------------------------------------------------
@auth.requires_login()
def customer():
    response.flash = T("Customer Interface")
    return dict()

#-----------------------------------------------------------------------
# Customers are able to search for auctions
#-----------------------------------------------------------------------
@auth.requires_login()
def customer_view():
    grid = SQLFORM.grid(db.questions,
                        fields=[db.questions.User,
                                db.questions.Address],
                        csv = False
                       )
    return dict(grid=grid)

#-----------------------------------------------------------------------
# Enlists Contractor's Company
#-----------------------------------------------------------------------
@auth.requires_login()
def company():
    response.flash = T("Enter Your Company's Name")
    form = SQLFORM(db.company)
    if form.process().accepted:
        redirect(URL('default','index'))
    return dict(form=form)


#-----------------------------------------------------------------------
# Contractor's main account interface
#-----------------------------------------------------------------------
@auth.requires_login()
def contractor():
    response.flash = T("Contractor's Interface")
    return dict()

#-----------------------------------------------------------------------
# Contractors are able to search for an auction
#-----------------------------------------------------------------------
@auth.requires_login()
def contractor_view():
    grid = SQLFORM.grid(db.questions,
                        fields=[db.questions.User, db.questions.City],
                        editable = False,
                        deletable = False,
                        create = False,
                        csv = False,
                        links=[dict(header=T('Respond to Customer'),
                                    body = lambda r: A('Respond', _class='btn',
                                    _href=URL('default', 'contractor_add', args=[r.id])))],
                        )
    return dict(grid=grid)

#-----------------------------------------------------------------------
# Allows contractors to respond to customer's auctions
#        by bidding prices to accommodate customer's interests
#-----------------------------------------------------------------------
@auth.requires_login()
def contractor_add():
    form = SQLFORM(db.reply)
    if form.process().accepted:
        r = random.getrandbits(60)
        form.vars.random_id = r
        session.flash = T('Inserted')
        redirect(URL('default', 'contractor', args = [form.vars.id, r]))
    return dict(form=form)

#-----------------------------------------------------------------------
# Allows customers to hold auctions
#-----------------------------------------------------------------------
@auth.requires_login()
def add():
    form = SQLFORM(db.questions)
    if form.process().accepted:
        r = random.getrandbits(60)
        form.vars.random_id = r
        session.flash = T('Inserted')
        redirect(URL('default', 'customer', args = [form.vars.id, r]))

    return dict(form=form)

#-----------------------------------------------------------------------
# Others
#-----------------------------------------------------------------------
def user():
    return dict(form=auth())

@cache.action()
def download():
    return response.download(request, db)

def call():
    return service()

@auth.requires_signature()
def data():
    return dict(form=crud())
