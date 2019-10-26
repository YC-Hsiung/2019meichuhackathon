import cv2
def choose_chart(pin_img,candidates):
    score=[]
    #conver images to gray for compare
    clone_gray_pin_img=cv2.cvtColor(pin_img.copy(),cv2.COLOR_BGR2GRAY)
    for i,candidate in enumerate(candidates):#calculate similarity score
        clone_gray_candidate=cv2.cvtColor(candidate.copy(),cv2.COLOR_BGR2GRAY)
        score.append(cv2.compare_ssim(clone_gray_pin_img,clone_gray_candidate,full=True)[0])
    choose_index= [i for i, in enumerate(score) if score[i]<0.8]#try to elminate original pin_img
    return candidates[choose_index]