# -*- coding: utf-8 -*-
from colorama import init,Back,Fore,Style
import time
import random
import os
import platform
import re

class card:
    def __init__(self, numb, name, attr, func,istramp):
        self.name = name
        self.numb = numb
        self.attr = attr
        self.func = func
        self.istramp=istramp

class player:
    def __init__(self, symbol, name, locate, buff, hp, defense, armor, tramp, cih,armorandtramps):
        self.symbol = symbol
        self.locate = locate
        self.name = name
        self.buff = buff
        self.hp = hp
        self.moveable = False
        self.defense = defense
        self.armor = armor
        self.tramp = tramp
        self.cih = cih
        self.armorandtramps=armorandtramps


class Game:
    def isanumber(self,instr):
        numstr=re.compile('^[0-9]$')
        return re.search(numstr,instr)
    def isarangenumber(self,instr):
        numstr=re.compile('^-?[0-3]$')
        return re.search(numstr,instr)
    def __init__(self):
        if not platform.architecture()[0]=='64bit':
            print('该程序可能不适合在非64位机器上运行哦')
            if not input('你确定还要继续运行吗')=='y':
                exit()
            else:
                print('好吧，游戏体验不好可别怪我哦*罒▽罒*')
                input()
        print('\033c')
        print('欢迎来到《法术大乱斗》')
        print('创意来自传奇工作室')
        print('创新工作室出品')
        print('题材作者:天峰')
        print('开发:Lsamc')
        print('技术支持:Lrjis')
        time.sleep(2)

        init(autoreset=True)
        self.color=[Fore.LIGHTYELLOW_EX,Fore.LIGHTGREEN_EX]
        self.bgcolor=[Back.LIGHTYELLOW_EX,Back.LIGHTGREEN_EX]
        self.symbol = ['·',
                       Fore.LIGHTYELLOW_EX+'✯',
                       Fore.LIGHTGREEN_EX+'✯']
        self.max_hp = 20
        self.start_defence = 0
        
        #buff:[火焰加成，风暴加成]，冰冻，弱化，沉默，流血，霸体，助燃
        #armor:无尽剑，荼毒匕首
        #tramp:防备，地雷，光明磊落，大地之盾
        #禁卡:无尽剑，五连火球术，风刃2，1

        print('\033c', end='')
        
        self.current, self.opposite = 0, 1
        
        self.Card = [card(0, '火球术  ', 'fire', self.fireball,False),
                     card(1, '疾电闪行 ', 'storm', self.flashmove,False),
                     card(2, '火球术  ', 'fire', self.fireball,False),
                     card(3, '助燃   ', 'fire', self.Combustion,False),
                     card(4, '助燃   ', 'fire', self.Combustion,False),
                     card(5, '疾电闪行 ', 'storm', self.flashmove,False),
                     card(6, '旋风斩  ', 'hit', self.whirlwind,False),
                     card(7, '旋风斩  ', 'hit', self.whirlwind,False),
                     card(8, '火球术  ', 'fire', self.fireball,False),
                     card(9, '火球术  ', 'fire', self.fireball,False),
                     card(10, '重拳出击 ', 'hit', self.punchhard,False),
                     card(11, '冰锥   ', 'ice', self.cone,False),
                     card(12, '虚弱诅咒 ', 'dark', self.weaken,False),
                     card(13, '停战协议 ', 'buff', self.silence,False),
                     card(14, '制导打击 ', 'tech', self.tracemissle,False),
                     card(15, '传送   ', 'tech', self.portal,False),
                     card(16, '防备   ', 'nah', self.beingaware,True),
                     card(17, '地雷   ', 'tech', self.mine,True),
                     card(18, '地雷   ', 'tech', self.mine,True),
                     card(19, '火种   ', 'fire', self.kindling,False),
                     card(20, '无尽剑  ', 'armor', self.infinitesword,False),
                     card(21, '五连火球术', 'fire', self.fire_fire,False),
                     card(22, '冰刺   ', 'ice', self.icestamp,False),
                     card(23,'荼毒匕首 ','armor',self.potionknife,False),
                     card(24,'光明磊落 ','light',self.brightandshine,True),
                     card(25,'风刃 Ⅲ ','storm',self.windblade3,False),
                     card(26,'风刃 Ⅱ ','storm',self.windblade2,False),
                     card(27,'风刃 Ⅰ ','storm',self.windblade1,False),
                     card(28,'大地之盾 ','nature',self.landshield,True),
                     card(29,'大风来  ','storm',self.gale,False)]

        self.turn = 0
        self.end = False
        self.deck = []
        self.discard = []
        self.record = [Back.LIGHTMAGENTA_EX+'开始']
        
        self.bannedcard = [20, 21,26,27]
        self.toolcard=[26,27]
        
        self.board = dict()
        flag=True
        while flag:
            print(Back.LIGHTWHITE_EX+Fore.BLACK+Style.DIM+'法术大乱斗')
            flag=False
            inp=int(input('1.开始新的游戏\n2.继续以前的游戏\n3.查看存档列表\n4.清理存档\n5.退出\n'))
            if inp==5:
                exit()
            elif inp==4:
                rmname=input('你想要清除哪个存档？')
                os.system('rm ./MagicFile/'+rmname+'sys.txt')
                os.system('rm ./MagicFile/'+rmname+'pla0.txt')
                os.system('rm ./MagicFile/'+rmname+'pla1.txt')
                print('清除成功')
                input()
                print('\033c')
                flag=True
                continue
            elif inp==3:
                filename=os.listdir('./MagicFile')
                print('存档：')
                for i in filename:
                    l=len(i)
                    if i[(l-7):]=='sys.txt':
                        print(i[:(l-7)])
                print('————————')
                input()
                print('\033c')
                flag=True
                continue
            elif inp==2:
                self.gamename=input('存档名:')
                self.p = [
                player(self.symbol[1], '', (0, 0), [[0,0],0,0,0,0,0,0], self.max_hp, self.start_defence, [0,0],
                       [0, [],0,0],[],0),   
                player(self.symbol[2], '', (6,6), [[0,0],0,0,0,0,0,0], self.max_hp, self.start_defence, [0,0],
                       [0, [],0,0],[],0)]
                self.read(self.gamename)
                self.currentcard = len(self.deck)
            elif inp==1:
                self.gamename=input('本局名称:')
                flag=True
                while flag:
                    flag=False
                    if os.path.isfile('./MagicFile/'+self.gamename+'sys.txt'):
                        inp=input('该存档已存在，是否覆盖？')
                        if inp=='n':
                            self.gamename=input('输入存档名')
                            flag=True
                        
                self.p = [
                player(self.symbol[1], input(self.color[self.current]+'玩家1名字:'), (0, 0), [[0,0],0,0,0,0,0,0], self.max_hp, self.start_defence, [0,0],
                       [0, [],0,0],[],0),   
                player(self.symbol[2], input(self.color[self.opposite]+'玩家2名字:'), (6,6), [[0,0],0,0,0,0,0,0], self.max_hp, self.start_defence, [0,0],
                       [0, [],0,0],[],0)]
                self.currentcard = len(self.Card)
                for i in range(0, self.currentcard):
                    self.deck.append(i)
                random.shuffle(self.deck)
                
            
                for i in range(0, 4):
                    flag=True
                    while flag:
                        a=self.deck.pop()
                        if a in self.bannedcard:
                            self.currentcard -= 1
                            self.discard.append(a)
                            flag=True
                            continue
                        else:
                            flag=False
                        self.p[0].cih.append(a)
                        self.currentcard -= 1
                for i in range(0, 4):
                    flag=True
                    while flag:
                        a=self.deck.pop()
                        if a in self.bannedcard:
                            self.currentcard -= 1
                            self.discard.append(a)
                            flag=True
                            continue
                        else:
                            flag=False
                        self.p[1].cih.append(a)
                        self.currentcard -= 1
            else:
                print('请输入正确的数字')
                input()
                print('\033c')
                flag=True
                continue
            
        self.setback()
        print('\033c')
        print(self.bgcolor[self.current]+Fore.BLACK+'%s的回合...' % self.p[self.current].name)
        input()
        self.save(0,self.gamename)

    def introduce(self):
        print('\033c')
        print('命令：m代表移动')
        print('     p代表结束回合')
        print('     #1代表使用编号1的卡')
        print('蓝色的格点代表可以移动的地方')
        print('红色的格点代表可以攻击的地方')
        print('黄蓝两棋分别代表先后手')
        print('方向：1左上\t2上\t3右上\t')
        print('      4左\t5自己\t6右\t')
        print('      7左下\t8下\t9右下\t')
        print('其他代表取消(取消建议不输入)')
        input()

    def switchside(self):
        self.current, self.opposite = self.opposite, self.current

    def save(self,suc,name):
        if not os.path.isdir('./MagicFile'):
            if os.name=='posix':os.system('mkdir MagicFile')
            elif os.name=='nt':os.system('md MagicFile')
            else:print('你用的什么操作系统？java？')
        with open('./MagicFile/'+name+'sys.txt','w+') as savefile1:
            for i in self.deck:
                savefile1.write(str(i)+' ')
            savefile1.write(' \n')
            for i in self.discard:
                savefile1.write(str(i)+' ')
            savefile1.write(' \n')
            savefile1.write(str(self.current)+' \n')
            savefile1.write(str(self.turn)+' \n')
            for i in self.record:
                savefile1.writelines(i+' ')
            
            if suc:savefile1.write('\n'+self.p[suc-1].name)
        
        with open('./MagicFile/'+name+'pla0.txt','w+') as savefile:
            cu=self.p[0]
            
            #name, locate,  hp, defense, armor, tramp, cih,armorandtramps,buff
            #地雷
            savefile.write(' '.join([cu.name,str(cu.locate[0]),str(cu.locate[1]),str(cu.hp),str(cu.defense),str(cu.armor[0]),str(cu.armor[1]),str(cu.tramp[0])]))
            savefile.write(' \n')
            for i in cu.tramp[1]:
                savefile.write(str(i[0])+' '+str(i[1])+';')
            savefile.write(' \n')
            savefile.write(' '.join([str(cu.tramp[2]),str(cu.tramp[3])]))
            savefile.write(' \n')
            for i in cu.cih:
                savefile.write(str(i)+' ')
            savefile.write(' \n')
            
            savefile.write(' '.join([str(cu.armorandtramps),str(cu.buff[0][0]),str(cu.buff[0][1]),str(cu.buff[1]),str(cu.buff[2]),str(cu.buff[3]),str(cu.buff[4]),str(cu.buff[5]),str(cu.buff[6])]))
            savefile.write(' \n')
            
        with open('./MagicFile/'+name+'pla1.txt','w+') as savefile:
            op=self.p[1]
            savefile.write(' '.join([op.name,str(op.locate[0]),str(op.locate[1]),str(op.hp),str(op.defense),str(op.armor[0]),str(op.armor[1]),str(op.tramp[0])]))
            savefile.write(' \n')
            for i in op.tramp[1]:
                savefile.write(str(i[0])+' '+str(i[1])+';')
            savefile.write(' \n')
            savefile.write(' '.join([str(op.tramp[2]),str(op.tramp[3])]))
            savefile.write(' \n')
            for i in op.cih:
                savefile.write(str(i)+' ')
            savefile.write(' \n')
            
            savefile.write(' '.join([str(op.armorandtramps),str(op.buff[0][0]),str(op.buff[0][1]),str(op.buff[1]),str(op.buff[2]),str(op.buff[3]),str(op.buff[4]),str(op.buff[5]),str(op.buff[6])]))
            savefile.write(' \n')
            
    def read(self,name):
        if not os.path.isfile('./MagicFile/'+name+'sys.txt'):
            print('存档名错误')
            input()
            exit()
        with open('./MagicFile/'+name+'sys.txt','r') as savefile1:
            re=savefile1.readlines()
            for i in re[0].split(' '):
                if not (i=='' or i=='\n'):self.deck.append(int(i))
            for i in re[1].split(' '):
                if not (i=='' or i=='\n'):self.discard.append(int(i))
            for i in re[2].split(' '):
                if not (i=='' or i=='\n'):
                    self.current=int(i)
                    self.opposite=1-self.current
            for i in re[3].split(' '):
                if not (i=='' or i=='\n'):self.turn=int(i)
            for i in re[4].split(' '):
                if not (i=='' or i=='\n'):self.record.append(i)
            if len(re)==6:
                print('该局已经结束\n'+re[5]+'是胜者')
                input()
                exit()
        with open('./MagicFile/'+name+'pla0.txt','r') as savefile:
            cu=self.p[0]
            
            #name, locate,  hp, defense, armor, tramp, cih,armorandtramps,buff
            #地雷
            re=savefile.readlines()
            re1=re[0].split(' ')
            cu.name=re1[0]
            cu.locate=(int(re1[1]),int(re1[2]))
            cu.hp=int(re1[3])
            cu.defense=int(re1[4])
            cu.armor[0]=int(re1[5])
            cu.armor[1]=int(re1[6])
            cu.tramp[0]=int(re1[7])
            
            for i in re[1].split(';'):
                if not (i=='' or i=='\n' or i==' \n'):
                    a=i.split(' ')
                    cu.tramp[1].append((int(a[0]),int(a[1])))
             
            re2=re[2].split(' ')
            cu.tramp[2]=int(re2[0])
            cu.tramp[3]=int(re2[1])
            
            for i in re[3].split(' '):
                if not (i=='' or i=='\n'):cu.cih.append(int(i))
            re3=re[4].split(' ')
            cu.armorandtramps=int(re3[0])
            cu.buff[0][0]=int(re3[1])
            cu.buff[0][1]=int(re3[2])
            cu.buff[1]=int(re3[3])
            cu.buff[2]=int(re3[4])
            cu.buff[3]=int(re3[5])
            cu.buff[4]=int(re3[6])
            cu.buff[5]=int(re3[7])
            cu.buff[6]=int(re3[8])
            self.p[0]=cu
            
        with open('./MagicFile/'+name+'pla1.txt','r') as savefile:
            op=self.p[1]
            re=savefile.readlines()
            re1=re[0].split(' ')
            op.name=re1[0]
            op.locate=(int(re1[1]),int(re1[2]))
            op.hp=int(re1[3])
            op.defense=int(re1[4])
            op.armor[0]=int(re1[5])
            op.armor[1]=int(re1[6])
            op.tramp[0]=int(re1[7])
            
            for i in re[1].split(';'):
                if not (i=='' or i=='\n' or i==' \n'):
                    a=i.split(' ')
                    op.tramp[1].append((int(a[0]),int(a[1])))
             
            re2=re[2].split(' ')
            op.tramp[2]=int(re2[0])
            op.tramp[3]=int(re2[1])
            
            for i in re[3].split(' '):
                if not (i=='' or i=='\n'):op.cih.append(int(i))
            re3=re[4].split(' ')
            op.armorandtramps=int(re3[0])
            op.buff[0][0]=int(re3[1])
            op.buff[0][1]=int(re3[2])
            op.buff[1]=int(re3[3])
            op.buff[2]=int(re3[4])
            op.buff[3]=int(re3[5])
            op.buff[4]=int(re3[6])
            op.buff[5]=int(re3[7])
            op.buff[6]=int(re3[8])
            self.p[1]=op
            
    def startstage(self):
        if self.p[self.current] == self.p[0]:
            self.turn += 1
        if not self.p[self.current].buff[1]:
            self.p[self.current].moveable = True
        if self.currentcard <= 1:
            for i in self.discard:
                self.discard.remove(i)
                self.deck.append(i)
                self.currentcard += 1
            random.shuffle(self.deck)

        if not len(self.p[self.current].cih) >= 5:
            flag = True
            while flag:
                a = self.deck.pop()
                if not a in self.bannedcard:
                    self.p[self.current].cih.append(a)
                    self.record.append(self.color[self.current]+self.p[self.current].name + '摸了张牌')
                    flag = False
                else:
                    self.discard.append(a)
                    self.currentcard -= 1
                    continue

        else:
            a = self.deck.pop()
            self.discard.append(a)
            self.record.append(self.color[self.current]+self.p[self.current].name + '摸弃了' + self.Card[a].name)
            print('你因牌数满了，无法获得%s' % self.Card[a].name)
            input()
        self.currentcard -= 1

    def battlestage(self):
        skip = False
        while not skip:
            self.printboard()
            command = input('你的命令？')
            if command == '':
                pass
            else:
                if command=='getcard':
                    a=int(input('#'))
                    if a in range(0,len(self.Card)):
                        self.p[self.current].cih.append(a)
                elif command=='save':
                    self.save(0,self.gamename)
                    print('存档成功')
                    input()
                elif command[0] == '#':
                    if self.p[self.current].buff[3]:
                        print('你被沉默了，无法出卡')
                        input()
                    else:
                        if int(command[1:]) in self.p[self.current].cih:
                            if self.Card[int(command[1:])].func():
                                if not self.Card[int(command[1:])].istramp:
                                    self.record.append(
                                        self.color[self.current]+self.p[self.current].name + '使用' + self.Card[int(command[1:])].name)
                                else:
                                    self.record.append(self.color[self.current]+self.p[self.current].name + '设置了陷阱')
                                self.p[self.current].cih.remove(int(command[1:]))
                                if not int(command[1:]) in self.toolcard:
                                    self.discard.append(int(command[1:]))
                        else:
                            print('你没有该卡')
                            input()
                elif command[0] == 'h':
                    self.introduce()
                elif command[0] == 'r':
                    print('\033c')
                    for i in self.record:
                        print(i)
                    input()
                elif command[0] == 'm':
                    if self.p[self.current].moveable:
                        if self.move():
                            self.record.append(self.color[self.current]+self.p[self.current].name + '进行了移动')
                            self.p[self.current].moveable = False
                    else:
                        print('你不能移动了')
                        input()
                elif command[0] == 'p':
                    print('结束回合....')
                    skip = True
                    input()
                elif command[0] == 's':
                    print('你投降了...')
                    self.end = True
                    input()
                    print('\033c')
                    print(self.p[self.opposite].name + '获得了胜利✌')
                    exit()
                else:
                    print('无效命令')
                    input()

    def endstage(self):
        if self.p[self.current].buff[4]:
            self.p[self.current].hp-=1
            self.ifsuccess()
            self.p[self.current].buff[4]-=1
            self.record.append(self.color[self.current]+self.p[self.current].name+'流血')
            print('你流血了')
        
        self.p[self.current].buff = [[0,0],0,0,0,self.p[self.current].buff[4],0,0]
        
        while len(self.p[self.current].cih) > 5:
            self.printboard()
            print('你的牌需弃至五张')
            ca = input('弃置:')
            if ca[0] == '#':
                if int(ca[1:]) in self.p[self.current].cih:
                    self.p[self.current].cih.remove(int(ca[1:]))
                    self.discard.append(int(ca[1:]))
                    self.record.append(self.color[self.current]+self.p[self.current].name + '弃置' + self.Card[int(ca[1:])].name)
                else:
                    print('你没有该卡')
                    input()
            print('\033c', end='')
        self.switchside()
        print('\033c', end='')
        print(self.bgcolor[self.current]+Fore.BLACK+'%s的回合...' % self.p[self.current].name)
        self.save(0,self.gamename)
        input()

    def printboard(self):
        print('\033c', end='')
        print('回合:%d' % self.turn, end='\t')
        print('牌堆还有:%d张牌' % len(self.deck), end='\t')
        print('弃牌堆有%d张牌' % len(self.discard))
        for i in range(0, 7):
            for j in range(0, 7):
                if j == 6:
                    print(self.board[(i, j)], end='‖')
                else:
                    print(self.board[(i, j)], end='   ')

            d = len(self.record) - 14
            if d > 0:
                print(self.record[2 * i+d])
            else:
                if not (2 * i) >= len(self.record):
                    print(self.record[2 * i])
                else:
                    print()
            
            if not i==6:print('                         ‖', end='')
            else:print('对方手牌数:%d             ‖'%len(self.p[self.opposite].cih),end='')
            if d > 0:
                print(self.record[2 * i + 1+d])
            else:
                if not (2 * i + 1) >= len(self.record):
                    print(self.record[2 * i + 1])
                else:
                    print()
        

        print(self.color[self.current]+self.p[self.current].name + ':HP:%d+%d' % (self.p[self.current].hp, self.p[self.current].defense),
              end='  ')
        if self.p[self.current].buff[6]: print('助燃%d' % self.p[self.current].buff[6], end='  ')
        if self.p[self.current].buff[0][1]:print('风暴%d'%self.p[self.current].buff[0][1], end='  ')
        if self.p[self.current].buff[1]: print('冰冻', end='  ')
        if self.p[self.current].buff[2]: print('弱化%d' % self.p[self.current].buff[2], end='  ')
        if self.p[self.current].buff[4]: print('流血%d' % self.p[self.current].buff[4], end='  ')
        if self.p[self.current].buff[3]: print('沉默', end='  ')
        if self.p[self.current].buff[5]: print('霸体', end='  ')
        if self.p[self.current].armor[0]: print('无尽剑:耐久%d' % self.p[self.current].armor[0], end='  ')
        if self.p[self.current].armor[1]: print('荼毒匕首:耐久%d' % self.p[self.current].armor[1], end='  ')
        if self.p[self.current].tramp[0]: print(Fore.BLUE+'防备', end='  ')
        if self.p[self.current].tramp[2]: print(Fore.BLUE+'光明磊落', end='  ')
        if self.p[self.current].tramp[3]: print(Fore.BLUE+'大地之盾', end='  ')
        print()
        if len(self.p[self.current].tramp[1]):
            print(Fore.BLUE+'地雷', end='')
            print(self.p[self.current].tramp[1])

        print(self.color[self.opposite]+self.p[self.opposite].name + ':HP:%d+%d' % (self.p[self.opposite].hp, self.p[self.opposite].defense),
              end='  ')
        if self.p[self.opposite].buff[6]: print('助燃%d' % self.p[self.opposite].buff[6], end='  ')
        if self.p[self.opposite].buff[0][1]:print('风暴', end='  ')
        if self.p[self.opposite].buff[1]: print('冰冻', end='  ')
        if self.p[self.opposite].buff[2]: print('弱化%d' % self.p[self.opposite].buff[2], end='  ')
        if self.p[self.opposite].buff[4]: print('流血%d' % self.p[self.opposite].buff[4], end='  ')
        if self.p[self.opposite].buff[3]: print('沉默', end='  ')
        if self.p[self.opposite].buff[5]: print('霸体', end='  ')
        if self.p[self.opposite].armor[0]: print('无尽剑:耐久%d' % self.p[self.opposite].armor[0], end='  ')
        if self.p[self.opposite].armor[1]: print('荼毒匕首:耐久%d' % self.p[self.opposite].armor[1], end='  ')
        print()
        if self.p[self.current].moveable: print('当前可移动，', end='')
        print('你的手牌：')
        j = False
        for i in self.p[self.current].cih:
            if not j:
                print('#%d %s' % (i, self.Card[i].name), end='\t')
                j = True
            else:
                j = False
                print('#%d %s' % (i, self.Card[i].name))
        if j:
            print()

    def setback(self):
        for i in range(0, 7):
            for j in range(0, 7):
                self.board[(i, j)] = self.symbol[0]

        self.board[self.p[0].locate] = self.symbol[1]
        self.board[self.p[1].locate] = self.symbol[2]

    def ifsuccess(self):
        if self.p[self.opposite].hp <= 0:
            self.setback()
            self.printboard()
            print('%s倒在了地上...' % self.p[self.opposite].name)
            input()
            print('\033c')
            print('%s获得了最终的胜利✌' % self.p[self.current].name)
            self.save(self.current+1,self.gamename)
            exit()
        elif self.p[self.current].hp <= 0:
            self.setback()
            self.printboard()
            print('%s倒在了地上...' % self.p[self.current].name)
            input()
            print('\033c')
            print('%s获得了最终的胜利✌' % self.p[self.opposite].name)
            self.save(self.opposite+1,self.gamename)
            exit()
            

    def damagemake(self, damage, attr, *word):
        bu = self.p[self.current].buff
        ar = self.p[self.current].armor
        tr = self.p[self.opposite].tramp
        if damage < 0:
            if ((bu[6]) and (attr == 'fire')):
                self.p[self.current].buff[6] = 0
            if ((bu[0][1]) and (attr == 'storm')):
                pass
            if len(word):
                print(word[0])
            return 0
        else:
            if ((bu[6]) and (attr == 'fire')):
                damage += bu[6]*3
                self.p[self.current].buff[6] = 0
            if ((bu[0][1]) and (attr == 'storm')):
                damage += bu[0][1]
                
                
            if bu[2]:
                damage -= bu[2]
            
            
            if ar[0]:
                damage *= 2
                ar[0] -= 1
                if not ar[0]:
                    self.p[self.current].armorandtramps-=1
                self.p[self.current].armor = ar
            if ar[1]:
                self.p[self.opposite].buff[4]=2
                ar[1]-=1
                if self.p[self.opposite].buff[5]:
                    self.p[self.opposite].buff[4]=0
                    print(self.color[self.opposite]+'霸体免疫')
                    self.record.append(self.color[self.opposite]+self.p[self.opposite].name+'霸体免疫')
                    input()
                elif self.p[self.opposite].tramp[2]:
                    self.p[self.opposite].tramp[2]=0
                    self.record.append(self.color[self.opposite]+self.p[self.opposite].name + '光明磊落被触发')
                    print('Guang!对手陷阱光明磊落被触发，获得霸体')
                    self.p[self.opposite].armorandtramps-=1
                    self.p[self.opposite].buff[5]+=1
                    self.p[self.opposite].buff[2]=0
                    self.p[self.opposite].buff[3]=0
                    self.p[self.opposite].buff[1]=0
                    self.p[self.opposite].buff[4]=0
                    input()
                else:
                    self.record.append(self.color[self.opposite]+self.p[self.opposite].name + '流血了因为')
                    
                if not ar[1]:
                    self.p[self.current].armorandtramps-=1
                self.p[self.current].armor = ar
                
            if tr[3]:
                if damage<=6:
                    self.record.append(self.color[self.opposite]+self.p[self.opposite].name + '大地之盾减伤%d' % damage)
                    print('Duang，触发对方大地之盾，本次攻击被挡住')
                    tr[3]=0
                    input()
                    return 1
                else:
                    damage-=6
                    self.record.append(self.color[self.opposite]+self.p[self.opposite].name + '大地之盾减伤6')
                    print('Duang，触发对方大地之盾，本次攻击减免6')
                    tr[3]=0
                    input()
                    

            self.record.append(self.color[self.opposite]+self.p[self.opposite].name + '失%dHP因为' % damage)
            if not self.p[self.opposite].defense:
                self.p[self.opposite].hp -= damage
            else:
                if (self.p[self.opposite].defense >= damage):
                    self.p[self.opposite].defense -= damage
                else:
                    self.p[self.opposite].hp -= (damage - self.p[self.opposite].defense)
                    self.p[self.opposite].defense = 0
            if len(word):
                print(word[1])
            self.ifsuccess()
            return 1

    def move(self):
        loc = self.p[self.current].locate
        for i in range(loc[0] - 1, loc[0] + 2):
            for j in range(loc[1] - 1, loc[1] + 2):
                if ((i in range(0, 7)) and (j in range(0, 7)) and (not (loc == self.p[self.opposite].locate))):
                    self.board[(i, j)] = Fore.LIGHTCYAN_EX+self.board[(i, j)]
        self.board[loc] = self.p[self.current].symbol
        self.printboard()
        print('移动中...')
        dire = input('方向？')
        if not self.isanumber(dire):
            self.setback()
            return 0
        dire = int(dire)
        self.setback()
        if dire == 0:
            return 0
        loc = list(loc)
        if os.name=='posix':
            if dire in (1, 4, 7): loc[1] -= 1
            if dire in (3, 6, 9): loc[1] += 1
            if dire in (1, 2, 3): loc[0] -= 1
            if dire in (7, 8, 9): loc[0] += 1
        elif os.name=='nt':
            if dire in (1, 4, 7): loc[1] -= 1
            if dire in (3, 6, 9): loc[1] += 1
            if dire in (7,8,9): loc[0] -= 1
            if dire in (1,2,3): loc[0] += 1
        loc = tuple(loc)
        if ((loc[0] in range(0, 7)) and (loc[1] in range(0, 7)) and (not (loc == self.p[self.opposite].locate))):
            self.p[self.current].locate = loc
            if self.p[self.opposite].tramp[0]:
                print('咔哒，触发对方陷阱:防备')
                print('对方护甲增加')
                self.record.append(self.color[self.current]+self.p[self.current].name+'触发'+self.p[self.opposite].name+'防备')
                self.p[self.opposite].defense += 4
                self.p[self.opposite].tramp[0] = 0
                self.p[self.opposite].armorandtramps-=1
                input()
            if (loc in self.p[self.opposite].tramp[1]):
                print('咔，轰！')
                print('你中了对方的暗雷！')
                self.record.append(self.color[self.current]+self.p[self.current].name+'中了'+self.p[self.opposite].name+'的雷')
                damage=5
                if self.p[self.current].tramp[3]:
                    self.record.append(self.color[self.current]+self.p[self.current].name + '大地之盾减伤%d' % damage)
                    print('Duang，触发己方大地之盾，本次攻击被挡住')
                    self.p[self.current].tramp[3]=0
                    self.p[self.opposite].tramp[1].remove(loc)
                    self.p[self.opposite].armorandtramps-=1
                    input()
                    return 1
                if not self.p[self.current].defense:
                    self.p[self.current].hp -= damage
                else:
                    if (self.p[self.current].defense >= damage):
                        self.p[self.current].defense -= damage
                    else:
                        self.p[self.current].hp -= (damage - self.p[self.current].defense)
                        self.p[self.current].defense = 0
                self.record.append(self.color[self.current]+self.p[self.current].name+'中了雷失%dHP'%damage)
                self.p[self.opposite].tramp[1].remove(loc)
                self.p[self.opposite].armorandtramps-=1
                self.ifsuccess()
                input()
            self.setback()
            return 1
        else:
            return 0

    def fireball(self):
        damage = -1
        ran=4
        loc = self.p[self.current].locate
        for i in range(loc[0] - ran, loc[0] + ran+1):
            if i in range(0, 7):
                if self.board[(i, loc[1])] == self.p[self.opposite].symbol: self.board[
                    (i, loc[1])] = Back.LIGHTRED_EX+self.p[self.opposite].symbol
                self.board[(i, loc[1])] = Fore.LIGHTRED_EX+self.board[i, loc[1]]
        for i in range(loc[1] - ran, loc[1] + ran+1):
            if i in range(0, 7):
                if self.board[(loc[0], i)] == self.p[self.opposite].symbol: self.board[
                    (loc[0], i)] = Back.LIGHTRED_EX+self.p[self.opposite].symbol
                self.board[(loc[0], i)] = Fore.LIGHTRED_EX+self.board[loc[0], i]
        self.board[loc] = self.p[self.current].symbol
        self.printboard()
        print('火球术！')
        dire = input('方向:')
        if not self.isanumber(dire):
            self.setback()
            return 0
        dire = int(dire)
        if ((dire == 2 and os.name=='posix')or(dire==8 and os.name=='nt')):
            if ((self.p[self.opposite].locate[1] == loc[1]) and (
                    self.p[self.opposite].locate[0] in range(loc[0] - ran, loc[0]))):
                damage = 3
        elif dire == 4:
            if ((self.p[self.opposite].locate[0] == loc[0]) and (
                    self.p[self.opposite].locate[1] in range(loc[1] - ran, loc[1]))):
                damage = 3
        elif ((dire == 8 and os.name=='posix')or(dire==2 and os.name=='nt')):
            if ((self.p[self.opposite].locate[1] == loc[1]) and (
                    self.p[self.opposite].locate[0] in range(loc[0] + 1, loc[0] + ran+1))):
                damage = 3
        elif dire == 6:
            if ((self.p[self.opposite].locate[0] == loc[0]) and (
                    self.p[self.opposite].locate[1] in range(loc[1] + 1, loc[1] + ran+1))):
                damage = 3
        else:
            self.setback()
            return 0

        self.damagemake(damage, 'fire')
        self.setback()
        return 1

    def Combustion(self):
        self.p[self.current].buff[6] += 1
        self.printboard()
        print('获得助燃buff')
        input()
        return 1

    def flashmove(self):
        if self.p[self.current].buff[1]:
            print('你被冻住了不能动')
            input()
            return 0
        loc = self.p[self.current].locate
        for i in range(loc[0] - 2, loc[0] + 3):
            if ((i in range(0, 7))and(not (i,loc[1]) in [self.p[0].locate,self.p[1].locate])):
                self.board[(i, loc[1])] = Fore.LIGHTCYAN_EX+self.board[i, loc[1]]
        for i in range(loc[1] - 2, loc[1] + 3):
            if ((i in range(0, 7))and(not (loc[0],i) in [self.p[0].locate,self.p[1].locate])):
                self.board[(loc[0], i)] = Fore.LIGHTCYAN_EX+self.board[loc[0], i]
        self.board[loc] = self.p[self.current].symbol
        self.printboard()
        print('闪现！')

        dire = input('方向:')
        dis = input('距离:')
        if not((self.isanumber(dire)) and (self.isanumber(dis))):
            self.setback()
            return 0
        dire, dis = int(dire), int(dis)
        if not dis in range(1, 3):
            print('距离过长')
            self.setback()
            input()
            return 0
        loc = list(loc)
        if ((dire == 2 and os.name=='posix')or(dire==8 and os.name=='nt')):
            loc[0] -= dis
        elif dire == 4:
            loc[1] -= dis
        elif ((dire == 8 and os.name=='posix')or(dire==2 and os.name=='nt')):
            loc[0] += dis
        elif dire == 6:
            loc[1] += dis
        else:
            self.setback()
            return 0
        loc = tuple(loc)
        if ((loc[0] in range(0, 7)) and (loc[1] in range(0, 7)) and (not (loc == self.p[self.opposite].locate))):
            self.p[self.current].locate = loc
            if (loc in self.p[self.opposite].tramp[1]):
                print('咔，轰！')
                print('你中了对方的暗雷！')
                self.record.append(self.color[self.current]+self.p[self.current].name+'中了'+self.p[self.opposite].name+'的雷')
                damage=5
                if self.p[self.current].tramp[3]:
                    self.record.append(self.color[self.current]+self.p[self.current].name + '大地之盾减伤%d' % damage)
                    print('Duang，触发己方大地之盾，本次攻击被挡住')
                    self.p[self.current].tramp[3]=0
                    self.p[self.opposite].tramp[1].remove(loc)
                    self.p[self.opposite].armorandtramps-=1
                    input()
                    return 1
                    
            
                self.p[self.current].hp -= damage
                self.record.append(self.color[self.current]+self.p[self.current].name+'中了雷失%dHP'%damage)
                self.p[self.opposite].tramp[1].remove(loc)
                self.p[self.opposite].armorandtramps-=1
                self.ifsuccess()
                input()
            self.p[self.current].buff[0][1] += 1
            self.setback()
            return 1
        else:
            self.setback()
            return 0

    def whirlwind(self):
        damage = -1
        loc = self.p[self.current].locate
        for i in range(loc[0] - 1, loc[0] + 2):
            for j in range(loc[1] - 1, loc[1] + 2):
                if ((i in range(0, 7)) and (j in range(0, 7))):
                    if self.board[(i, j)] == self.p[self.opposite].symbol:
                        damage = 2
                        self.board[(i, j)] = Back.LIGHTRED_EX+self.p[self.opposite].symbol
                    else:self.board[(i, j)] = Fore.LIGHTRED_EX+self.board[(i, j)]
        self.board[loc] = self.p[self.current].symbol
        self.printboard()
        print('旋风斩！')

        self.damagemake(damage, 'hit')
        self.damagemake(damage, 'hit')
        input()
        self.setback()
        return 1

    def cone(self):
        damage = -1
        ran=3
        loc = self.p[self.current].locate
        for i in range(loc[0] - ran, loc[0] + ran+1):
            if i in range(0, 7):
                if self.board[(i, loc[1])] == self.p[self.opposite].symbol: self.board[
                    (i, loc[1])] = Back.LIGHTRED_EX+self.p[self.opposite].symbol
                self.board[(i, loc[1])] = Fore.LIGHTRED_EX+self.board[i, loc[1]]
        for i in range(loc[1] - ran, loc[1] + ran+1):
            if i in range(0, 7):
                if self.board[(loc[0], i)] == self.p[self.opposite].symbol: self.board[
                    (loc[0], i)] = Back.LIGHTRED_EX+self.p[self.opposite].symbol
                self.board[(loc[0], i)] = Fore.LIGHTRED_EX+self.board[loc[0], i]
        self.board[loc] = self.p[self.current].symbol
        self.printboard()
        print('冰锥！')
        dire = input('方向:')
        if not self.isanumber(dire):
            self.setback()
            return 0
        dire = int(dire)
        if ((dire == 2 and os.name=='posix')or(dire==8 and os.name=='nt')):
            if ((self.p[self.opposite].locate[1] == loc[1]) and (
                    self.p[self.opposite].locate[0] in range(loc[0] - ran, loc[0]))):
                damage = 1
        elif dire == 4:
            if ((self.p[self.opposite].locate[0] == loc[0]) and (
                    self.p[self.opposite].locate[1] in range(loc[1] - ran, loc[1]))):
                damage = 1
        elif ((dire == 8 and os.name=='posix')or(dire==2 and os.name=='nt')):
            if ((self.p[self.opposite].locate[1] == loc[1]) and (
                    self.p[self.opposite].locate[0] in range(loc[0] + 1, loc[0] + ran+1))):
                damage = 1
        elif dire == 6:
            if ((self.p[self.opposite].locate[0] == loc[0]) and (
                    self.p[self.opposite].locate[1] in range(loc[1] + 1, loc[1] + ran+1))):
                damage = 1
        else:
            self.setback()
            return 0

        if self.damagemake(damage, 'buff'):
            self.p[self.opposite].buff[1] = 1
            if self.p[self.opposite].buff[5]:
                self.p[self.opposite].buff[1]=0
                print(self.color[self.opposite]+'霸体免疫')
                self.record.append(self.color[self.opposite]+self.p[self.opposite].name+'霸体免疫')
                input()
            elif self.p[self.opposite].tramp[2]:
                self.p[self.opposite].tramp[2]=0
                self.record.append(self.color[self.opposite]+self.p[self.opposite].name + '光明磊落被触发')
                print('Guang!对手陷阱光明磊落被触发，获得霸体')
                self.p[self.opposite].armorandtramps-=1
                self.p[self.opposite].buff[5]+=1
                self.p[self.opposite].buff[2]=0
                self.p[self.opposite].buff[3]=0
                self.p[self.opposite].buff[1]=0
                self.p[self.opposite].buff[4]=0
                input()
            else:self.record.append(self.color[self.opposite]+self.p[self.opposite].name + '被冰冻了因为')

        self.setback()
        return 1

    def weaken(self):
        print('弱化！')
        self.p[self.opposite].buff[2] += 1
        if self.p[self.opposite].buff[5]:
            self.p[self.opposite].buff[2]=0
            print(self.color[self.opposite]+'霸体免疫')
            self.record.append(self.color[self.opposite]+self.p[self.opposite].name+'霸体免疫')
            input()
        elif self.p[self.opposite].tramp[2]:
            self.p[self.opposite].tramp[2]=0
            self.record.append(self.color[self.opposite]+self.p[self.opposite].name + '光明磊落被触发')
            print('Guang!对手陷阱光明磊落被触发，获得霸体')
            self.p[self.opposite].armorandtramps-=1
            self.p[self.opposite].buff[5]+=1
            self.p[self.opposite].buff[2]=0
            self.p[self.opposite].buff[3]=0
            self.p[self.opposite].buff[1]=0
            self.p[self.opposite].buff[4]=0
            input()
        else:
            self.record.append(self.color[self.opposite]+self.p[self.opposite].name + '被弱化了因为')
        return 1

    def silence(self):
        print('停战！')
        self.p[self.current].buff[3] = 1
        self.p[self.opposite].buff[3] = 1
        if self.p[self.opposite].buff[5]:
            self.p[self.opposite].buff[4]=0
            print(self.color[self.opposite]+'霸体免疫')
            self.record.append(self.color[self.opposite]+self.p[self.opposite].name+'霸体免疫')
            input()
        elif self.p[self.opposite].tramp[2]:
            self.p[self.opposite].tramp[2]=0
            self.record.append(self.color[self.opposite]+self.p[self.opposite].name + '光明磊落被触发')
            print('Guang!对手陷阱光明磊落被触发，获得霸体')
            self.p[self.opposite].armorandtramps-=1
            self.p[self.opposite].buff[5]+=1
            self.p[self.opposite].buff[2]=0
            self.p[self.opposite].buff[3]=0
            self.p[self.opposite].buff[1]=0
            self.p[self.opposite].buff[4]=0
            input()
        else:
            self.record.append('大家被沉默因为')

        return 1

    def tracemissle(self):
        damage = -1
        loc = self.p[self.current].locate
        for i in range(loc[0] - 3, loc[0] + 4):
            for j in range(loc[1] - 3, loc[1] + 4):
                if ((i in range(0, 7)) and (j in range(0, 7))):
                    if self.board[(i, j)] == self.p[self.opposite].symbol: 
                        self.board[(i, j)] = Back.LIGHTRED_EX+self.p[self.opposite].symbol
                    self.board[(i, j)] = Fore.LIGHTRED_EX+self.board[(i, j)]
        self.board[loc] = self.p[self.current].symbol
        self.printboard()

        print('追踪导弹！')
        dx = input('输入增量行')
        dy = input('输入增量列')
        if ((self.isarangenumber(dx)) and (self.isarangenumber(dy))):
            dx, dy = int(dx), int(dy)
            if ((dx in range(-3, 4)) and (dx in range(-3, 4))):
                if ((loc[0] + dx, loc[1] + dy) == self.p[self.opposite].locate):
                    damage = 3
            else:
                self.setback()
                return 0
        else:
            self.setback()
            return 0
        self.damagemake(damage, 'hit', '啪叽', '轰！')
        input()
        self.setback()
        return 1

    def portal(self):
        if self.p[self.current].buff[1]:
            print('你被冻住了不能动')
            input()
            return 0
        loc = self.p[self.current].locate
        for i in range(loc[0] - 3, loc[0] + 4):
            for j in range(loc[1] - 3, loc[1] + 4):
                if ((i in range(0, 7)) and (j in range(0, 7)) and (not (loc == self.p[self.opposite].locate))):
                    self.board[(i, j)] = Fore.LIGHTCYAN_EX+self.board[(i, j)]
        self.board[loc] = self.p[self.current].symbol
        self.printboard()

        print('传送！')
        dx = input('输入增量行')
        dy = input('输入增量列')
        if ((self.isarangenumber(dx)) and (self.isarangenumber(dy))):
            dx, dy = int(dx), int(dy)
            if ((dx in range(-3, 4)) and (dx in range(-3, 4))):
                loc = list(loc)
                loc[0] += dx
                loc[1] += dy
                loc = tuple(loc)
                if not loc == self.p[self.opposite].locate:
                    self.p[self.current].locate = loc
                    if (loc in self.p[self.opposite].tramp[1]):
                        print('咔，轰！')
                        print('你中了对方的暗雷！')
                        self.record.append(self.color[self.current]+self.p[self.current].name+'中了'+self.p[self.opposite].name+'的雷')
                        damage=5
                        if self.p[self.current].tramp[3]:
                            self.record.append(self.color[self.current]+self.p[self.current].name + '大地之盾减伤%d' % damage)
                            print('Duang，触发己方大地之盾，本次攻击被挡住')
                            self.p[self.current].tramp[3]=0
                            self.p[self.opposite].tramp[1].remove(loc)
                            self.p[self.opposite].armorandtramps-=1
                            input()
                            return 1
                            
                        self.p[self.current].hp -= damage
                        self.record.append(self.color[self.current]+self.p[self.current].name+'中了雷失%dHP'%damage)
                        self.p[self.opposite].tramp[1].remove(loc)
                        self.p[self.opposite].armorandtramps-=1
                        self.ifsuccess()
                        input()
                    self.setback()
                    return 1
                else:
                    self.setback()
                    return 0
            else:
                self.setback()
                return 0
        else:
            self.setback()
            return 0

    def beingaware(self):
        if self.p[self.current].armorandtramps>=5:
            print('你的陷阱和武器已达上限')
            input()
            return 0
        self.p[self.current].armorandtramps+=1
        self.p[self.current].tramp[0] = 1
        return 1

    def mine(self):#暂不允许叠雷
        if self.p[self.current].armorandtramps>=5:
            print('你的陷阱和武器已达上限')
            input()
            return 0
        loc = self.p[self.current].locate
        for i in range(loc[0] - 3, loc[0] + 4):
            for j in range(loc[1] - 3, loc[1] + 4):
                if ((i in range(0, 7)) and (j in range(0, 7))):
                    self.board[(i, j)] = Fore.LIGHTRED_EX+self.board[(i, j)]
        self.board[loc] = self.p[self.current].symbol
        self.printboard()
        print('地雷！')
        dx = input('输入增量行')
        dy = input('输入增量列')
        if ((self.isarangenumber(dx)) and (self.isarangenumber(dy))):
            dx, dy = int(dx), int(dy)
            if not ((dx in range(-3, 4)) and (dy in range(-3, 4))):
                self.setback()
                return 0
            loc = list(loc)
            loc[0] += dx
            loc[1] += dy
            loc = tuple(loc)
            self.setback()
            if ((loc[0] in range(0, 7)) and (loc[1] in range(0, 7)) and (not loc == self.p[self.opposite].locate) and (
                    not loc == self.p[self.current].locate)and(not loc in self.p[self.current].tramp[1])):
                self.p[self.current].tramp[1].append(loc)
                for i in self.p[self.current].tramp[1]:
                    self.board[i] = Fore.LIGHTRED_EX+self.board[i]

                print('\033c')
                self.printboard()
                self.p[self.current].armorandtramps+=1
                print('请查看地雷位置')
                input()
                self.setback()
                return 1
            else:
                return 0
        else:
            self.setback()
            return 0

    def infinitesword(self):
        if self.p[self.current].armorandtramps>=5:
            print('你的陷阱和武器已达上限')
            input()
            return 0
        self.p[self.current].armorandtramps+=1
        self.p[self.current].armor[0] = 3
        print('已装备无尽剑!')
        return 1

    def fire_fire(self):
        damage = -1
        ran=4
        loc = self.p[self.current].locate
        for i in range(loc[0] - ran, loc[0] + ran+1):
            if i in range(0, 7):
                if self.board[(i, loc[1])] == self.p[self.opposite].symbol: self.board[
                    (i, loc[1])] = Back.LIGHTRED_EX+self.p[self.opposite].symbol
                self.board[(i, loc[1])] = Fore.LIGHTRED_EX+self.board[i, loc[1]]
        for i in range(loc[1] - ran, loc[1] + ran+1):
            if i in range(0, 7):
                if self.board[(loc[0], i)] == self.p[self.opposite].symbol: self.board[
                    (loc[0], i)] = Back.LIGHTRED_EX+self.p[self.opposite].symbol
                self.board[(loc[0], i)] = Fore.LIGHTRED_EX+self.board[loc[0], i]
        self.board[loc] = self.p[self.current].symbol
        self.printboard()
        print('五连火球术！')
        dire = input('方向:')
        if not self.isanumber(dire):
            self.setback()
            return 0
        dire = int(dire)
        if ((dire == 2 and os.name=='posix')or(dire==8 and os.name=='nt')):
            if ((self.p[self.opposite].locate[1] == loc[1]) and (
                    self.p[self.opposite].locate[0] in range(loc[0] - ran, loc[0]))):
                damage = 3
        elif dire == 4:
            if ((self.p[self.opposite].locate[0] == loc[0]) and (
                    self.p[self.opposite].locate[1] in range(loc[1] - ran, loc[1]))):
                damage = 3
        elif ((dire == 8 and os.name=='posix')or(dire==2 and os.name=='nt')):
            if ((self.p[self.opposite].locate[1] == loc[1]) and (
                    self.p[self.opposite].locate[0] in range(loc[0] + 1, loc[0] + ran+1))):
                damage = 3
        elif dire == 6:
            if ((self.p[self.opposite].locate[0] == loc[0]) and (
                    self.p[self.opposite].locate[1] in range(loc[1] + 1, loc[1] + ran+1))):
                damage = 3
        else:
            self.setback()
            return 0

        if damage > 0:
            damage = len(self.p[self.current].cih) - 1
            self.damagemake(damage, 'fire')
        self.setback()
        return 1

    def kindling(self):
        flag = True
        while flag:
            again = True
            if self.currentcard <= 1:
                for i in self.discard:
                    self.discard.remove(i)
                    self.deck.append(i)
                    self.currentcard += 1
                    random.shuffle(self.deck)
            while again:
                a = self.deck.pop()
                if a in self.bannedcard:
                    self.discard.append(a)
                    self.currentcard -= 1
                    continue
                else:
                    again = False
                    self.p[self.current].cih.append(a)
                    if self.Card[a].attr == 'fire':
                        flag = True
                        
                    else:
                        flag = False
                    self.currentcard -= 1
                print('你摸到了%s' % self.Card[a].name, end='')
                self.record.append(self.color[self.current]+self.p[self.current].name + '摸到了' + self.Card[a].name)
                input()
            
        return 1

    def icestamp(self):
        damage = -1
        ran=2
        loc = self.p[self.current].locate
        for i in range(loc[0] - ran, loc[0] + ran+1):
            if i in range(0, 7):
                if self.board[(i, loc[1])] == self.p[self.opposite].symbol: self.board[
                    (i, loc[1])] = Back.LIGHTRED_EX+self.p[self.opposite].symbol
                self.board[(i, loc[1])] = Fore.LIGHTRED_EX+self.board[i, loc[1]]
        for i in range(loc[1] - ran, loc[1] + ran+1):
            if i in range(0, 7):
                if self.board[(loc[0], i)] == self.p[self.opposite].symbol: self.board[
                    (loc[0], i)] = Back.LIGHTRED_EX+self.p[self.opposite].symbol
                self.board[(loc[0], i)] = Fore.LIGHTRED_EX+self.board[loc[0], i]
        self.board[loc] = self.p[self.current].symbol
        self.printboard()
        print('冰刺！')
        dire = input('方向:')
        if not self.isanumber(dire):
            self.setback()
            return 0
        dire = int(dire)
        if ((dire == 2 and os.name=='posix')or(dire==8 and os.name=='nt')):
            if ((self.p[self.opposite].locate[1] == loc[1]) and (
                    self.p[self.opposite].locate[0] in range(loc[0] - ran, loc[0]))):
                damage = 2
        elif dire == 4:
            if ((self.p[self.opposite].locate[0] == loc[0]) and (
                    self.p[self.opposite].locate[1] in range(loc[1] - ran, loc[1]))):
                damage = 2
        elif ((dire == 8 and os.name=='posix')or(dire==2 and os.name=='nt')):
            if ((self.p[self.opposite].locate[1] == loc[1]) and (
                    self.p[self.opposite].locate[0] in range(loc[0] + 1, loc[0] + ran+1))):
                damage = 2
        elif dire == 6:
            if ((self.p[self.opposite].locate[0] == loc[0]) and (
                    self.p[self.opposite].locate[1] in range(loc[1] + 1, loc[1] + ran+1))):
                damage = 2
        else:
            self.setback()
            return 0

        if self.damagemake(damage, 'ice'):
            if self.p[self.opposite].buff[1]:
                oppoloc=list(self.p[self.opposite].locate)
                self.p[self.opposite].hp -= 5
                if ((((dire == 2 and os.name=='posix')or(dire==8 and os.name=='nt'))) and (self.p[self.opposite].locate[0] > 0)):
                    oppoloc[0] -= 1
                elif ((dire == 4) and (self.p[self.opposite].locate[1] > 0)):
                    oppoloc[1] -= 1
                elif ((dire == 6) and (self.p[self.opposite].locate[1] < 6)):
                    oppoloc[1] += 1
                elif ((((dire == 8 and os.name=='posix')or(dire==2 and os.name=='nt'))) and (self.p[self.opposite].locate[0] < 6)):
                    oppoloc[0] += 1
                self.p[self.opposite].locate=tuple(oppoloc)
                self.setback()
                self.printboard()
                print('破冰！')
                self.record.append(self.color[self.opposite]+self.p[self.opposite].name + '被破冰')
                input()
            else:self.setback()
        else:
            self.setback()
        return 1

    def potionknife(self):
        if self.p[self.current].armorandtramps>=5:
            print('你的陷阱和武器已达上限')
            input()
            return 0
        self.p[self.current].armorandtramps+=1
        self.p[self.current].armor[1]=4
        print('已装备荼毒匕首！')
        return 1
    
    def brightandshine(self):
        if self.p[self.current].armorandtramps>=5:
            print('你的陷阱和武器已达上限')
            input()
            return 0
        self.p[self.current].armorandtramps+=1
        self.p[self.current].tramp[2]=1
        return 1
    
    def windblade3(self):#风刃打两根还是三格？
        damage = -1
        ran=2
        loc = self.p[self.current].locate
        for i in range(loc[0] - ran, loc[0] + ran+1):
            if i in range(0, 7):
                if self.board[(i, loc[1])] == self.p[self.opposite].symbol: self.board[
                    (i, loc[1])] = Back.LIGHTRED_EX+self.p[self.opposite].symbol
                self.board[(i, loc[1])] = Fore.LIGHTRED_EX+self.board[i, loc[1]]
        for i in range(loc[1] - ran, loc[1] + ran+1):
            if i in range(0, 7):
                if self.board[(loc[0], i)] == self.p[self.opposite].symbol: self.board[
                    (loc[0], i)] = Back.LIGHTRED_EX+self.p[self.opposite].symbol
                self.board[(loc[0], i)] = Fore.LIGHTRED_EX+self.board[loc[0], i]
        self.board[loc] = self.p[self.current].symbol
        self.printboard()
        print('风刃！')
        dire = input('方向:')
        if not self.isanumber(dire):
            self.setback()
            return 0
        dire = int(dire)
        if ((dire == 2 and os.name=='posix')or(dire==8 and os.name=='nt')):
            if ((self.p[self.opposite].locate[1] == loc[1]) and (
                    self.p[self.opposite].locate[0] in range(loc[0] - ran, loc[0]))):
                damage = 1
        elif dire == 4:
            if ((self.p[self.opposite].locate[0] == loc[0]) and (
                    self.p[self.opposite].locate[1] in range(loc[1] - ran, loc[1]))):
                damage = 1
        elif ((dire == 8 and os.name=='posix')or(dire==2 and os.name=='nt')):
            if ((self.p[self.opposite].locate[1] == loc[1]) and (
                    self.p[self.opposite].locate[0] in range(loc[0] + 1, loc[0] + ran+1))):
                damage = 1
        elif dire == 6:
            if ((self.p[self.opposite].locate[0] == loc[0]) and (
                    self.p[self.opposite].locate[1] in range(loc[1] + 1, loc[1] + ran+1))):
                damage = 1
        else:
            self.setback()
            return 0
        
        self.damagemake(damage,'storm')
        self.p[self.current].cih.append(26)
        self.setback()
        return 1
    def windblade2(self):#风刃打两根还是三格？
        damage = -1
        ran=2
        loc = self.p[self.current].locate
        for i in range(loc[0] - ran, loc[0] + ran+1):
            if i in range(0, 7):
                if self.board[(i, loc[1])] == self.p[self.opposite].symbol: self.board[
                    (i, loc[1])] = Back.LIGHTRED_EX+self.p[self.opposite].symbol
                self.board[(i, loc[1])] = Fore.LIGHTRED_EX+self.board[i, loc[1]]
        for i in range(loc[1] - ran, loc[1] + ran+1):
            if i in range(0, 7):
                if self.board[(loc[0], i)] == self.p[self.opposite].symbol: self.board[
                    (loc[0], i)] = Back.LIGHTRED_EX+self.p[self.opposite].symbol
                self.board[(loc[0], i)] = Fore.LIGHTRED_EX+self.board[loc[0], i]
        self.board[loc] = self.p[self.current].symbol
        self.printboard()
        print('风刃！')
        dire = input('方向:')
        if not self.isanumber(dire):
            self.setback()
            return 0
        dire = int(dire)
        if ((dire == 2 and os.name=='posix')or(dire==8 and os.name=='nt')):
            if ((self.p[self.opposite].locate[1] == loc[1]) and (
                    self.p[self.opposite].locate[0] in range(loc[0] - ran, loc[0]))):
                damage = 1
        elif dire == 4:
            if ((self.p[self.opposite].locate[0] == loc[0]) and (
                    self.p[self.opposite].locate[1] in range(loc[1] - ran, loc[1]))):
                damage = 1
        elif ((dire == 8 and os.name=='posix')or(dire==2 and os.name=='nt')):
            if ((self.p[self.opposite].locate[1] == loc[1]) and (
                    self.p[self.opposite].locate[0] in range(loc[0] + 1, loc[0] + ran+1))):
                damage = 1
        elif dire == 6:
            if ((self.p[self.opposite].locate[0] == loc[0]) and (
                    self.p[self.opposite].locate[1] in range(loc[1] + 1, loc[1] + ran+1))):
                damage = 1
        else:
            self.setback()
            return 0
        
        self.damagemake(damage,'storm')
        self.p[self.current].cih.append(27)
        self.setback()
        return 1
    def windblade1(self):
        damage = -1
        ran=2
        loc = self.p[self.current].locate
        for i in range(loc[0] - ran, loc[0] + ran+1):
            if i in range(0, 7):
                if self.board[(i, loc[1])] == self.p[self.opposite].symbol: self.board[
                    (i, loc[1])] = Back.LIGHTRED_EX+self.p[self.opposite].symbol
                self.board[(i, loc[1])] = Fore.LIGHTRED_EX+self.board[i, loc[1]]
        for i in range(loc[1] - ran, loc[1] + ran+1):
            if i in range(0, 7):
                if self.board[(loc[0], i)] == self.p[self.opposite].symbol: self.board[
                    (loc[0], i)] = Back.LIGHTRED_EX+self.p[self.opposite].symbol
                self.board[(loc[0], i)] = Fore.LIGHTRED_EX+self.board[loc[0], i]
        self.board[loc] = self.p[self.current].symbol
        self.printboard()
        print('风刃！')
        dire = input('方向:')
        if not self.isanumber(dire):
            self.setback()
            return 0
        dire = int(dire)
        if ((dire == 2 and os.name=='posix')or(dire==8 and os.name=='nt')):
            if ((self.p[self.opposite].locate[1] == loc[1]) and (
                    self.p[self.opposite].locate[0] in range(loc[0] - ran, loc[0]))):
                damage = 1
        elif dire == 4:
            if ((self.p[self.opposite].locate[0] == loc[0]) and (
                    self.p[self.opposite].locate[1] in range(loc[1] - ran, loc[1]))):
                damage = 1
        elif ((dire == 8 and os.name=='posix')or(dire==2 and os.name=='nt')):
            if ((self.p[self.opposite].locate[1] == loc[1]) and (
                    self.p[self.opposite].locate[0] in range(loc[0] + 1, loc[0] + ran+1))):
                damage = 1
        elif dire == 6:
            if ((self.p[self.opposite].locate[0] == loc[0]) and (
                    self.p[self.opposite].locate[1] in range(loc[1] + 1, loc[1] + ran+1))):
                damage = 1
        else:
            self.setback()
            return 0
        
        self.damagemake(damage,'storm')
        self.setback()
        return 1
      
    def landshield(self):
        if self.p[self.current].armorandtramps>=5:
            print('你的陷阱和武器已达上限')
            input()
            return 0
        self.p[self.current].armorandtramps+=1
        self.p[self.current].tramp[3] = 1
        return 1
    
    def gale(self):
        name=input('选择目标？')
        target=0
        if name==self.p[self.current].name:target=self.current
        elif name==self.p[self.opposite].name:target=self.opposite
        else:
            return 0
        
        loc = self.p[target].locate
        ran=1
        for i in range(loc[0] - ran, loc[0] + ran+1):
            if ((i in range(0, 7))and(not (i,loc[1]) in [self.p[self.current].locate,self.p[self.opposite].locate])):
                self.board[(i, loc[1])] = Fore.LIGHTCYAN_EX+self.board[i, loc[1]]
        for i in range(loc[1] - ran, loc[1] + ran+1):
            if ((i in range(0, 7))and(not (i,loc[1]) in [self.p[self.current].locate,self.p[self.opposite].locate])):
                self.board[(loc[0], i)] = Fore.LIGHTCYAN_EX+self.board[loc[0], i]
        self.printboard()
        print('大风来！')
        
        
        dire = input('方向:')
        dis = 1
        if not self.isanumber(dire):
            self.setback()
            return 0
        dire = int(dire)
        loc = list(loc)
        if ((dire == 2 and os.name=='posix')or(dire==8 and os.name=='nt')):
            loc[0] -= dis
        elif dire == 4:
            loc[1] -= dis
        elif ((dire == 8 and os.name=='posix')or(dire==2 and os.name=='nt')):
            loc[0] += dis
        elif dire == 6:
            loc[1] += dis
        else:
            self.setback()
            return 0
        loc = tuple(loc)
        if ((loc[0] in range(0, 7)) and (loc[1] in range(0, 7)) and (not loc == self.p[self.opposite].locate) and (not loc == self.p[self.current].locate)):
            
            self.p[target].locate = loc
            if target==self.current:
                if loc in self.p[self.opposite].tramp[1]:
                    print('咔，轰！')
                    print('你中了对方的暗雷！')
                    self.record.append(self.color[self.current]+self.p[self.current].name+'中了'+self.p[self.opposite].name+'的雷')
                    damage=5
                    if self.p[self.current].tramp[3]:
                        self.record.append(self.color[self.current]+self.p[self.current].name + '大地之盾减伤%d' % damage)
                        print('Duang，触发己方大地之盾，本次攻击被挡住')
                        self.p[self.current].tramp[3]=0
                        self.p[self.opposite].tramp[1].remove(loc)
                        self.p[self.opposite].armorandtramps-=1
                        input()
                        return 1
                        
                
                    if not self.p[self.current].defense:
                        self.p[self.current].hp -= damage
                    else:
                        if (self.p[self.current].defense >= damage):
                            self.p[self.current].defense -= damage
                        else:
                            self.p[self.current].hp -= (damage - self.p[self.current].defense)
                            self.p[self.current].defense = 0
                    self.record.append(self.color[self.current]+self.p[self.current].name+'中了雷失%dHP'%damage)
                    
                    self.p[self.opposite].tramp[1].remove(loc)
                    self.p[self.opposite].armorandtramps-=1
                    self.ifsuccess()
                    input()
            if target==self.opposite:
                if loc in self.p[self.current].tramp[1]:
                    print('咔，轰！')
                    print('对方中了你的暗雷！')
                    self.record.append(self.color[self.opposite]+self.p[self.opposite].name+'中了'+self.p[self.current].name+'的雷')
                    damage=5
                    if self.p[self.opposite].tramp[3]:
                        self.record.append(self.color[self.opposite]+self.p[self.opposite].name + '大地之盾减伤%d' % damage)
                        print('Duang，触发对方大地之盾，本次攻击被挡住')
                        self.p[self.opposite].tramp[3]=0
                        self.p[self.current].tramp[1].remove(loc)
                        self.p[self.current].armorandtramps-=1
                        input()
                        return 1
                        
                    if not self.p[self.opposite].defense:
                        self.p[self.opposite].hp -= damage
                    else:
                        if (self.p[self.opposite].defense >= damage):
                            self.p[self.opposite].defense -= damage
                        else:
                            self.p[self.opposite].hp -= (damage - self.p[self.opposite].defense)
                            self.p[self.opposite].defense = 0
                    self.record.append(self.color[self.opposite]+self.p[self.opposite].name+'中了雷失%dHP'%damage)
                    
                    self.p[self.current].tramp[1].remove(loc)
                    self.p[self.current].armorandtramps-=1
                    self.ifsuccess()
                    input()
            self.setback()
            return 1
        else:
            self.setback()
            return 0
    def punchhard(self):
        loc = self.p[self.current].locate
        damage=0
        ran=1
        for i in range(loc[0] - ran, loc[0] + ran+1):
            if i in range(0, 7):
                if (i,loc[1])==self.p[self.opposite].locate:self.board[(i, loc[1])] =Back.LIGHTRED_EX+self.p[self.opposite].symbol
                else:self.board[(i, loc[1])] = Fore.LIGHTRED_EX+self.board[i, loc[1]]
        for i in range(loc[1] - ran, loc[1] + ran+1):
            if i in range(0, 7):
                if (loc[0],i)==self.p[self.opposite].locate:self.board[(loc[0],i)] =Back.LIGHTRED_EX+self.p[self.opposite].symbol
                else:
                    self.board[(loc[0], i)] = Fore.LIGHTRED_EX+self.board[loc[0], i]
        self.board[loc] = self.p[self.current].symbol
        self.printboard()
        print('重拳出击！')
       
        dire = input('方向:')
        if not self.isanumber(dire):
            self.setback()
            return 0
        dire = int(dire)
        if ((dire == 2 and os.name=='posix')or(dire==8 and os.name=='nt')):
            if ((self.p[self.opposite].locate[1] == loc[1]) and (
                    self.p[self.opposite].locate[0] in range(loc[0] - ran, loc[0]))):
                damage = 2
        elif dire == 4:
            if ((self.p[self.opposite].locate[0] == loc[0]) and (
                    self.p[self.opposite].locate[1] in range(loc[1] - ran, loc[1]))):
                damage = 2
        elif ((dire == 8 and os.name=='posix')or(dire==2 and os.name=='nt')):
            if ((self.p[self.opposite].locate[1] == loc[1]) and (
                    self.p[self.opposite].locate[0] in range(loc[0] + 1, loc[0] + ran+1))):
                damage = 2
        elif dire == 6:
            if ((self.p[self.opposite].locate[0] == loc[0]) and (
                    self.p[self.opposite].locate[1] in range(loc[1] + 1, loc[1] + ran+1))):
                damage = 2
        else:
            self.setback()
            return 0
        oppoloc=list(self.p[self.opposite].locate)
        if self.damagemake(damage,'hit'):
            if ((dire == 2 and os.name=='posix')or(dire==8 and os.name=='nt')):
                oppoloc[0] =0
            elif dire == 4:
                oppoloc[1] =0
            elif ((dire == 8 and os.name=='posix')or(dire==2 and os.name=='nt')):
                oppoloc[0] =6
            elif dire == 6:
                oppoloc[1] =6
            self.p[self.opposite].locate=tuple(oppoloc)
            print('咚。。。')
            self.record.append(self.color[self.opposite]+self.p[self.opposite].name+'被击退因为')
            
        self.setback()
        return 1
game = Game()
while not game.end:
    game.startstage()
    game.battlestage()
    game.endstage()
    
