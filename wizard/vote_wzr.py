# -*- coding: utf-8 -*-
from osv import fields,osv
import datetime
class vote_wzr(osv.osv_memory):
    _name = 'memento_idea.wizard.vote_wzr'

    def list_ideas(self,cr,uid,context=None):
        '''
        Muestra ideas en valoración que el usuario actual no ha votado. 
        '''
        res =[]
        votos_usuario = self.pool.get('memento.vote').search(cr,uid,[('creator_id','=',uid)])     
        ideas_votadas_usuario = self.pool.get('memento.idea').search(cr,uid,[('vote_ids','=',votos_usuario)])
        ids_ideas = self.pool.get('memento.idea').search(cr,uid,[('id','not in',ideas_votadas_usuario),('state','=','in_valuation')])
        ideas = self.pool.get('memento.idea').browse(cr,uid,ids_ideas)
        for i in ideas:
            res.append((i.id,i.name))
        return res

    _columns = {
        'voto': fields.float('Vote',digits=(2,1)),        
        'idea': fields.selection(list_ideas, 'Idea', help='Ideas que no he votado'),
        'usuario': fields.integer('User', readonly=True)
    }
    
    
    def cleanup(self, cr, uid, ids, context={}):
        voto = self.pool.get('memento.vote')
        
        for w in self.browse(cr,uid,ids):     
            voto.votar(cr, uid, w.idea,w.voto)
    

        
vote_wzr()