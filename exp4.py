

class AddressBook:


    def __init__(self) -> None:
        '''初始化'''
        self.contacts: dict[str,dict[str,str]]={}
    
    def add_contact(self, name: str, phone: str, email: str, work: str) -> None:
        '''添加某人的信息'''
        if name in self.contacts:
            print(f'联系人{name}已存在，将更新其信息')
        self.contacts[name]={
            'phone':phone,
            'email':email,
            'work':work
        }
        print(f'联系人{name}信息添加/更新成功')
    
    def del_contact(self, name: str) -> None:
        '''删除某人信息，如果某人不存在则反馈'''
        if name not in self.contacts:
            print(f'该联系人{name}不存在')
        else:
            del self.contacts[name]
            print(f'该联系人{name}已删除')

    def find_contact(self,name: str) -> dict[str,str] | None:
        '''查找某人并列出详细信息'''
        if name in self.contacts:
            info: dict[str,str] = self.contacts[name]
            print(f'该联系人{name}已找到，其相关信息如下:')
            print(f'姓名：{name}')
            print(f'电话：{info['phone']}')
            print(f'邮箱：{info['email']}')
            print(f'工作地点：{info['work']}')
            return info
        else:
            print('该联系人找不到，不在通讯录内')
            return None
        
    def show_contact(self) -> None:
        '''列出通讯录所有人信息'''
        if not self.contacts:
            print('通讯录为空！')
            return
        print('--------所有联系人如下--------')
        i: int = 1
        for name,info in self.contacts.items():
            print(f'联系人{i}:')
            i += 1
            print(f'姓名：{name}')
            print(f'电话：{info['phone']}')
            print(f'邮箱：{info['email']}')
            print(f'工作地点：{info['work']}')
        print('-----------------------')
        print(f'共有{len(self.contacts)}位联系人')
    
def main() -> None:
    book: AddressBook = AddressBook()

    while True:
        print('---通讯录菜单---')
        print('1.添加联系人')
        print('2.删除联系人')
        print('3.查询联系人')
        print('4.列出全部联系人')
        print('5.退出通讯录')
        choice: str = input('请选择(输入1-5数字来选择):').strip()
        if choice == '1':
            print('请输入联系人信息：')
            name: str = input('请输入姓名：').strip()
            phone: str = input('请输入联系方式：').strip()
            email: str = input('请输入邮箱地址：').strip()
            work: str = input('请输入工作地址：').strip()
            book.add_contact(name,phone,email,work)
            print('新的联系人{name}已加入通讯录')
        elif choice == '2':
            name = input('请输入要删除的联系人：').strip()
            if name:
                book.del_contact(name)
                print(f'联系人{name}已删除')
            else:
                print('姓名不能为空')
        elif choice == '3':
            name = input('请输入要查询的联系人：').strip()
            _ = book.find_contact(name)
        elif choice == '4':
            book.show_contact()
        elif choice == '5':
            print('已退出')
            break
        else:
            print('无效选项，请重新输入')

if __name__ =='__main__':
    main()


    

