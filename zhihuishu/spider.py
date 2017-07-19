from pyquery import PyQuery as pq
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from config import *
import time

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 50)

def into_index():
	try:
		print('正在进入主页......')
		browser.get('http://www.zhihuishu.com/')
		first_place = wait.until(
		        EC.element_to_be_clickable((By.XPATH, "//*[@id='login-register']/li[1]/a"))
		    )
		first_place.click()
		time.sleep(3)
		login()
	except TimeoutException:
		print("超时，重新进入主页......")
		into_index()

def login():
	try:
		print('进入主页成功，准备进入登录页面......')
		print('尝试登录，正在输入账号和密码......')
		u = wait.until(
		        EC.presence_of_element_located((By.CSS_SELECTOR, "#lUsername"))
		    )
		p = wait.until(
		        EC.presence_of_element_located((By.CSS_SELECTOR, "#lPassword"))
		    )
		Login = wait.until(
				EC.element_to_be_clickable((By.CSS_SELECTOR, "#f_sign_up > div > span"))
			)
		u.send_keys(username)
		p.send_keys(password)
		Login.click()
		time.sleep(3)
		into_study_page()	
	except TimeoutException:
		print('登录失败,重新进入主页......')
		into_index()

def into_study_page():
	try:
		print('登录成功，进入学习页面......')
		second_place = wait.until(
				EC.element_to_be_clickable((By.CSS_SELECTOR, "#course_recruit_studying_ul > li:nth-child(1) > div.new_stuCurseInfoBox.fr > div.promoteSchedule.mt15.clearfix > a"))
			)
		second_place.click()
		time.sleep(5)
		# 重定向窗口
		browser.switch_to_window(browser.window_handles[1])
		try:
			p_1 = WebDriverWait(browser, 30).until(
					EC.element_to_be_clickable((By.XPATH, "//*[starts-with(@id, 'tm_dialog_win_')]/div[1]/div[2]/a[1]"))
				)
			p_1.click()
		except TimeoutException:
			print('......')
		try:
			p_2 = WebDriverWait(browser, 20).until(
					EC.element_to_be_clickable((By.CSS_SELECTOR, "#j-assess-criteria_popup > span.popup_delete.j-popup-close	"))
				)
			time.sleep(5)
			p_2.click()
			time.sleep(3)
		except TimeoutException:
			print('......')
		all_time = get_all_time()
		while True:
			if all_time != 0:
				try:
					print('进入下一节学习成功')
					video_look(all_time)
					next_page = wait.until(
							EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.study_page > div.main_left > div > div.next_lesson > div > a"))
						)
					next_page.click()
					print('进入下一节的学习......')
					time.sleep(10)
					all_time = get_all_time()
				except:
					print('学习完毕')
					browser.close()
			else:
				print('翻页失败，尝试重新进入下一节')
				next_page.click()
				time.sleep(10)
				all_time = get_all_time()

	except TimeoutException:
		print('超时了...')

def video_look(all_time):
	html = browser.page_source
	doc = pq(html)
	question_num = doc('#examDot_undefined').items()
	time_group = []
	num = 1
	for item in question_num:
		T = item.attr('timenote')
		print('第', num, '次答题时间点：', T)
		Time = int((int(T[3:5])*60+int(T[6:])))
		time_group.append(Time)
		if num == 1:
			wait_answer(time_group[-1])
		else:
			wait_answer(time_group[-1]-time_group[-2])
		num += 1
	wait_time = all_time - time_group[-1]
	print('答题后需等待', wait_time, '秒后，完成本节课学习。')
	time.sleep(wait_time)

def wait_answer(wait_time):
	time.sleep(wait_time)
	answer = WebDriverWait(browser, 25).until(
				EC.element_to_be_clickable((By.XPATH, "//*[starts-with(@id, 'tm_dialog_win_')]/div[1]/div[2]/a[1]/span"))
		)
	answer.click()
	print('答题成功')

def get_all_time():
	mouse = wait.until(
	        EC.presence_of_element_located((By.CSS_SELECTOR, "#vjs_mediaplayer > div.videoArea.container"))
	    )
	ActionChains(browser).move_to_element(mouse).perform()
	tt1 = WebDriverWait(browser, 10).until(
				EC.presence_of_element_located((By.XPATH, "//*[@id='vjs_mediaplayer']/div[9]/div[3]/span[2]"))
		)
	tt2 = WebDriverWait(browser, 10).until(
				EC.presence_of_element_located((By.XPATH, "//*[@id='vjs_mediaplayer']/div[9]/div[3]/span[1]"))
		)
	T1 = tt1.text
	T2 = tt2.text
	if T1 == T2:
		return 0
	print('本次视频时长：', T1)
	all_time = int((int(T1[3:5])*60+int(T1[6:])))
	return all_time

def main():
	into_index()
	login()
	browser.close()


if __name__ == '__main__':
	main()

