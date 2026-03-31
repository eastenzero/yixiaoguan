import os

def replace_in_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

base_dir = r"c:\Users\Administrator\Documents\code\yixiaoguan\services\business-api\ruoyi-admin\src\main\java\com\yixiaoguan"

replacements = [
    ("PageUtils.getPageDomain()", "com.ruoyi.common.core.page.TableSupport.buildPageRequest()"),
    ("javax.servlet.http", "jakarta.servlet.http"),
    ("com.yixiaoguan.common.core.page.TableDataInfo", "com.ruoyi.common.core.page.TableDataInfo")
]

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.java'):
            filepath = os.path.join(root, file)
            replace_in_file(filepath, replacements)

print("Replacement complete.")
