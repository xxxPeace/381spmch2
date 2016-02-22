# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

from gluon.tools import Crud
crud = Crud(db)


def index():
    show_all = request.args(0) == 'all'
    if show_all:
        button = A('Show available items', _class="btn btn-info", _href=URL('default', 'index'))
    else:
        button = A('Show all items', _class="btn btn-info", _href=URL('default', 'index', args=['all']))

    if show_all:
        q = db.forSaleList
        listings = db().select(db.forSaleList.ALL, orderby = db.forSaleList.Title)
    else:
        q=(db.forSaleList.Status == True)
        listings = db(db.forSaleList.Status == True).select(db.forSaleList.ALL, orderby = db.forSaleList.Title)

    form = SQLFORM.grid(q,
        args=request.args[:1],
        fields=[db.forSaleList.Title,
                    db.forSaleList.Seller,
                    db.forSaleList.Description,
               ],
        editable=False, deletable=False,
        paginate=10,
        csv=False,
        create=False,
        searchable=False
        )
    return locals()

def showList():
    depts = db().select(db.forSaleList.ALL, orderby=db.forSaleList.Date)
    return locals()

def imageTables(): 
   return dict(tables=db().select(db.imageList.ALL))

@auth.requires_login()
def addItem():
    crud.messages.submit_button = 'Place on market'
    crud.settings.keepvalues = True
    crud.settings.label_separator = ' :'
    crud.settings.formstyle = 'ul'
    form = crud.create(db.forSaleList)
    return locals()

@auth.requires_login()
def add():
    """Add a post."""
    SQLFORM.messages.submit_button = 'Place on market'
    form = SQLFORM(db.forSaleList)
    if form.process().accepted:
        # Successful processing.
        session.flash = T("inserted")
        redirect(URL('default', 'index'))
    return locals()

@auth.requires_login()
def addImage():
    """Add a post."""
    saleList = db.forSaleList(request.args(0,cast=int)) or redirect(URL('index'))
    db.imageList.forSaleList_id.default = saleList.id
    #form = SQLFORM(db.imageList)
    form = crud.create(db.imageList)
    if form.process().accepted:
        # Successful processing.
        session.flash = T("inserted")
        redirect(URL('default', 'index'))
    return locals()

@auth.requires_login()
def manageItems():
    grid = SQLFORM.grid(db.forSaleList)
    return locals()


def show():
    image = db.forSaleList(request.args(0,cast=int)) or redirect(URL('index'))
    #forum = db.post(request.args(0,cast=int)) or redirect(URL('generalForum'))
    #comms  = db(db.comm.post_id==forum.id).select(db.comm.ALL, orderby=db.comm.datetime)
    db.imageList.forSaleList_id.default = image.id
    
    form = SQLFORM(db.imageList,record=None,
        deletable=False, linkto=None,
        upload=None, fields=None, labels=None,
        col3={}, submit_button='Post image',
        delete_label='Check to delete:',
        showid=True, readonly=False,
        comments=True, keepopts=[],
        ignore_rw=False, record_id=None,
        formstyle='bootstrap3_stacked',
        buttons=['submit'], separator=':')
    #form = crud.create(db.imageList)
    if form.process().accepted:
        # Successful processing.
        session.flash = T("inserted")
        redirect(URL('default', 'index'))
    itemImages= db(db.imageList.forSaleList_id==image.id).select(db.imageList.ALL)
    return locals()



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
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
