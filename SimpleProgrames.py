import time

class sorting_alg:

    #Selection sort
    def selection_sort(list):
        a=0
        for i in range(len(list)):
            min = list[i]
            j=i+1
            while True:
                if j >= len(list):
                    break
                if min > list[j]:
                    min = list[j]
                    a=j
                j+=1
            if min != list[i]:
                list[a] = list[i]
                list[i] = min
        return list

    #Insertion sort
    def insertion_sort(list):
        for i in range(len(list)-1):
            el=i
            if list[i] > list[i+1]:
                c = list[i]
                list[i] = list[i+1]
                list[i+1] = c
                if i != 0:
                    j=i
                    while j > 0:
                        if list[j] < list[j-1]:
                            c = list[j]
                            list[j] = list[j-1]
                            list[j-1] = c
                        j-=1
        return list
        
    #Merge sort
    def merge_sort(list):
        if len(list) == 1:
            return list
        left = sorting_alg.merge_sort(list[:len(list)//2])
        right = sorting_alg.merge_sort(list[len(list)//2:])
        return sorting_alg.merge(left,right)

    def merge(left,right):
        list_ = []
        left_count = 0
        right_count = 0
        try:
            while True:
                if left[left_count] > right[right_count]:
                    list_.append(right[right_count])
                    right_count+=1
                else:
                    list_.append(left[left_count])
                    left_count+=1
        except:
            return list_ + left[left_count:] + right[right_count:]

st = time.time()
list = [5,3,1,4,8,0,7,2,6]
et = time.time()
elapsed_time = time.time() - st
print("Run time of programe:", elapsed_time * 1000)