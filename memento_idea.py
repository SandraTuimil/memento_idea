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


class memento_comment(osv.osv):
    _name = 'memento.comment'
    _columns = {
        'content': fields.text('Comment'),
        'idea_id': fields.many2one('memento.idea','Idea'),
    }
memento_comment()


class memento_idea(osv.osv):
    _name = 'memento.idea'
    _columns = {
        'name': fields.char('Title', size=64, required=True, translate=True),
        'state': fields.selection([('draft','Draft'),('in_valuation','in valuation'),
                                ('accepted','Accepted'),('confirmed','Confirmed'),('closed','Closed')],
            'State',required=True, readonly=True),
        'description': fields.text('Description', readonly=True, 
                    states={'draft':[('readonly',False)]}),
        'category_id': fields.many2one('memento.category','Category'),
        'inventor_id': fields.many2one('res.partner','Inventor'),
        'inventor_company_id': fields.related('inventor_id','company_id',
            readonly=True, type='many2one',
            relation='res.company', string='Inventor Company'),
        'comment_ids': fields.one2many('memento.comment','idea_id','Comments'),
        'active': fields.boolean('Active', select=True),
        'creator_id': fields.many2one('res.users','Creator', readonly=True),
        'voto_pruebas': fields.float('Vote',digits=(2,1)),
    }
  #  def get_employee_from_user: 
    
    _defaults = {
        'active': lambda *a: True,
        'state': lambda *a: 'draft',
    }
    _sql_constraints = [('name_uniq','unique(name)', 'Idea must be unique!')]
    
    def create(self, cr, uid, vals, context=None):
        vals.update({'state': 'in_valuation'})
        vals.update({'creator_id':uid})
        return super(memento_idea,self).create(cr, uid, vals, context=context)
        
    
    
    
memento_idea()


class memento_vote(osv.osv):
    _name = 'memento.vote'
    _rec_name = 'id'
    _columns = {
        'id': fields.integer('Id'),
        'vote': fields.float('Vote',digits=(2,1)),
        'partner_id': fields.many2one('res.partner','Partner', ondelete = "restrict"),
        'idea_id': fields.many2one('memento.idea','Idea',  ondelete = "restrict"),
        'creator_id': fields.many2one('res.users','Creator', readonly=True),
    }
    
    _sql_constraints = [('partner_idea_unique', 'unique(partner_id,idea_id)', 'Un usuario sólo puede votar una idea una vez. ')]



    def create(self, cr, uid, vals, context=None):
        vote_ids = self.pool.get('memento.vote').browse(cr,uid,ids,context=context)    
        
        vals.update({'creator_id': uid})
        
        return super(memento_vote,self).create(cr, uid, vals, context=context)
    
    
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
            # import ipdb; ipdb.set_trace()
            vote_num = len(idea.vote_ids)
            vote_sum = sum([v.vote for v in idea.vote_ids])     
            
            if vote_num != 0: 
                vote_avg = vote_sum / vote_num
            else: 
                vote_avg = 0
                                           
            res[idea.id] = {
                'vote_num' : vote_num,
                'vote_avg' : int(vote_avg)           
            }          
        return res
    
    _columns = {
        'vote_ids': fields.one2many('memento.vote', 'idea_id', 'Votes', 
                        readonly=True),
        'vote_num': fields.function(_compute,method=True,string='Vote Count',multi='votes',
            store= {
            'memento.vote':(_get_idea_from_vote,['vote'],10)
            }),            
        'vote_avg': fields.function(_compute,method=True,string='Vote Average',multi='votes',
            store= {
            'memento.vote':(_get_idea_from_vote,['vote'],10)
            }),            
    }
    
    
    def votar(self,cr,uid,ids,arg,context={}):
        print('------------------ !!!!!!VOTAR!!!!!!!!!---------------')
        return True
        
        
memento_idea2()
