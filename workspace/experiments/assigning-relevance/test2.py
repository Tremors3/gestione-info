import undetected_chromedriver as uc

options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
driver = uc.Chrome(options=options)

driver.get("https://duckduckgo.com/?q=QUIC+protocol+site%3Ahttps%3A%2F%2Fwww.rfc-editor.org%2Frfc%2F")
print(driver.page_source)
driver.get
driver.quit()
