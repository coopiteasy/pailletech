{'name' : 'Quick Record Search',
 'version' : '1.1',
 'author' : 'Emipro Technologies Pvt. Ltd.',
 'maintainer': 'Emipro Technologies Pvt. Ltd.',
 'summary': 'Quick Record Search',
 'category': 'Search',
 'complexity': "normal",  # easy, normal, expert
 'depends' : ['base'],
 'description': """
   This module provides you a facility to search any record quickly, based on your preferences.
   
   For any queries, contact us at info@emiprotechnologies.com
 
   For more tutorials regarding Odoo, you can visit our website www.emiprotechnologies.com
    

""",
 'website': 'http://www.emiprotechnologies.com',
 'data': ['view/res_users.xml',
          'view/js_view.xml',
          'view/quick_record_search_view.xml',
          'security/ir.model.access.csv',         
          ],
 'qweb': ['static/src/xml/job_search.xml',],
 'js': ['static/src/js/job_search.js',],
 'css': ['static/src/css/job_search.css',],
 'installable': True,
 'images' : [''], 
 'auto_install': False,
 
}
