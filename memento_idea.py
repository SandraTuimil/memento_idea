# -*- coding: utf-8 -*-
from osv import osv, fields

class category(osv.osv):
    _name = 'memento.category'
    _columns = {
        'name': fields.char('Title', size=64, required=True, translate=True),
        'description': fields.char('Description', size=64, required=True, translate=True),   
        'parent_id': fields.many2one('memento.category','Parent Category',ondelete="set null"),
        'child_ids': fields.one2many('memento.category','parent_id','Child Categories'),
    }
category()


class comment(osv.osv):
    _name = 'memento.comment'
    _columns = {
        'content': fields.text('Comment'),
        'idea_id': fields.many2one('memento.idea','Idea'),
    }
comment()


class idea(osv.osv):
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
        'voto_pruebas': fields.float('Vote',digits=(2,1)),# sólo para probar 
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
        return super(idea,self).create(cr, uid, vals, context=context)
        
    
    
    
idea()


class vote(osv.osv):
    _name = 'memento.vote'
    _rec_name = 'id'
    _columns = {
        'id': fields.integer('Id'),
        'vote': fields.float('Vote',digits=(2,1)),
        'partner_id': fields.many2one('res.partner','Partner', ondelete = "restrict"),
        'idea_id': fields.many2one('memento.idea','Idea',  ondelete = "restrict"),
        'creator_id': fields.many2one('res.users','Creator', readonly=True),
    }
    
    _sql_constraints = [('creator_idea_unique', 'unique(creator_id,idea_id)', 'Un usuario sólo puede votar una idea una vez. ')]



    def create(self, cr, uid, vals, context=None):     
        vals.update({'creator_id': uid})        
        return super(vote,self).create(cr, uid, vals, context=context)
    
    
    def votar(self,cr,uid,id_idea,voto_pruebas):
        '''
        Comprueba si hay un voto anterior de ese usuario para esa idea. Si no lo hay, lo crea. 
        '''
        posible_voto= self.pool.get('memento.vote').search(cr,uid, [('idea_id','=',id_idea),('creator_id','=',uid)])
        print posible_voto
        try: 
            posible_voto.pop()
        except: 
            self.pool.get('memento.vote').create(cr, uid, {'idea_id':id_idea, 'vote':voto_pruebas})
vote()


class idea2(osv.osv):
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
    
#    def read(cr,user,ids): 
#        
#        print('-------------------READ-----------------------')
#        return super(idea,self).read()
    


    def votar(self,cr,uid,ids,arg,context={}):
        idea = self.pool.get('memento.idea').browse(cr,uid,ids,context=context) 
        
        
#        id_idea = 1
#        for i in idea: id_idea = i.id
        
        vote_object =  self.pool.get('memento.vote')
        
        for i in idea:             
            vote_object.votar(cr,uid,i.id,i.voto_pruebas)
        
        
        return True
        
        
idea2()
