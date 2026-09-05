class ListNode:
    def __init__(self, val: int = 0, next = None):
        self.val = val
        self.next = next



class Solution:
    def reverseList_head(self, head:ListNode) -> ListNode | None:
        '''头插法反转链表'''
        pre = None
        cur = head
        while cur:
            '''用三个指针完成逐步翻转：pre: 前一个节点，cur: 当前节点，nxt: 下一个节点'''
            nxt = cur.next
            cur.next = pre
            pre = cur
            cur = nxt
        return pre

    def reverseList_tail(self, head: ListNode) -> ListNode | None:
        '''尾插递归法反转链表'''
        if head is None or head.next is None:
            return head
        new_head = self.reverseList_tail(head.next) # 递归调用，递归得到原链表的尾巴 - 新链表的表头
        tail = head.next # 原链表的尾节点
        tail.next = head  # 让原链表尾节点指向倒数第二个节点
        head.next = None # 断开原链表倒数第二个节点与尾节点的连接
        return new_head # 返回新链表表头


