db.define_table ('person',
   Field('name','text'),
   Field('rank_num', 'integer', default=0),
   )


db.person.rank_num.label = 'Count number'