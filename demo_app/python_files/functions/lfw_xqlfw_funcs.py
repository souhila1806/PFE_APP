import pandas as pd

from demo_app.python_files.utils import get_name_num_from_img, calcul_threshold_acc

def verif_pair(dataset,path_img1,path_img2,rec_model,rest=None):
    data=pd.read_csv(rf"C:\Users\HP\PycharmProjects\pythonProject\demo_app\data\files\{dataset.lower()}_scores.csv")
    data['image1'] = data['image1'].astype(int)
    data['image2'] = data['image2'].astype(int)
    name1, img1 = get_name_num_from_img(path_img1)
    name2, img2 = get_name_num_from_img(path_img2)
    if rest == None:
        col=rec_model.lower()
    else:
        col=f"{rec_model.lower()}_{rest.lower()}"
    print(col)
    line = data.loc[
        (data['name1'] == name1) & (data['name2'] == name2) & (data['image1'] == img1) & (data['image2'] == img2)]
    i = line.index[0] // 600
    score = line[col].iloc[0]
    threshold, acc, far, frr = calcul_threshold_acc(data[[col]], i)
    return score, threshold

def verif_fold(dataset,nb_fold,rec_model,rest=None):
    data=pd.read_csv(rf"C:\Users\HP\PycharmProjects\pythonProject\demo_app\data\files\{dataset.lower()}_scores.csv")
    data['image1'] = data['image1'].astype(int)
    data['image2'] = data['image2'].astype(int)
    if rest == None:
        col = rec_model.lower()
    else:
        col = f"{rec_model.lower()}_{rest.lower()}"
    threshold, acc, far, frr = calcul_threshold_acc(data[[col]],nb_fold)
    return acc, threshold

def verif_all(dataset,rec_model,rest=None):
    THR = []
    ACC = []
    FAR = []
    FRR = []
    data=pd.read_csv(rf"C:\Users\HP\PycharmProjects\pythonProject\demo_app\data\files\{dataset.lower()}_scores.csv")
    data['image1'] = data['image1'].astype(int)
    data['image2'] = data['image2'].astype(int)
    if rest == None:
        col = rec_model.lower()
    else:
        col = f"{rec_model.lower()}_{rest.lower()}"
    for i in range (10):
        threshold, acc, far, frr = calcul_threshold_acc(data[[col]],i)
        THR.append(threshold)
        ACC.append(acc)
        FAR.append(far)
        FRR.append(frr)


    total_acc = sum(ACC) / len(ACC)
    return total_acc


if __name__ == '__main__':

    #path_img1 = "demo_app/data/images/XQLFW/Nathalie_Baye_0002.jpg"
    #path_img2 = "demo_app/data/images/XQLFW/Nathalie_Baye_0004.jpg"
    path_img1 = "demo_app/data/images/XQLFW/Jonathan_Edwards_0005.jpg"
    path_img2 = "demo_app/data/images/XQLFW/Mark_Hurlbert_0003.jpg"
    rec_model='arcFace'
    #score,threshold=verif_pair('XQLFW',path_img1, path_img2, rec_model ,"gpen")
    acc,threshold=verif_fold('XQLFW',9,rec_model,"gpen")
    #acc=verif_all('xqlFW',rec_model)
    print(f"score is {acc} and threshold is{threshold}")
