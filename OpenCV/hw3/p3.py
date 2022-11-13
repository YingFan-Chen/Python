import cv2
import math
from matplotlib.colors import Normalize
import numpy as np
import matplotlib.pyplot as plt

def imread(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return img

def plot(pos, img, title):
    plt.subplot(pos)
    plt.xticks([]), plt.yticks([])
    plt.title(title)
    plt.imshow(img, cmap = 'gray')

def show():
    plt.show()

def save(path, img):
    plt.imsave(path, img, cmap = 'gray')

def erosion(img, kernel):
    h1, w1 = img.shape
    h2, w2 = kernel.shape
    mid = [h2//2, w2//2]
    res = np.zeros((h1, w1))
    for x in range(h1 - h2):
        for y in range(w1 - w2):
            if (img[x:x+h2, y:y+w2] == kernel).all():
                res[x + mid[0], y + mid[1]] = 1
    return res

def particle_size(img):
    h, w = img.shape
    res_h, res_w = 0, 0
    for i in range(h):
        if img[i, 0]:
            res_h += 1
        elif res_h:
            break
    for i in range(w):
        if img[0, i]:
            res_w += 1
        elif res_w:
            break
    return res_h, res_w 

def solve_A(img, overlap, h_k, w_k):
    h, w = img.shape
    mid = [h_k // 2, w_k // 2]
    res = np.zeros((h, w))
    for x in range(h):
        for y in range(w):
            if img[x, y]:
                if overlap[x-mid[0]:x-mid[0]+h_k, y-mid[1]:y-mid[1]+w_k].sum() > 1:
                    res[x-mid[0]:x-mid[0]+h_k, y-mid[1]:y-mid[1]+w_k] = 1
    return res

def vertical2dot(img):
    h, w = img.shape
    res = np.zeros((h, w))
    for x in range(h - 1):
        for y in range(w):
            if img[x, y]:
                if x - 1 >= 0 and img[x - 1, y] and img[x + 1, y] == 0:
                    res[x, y] = 0
                else:
                    res[x, y] = 1
    return res
 
def horizontal2dot(img):
    h, w = img.shape
    res = np.zeros((h, w))
    for x in range(h):
        for y in range(w - 1):
            if img[x, y]:
                if y - 1 >= 0 and img[x, y - 1] and img[x, y + 1] == 0:
                    res[x, y] = 0
                else:
                    res[x, y] = 1
    return res

def sub(A, B):
    res = A - B
    h, w = res.shape
    for x in range(h):
        for y in range(w):
            if res[x, y] == -1:
                res[x, y] = 0
    return res

def solve_B(img, h_k, w_k):
    h, w = img.shape
    mid = [h_k // 2 + 5, w_k // 2 + 5]
    for x in range(h):
        for y in range(w):
            if x - mid[0] <= 0 or x + mid[0] >= h:
                img[x ,y] = 0
            if y - mid[1] <= 0 or y + mid[1] >= w:
                img[x, y] = 0
    res = np.zeros((h, w))
    for x in range(h):
        for y in range(w):
            if tmp[x, y]:
                res[x-mid[0]:x-mid[0]+h_k, y-mid[1]:y-mid[1]+w_k] = 1
    return res

if __name__ == '__main__':
    img = imread('./images/bricks.tif')
    img = np.bool_(img)
    plot(221, img, 'Origin')

    # (A)
    particle = particle_size(img)
    overlap = img

    for i in range(particle[0]):
        overlap = vertical2dot(overlap)
    plot(222, overlap, 'Overlap 1')

    for i in range(particle[1]):
        overlap = horizontal2dot(overlap)
    plot(223, overlap, 'Overlap 2')

    kernel = np.ones((particle[0] - 3, particle[1] - 1))
    ero = erosion(img, kernel)

    A = solve_A(ero, overlap, particle[0], particle[1])
    plot(224, A, 'A')
    show()
    save('./images/3_a.jpg', A)

    # (B)
    plot(221, img, 'Origin')

    tmp = sub(img, A)
    plot(222, tmp, 'Sub')

    tmp = erosion(tmp, kernel)
    B = solve_B(tmp, particle[0], particle[1])
    plot(223, B, 'B')
    show()
    save('./images/3_b.jpg', B)