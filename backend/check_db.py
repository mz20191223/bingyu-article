from app import create_app, db
from app.models import SysDept, SysPost

app = create_app()
with app.app_context():
    print('部门表数据：')
    depts = SysDept.query.all()
    for d in depts:
        print(f'{d.dept_id}: {d.dept_name}')
    
    print('\n岗位表数据：')
    posts = SysPost.query.all()
    for p in posts:
        print(f'{p.post_id}: {p.post_name}')