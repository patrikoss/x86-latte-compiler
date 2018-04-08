	.file	"runtime.c"
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC0:
	.string	"%d\n"
	.section	.text.unlikely,"ax",@progbits
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4,,15
	.globl	printInt
	.type	printInt, @function
printInt:
.LFB60:
	.cfi_startproc
	subl	$16, %esp
	.cfi_def_cfa_offset 20
	pushl	20(%esp)
	.cfi_def_cfa_offset 24
	pushl	$.LC0
	.cfi_def_cfa_offset 28
	pushl	$1
	.cfi_def_cfa_offset 32
	call	__printf_chk
	addl	$28, %esp
	.cfi_def_cfa_offset 4
	ret
	.cfi_endproc
.LFE60:
	.size	printInt, .-printInt
	.section	.text.unlikely
.LCOLDE1:
	.text
.LHOTE1:
	.section	.text.unlikely
.LCOLDB2:
	.text
.LHOTB2:
	.p2align 4,,15
	.globl	printString
	.type	printString, @function
printString:
.LFB61:
	.cfi_startproc
	jmp	puts
	.cfi_endproc
.LFE61:
	.size	printString, .-printString
	.section	.text.unlikely
.LCOLDE2:
	.text
.LHOTE2:
	.section	.text.unlikely
.LCOLDB3:
	.text
.LHOTB3:
	.p2align 4,,15
	.globl	_error
	.type	_error, @function
_error:
.LFB62:
	.cfi_startproc
	subl	$24, %esp
	.cfi_def_cfa_offset 28
	pushl	28(%esp)
	.cfi_def_cfa_offset 32
	call	puts
	movl	$-1, (%esp)
	call	exit
	.cfi_endproc
.LFE62:
	.size	_error, .-_error
	.section	.text.unlikely
.LCOLDE3:
	.text
.LHOTE3:
	.section	.rodata.str1.1
.LC4:
	.string	"Runtime error"
	.section	.text.unlikely
.LCOLDB5:
	.text
.LHOTB5:
	.p2align 4,,15
	.globl	error
	.type	error, @function
error:
.LFB63:
	.cfi_startproc
	subl	$24, %esp
	.cfi_def_cfa_offset 28
	pushl	$.LC4
	.cfi_def_cfa_offset 32
	call	_error
	.cfi_endproc
.LFE63:
	.size	error, .-error
	.section	.text.unlikely
.LCOLDE5:
	.text
.LHOTE5:
	.section	.rodata.str1.1
.LC6:
	.string	"Runtime error: readInt failed"
	.section	.text.unlikely
.LCOLDB7:
	.text
.LHOTB7:
	.p2align 4,,15
	.globl	readInt
	.type	readInt, @function
readInt:
.LFB64:
	.cfi_startproc
	subl	$36, %esp
	.cfi_def_cfa_offset 40
	movl	%gs:20, %eax
	movl	%eax, 20(%esp)
	xorl	%eax, %eax
	leal	16(%esp), %eax
	pushl	%eax
	.cfi_def_cfa_offset 44
	pushl	$.LC0
	.cfi_def_cfa_offset 48
	call	__isoc99_scanf
	addl	$16, %esp
	.cfi_def_cfa_offset 32
	cmpl	$-1, %eax
	je	.L13
	movl	12(%esp), %edx
	xorl	%gs:20, %edx
	movl	8(%esp), %eax
	jne	.L14
	addl	$28, %esp
	.cfi_remember_state
	.cfi_def_cfa_offset 4
	ret
.L13:
	.cfi_restore_state
	subl	$12, %esp
	.cfi_remember_state
	.cfi_def_cfa_offset 44
	pushl	$.LC6
	.cfi_def_cfa_offset 48
	call	_error
.L14:
	.cfi_restore_state
	call	__stack_chk_fail
	.cfi_endproc
.LFE64:
	.size	readInt, .-readInt
	.section	.text.unlikely
.LCOLDE7:
	.text
.LHOTE7:
	.section	.rodata.str1.4,"aMS",@progbits,1
	.align 4
.LC8:
	.string	"Runtime error: readString failed."
	.section	.text.unlikely
.LCOLDB9:
	.text
.LHOTB9:
	.p2align 4,,15
	.globl	readString
	.type	readString, @function
