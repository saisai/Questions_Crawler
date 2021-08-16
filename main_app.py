import time

from web_browser import WebBrowser


def main(json_data):
    url = "https://www.google.com/webhp?safe=strict&ie=utf-8&hl={}&gl={}&num={}".format(json_data["lang"],
                                                                                        json_data["plac"],
                                                                                        json_data["num"])
    driver = WebBrowser(0)
    driver.google_searcher(url, json_data["keyword"])
    elems = driver.browser.execute_script('return document.querySelectorAll("h3 ~ div > div")')

    if len(elems) < 4:
        ques = {"Err": "No questions Found"}
    else:
        ques = {}
        for i in range(int(json_data["ques_num"])):
            elems = driver.browser.execute_script('return document.querySelectorAll("h3 ~ div > div")')
            if len(elems) - 5 < i:
                print("FAIL")
                break
            elems[i].click()
            time.sleep(1)

            t = driver.browser.execute_script(
                """elems = arguments[0].querySelectorAll("div");
                    arr = [];
                    for(i=0;i<elems.length;i++)
                      if(elems[i].innerText.length && (elems[i].querySelector("div, cite, h3, a")==null || \
                                                                                elems[i].querySelector(":scope >  ul")))
                        arr.push(elems[i].inner""" + json_data["resp_type"] + """)  
                    return arr
                        """, elems[i])
            ques.update({t[0]: "\n".join(t[1:])})
    driver.browser.close()
    return ques
