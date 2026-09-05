from dataclasses import dataclass, field, asdict
import os
import subprocess
from pathlib import Path
import json
import csv

# 自定义异常层级
class ContactError(Exception):
    '''通讯录所有异常的基类'''
    pass


class ValidationError(ContactError):
    '''输入校验失败（姓名/手机号/邮箱不合法）'''
    pass

class ContactNotFoundError(ContactError):
    '''联系人不存在'''
    pass




@dataclass
class Person:
    '''单个联系人实体'''
    name: str
    phone: str
    email: str = ''
    work: str = ''

    @staticmethod
    def  validate_name(name: str) ->  None:
        if not name or not name.strip():
            raise ValidationError('姓名不能为空')

    @staticmethod
    def validate_phone(phone: str) -> None:
        if not phone:
            raise ValidationError('手机号不能为空')
        if not phone.isdigit():
            raise ValidationError(f'手机号必须为纯数字，当前输入为：{phone}')
        if len(phone) != 11:
            raise ValidationError(f'手机号必须为11位数字，当前输入为：{phone}')

    @staticmethod
    def validate_email(email: str) -> None:
        if email and ('@' not in email or '.'  not in email):
            raise ValidationError(f'邮箱地址不合法，当前输入为：{email}')





def clear_screen() -> None:
    '''跨平台清屏：Windows 用 cls，其它系统用 clear'''
    _ = subprocess.run('cls' if os.name == 'nt' else 'clear', shell = True, check = False)


@dataclass
class ContactBook:
    '''通讯录'''
    
    contacts: dict[str, Person] = field(default_factory = dict, repr = False)
    filepath: str = 'contacts.json'
    filepath_csv: str = 'contacts.csv'

    def __post_init__(self):
        '''将目录里面的json文件加载到当前通讯录中'''
        if Path(self.filepath).exists():
            try:
                with open(self.filepath, 'r', encoding = 'utf-8') as f:
                    data = json.load(f)
                    for name, person_data in data.items():
                        self.contacts[name] = Person(**person_data)
            except(json.JSONDecodeError, KeyError):
                print('文件格式损坏，将使用空白通讯录')
                
    def save(self):
        '''将当前的通讯录信息保存在json文件中'''
        with open(self.filepath, 'w', encoding = 'utf-8') as f:
            data = {name: asdict(person) for name, person in self.contacts.items()}
            json.dump(data, f, ensure_ascii = False, indent = 4)

        print('文件已写入，保存成功')





    @property
    def count(self) -> int:
        '''实时返回当前的总联系人数量'''
        return len(self.contacts)

    def add_contact(self, name: str) -> None:
        '''添加/更新联系人信息'''
        Person.validate_name(name)
        phone: str = input('请输入电话：').strip()
        Person.validate_phone(phone)
        email: str = input('请输入邮箱：').strip()
        Person.validate_email(email)
        work: str = input('请输入工作地点：').strip()
        # 能运行到此处，证明校验全部通过

        self.contacts[name] = Person(name = name, phone = phone, email = email, work = work)
        print(f'联系人{name}信息添加/更新成功')

    def search_contact(self, name: str) -> Person | None:
        '''查找指定联系人的信息'''
        if not name:
            raise ValidationError('姓名不能为空')
        person: Person | None = self.contacts.get(name)
        if person is None:
            raise ContactNotFoundError(f'联系人{name}不存在')        
        print(f'联系人{name}已找到，其信息如下：')
        print(f'  电话：{person.phone}')
        print(f'  邮箱: {person.email}')
        print(f'  工作: {person.work}')
        return person


    def del_contact(self, name: str) -> None:
        '''删除指定联系人'''
        if not name:
            raise ValidationError('姓名不能为空')
        if name not in self.contacts:
            raise ContactNotFoundError(f'联系人{name}不存在')
        _ = self.contacts.pop(name)
        print(f'联系人{name}已删除')

    def show_contacts(self) -> None:
        '''列出所有联系人'''
        if not self.contacts:
            print('通讯录为空！')
            return
        print('______________所有联系人如下______________')
        for i, (name, person) in enumerate( self.contacts.items(), start = 1):
            print(f'第{i}位联系人{name}:')
            print(f'phone : {person.phone}')
            print(f'email : {person.email}')
            print(f'work : {person.work}')
            print('----------------------------------------')
        print(f'共有{self.count}位联系人')
        
    def show_numbers(self) -> None:
        '''显示当前的总联系人数量'''  
        print(f'当前总共有{self.count}位联系人')




def main() -> None:
    book: ContactBook = ContactBook(filepath = 'contacts.json')
    while(True):
        clear_screen()
        print('1.添加/更新联系人')
        print('2.查找联系人')
        print('3.删除联系人')
        print('4.列出所有联系人')
        print('5.显示当前的总联系人数量')
        print('6.退出并保存通讯录')
        sem: str = input('请输入操作对应的序号：').strip()

        try:
            if not sem:
                print('输入不能为空，请重新选择')
                _ = input('按回车键继续...')
                continue
            if sem == '1':
                print('添加新联系人：')
                name =input('姓名：').strip()
                if name in book.contacts:
                    print(f'联系人{name}已存在，将更新其信息')
                book.add_contact(name = name)
                _ = input('按回车键继续...')
            elif sem == '2':
                print('查找联系人：')
                name = input('姓名：')
                _ = book.search_contact(name = name)
                _ = input('按回车键继续...')
            elif sem == '3':
                print('删除联系人：')
                name: str = input('姓名：')
                book.del_contact(name = name)
                _ = input('按回车键继续...')
            elif sem == '4':
                print('列出所有联系人：')
                book.show_contacts()
                _ = input('按回车键继续...')
            elif sem == '5':
                print('显示当前的总联系人数量：')
                book.show_numbers()
                _ = input('按回车键继续...')
            elif sem == '6':
                book.save()
                print('退出通讯录')
                break
            else:
                print('输入错误，请重新输入')
                _ = input('按回车键继续...')
        except ValidationError as e:
            print(f'[输入错误]{e}')
            _ = input('按回车键继续...')
        except  ContactNotFoundError as e:
            print(f'[操作失败]{e}')
            _ = input('按回车键继续...')
        except KeyboardInterrupt:
            print('\n[检测到Ctrl+C，即将退出]')
            book.save()
            _ = input('按回车键继续...')
            break
        except Exception as e:
            print(f'[系统错误]发生位置错误: {type(e).__name__}: {e}')
            _ = input('按回车键继续...')

if __name__ == '__main__':
    main()