import numpy as np

def get_matrix(name):
    print(f"\nEnter {name} matrix:")
    r = int(input("Rows: "))
    c = int(input("Cols: "))
    print("Enter rows (space-separated numbers):")
    data = [list(map(float, input().split())) for _ in range(r)]
    return np.array(data)

while True:
    print("\n=== Matrix Operations Tool ===")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Transpose")
    print("5. Determinant")
    print("6. Exit")
    ch = input("Choose option: ")

    if ch == '6':
        print("Goodbye!")
        break

    if ch in ('1', '2', '3'):
        A = get_matrix("Matrix A")
        B = get_matrix("Matrix B")

        if ch == '1':
            result = A + B
        elif ch == '2':
            result = A - B
        else:
            if A.shape[1] == B.shape[0]:
                result = A @ B
            else:
                result = "Error: Incompatible sizes for multiplication!"
    else:
        A = get_matrix("Matrix")
        if ch == '4':
            result = A.T
        elif ch == '5':
            if A.shape[0] == A.shape[1]:
                result = np.linalg.det(A)
            else:
                result = "Error: Determinant only works for square matrices!"
        else:
            print("Invalid choice!")
            continue

    print("\n--- Result ---")
    print(result)