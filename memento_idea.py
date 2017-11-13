# -*- coding: utf-8 -*-
from osv import osv, fields

class memento_category(osv.osv):
    _name = 'memento.category'
    _columns = {
        'name': fields.char('Title', size=64, required=True, translate=True),
        'description': fields.char('Description', size=64, required=True, translate=True),   
        'parent_id': fields.many2one('memento.category','Parent Category',ondelete="set null"),
        'child_ids': fields.one2many('memento.category','parent_id','Child Categories'),
    }
memento_category()



class memento_idea(osv.osv):
    _name = 'memento.idea'
    _columns = {
        'name': fields.char('Title', size=64, required=True, translate=True),
        'description': fields.text('Description'),
        'category_id': fields.many2one('memento.category','Category'),
    }
memento_idea()


class memento_vote(osv.osv):
    _name = 'memento.vote'
    _rec_name = 'id'
    _columns = {
        'id': fields.integer('Id'),
        'vote': fields.float('Vote',digits=(2,1)),
        'partner_id': fields.many2one('res.partner','Partner'),
        'idea_id': fields.many2one('memento.idea','Idea'),
    
    }
memento_vote()

'''
class memento_idea2(osv.osv):
    _name = ?? 
    _inherit = memento_idea
 
 
 
memento_idea2()
    
'''