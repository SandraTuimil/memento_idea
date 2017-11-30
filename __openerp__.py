# -*- coding: utf-8 -*-

{
    'name' :  'memento_idea',
    'version' :  '1.0',
    'author' :  'OpenERP',
    'description' :  'Ideas management module',
    'category' :  'Enterprise Innovation',  
  
    'depends' :  ['base']  ,
    'update_xml' :  [   
        'security/groups.xml',
        'security/ir.model.access.csv',      
        'view/views.xml',

    
    
    ]  ,

    'installable': True, 
    'active': True,    
}