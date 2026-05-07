import os
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, Keyword
import openpyxl

app = create_app()

def import_keywords():
    # 关键词文件路径
    keyword_file = r'D:\python project\auto_publish.py\Function-promotiom\关键词.xlsx'
    
    if not os.path.exists(keyword_file):
        print(f"错误：文件不存在 - {keyword_file}")
        print("请检查文件路径是否正确")
        return
    
    try:
        # 打开 Excel 文件
        wb = openpyxl.load_workbook(keyword_file)
        sheet = wb.active
        
        with app.app_context():
            # 获取已存在的关键词
            existing_keywords = set()
            for kw in Keyword.query.all():
                existing_keywords.add(kw.keyword.strip())
            
            imported_count = 0
            skipped_count = 0
            
            # 遍历所有行（跳过标题行）
            for row in sheet.iter_rows(min_row=2, values_only=True):
                keyword = str(row[0]).strip() if row[0] else None
                
                if keyword and keyword != 'None':
                    if keyword not in existing_keywords:
                        new_keyword = Keyword(keyword=keyword, status=0)
                        db.session.add(new_keyword)
                        imported_count += 1
                        existing_keywords.add(keyword)
                    else:
                        skipped_count += 1
            
            db.session.commit()
            print(f"关键词导入完成！")
            print(f"成功导入: {imported_count} 个")
            print(f"重复跳过: {skipped_count} 个")
            
    except Exception as e:
        print(f"导入失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    import_keywords()