# -*- coding: utf-8 -*-

{
    'name' :  'memento_idea',
    'version' :  '1.0',
    'author' :  'OpenERP - Sandra Tuimil Calvo',
    'description' :  '''Ideas management module. 
        
        CONFIGURACIÓN: 
        Añadir acceso al menú ¡Idea!/Configuración al grupo Memento-Idea / Manager para que sólo este grupo tenga acceso. 
    
    ''',
    'category' :  'Enterprise Innovation',  
  
    'depends' :  [
                'base', 
                ]  ,
    'update_xml' :  [   
        'security/groups.xml',
        'security/ir.model.access.csv',      
        'view/views.xml',
        'wizard/wizard_vote.xml',
    
    
    ]  ,

    'installable': True, 
    'active': True,    
}