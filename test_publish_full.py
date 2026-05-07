from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 目标网站信息
TARGET_URL = "https://yomowoo.com"
USERNAME = "290191683@qq.com"
PASSWORD = "a12345678"

def test_publish_article():
    """测试发布文章并验证返回的链接"""
    driver = None
    try:
        # 1. 初始化浏览器
        print("正在初始化浏览器...")
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.implicitly_wait(10)
        
        # 2. 打开登录页面
        print("正在打开登录页面...")
        driver.get(TARGET_URL + "/login")
        
        # 3. 执行登录
        print("正在登录...")
        driver.find_element(By.NAME, "email").send_keys(USERNAME)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # 等待登录成功
        time.sleep(3)
        
        # 4. 打开发布页面
        print("正在打开发布页面...")
        driver.get(TARGET_URL + "/user/postedt.html")
        
        # 5. 创建测试文章
        test_title = "测试文章_" + str(int(time.time()))
        test_content = "这是一篇测试文章的内容，用于验证文章链接获取功能。"
        
        print(f"准备发布文章: {test_title}")
        
        # 6. 填写表单并发布（根据实际页面结构调整）
        # 找到标题输入框
        title_input = driver.find_element(By.NAME, "title")
        title_input.clear()
        title_input.send_keys(test_title)
        
        # 找到内容输入框
        content_input = driver.find_element(By.NAME, "content")
        content_input.clear()
        content_input.send_keys(test_content)
        
        # 点击发布按钮
        driver.find_element(By.CSS_SELECTOR, "button.submit").click()
        
        # 等待发布完成
        time.sleep(5)
        
        # 7. 获取当前URL
        current_url = driver.current_url
        print(f"发布后当前URL: {current_url}")
        
        # 8. 根据标题查找文章链接
        print("正在根据标题查找文章链接...")
        
        # 尝试从页面中找到刚发布的文章
        articles = driver.find_elements(By.CSS_SELECTOR, "article, .article-item, .post-item")
        found_url = None
        
        for article in articles:
            try:
                title_element = article.find_element(By.CSS_SELECTOR, "h2, h3, .title, a")
                if test_title in title_element.text:
                    link_element = article.find_element(By.TAG_NAME, "a")
                    found_url = link_element.get_attribute("href")
                    break
            except:
                continue
        
        # 如果找到了文章链接
        if found_url:
            print(f"找到文章链接: {found_url}")
            
            # 点击进入详情页获取最终链接
            driver.get(found_url)
            final_url = driver.current_url
            print(f"最终文章链接: {final_url}")
            
            # 验证链接格式
            if "/post/" in final_url and ".html" in final_url:
                print("✅ 文章链接格式正确！")
            else:
                print("❌ 文章链接格式不正确")
                
            return final_url
        else:
            print("❌ 未找到发布的文章")
            return None
            
    except Exception as e:
        print(f"测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        if driver:
            driver.quit()
            print("浏览器已关闭")

if __name__ == "__main__":
    result_url = test_publish_article()
    print(f"\n测试结果: {result_url}")