readString:
.LFB65:
	.cfi_startproc
	subl	$32, %esp
	.cfi_def_cfa_offset 36
	movl	%gs:20, %eax
	movl	%eax, 16(%esp)
	xorl	%eax, %eax
	movl	$0, 8(%esp)
	movl	$0, 12(%esp)
	pushl	stdin
	.cfi_def_cfa_offset 40
	leal	16(%esp), %eax
	pushl	%eax
	.cfi_def_cfa_offset 44
	leal	16(%esp), %eax
	pushl	%eax
	.cfi_def_cfa_offset 48
	call	getline
	addl	$16, %esp
	.cfi_def_cfa_offset 32
	cmpl	$-1, %eax
	je	.L20
	movl	4(%esp), %edx
	cmpb	$10, -1(%edx,%eax)
	jne	.L17
	movb	$0, -1(%edx,%eax)
	movl	4(%esp), %edx
.L17:
	movl	12(%esp), %ecx
	xorl	%gs:20, %ecx
	movl	%edx, %eax
	jne	.L21
	addl	$28, %esp
	.cfi_remember_state
	.cfi_def_cfa_offset 4
	ret
.L20:
	.cfi_restore_state
	subl	$12, %esp
	.cfi_remember_state
	.cfi_def_cfa_offset 44
	pushl	$.LC8
	.cfi_def_cfa_offset 48
	call	_error
.L21:
	.cfi_restore_state
	call	__stack_chk_fail
	.cfi_endproc
.LFE65:
	.size	readString, .-readString
	.section	.text.unlikely
.LCOLDE9:
	.text
.LHOTE9:
	.section	.rodata.str1.1
.LC10:
	.string	"Runtime error: concat"
	.section	.text.unlikely
.LCOLDB11:
	.text
.LHOTB11:
	.p2align 4,,15
	.globl	concat
	.type	concat, @function
concat:
.LFB66:
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	pushl	%edi
	.cfi_def_cfa_offset 12
	.cfi_offset 7, -12
	pushl	%esi
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	pushl	%ebx
	.cfi_def_cfa_offset 20
	.cfi_offset 3, -20
	subl	$24, %esp
	.cfi_def_cfa_offset 44
	movl	44(%esp), %ebp
	pushl	%ebp
	.cfi_def_cfa_offset 48
	call	strlen
	popl	%edx
	.cfi_def_cfa_offset 44
	pushl	48(%esp)
	.cfi_def_cfa_offset 48
	movl	%eax, %ebx
	call	strlen
	movl	%eax, %esi
	leal	1(%ebx,%eax), %eax
	movl	%eax, (%esp)
	call	malloc
	addl	$16, %esp
	.cfi_def_cfa_offset 32
	testl	%eax, %eax
	je	.L25
	subl	$4, %esp
	.cfi_def_cfa_offset 36
	movl	%eax, %edi
	addl	$1, %esi
	pushl	%ebx
	.cfi_def_cfa_offset 40
	pushl	%ebp
	.cfi_def_cfa_offset 44
	addl	%edi, %ebx
	pushl	%eax
	.cfi_def_cfa_offset 48
	call	memcpy
	addl	$12, %esp
	.cfi_def_cfa_offset 36
	pushl	%esi
	.cfi_def_cfa_offset 40
	pushl	44(%esp)
	.cfi_def_cfa_offset 44
	pushl	%ebx
	.cfi_def_cfa_offset 48
	call	memcpy
	addl	$28, %esp
	.cfi_def_cfa_offset 20
	movl	%edi, %eax
	popl	%ebx
	.cfi_restore 3
	.cfi_def_cfa_offset 16
	popl	%esi
	.cfi_restore 6
	.cfi_def_cfa_offset 12
	popl	%edi
	.cfi_restore 7
	.cfi_def_cfa_offset 8
	popl	%ebp
	.cfi_restore 5
	.cfi_def_cfa_offset 4
	ret
.L25:
	.cfi_def_cfa_offset 32
	.cfi_offset 3, -20
	.cfi_offset 5, -8
	.cfi_offset 6, -16
	.cfi_offset 7, -12
	subl	$12, %esp
	.cfi_def_cfa_offset 44
	pushl	$.LC10
	.cfi_def_cfa_offset 48
	call	_error
	.cfi_endproc
.LFE66:
	.size	concat, .-concat
	.section	.text.unlikely
.LCOLDE11:
	.text
.LHOTE11:
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.5) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
