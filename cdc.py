from selenium import webdriver
import os
import time

url = "http://www.chinacdc.cn/jkzt/crb/zl/szkb_11803"

fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)  # 0 for defualt dir, 2 for comstumize
fp.set_preference("browser.download.dir", "/home/perom/cdc")
fp.set_preference("browser.download.manager.showWhenStarting", False)

# dont open in browser
fp.set_preference("plugin.disable_full_page_plugin_for_types", \
        "application/pd")
fp.set_preference("pdfjs.disabled", True)

# pdf file don't ask open or save
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
driver = webdriver.Firefox(firefox_profile = fp)
driver.get(url)


def process_item(item, driver):
    item_url = item.get_attribute('href')
    #driver.set_page_load_timeout(20)
    try:
        item.click()
    except:
        pass
    if not item_url.endswith('.pdf'):
        try:
            what = driver.find_element_by_class_name("cn-main-left")
            title = what.find_element_by_class_name("cn-main-title")
            detail = what.find_element_by_class_name("TRS_Editor")
        except:
            pass
        driver.back()


methods = driver.find_elements_by_class_name("method-item-title")
method_count = len(methods)
for i in range(method_count):
    methods = driver.find_elements_by_class_name("method-item-title")
    methods[i].click()

    loop_para = 1
    while loop_para:
        content = driver.find_element_by_class_name("jal-item-list")
        items = content.find_elements_by_tag_name('a')
        items_count = len(items)
        for j in range(items_count):
            content = driver.find_element_by_class_name("jal-item-list")
            items = content.find_elements_by_tag_name('a')
            process_item(items[j], driver)
            driver.refresh()
        try:
            driver.find_element_by_link_text("尾页").click()
        except:
            loop_para = 0
    driver.get(url)

