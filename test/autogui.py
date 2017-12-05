import pyautogui as gui


# gui.mouseDown(200,500)
# gui.mouseUp(100,500)
# gui.moveTo(200,100)

# gui.click(180,1060)
# gui.doubleClick(180,1000)

# gui. typewrite("Hello!!" ,interval=0.1)  # interval 한글자간 텀

# gui.alert(text='',title='',button='OK')
# gui.confirm(text='comfirm ㅊㅇ ',title=' 입력',buttons=['OK','Cancel'])
# gg = gui.prompt( text='Prompt 창',title=' 입력하세요',default='')  # 입력 값을 받아옴
# print(gg)
# ps = gui.password(text='Password 창 ',title=' 비밀번호를 입력',default='kjm092244',mask='*')  # 입력 값을 받아옴
# print(ps)

wid = 60
hei = 450
# gui.moveTo(wid,hei)

position = gui.position()  # 위치 가져오기
print(position)

*** 클릭 했을때 포지션 위치 파악해서 데이터 보관 ***
