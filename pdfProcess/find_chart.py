import cv2
import os
import pdf2jpg
from skimage.measure import compare_ssim
def choose_chart(componentname,candidates_index):
    ##constants
    convert_width=1500
    convert_height=2000
    threshold_pin_similarity=0.6
    threshold_chart_similarity=0.5
    ##constants
    (pin_img,candidates)=ReadComponentImg(componentname,candidates_index)
    chart_img=cv2.imread("chart.png")
    #conver images to gray for compare
    clone_gray_chart_img=cv2.cvtColor(cv2.resize(chart_img.copy(),(convert_width,convert_height)),cv2.COLOR_BGR2GRAY)
    clone_gray_pin_img=cv2.cvtColor(cv2.resize(pin_img.copy(),(convert_width,convert_height)),cv2.COLOR_BGR2GRAY)
    clone_gray_candidates=[]
     #try to eliminate original pin_img
    print("eliminating image similar to pin_img")
    new_candidates=[]
    for i,candidate in enumerate(candidates):#calculate similarity score
        clone_gray_candidates.append(cv2.cvtColor(cv2.resize(candidate.copy(),(convert_width,convert_height)),cv2.COLOR_BGR2GRAY))
        score=compare_ssim(clone_gray_pin_img,clone_gray_candidates[i],full=True)[0]
        print(score)
        if score<threshold_pin_similarity:
            new_candidates.append(clone_gray_candidates[i])
    print("completed")   
    #try to choose chart
    print("choosing image similar to chart")
    charts=[]
    for i,gray_candidate in enumerate(new_candidates):#calculate similarity score
        score=compare_ssim(clone_gray_chart_img,gray_candidate,full=True)[0]
        print(score)
        if score>threshold_chart_similarity:
            charts.append(new_candidates[i])
    return charts
def ReadComponentImg(component_name,candidates_index):
    dir_path=os.path.join('tests',component_name,component_name)
    pin_img=cv2.imread(dir_path+".png")
    print("converting to jpg...")
    pdf2jpg.pdf2jpg(dir_path+".pdf")
    print("convert completed")
    candidates=[]
    for i in candidates_index:
        candidates.append(cv2.imread(os.path.join(dir_path,str(i+1)+".png")))

    return (pin_img,candidates)
if __name__=='__main__':
    charts=choose_chart('42-45S83200G-16160G',range(0,63))
    for img in charts:
        img=cv2.resize(img,(1000,1000))
        cv2.imshow('',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
