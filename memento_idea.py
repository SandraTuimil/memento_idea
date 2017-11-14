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


class memento_idea2(osv.osv):
    _name = 'memento.idea'
    _inherit = 'memento.idea'
 
    # busca la idea de la cual se deben actualizar campos
    def _get_idea_from_vote(self,cr,uid,ids,context={}):
        res = {}
        vote_ids = self.pool.get('memento.vote').browse(cr,uid,ids,context=context)        
        for v in vote_ids:
            res[v.idea_id.id] = True 
            print('---------------v.idea_id.id: ')
            print(v.idea_id.id)
        return res.keys()
 
 
    def _compute(self,cr,uid,ids,field_name,arg,context={}):
        res = {}
        for idea in self.browse(cr,uid,ids):
            vote_num = len(idea.vote_ids)
        #    vote_sum = sum([v.vote for v in idea.vote_ids])        

            #import ipdb
            #ipdb.set_trace()
            

                                   
            res[idea.id] = vote_num
            
            
            #    'vote_num' : vote_num,                
            #    'vote_avg': vote_sum/vote_num   , 
            
            
            print '---------------- tipo de vote_num:'
            print type(vote_num)
         #   print '---------------- tipo de vote_sum:'
         #   print type(vote_sum)
            
        
        import traceback
        traceback.print_stack()
        return res
    
    _columns = {
        'vote_ids': fields.one2many('memento.vote', 'idea_id', 'Votes'),
        'vote_num': fields.function(_compute,method=True,string='Vote Count',
            store= {
            'memento.vote':(_get_idea_from_vote,['vote'],10)
            }),
    }
    
    '''    'vote_avg': fields.function(_compute,method=True,string='Vote Count',
            store= {
            'memento.vote':(_get_idea_from_vote,['vote'],10)
            }),
    '''
 
memento_idea2()
