# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
import random

def index():
    increment_count = URL('increment_count')
    decrement_count = URL('decrement_count')
    db.person.truncate()
    message = 'wtf is this'
    add_url = URL('addtotable')
    add_btn = A('Submit', _class='btn', _href=URL('default', 'counts'))
    return dict(message=message, add_url=add_url, add_btn=add_btn,
                increment_count=increment_count, decrement_count=decrement_count)


def part2():
    import random
    scramble = 30
    temp_player = 'temp'
    random_rank = ["Wun","Tooh","Thuhree","Fior","Vive Jive",
                    "Sicksy","Zeben","Aight","Nein","Tent" ]
    while scramble > 0:
      index1 = random.randint(0,9)
      part2 = random.randint(0,9)
      if index1 != part2:
        temp_player = random_rank[index1]
        random_rank[index1] = random_rank[part2]
        random_rank[part2] = temp_player
        scramble = scramble - 1
        pass
    pass
    return dict(random_rank=random_rank)

def addtotable():
    s = request.vars.msg or ''
    db.person.insert(name = s)
    return response.json(dict(result=s))


def addone():
    s = request.vars.msg or ''
    return response.json(dict(result=s))

def increment_count():
    s = request.vars.msg or ''
    db(db.person.name == s).update(rank_num = db.person.rank_num + 1)
    return response.json(dict(result="success"))

def decrement_count():
    s = request.vars.msg or ''
    db(db.person.name == s).update(rank_num = db.person.rank_num -1)
    db(db.person.rank_num < 0 ).update(rank_num = 0)
    return response.json(dict(result="success"))

def counts():
    posts = SQLFORM.grid(db.person,
             fields=[
                     db.person.name,
                     db.person.rank_num,
                     
                     ],
             deletable=True,
             sortable = True,
             csv = False,
             details = False,
             create = True,
             editable = True,
             orderby = db.person.rank_num,

             )
    return dict(posts=posts)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
