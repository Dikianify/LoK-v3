
def get_product_array(arr):
    prod_arr = []
    incoming = 1
    for index, num in enumerate(arr):
        if index != i-1:
            incoming *= num
        prod_arr.append(incoming)
        incoming = 1
    return prod_arr

print(get_product_array([1,2,3,4]))