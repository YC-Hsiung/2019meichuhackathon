import cv2
import os
import pdf2jpg
def choose_chart(componentname,candidates_index):
    (pin_img,candidates)=ReadComponentImg(componentname,candidates_index)
    chart_img=cv2.imread("chart.png")
    clone_gray_chart_img=cv2.cvtColor(chart_img.copy(),cv2.COLOR_BGR2GRAY)
    score=[]
    #conver images to gray for compare
    clone_gray_pin_img=cv2.cvtColor(pin_img.copy(),cv2.COLOR_BGR2GRAY)
    for i,candidate in enumerate(candidates):#calculate similarity score
        clone_gray_candidate=cv2.cvtColor(candidate.copy(),cv2.COLOR_BGR2GRAY)
        score.append(cv2.compare_ssim(clone_gray_pin_img,clone_gray_candidate,full=True)[0])
    choose_index= [i for i, in enumerate(score) if score[i]<0.8]#try to eliminate original pin_img
    candidates=candidates[choose_index]
    for i,candidate in enumerate(candidates):#calculate similarity score
        clone_gray_candidate=cv2.cvtColor(candidate.copy(),cv2.COLOR_BGR2GRAY)
        score.append(cv2.compare_ssim(clone_gray_chart_img,clone_gray_candidate,full=True)[0])
    choose_index= [i for i, in enumerate(score) if score[i]>0.6]#try to choose chart
    return candidates[choose_index]
def ReadComponentImg(component_name,candidates_index):
    dir_path=os.path.join('tests',component_name)
    pin_img=cv2.imread(dir_path+".png",))
    pdf2jpg(dir_path)
    candidates=[]
    for i in candidates_index:
        candidates.append(cv2.imread(dir_path+"_"+str(i)+".png"))
    return (pin_img,candidates_index)
