; Declare arrays
.data
    x: .byte 1, 2, 3, 4, 5
    y: .short 2, 54, 32, 8
    z: .long 10 DUP (50)

; Storing values into memory using register arithmetic
.text
	mov $6, %eax
	mov 2(x), (%eax)
	mov 3(y), 2(%eax)
	mov (z), (%ebx)
	mov 3, %ecx
	mov 2(y), -5(%eax, 3)
	mov 4(x), (%eax, 2, %ecx)
	mov 4(x), 12(%eax, 2, %ecx)
	mov 4(x), 12(%eax, 2, %ecx, 4)